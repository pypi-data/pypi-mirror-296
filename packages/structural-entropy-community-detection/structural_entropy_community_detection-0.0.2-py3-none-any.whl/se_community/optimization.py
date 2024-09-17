from collections import defaultdict
import multiprocessing as mp

from se_community.structural_entropy import compute_structural_entropy


def _merge_node(G, partition, small_communities, node):
    comm = partition[node]
    if comm in small_communities:
        neighbors = list(G.neighbors(node))
        neighbor_comms = [
            partition[neigh]
            for neigh in neighbors
            if partition[neigh] not in small_communities
        ]
        if neighbor_comms:
            return node, max(set(neighbor_comms), key=neighbor_comms.count)
    return node, comm


def merge_small_communities(G, partition, size_threshold=5):
    community_sizes = defaultdict(int)
    for comm in partition.values():
        community_sizes[comm] += 1

    small_communities = [
        comm for comm, size in community_sizes.items() if size < size_threshold
    ]

    # Use multiprocessing to merge small communities in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _merge_node, [(G, partition, small_communities, node) for node in G.nodes()]
        )

    # Update the partition based on the results
    for node, new_comm in results:
        partition[node] = new_comm

    return partition


def _optimize_node(G, partition, node):
    current_community = partition[node]
    neighbor_comms = defaultdict(float)
    for neighbor in G.neighbors(node):
        neighbor_comm = partition[neighbor]
        edge_weight = G[node][neighbor].get(
            "weight", 1
        )  # Use edge weight if present, otherwise assume 1
        neighbor_comms[neighbor_comm] += edge_weight

    best_community = max(
        neighbor_comms, key=neighbor_comms.get, default=current_community
    )

    if best_community != current_community:
        original_partition = partition.copy()
        partition[node] = best_community
        old_entropy = compute_structural_entropy(G, original_partition)
        new_entropy = compute_structural_entropy(G, partition)

        if new_entropy > old_entropy:
            return node, current_community
        return node, best_community

    return node, current_community


def optimize_boundary_nodes(G, partition):
    """
    Optimize the boundary nodes by reassigning them to their most appropriate community,
    considering both the number and strength of connections to neighboring communities.

    Parameters
    ----------
    G : networkx.Graph
        The input graph.
    partition : dict
        The current partition mapping nodes to community labels.

    Returns
    -------
    dict
        The optimized partition.
    """
    # Use multiprocessing to optimize boundary nodes in parallel
    # Use multiprocessing to optimize boundary nodes in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _optimize_node, [(G, partition, node) for node in G.nodes()]
        )

    # Update the partition based on the results
    for node, new_comm in results:
        partition[node] = new_comm

    return partition
