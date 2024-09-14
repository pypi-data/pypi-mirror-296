import cupy as cp
import numpy as np
import pandas as pd
import cudf
import cugraph
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
from concurrent.futures import ThreadPoolExecutor
from scipy.sparse.csgraph import floyd_warshall as fw_cpu
from cualgo.graph import floydwarshall as fw_gpu


GRAPH_NODE_COORDS_KEY = 'self.nodes'
GRAPH_NODE_IDS_KEY = 'self.node_ids'
GRAPH_TERMINALS_KEY = 'self.terminals'
GRAPH_EDGES_KEY = 'self.edges'
GRAPH_REQUIRED_CURRENTS_KEY = 'self.required_currents'
GRAPH_CABLE_TYPES_KEY = 'cable_types'



def is_gpu_available():
    try:
        cp.cuda.Device(0).compute_capability
        return True
    except cp.cuda.runtime.CUDARuntimeError:
        return False

use_gpu = False # is_gpu_available()

def manhattan_distance(p1, p2):
    return cp.abs(p1[0] - p2[0]) + cp.abs(p1[1] - p2[1]) if use_gpu else np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])

def euclidean_distance(p1, p2):
    return cp.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) if use_gpu else np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_optimal_cables(required_current, cable_types):
    cable_combinations = []
    for cable in cable_types:
        count = (required_current + cable['capacity'] - 1) // cable['capacity']
        total_cost = count * cable['cost']
        cable_combinations.append((total_cost, count, cable['capacity']))
    # Select the combination with the minimum total cost
    optimal_combination = min(cable_combinations, key=lambda x: x[0])
    return optimal_combination[1], optimal_combination[0]  # Return count and total cost


def create_distance_matrix(nodes, edges, distance_func, use_gpu, required_currents, cable_types):
    n = len(nodes)
    if use_gpu:
        dist_matrix = cp.full((n, n), cp.inf, dtype=cp.float32)
    else:
        dist_matrix = np.full((n, n), np.inf, dtype=np.float32)

    for (u, v, attrs) in edges:
        dist = distance_func(nodes[u], nodes[v])
        required_current = required_currents.get((u, v), 0)
        num_cables, total_cost = calculate_optimal_cables(required_current, cable_types)
        dist *= total_cost  # Use the total cost as the weight
        if dist < dist_matrix[u, v]:
            dist_matrix[u, v] = dist
            dist_matrix[v, u] = dist
    return dist_matrix


def compute_metric_closure_with_steiner(nodes, edges, distance_func, use_gpu, required_currents, cable_types):
    dist_matrix = create_distance_matrix(nodes, edges, distance_func, use_gpu, required_currents, cable_types)
    sources, targets, weights = [], [], []
    n = len(nodes)

    if use_gpu:
        for i in range(n):
            for j in range(i + 1, n):
                if dist_matrix[i, j] < (cp.inf if use_gpu else np.inf):
                    sources.append(i)
                    targets.append(j)
                    weights.append(dist_matrix[i, j])

        df = cudf.DataFrame({'src': sources, 'dst': targets, 'weight': weights})
        G = cugraph.Graph()
        G.from_cudf_edgelist(df, source='src', destination='dst', edge_attr='weight')
        # Convert G to a Python list of lists
        df_pandas = df.to_pandas()
        num_nodes = max(df_pandas['src'].max(), df_pandas['dst'].max()) + 1
        adj_matrix = np.zeros((num_nodes, num_nodes))

        for _, row in df_pandas.iterrows():
            adj_matrix[int(row['src']), int(row['dst'])] = row['weight']
            adj_matrix[int(row['dst']), int(row['src'])] = row['weight']  # Assuming undirected graph

        # Convert adjacency matrix to list of lists
        adj_matrix_list = adj_matrix.tolist()
        dist_matrix_gpu = fw_gpu(adj_matrix_list)
        # Convert the distance matrix to a CuPy array
        dist_matrix_gpu = cp.asarray(dist_matrix_gpu)

        return dist_matrix_gpu
    else:
        dist_matrix_cpu = np.zeros((n, n), dtype=np.float64)
        for i in range(n):
            for j in range(i + 1, n):
                dist_matrix_cpu[i, j] = dist_matrix[i, j]
                dist_matrix_cpu[j, i] = dist_matrix[i, j]
        return fw_cpu(dist_matrix_cpu, directed=False)


