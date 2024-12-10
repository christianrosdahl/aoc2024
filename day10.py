# Advent of Code 2024 - day 10
from common import get_input


# Part 1
def main1():
    input_data = get_input("input10.txt")
    typographic_map = parse_input(input_data)
    map_height = len(typographic_map)
    map_width = len(typographic_map[0])

    score = 0
    for row in range(map_height):
        for col in range(map_width):
            if typographic_map[row][col] == 0:
                score += len(get_reachable_9_positions(row, col, typographic_map))

    print(f"Answer 1 is: {score}")


def parse_input(input_data):
    typographic_map = []
    for row in input_data:
        row_values = []
        for value in row:
            row_values.append(int(value))
        typographic_map.append(row_values)
    return typographic_map


def get_reachable_9_positions(row, col, typographic_map):
    value = typographic_map[row][col]
    if value == 9:
        return {(row, col)}

    reachable_9_pos = set()
    next_positions = get_next_pos(row, col, typographic_map)
    for next_pos in next_positions:
        next_row, next_col = next_pos
        reachable_9_pos |= get_reachable_9_positions(
            next_row, next_col, typographic_map
        )
    return reachable_9_pos


def get_next_pos(row, col, typographic_map):
    current_value = typographic_map[row][col]
    next_pos = []
    d_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d_pos in d_positions:
        new_row = row + d_pos[0]
        new_col = col + d_pos[1]
        if is_inside_map(new_row, new_col, typographic_map):
            new_value = typographic_map[new_row][new_col]
            if new_value == current_value + 1:
                next_pos.append((new_row, new_col))
    return next_pos


def is_inside_map(row, col, typographic_map):
    map_height = len(typographic_map)
    map_width = len(typographic_map[0])
    if row < 0 or col < 0:
        return False
    elif row >= map_height or col >= map_width:
        return False
    return True


# Part 2
def main2():
    input_data = get_input("input10.txt")
    typographic_map = parse_input(input_data)
    map_height = len(typographic_map)
    map_width = len(typographic_map[0])

    score = 0
    for row in range(map_height):
        for col in range(map_width):
            if typographic_map[row][col] == 0:
                score += num_trails_from_pos(row, col, typographic_map)

    print(f"Answer 2 is: {score}")


def num_trails_from_pos(row, col, typographic_map):
    value = typographic_map[row][col]
    if value == 9:
        return 1

    num_trails = 0
    next_positions = get_next_pos(row, col, typographic_map)
    for next_pos in next_positions:
        next_row, next_col = next_pos
        num_trails += num_trails_from_pos(next_row, next_col, typographic_map)
    return num_trails


if __name__ == "__main__":
    main1()
    main2()
