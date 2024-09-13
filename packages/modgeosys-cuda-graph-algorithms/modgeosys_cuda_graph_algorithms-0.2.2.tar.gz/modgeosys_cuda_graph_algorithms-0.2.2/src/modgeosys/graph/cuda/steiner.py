import cupy as cp
import numpy as np
import pandas as pd
import cudf
import cugraph
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
from scipy.sparse.csgraph import floyd_warshall as fw_cpu
from cualgo.graph import floydwarshall as fw_gpu

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


def compute_metric_closure(nodes, edges, distance_func, use_gpu, required_currents, cable_types):
    dist_matrix = create_distance_matrix(nodes, edges, distance_func, use_gpu, required_currents, cable_types)
    sources, targets, weights = [], [], []
    n = len(nodes)

    for i in range(n):
        for j in range(i + 1, n):
            if dist_matrix[i, j] < (cp.inf if use_gpu else np.inf):
                sources.append(i)
                targets.append(j)
                weights.append(dist_matrix[i, j])

    if use_gpu:
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
        dist_matrix_cpu = np.zeros((n, n), dtype=np.float32)
        for i in range(n):
            for j in range(i + 1, n):
                dist_matrix_cpu[i, j] = dist_matrix[i, j]
                dist_matrix_cpu[j, i] = dist_matrix[i, j]
        return fw_cpu(dist_matrix_cpu, directed=False)


def construct_mst(distance_matrix, terminals, use_gpu):
    sources, targets, weights = [], [], []
    if use_gpu:
        dist_matrix = distance_matrix
        n = len(terminals)
    else:
        dist_matrix = distance_matrix
        n = dist_matrix.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            if dist_matrix[i, j] < (cp.inf if use_gpu else np.inf):
                sources.append(i)
                targets.append(j)
                weights.append(dist_matrix[i, j])

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


def steiner_tree_approximation(nodes, terminals, edges, distance_func_gpu, distance_func_cpu, use_gpu, required_currents, cable_types):
    # Step 1: Compute metric closure using the specified distance function
    distance_func = distance_func_gpu if use_gpu else distance_func_cpu

    metric_closure = compute_metric_closure(nodes, edges, distance_func, use_gpu, required_currents, cable_types)

    # Step 2: Construct MST from the metric closure
    mst = construct_mst(metric_closure, terminals, use_gpu)

    # Step 3: Steiner node addition
    original_graph = nx.MultiGraph()
    for (u, v, attrs) in edges:
        distance = distance_func(nodes[u], nodes[v])
        required_current = required_currents.get((u, v), 0)
        num_cables, total_cost = calculate_optimal_cables(required_current, cable_types)
        original_graph.add_edge(u, v, weight=distance, num_cables=num_cables, total_cost=total_cost)

    steiner_tree = nx.MultiGraph()

    def add_shortest_path(u, v):
        path = shortest_path(original_graph, u, v)
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
