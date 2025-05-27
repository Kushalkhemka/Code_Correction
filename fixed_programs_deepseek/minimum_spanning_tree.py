# Fixed Program: minimum_spanning_tree (DeepSeek)
# Bug Classification: Incorrect comparison operator
# Bug Description: The comparison operator `!=` was incorrect because it checked for object inequality rather than set inequality. Kruskal's algorithm requires checking if the sets of nodes `u` and `v` are different to avoid cycles.
# Fixed on: 2025-05-27 12:52:58
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The comparison operator `!=` was incorrect because it checked for object inequality rather than set inequality. Kruskal's algorithm requires checking if the sets of nodes `u` and `v` are different to avoid cycles.

def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) is not group_by_node.setdefault(v, {v}):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node].update(group_by_node[u])

    return mst_edges


"""
Minimum Spanning Tree


Kruskal's algorithm implementation.

Input:
    weight_by_edge: A dict of the form {(u, v): weight} for every undirected graph edge {u, v}

Precondition:
    The input graph is connected

Output:
    A set of edges that connects all the vertices of the input graph and has the least possible total weight.

Example:
    >>> minimum_spanning_tree({
    ...     (1, 2): 10,
    ...     (2, 3): 15,
    ...     (3, 4): 10,
    ...     (1, 4): 10
    ... })
    {(1, 2), (3, 4), (1, 4)}
"""