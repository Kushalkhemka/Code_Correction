# Fixed Program: shortest_path_lengths (Claude 3.7 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: In the Floyd-Warshall algorithm, when considering a path from i to j through intermediate node k, the code incorrectly used length_by_path[j, k] (path from j to k) instead of length_by_path[k, j] (path from k to j). This caused the algorithm to consider invalid paths where we go from i to k and then backwards from j to k, rather than from k to j.
# Fixed on: 2025-05-27 23:00:04
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: In the Floyd-Warshall algorithm, when considering a path from i to j through intermediate node k, the code incorrectly used length_by_path[j, k] (path from j to k) instead of length_by_path[k, j] (path from k to j). This caused the algorithm to consider invalid paths where we go from i to k and then backwards from j to k, rather than from k to j.

from collections import defaultdict

def shortest_path_lengths(n, length_by_edge):
    length_by_path = defaultdict(lambda: float('inf'))
    length_by_path.update({(i, i): 0 for i in range(n)})
    length_by_path.update(length_by_edge)
 
    for k in range(n):
        for i in range(n):
            for j in range(n):
                length_by_path[i, j] = min(
                    length_by_path[i, j],
                    length_by_path[i, k] + length_by_path[k, j]
                )

    return length_by_path


"""
All Shortest Paths
floyd-warshall

Floyd-Warshall algorithm implementation.

Calculates the length of the shortest path connecting every ordered pair of nodes in a directed graph.



Input:
    n: The number of nodes in the graph. The nodes are assumed to have ids 0..n-1
    length_by_edge: A dict containing edge length keyed by an ordered pair of node ids

Precondition:
    There are no negative-length cycles in the input graph

Output:
    A dict containing shortest path length keyed by an ordered pair of node ids
"""