def shortest_paths(source, weight_by_edge):
    # Initialize the weight (distance) of each node to infinity, except for the source
    weight_by_node = {v: float('inf') for u, v in weight_by_edge}
    weight_by_node[source] = 0

    # Relax edges repeatedly
    for i in range(len(weight_by_node) - 1):
        for (u, v), weight in weight_by_edge.items():
            # Update the distance for node v if a shorter path is found via u
            weight_by_node[v] = min(weight_by_node[u] + weight, weight_by_node[v])

    return weight_by_node


if __name__ == "__main__":
    # Example usage:
    result = shortest_paths('A', {
        ('A', 'B'): 3,
        ('A', 'C'): 3,
        ('A', 'F'): 5,
        ('C', 'B'): -2,
        ('C', 'D'): 7,
        ('C', 'E'): 4,
        ('D', 'E'): -5,
        ('E', 'F'): -1
    })
    print(result)
