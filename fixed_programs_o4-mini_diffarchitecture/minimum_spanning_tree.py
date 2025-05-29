def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()
    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        group_u = group_by_node.setdefault(u, {u})
        group_v = group_by_node.setdefault(v, {v})
        if group_u is not group_v:
            mst_edges.add(edge)
            group_u.update(group_v)
            for node in group_v:
                group_by_node[node].update(group_u)
    return mst_edges