from typing import Dict
import networkx as nx
import numpy as np
import multiprocessing as mp

from se_community.optimization import merge_small_communities, optimize_boundary_nodes
from se_community.structural_entropy import compute_structural_entropy


def _swap_entropy(G, partition, node_i, node_j, initial_entropy):
    """
    Helper function to compute the entropy after swapping two nodes.
    """
    partition[node_i], partition[node_j] = partition[node_j], partition[node_i]
    new_entropy = compute_structural_entropy(G, partition)
    entropy_gain = initial_entropy - new_entropy
    partition[node_i], partition[node_j] = (
        partition[node_j],
        partition[node_i],
    )  # Revert swap
    return (entropy_gain, node_i, node_j)


def _kernighan_lin(
    G, initial_partition, *, max_iterations: int = 100, verbose=False
) -> Dict[int, str]:
    nodes = list(G.nodes())
    partition = initial_partition.copy()
    best_partition = partition.copy()
    original_entropy = compute_structural_entropy(G, initial_partition)
    best_entropy = original_entropy

    for iteration in range(max_iterations):
        gains = []

        # Create a multiprocessing pool to parallelize swaps
        with mp.Pool(processes=mp.cpu_count()) as pool:
            swap_results = pool.starmap(
                _swap_entropy,
                [
                    (G, partition, nodes[i], nodes[j], best_entropy)
                    for i in range(len(nodes))
                    for j in range(i + 1, len(nodes))
                    if partition[nodes[i]] != partition[nodes[j]]
                ],
            )

        # Process the swap results
        for entropy_gain, node_i, node_j in swap_results:
            if entropy_gain > 0:
                gains.append((entropy_gain, node_i, node_j))

        # If no improvements, break early
        if not gains:
            if verbose:
                print("No improvements found, stopping early")
            break

        # Find the best swap
        best_gain, best_i, best_j = max(gains, key=lambda x: x[0])

        # Apply the best swap
        partition[best_i], partition[best_j] = partition[best_j], partition[best_i]
        best_entropy -= best_gain
        best_partition = partition.copy()  # Update the best partition

        if verbose:
            print(f"Iteration {iteration}: {best_entropy} ")

    return best_partition


# split the nodes in the graph into two communities, a and b
def _two_way_partition(
    G: nx.Graph, hierarchical_label_prefix: str, *, max_iterations=100, verbose=False
):
    if verbose:
        print(f"Two-Way Partition: {G.number_of_nodes()}, {G.number_of_edges()}")

    # Initial partition: spectral bisection
    laplacian = nx.laplacian_matrix(G)
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian.toarray())
    fiedler_vector = eigenvectors[:, 1]
    initial_partition = {
        node: (
            hierarchical_label_prefix + "0"
            if fiedler_vector[i] >= 0
            else hierarchical_label_prefix + "1"
        )
        for i, node in enumerate(G.nodes())
    }

    # Refine the partition using Kernighan-Lin algorithm
    refined_partition = _kernighan_lin(
        G, initial_partition, max_iterations=max_iterations, verbose=verbose
    )

    return refined_partition


