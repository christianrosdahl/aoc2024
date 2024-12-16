# Advent of Code 2024 - day 16
from common import get_input


# Part 1
def main1():
    input_data = get_input("input16.txt")
    nodes, edges, start_node, end_nodes = parse_input(input_data)
    dist, _ = dijkstra(nodes, edges, start_node)
    ans = min([dist[end_node] for end_node in end_nodes])
    print(f"Answer 1 is: {ans}")


def parse_input(input_data):
    nodes = []
    edges = {}
    start_node = None
    end_nodes = []
    for row, line in enumerate(input_data):
        for col, char in enumerate(line):
            if char in [".", "S", "E"]:
                for direction in ["n", "s", "e", "w"]:
                    node = (row, col, direction)
                    nodes.append(node)
                    edges[node] = get_edges(node, input_data)
                    if char == "E":
                        end_nodes.append(node)
                    if char == "S" and direction == "e":
                        start_node = node
    return nodes, edges, start_node, end_nodes


def get_edges(node, input_data):
    rotations = {
        "left": {"n": "w", "e": "n", "s": "e", "w": "s"},
        "right": {"n": "e", "e": "s", "s": "w", "w": "n"},
        "none": {"n": "n", "e": "e", "s": "s", "w": "w"},
    }
    directions_coord = {"n": (-1, 0), "e": (0, 1), "s": (1, 0), "w": (0, -1)}
    edges = {}
    for rotation in ["left", "right", "none"]:
        cost = 1
        if rotation in ["left", "right"]:
            cost += 1000
        row, col, node_direction = node
        new_direction = rotations[rotation][node_direction]
        new_direction_coord = directions_coord[new_direction]
        new_row = row + new_direction_coord[0]
        new_col = col + new_direction_coord[1]
        if not input_data[new_row][new_col] == "#":
            edges[(new_row, new_col, new_direction)] = cost
    return edges


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


# Part 2
def main2():
    input_data = get_input("input16.txt")
    visualize = False

    nodes, edges, start_node, end_nodes = parse_input(input_data)
    dist, prev = dijkstra(nodes, edges, start_node)

    best_path_nodes = set()
    lowest_cost = min([dist[end_node] for end_node in end_nodes])
    lowest_cost_end_nodes = [node for node in end_nodes if dist[node] == lowest_cost]
    for end_node in lowest_cost_end_nodes:
        best_path_nodes.add(end_node)
        add_prev_to_set(end_node, start_node, prev, best_path_nodes)
    best_path_tiles = nodes_to_tiles(best_path_nodes)

    if visualize:
        display(input_data, best_path_tiles)
    print(f"Answer 2 is: {len(best_path_tiles)}")


def display(input_data, marked_tiles):
    for row, line in enumerate(input_data):
        for col, _ in enumerate(line):
            tile = (row, col)
            if tile in marked_tiles:
                line = line[:col] + "O" + line[col + 1 :]
        print(line)


def add_prev_to_set(node, start_node, prev, node_set):
    if node == start_node:
        node_set.add(start_node)
    else:
        for previous_node in prev[node]:
            node_set.add(previous_node)
            add_prev_to_set(previous_node, start_node, prev, node_set)


def nodes_to_tiles(nodes):
    tiles = set()
    for node in nodes:
        row, col, _ = node
        tile = (row, col)
        tiles.add(tile)
    return tiles


if __name__ == "__main__":
    main1()
    main2()