def construct_mst_on_terminals(terminals, metric_closure, use_gpu):
    """
    Construct an MST using only terminal nodes, based on the metric closure.
    """
    sources, targets, weights = [], [], []

    for i in range(len(terminals)):
        for j in range(i + 1, len(terminals)):
            u = terminals[i]
            v = terminals[j]
            if metric_closure[i, j] < (cp.inf if use_gpu else np.inf):
                sources.append(u)
                targets.append(v)
                weights.append(metric_closure[i, j])

    if use_gpu:
        df = cudf.DataFrame({'src': sources, 'dst': targets, 'weight': weights})
        G = cugraph.Graph()
        G.from_cudf_edgelist(df, source='src', destination='dst', edge_attr='weight')
        mst = cugraph.minimum_spanning_tree(G)
        return mst
    else:
        G = nx.Graph()
        for src, dst, weight in zip(sources, targets, weights):
            G.add_edge(src, dst, weight=weight)
        mst = nx.minimum_spanning_tree(G)
        return mst


def shortest_path(graph, source, target, weight='weight'):
    return nx.shortest_path(graph, source=source, target=target, weight=weight)


def steiner_tree_approximation(graph, distance_func_gpu, distance_func_cpu, use_gpu):

    purge_unreachable_subgraphs(graph)
    node_coords, node_ids, terminals, edges, required_currents, cable_types = extract_graph_components(graph)

    if use_gpu:
        nodes = cp.array(node_coords, dtype=cp.float64)
    else:
        nodes = np.array(node_coords, dtype=np.float64)

    # Step 1: Compute metric closure using the specified distance function
    distance_func = distance_func_gpu if use_gpu else distance_func_cpu

    metric_closure = compute_metric_closure_with_steiner(nodes, edges, distance_func, use_gpu, required_currents, cable_types)

    # Step 2: Construct MST from the metric closure
    mst = construct_mst_on_terminals(terminals, metric_closure, use_gpu)

    # Step 3: Steiner node addition
    original_graph = nx.MultiGraph()
    for (u, v, attrs) in edges:
        distance = distance_func(nodes[u], nodes[v])
        required_current = required_currents.get((u, v), 0)
        num_cables, total_cost = calculate_optimal_cables(required_current, cable_types)
        original_graph.add_edge(u, v, weight=distance, num_cables=num_cables, total_cost=total_cost)

    steiner_tree = nx.MultiGraph()

    def add_shortest_path(u, v):
        # try:
        path = shortest_path(original_graph, u, v)
        # except nx.exception.NetworkXNoPath:
        #     return
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            num_cables = original_graph[u][v][0]['num_cables']
            total_cost = original_graph[u][v][0]['total_cost']
            steiner_tree.add_edge(u, v, weight=original_graph[u][v][0]['weight'], num_cables=num_cables, total_cost=total_cost)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(add_shortest_path, u, v) for u, v in mst.edges()]
        for future in futures:
            future.result()

    return steiner_tree


