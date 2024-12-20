# Advent of Code 2024 - day 20
from common import get_input, dijkstra
import sys


# Part 1 - First apprach. A simpler and more efficient solution can be found below.
def main1_first_approach():
    saved_dist_threshold = 100
    input_data = get_input("input20.txt")
    start_pos, end_pos, positions = parse_input(input_data)
    sys.setrecursionlimit(10000)

    dist_without_cheating = get_dist_without_cheating(start_pos, end_pos, positions)
    blocked_cheat_pos = set()
    num_cheats = 0
    while True:
        dist_with_cheating, cheat_pos = get_dist_with_cheating(
            start_pos, end_pos, positions, blocked_cheat_pos
        )
        saved_dist = dist_without_cheating - dist_with_cheating
        if saved_dist < saved_dist_threshold:
            break
        print("saved distance: ", saved_dist)
        num_cheats += len(cheat_pos)
        blocked_cheat_pos |= cheat_pos

    print(f"Answer 1 is: {num_cheats}")


def parse_input(input_data):
    start = None
    end = None
    positions = set()
    for row, line in enumerate(input_data):
        for col, char in enumerate(line):
            if char in [".", "S", "E"]:
                positions.add((row, col))
            if char == "S":
                start = (row, col)
            elif char == "E":
                end = (row, col)
    return start, end, positions


def get_nodes(positions):
    """
    Each node consists of the values (row, col, has_cheated).
    """
    nodes = set()
    for pos in positions:
        nodes.add((pos, True))
        nodes.add((pos, False))
    return nodes


def get_edges(node, positions, blocked_cheat_pos=None):
    edges = {}
    has_cheated = node[1]
    for step in ([-1, 0], [1, 0], [0, -1], [0, 1]):
        node_pos = node[0]
        new_pos = (node_pos[0] + step[0], node_pos[1] + step[1])
        if new_pos in positions:
            new_node = (new_pos, has_cheated)
            edges[new_node] = 1
    if not has_cheated:
        for step in ([-1, 0], [1, 0], [0, -1], [0, 1]):
            node_pos = node[0]
            middle_pos = (node_pos[0] + step[0], node_pos[1] + step[1])
            new_pos = (node_pos[0] + 2 * step[0], node_pos[1] + 2 * step[1])
            if new_pos in positions and middle_pos not in positions:
                if blocked_cheat_pos and middle_pos in blocked_cheat_pos:
                    continue
                has_cheated = True
                new_node = (new_pos, has_cheated)
                edges[new_node] = 2
    return edges


def get_best_paths(start, end, prev):
    paths = []
    for prev_node in prev[end]:
        if prev_node == start:
            paths.append([start, end])
        else:
            for prev_path in get_best_paths(start, prev_node, prev):
                paths.append(prev_path + [end])
    return paths


def get_dist_without_cheating(start_pos, end_pos, positions):
    nodes = get_nodes(positions)
    edges = {}
    for node in nodes:
        edges[node] = get_edges(node, positions)
    start_node = (start_pos, True)
    end_node = (end_pos, True)
    dist, _ = dijkstra(nodes, edges, start_node)
    return dist[end_node]


def get_dist_with_cheating(start_pos, end_pos, positions, blocked_cheat_pos):
    nodes = get_nodes(positions)
    edges = {}
    for node in nodes:
        edges[node] = get_edges(node, positions, blocked_cheat_pos)
    start_node = (start_pos, False)
    end_node = (end_pos, True)
    dist, prev = dijkstra(nodes, edges, start_node)
    best_paths = get_best_paths(start_node, end_node, prev)
    cheat_pos = get_cheat_pos(best_paths)
    return dist[end_node], cheat_pos


def get_cheat_pos(paths):
    cheat_positions = set()
    for path in paths:
        for i in range(len(path) - 1):
            has_cheated_at_node1 = path[i][1]
            has_cheated_at_node2 = path[i + 1][1]
            if not has_cheated_at_node1 and has_cheated_at_node2:
                pos1 = path[i][0]
                pos2 = path[i + 1][0]
                cheat_pos = (int((pos1[0] + pos2[0]) / 2), int((pos1[1] + pos2[1]) / 2))
                cheat_positions.add(cheat_pos)
    return cheat_positions


# Part 2
def main2():
    min_dist_saved = 100
    max_cheat_length = 20
    input_data = get_input("input20.txt")
    start_pos, end_pos, positions = parse_input(input_data)
    original_path = get_path(start_pos, end_pos, positions)
    num_shorter_paths = get_num_shorter_paths(
        original_path, min_dist_saved, max_cheat_length
    )

    print(f"Answer 2 is: {num_shorter_paths}")


def get_path(start, end, positions):
    path = []
    path.append(start)
    previous = None
    pos = start
    while not pos == end:
        for diff in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos[0] + diff[0], pos[1] + diff[1])
            if new_pos in positions and not new_pos == previous:
                path.append(new_pos)
                previous = pos
                pos = new_pos
                continue
    return path


def get_num_shorter_paths(original_path, min_dist_saved, max_cheat_length):
    original_path_len = len(original_path) - 1
    num_shorter_paths = 0
    for i, pos1 in enumerate(original_path):
        for j, pos2 in enumerate(original_path):
            if j <= i:
                continue
            cheat_dist = dist(pos1, pos2)
            if cheat_dist <= max_cheat_length:
                total_dist = i + cheat_dist + (original_path_len - j)
                if original_path_len - total_dist >= min_dist_saved:
                    num_shorter_paths += 1
    return num_shorter_paths


def dist(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])


# Part 1 - Second apporach. Builds on the same principle as part 2 and is simpler and faster than the first approach.
def main1():
    min_dist_saved = 100
    max_cheat_length = 2
    input_data = get_input("input20.txt")
    start_pos, end_pos, positions = parse_input(input_data)
    original_path = get_path(start_pos, end_pos, positions)
    num_shorter_paths = get_num_shorter_paths(
        original_path, min_dist_saved, max_cheat_length
    )

    print(f"Answer 1 is: {num_shorter_paths}")


if __name__ == "__main__":
    # main1_first_approach()
    main1()
    main2()
