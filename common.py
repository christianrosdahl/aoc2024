# Common functions, used in several of the solutions
def get_input(path):
    file = open(path, "r")
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    file.close()
    return lines


def dijkstra(nodes, edges, start_node):
    dist = {}
    prev = {}
    unvisited_nodes = []
    for node in nodes:
        dist[node] = float("inf")
        prev[node] = []
        unvisited_nodes.append(node)
    dist[start_node] = 0

    while len(unvisited_nodes) > 0:
        min_dist = float("inf")
        for unvisited_node in unvisited_nodes:
            if dist[unvisited_node] <= min_dist:
                min_dist = dist[unvisited_node]
                selected_node = unvisited_node
        unvisited_nodes.remove(selected_node)

        for neighbor, edge_cost in edges[selected_node].items():
            alt_dist = dist[selected_node] + edge_cost
            if alt_dist <= dist[neighbor]:
                dist[neighbor] = alt_dist
                prev[neighbor].append(selected_node)

    return dist, prev
