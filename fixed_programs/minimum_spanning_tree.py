def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        # Initialize the groups if the nodes haven't been seen yet
        if u not in group_by_node:
            group_by_node[u] = {u}
        if v not in group_by_node:
            group_by_node[v] = {v}

        # If u and v belong to different groups, merge them
        if group_by_node[u] != group_by_node[v]:
            mst_edges.add(edge)
            # Merge the groups into a new_group
            new_group = group_by_node[u] | group_by_node[v]
            # Update every node in the new_group to have the new_group as its connectivity set
            for node in new_group:
                group_by_node[node] = new_group

    return mst_edges


if __name__ == '__main__':
    # Example usage
    example = {
        (1, 2): 10,
        (2, 3): 15,
        (3, 4): 10,
        (1, 4): 10
    }
    print(minimum_spanning_tree(example))
