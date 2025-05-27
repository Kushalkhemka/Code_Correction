# Fixed Program: minimum_spanning_tree (Claude 3.7 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: The bug is in the component merging logic. When merging two groups, the code incorrectly updates each node in group_by_node[v] with group_by_node[u], which creates inconsistent references since group_by_node[u] was just modified. Instead, nodes in merged components should all point to the same set object.
# Fixed on: 2025-05-27 22:52:35
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: The bug is in the component merging logic. When merging two groups, the code incorrectly updates each node in group_by_node[v] with group_by_node[u], which creates inconsistent references since group_by_node[u] was just modified. Instead, nodes in merged components should all point to the same set object.

def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) != group_by_node.setdefault(v, {v}):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node] = group_by_node[u]

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