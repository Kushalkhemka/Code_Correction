def shortest_path_lengths(n, graph):
    dist = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for (u, v), w in graph.items():
        dist[u][v] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    result = {}
    for i in range(n):
        for j in range(n):
            result[(i, j)] = dist[i][j]
    return result