def _recursive_partition(
    G: nx.Graph,
    hierarchical_label_prefix: str,
    original_structural_entropy: float,
    *,
    level=0,
    max_depth=10,
    max_iterations=100,
    entropy_threshold=0.01,
    min_community_size=2,
    verbose=False,
):
    if verbose:
        print(f"Recursive Level {level}: {G.number_of_nodes()} nodes")
    if G.number_of_nodes() <= min_community_size or level >= max_depth:
        if verbose:
            print(
                f"Reached max depth {level} or min community size {G.number_of_nodes()}"
            )

        return {node: hierarchical_label_prefix + "0" for node in G.nodes()}

    binary_partition = _two_way_partition(
        G,
        hierarchical_label_prefix=hierarchical_label_prefix,
        max_iterations=max_iterations,
        verbose=verbose,
    )

    new_structural_entropy = compute_structural_entropy(G, binary_partition)
    if verbose:
        print(f"Original Entropy: {original_structural_entropy}")
        print(f"New Entropy: {new_structural_entropy}")

    partition = binary_partition.copy()

    # If the new partition entropy get better but decrease level is not enough, stop partitioning
    if (
        new_structural_entropy < original_structural_entropy
        and new_structural_entropy > original_structural_entropy - entropy_threshold
    ):
        if verbose:
            print("New partition is already better, keep this partition")
        return partition
    else:
        if verbose:
            print("New partition is not better, continue partitioning its subgraphs")

        # Split the graph into subgraphs based on the partition
        subgraphs = [
            G.subgraph([node for node, part in partition.items() if part == i])
            for i in set(partition.values())
        ]

        for i, subgraph in enumerate(subgraphs):
            # Only continue partitioning if the subgraph size is above the minimum threshold
            if subgraph.number_of_nodes() > min_community_size:
                if verbose:
                    print(
                        f"Partitioning Subgraph {i} with {subgraph.number_of_nodes()} nodes"
                    )
                subgraph_entropy = compute_structural_entropy(subgraph, {n: 0 for n in subgraph.nodes()})

                sub_partition = _recursive_partition(
                    subgraph,
                    hierarchical_label_prefix=hierarchical_label_prefix + str(i),
                    original_structural_entropy=subgraph_entropy,
                    level=level + 1,
                    max_depth=max_depth,
                    max_iterations=max_iterations,
                    verbose=verbose,
                )
                partition.update(sub_partition)

            else:
                # Assign a unique label if subgraph is too small to partition further
                if verbose:
                    print(f"Subgraph {i} too small to partition further")
                partition.update(
                    {
                        node: hierarchical_label_prefix + str(i)
                        for node in subgraph.nodes()
                    }
                )

        return partition


def community_detection(
    G: nx.Graph,
    *,
    max_depth=15,
    max_iterations=100,
    size_threshold=5,
    min_community_size=2,
    verbose=False,
):
    """
    Detect communities in a graph based on structural entropy minimizing.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    level : int, optional
        The current level of recursion, by default 0
    entropy_threshold : float, optional
        Minimum improvement in entropy to continue partitioning, by default 0.01
    size_threshold : int, optional
        Communities with fewer nodes than this threshold will be merged with their neighbors, by default 5
    max_depth : int, optional
        Maximum depth of recursion for partitioning, by default 10
    max_iterations : int, optional
        Maximum number of iterations for the Kernighan-Lin algorithm, by default 100

    Returns
    -------
    dict
        A dictionary mapping node labels to community labels
    """
    original_structural_entropy = compute_structural_entropy(
        G, {node: 0 for node in G.nodes()}
    )
    if verbose:
        print(f"Community Detection: {G.number_of_nodes()}, {G.number_of_edges()}")
        print(f"Original Entropy: {original_structural_entropy}")

    partition = _recursive_partition(
        G,
        hierarchical_label_prefix="",
        original_structural_entropy=original_structural_entropy,
        level=0,
        max_depth=max_depth,
        max_iterations=max_iterations,
        min_community_size=min_community_size,
        verbose=verbose,
    )

    if verbose:
        print(f"Partition entropy: {compute_structural_entropy(G, partition)}")

    # Merge small communities
    partition = merge_small_communities(G, partition, size_threshold)
    if verbose:
        print(f"Merge Small entropy: {compute_structural_entropy(G, partition)}")

    # Optimize boundary nodes
    partition = optimize_boundary_nodes(G, partition)

    if verbose:
        print(f"Optimize Boundary entropy: {compute_structural_entropy(G, partition)}")

    # Convert hierarchical labels to flat numeric labels
    unique_labels = sorted(set(partition.values()))
    label_map = {label: i for i, label in enumerate(unique_labels)}
    return {node: label_map[partition[node]] for node in G.nodes()}
