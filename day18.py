# Advent of Code 2024 - day 18
from common import get_input, dijkstra


# Part 1
def main1():
    use_example = False
    example_input = "ex_input18.txt"
    real_input = "input18.txt"
    if use_example:
        input_data = get_input(example_input)[:12]
        end = (6, 6)
    else:
        input_data = get_input(real_input)[:1024]
        end = (70, 70)
    start = (0, 0)
    blocked = parse_input(input_data)
    height = end[0] - start[0] + 1
    width = end[1] - start[1] + 1

    nodes = set()
    edges = {}
    for row in range(height):
        for col in range(width):
            node = (row, col)
            if not node in blocked:
                nodes.add(node)
                edges[node] = get_edges(node, blocked, height, width)

    dist, _ = dijkstra(nodes, edges, start)
    steps_to_end = dist[end]
    print(f"Answer 1 is: {steps_to_end}")


def parse_input(input_data):
    blocked = []
    for line in input_data:
        col, row = line.split(",")
        row, col = int(row), int(col)
        blocked.append((row, col))
    return blocked


def get_edges(node, blocked, height, width):
    edges = {}
    for step in ([-1, 0], [1, 0], [0, -1], [0, 1]):
        new_node = (node[0] + step[0], node[1] + step[1])
        if not outside_grid(new_node, width, height) and not new_node in blocked:
            edges[new_node] = 1
    return edges


def outside_grid(node, width, height):
    row, col = node
    if not 0 <= row < height:
        return True
    if not 0 <= col < width:
        return True
    return False


# Part 2
def main2():
    use_example = False
    example_input = "ex_input18.txt"
    real_input = "input18.txt"
    if use_example:
        input_data = get_input(example_input)
        end = (6, 6)
        max_num_bytes = len(input_data)
    else:
        input_data = get_input(real_input)
        end = (70, 70)
        max_num_bytes = len(input_data)
    start = (0, 0)
    blocked = parse_input(input_data)
    height = end[0] - start[0] + 1
    width = end[1] - start[1] + 1

    first_blocking_byte = get_first_blocking_byte(
        max_num_bytes, blocked, height, width, start, end
    )
    row, col = first_blocking_byte
    ans = f"{col},{row}"

    print(f"Answer 2 is: {ans}")


def exit_possible(num_bytes, all_blocked, height, width, start, end):
    blocked = all_blocked[:num_bytes]
    nodes = set()
    edges = {}
    for row in range(height):
        for col in range(width):
            node = (row, col)
            if not node in blocked:
                nodes.add(node)
                edges[node] = get_edges(node, blocked, height, width)

    dist, _ = dijkstra(nodes, edges, start)
    steps_to_end = dist[end]
    return steps_to_end < float("inf")


def get_first_blocking_byte(max_num_bytes, all_blocked, height, width, start, end):
    interval_min = 0
    interval_max = max_num_bytes
    while interval_min + 1 < interval_max:
        interval_middle = int((interval_min + interval_max) / 2)
        can_exit = exit_possible(
            interval_middle, all_blocked, height, width, start, end
        )
        if can_exit:
            interval_min = interval_middle
        else:
            interval_max = interval_middle
    return all_blocked[interval_min]


if __name__ == "__main__":
    main1()
    main2()