def plot_graph_with_unreachable_nodes(G, reachable_nodes, unreachable_nodes, width=15, height=12):
    # Set the figure size
    fig, ax = plt.subplots(figsize=(width, height))

    # Get positions from node attributes
    pos = nx.get_node_attributes(G, 'pos')

    # Draw the graph using the positions
    nodes_draw = nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=reachable_nodes, node_color='lightblue', node_size=10)
    edges_draw = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray')

    # Highlight unreachable nodes
    unreachable_nodes_draw = nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=unreachable_nodes, node_color='red', node_size=10)

    # Add tooltips for reachable nodes
    node_labels = {node: f"Node {node}\nPos: {pos[node]}" for node in reachable_nodes}
    node_tooltips = plugins.PointLabelTooltip(nodes_draw, labels=[node_labels[n] for n in reachable_nodes])
    plugins.connect(fig, node_tooltips)

    # Add tooltips for unreachable nodes
    unreachable_node_labels = {node: f"Node {node}\nPos: {pos[node]}" for node in unreachable_nodes}
    unreachable_node_tooltips = plugins.PointLabelTooltip(unreachable_nodes_draw, labels=[unreachable_node_labels[n] for n in unreachable_nodes])
    plugins.connect(fig, unreachable_node_tooltips)

    # Add tooltips for edges
    edge_labels = {edge: f"Edge {edge}" for edge in G.edges()}
    edge_tooltips = plugins.LineHTMLTooltip(edges_draw, [edge_labels[e] for e in G.edges()])
    plugins.connect(fig, edge_tooltips)

    plt.title("Graph with Unreachable Nodes Highlighted", fontsize=12, pad=20)
    mpld3.show()


def partition_nx_graph_by_reachability(G):
    # Choose a starting node (e.g., the first node in the list)
    start_node = 0
    # Perform BFS or DFS to check reachability
    reachable_nodes = nx.node_connected_component(G, start_node)
    # Find unreachable nodes
    unreachable_nodes = set(G.nodes) - reachable_nodes
    return reachable_nodes, unreachable_nodes


def create_nx_graph(edges, nodes):
    # Create a graph
    G = nx.Graph()
    # Add nodes with coordinates as attributes
    for i, coord in enumerate(nodes):
        G.add_node(i, pos=coord[0:2])
    # Add edges
    G.add_edges_from([(u, v) for u, v, _ in edges])
    return G


def purge_unreachable_subgraphs(graph):

    G = create_nx_graph(graph[GRAPH_EDGES_KEY], graph[GRAPH_NODE_COORDS_KEY])
    reachable_nodes, unreachable_nodes = partition_nx_graph_by_reachability(G)

    if unreachable_nodes:

        print('Not all nodes are reachable.')
        print('Reachable nodes:', len(reachable_nodes))
        print('Unreachable nodes:', unreachable_nodes)

        # Remove unreachable nodes from the graph.
        for node_index in reversed(sorted(unreachable_nodes)):

            print('Removing node:', node_index)

            if node_index in graph[GRAPH_TERMINALS_KEY]:
                raise ValueError('A terminal node is unreachable.')

            graph[GRAPH_NODE_COORDS_KEY].pop(node_index)
            graph[GRAPH_NODE_IDS_KEY].pop(node_index)
            graph[GRAPH_TERMINALS_KEY] = [t - 1 if t > node_index else t for t in graph[GRAPH_TERMINALS_KEY]]
            graph[GRAPH_EDGES_KEY] = [edge for edge in graph[GRAPH_EDGES_KEY] if edge[0] != node_index and edge[1] != node_index]
            graph[GRAPH_REQUIRED_CURRENTS_KEY] = {k: v for k, v in graph[GRAPH_REQUIRED_CURRENTS_KEY].items() if k[0] != node_index and k[1] != node_index}

            # Adjust the indices of the remaining nodes in the edges.
            for i, edge in enumerate(graph[GRAPH_EDGES_KEY]):
                if edge[0] > node_index or edge[1] > node_index:
                    new_edge = (edge[0] - 1 if edge[0] > node_index else edge[0], edge[1] - 1 if edge[1] > node_index else edge[1], edge[2])
                    graph[GRAPH_EDGES_KEY][i] = new_edge

        # plot_graph_with_unreachable_nodes(G, reachable_nodes, unreachable_nodes)
        # exit(0)


def extract_graph_components(graph):
    node_coords = graph[GRAPH_NODE_COORDS_KEY]
    node_ids = graph[GRAPH_NODE_IDS_KEY]
    terminals = graph[GRAPH_TERMINALS_KEY]
    edges = graph[GRAPH_EDGES_KEY]
    required_currents = graph[GRAPH_REQUIRED_CURRENTS_KEY]
    cable_types = graph[GRAPH_CABLE_TYPES_KEY]

    return node_coords, node_ids, terminals, edges, required_currents, cable_types
