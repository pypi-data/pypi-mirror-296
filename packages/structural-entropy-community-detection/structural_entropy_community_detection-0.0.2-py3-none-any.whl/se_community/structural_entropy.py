import multiprocessing as mp
from collections import defaultdict
from typing import Dict
import networkx as nx
import numpy as np
from scipy.special import xlogy

def _compute_community_entropy(G: nx.Graph, partition, community):
    """
    Compute the entropy contribution of a single community.
    """
    nodes = [node for node, comm in partition.items() if comm == community]
    subgraph = G.subgraph(nodes)

    degree_dict = dict(subgraph.degree())
    total_degree = sum(degree_dict.values())
    if total_degree == 0:
        return 0

    # Calculate probabilities
    p = np.array([deg / total_degree for deg in degree_dict.values()])

    structural_entropy = -np.sum(xlogy(p, p))

    return structural_entropy


def compute_structural_entropy_mp(G: nx.Graph, partition: Dict[int, str]) -> float:
    """
    Compute the structural entropy of a graph partition, with multiprocessing on communities.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    partition : dict
        A dictionary mapping node labels to community labels

    Returns
    -------
    float
        The structural entropy of the partition
    """
    communities = set(partition.values())

    # Use multiprocessing to compute entropy for each community in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _compute_community_entropy,
            [(G, partition, community) for community in communities],
        )

    # Sum up the entropy contributions from all communities
    total_entropy = sum(results)

    return total_entropy


def compute_structural_entropy(G: nx.Graph, partition: Dict[int, str]) -> float:
    """
    Compute the structural entropy of a graph partition.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    partition : dict
        A dictionary mapping node labels to community labels

    Returns
    -------
    float
        The structural entropy of the partition
    """
    # Loop over each community
    total_structural_entropy = 0
    for community in set(partition.values()):
        structural_entropy = _compute_community_entropy(G, partition, community)
        total_structural_entropy += structural_entropy

    return total_structural_entropy
