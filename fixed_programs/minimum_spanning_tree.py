def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        # Initialize components if not already done
        if u not in group_by_node:
            group_by_node[u] = {u}
        if v not in group_by_node:
            group_by_node[v] = {v}

        # If nodes are in different components
        if group_by_node[u] != group_by_node[v]:
            mst_edges.add(edge)
            # Compute the union of the two components
            union_set = group_by_node[u] | group_by_node[v]
            # Update all nodes in the merged component to reference the union set
            for node in union_set:
                group_by_node[node] = union_set

    return mst_edges


if __name__ == '__main__':
    # Example usage
    weights = {
        (1, 2): 10,
        (2, 3): 15,
        (3, 4): 10,
        (1, 4): 10
    }
    print(minimum_spanning_tree(weights))
