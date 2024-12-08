# Advent of Code 2024 - day 8
from common import get_input


# Part 1
def main1():
    input_data = get_input("input08.txt")
    antennas, map_dim = parse_input(input_data)
    antinodes = get_all_antinodes(antennas, map_dim)
    visualize(input_data, antinodes)
    print(f"Answer 1 is: {len(antinodes)}")


def parse_input(input_data):
    map_height = len(input_data)
    map_width = len(input_data[0])
    map_dim = (map_height, map_width)
    antennas = {}
    for line, line_text in enumerate(input_data):
        for col, col_text in enumerate(line_text):
            if col_text == ".":
                continue
            freq = col_text
            if freq in antennas:
                antennas[freq].append((line, col))
            else:
                antennas[freq] = [(line, col)]

    return antennas, map_dim


def get_all_antinodes(antennas, map_dim, any_distance=False):
    antinodes = set()
    for freq, antennas in antennas.items():
        antinodes_for_freq = get_antinodes_for_freq(antennas, map_dim, any_distance)
        for antinode in antinodes_for_freq:
            antinodes.add(antinode)
    return antinodes


def get_antinodes_for_freq(antennas, map_dim, any_distance):
    antinodes = set()
    for antenna1 in antennas:
        for antenna2 in antennas:
            if antenna1 == antenna2:
                continue
            antinodes_for_pair = get_antinodes(
                antenna1, antenna2, map_dim, any_distance
            )
            for antinode in antinodes_for_pair:
                if inside_map(antinode, map_dim):
                    antinodes.add(antinode)
    return antinodes


def get_antinodes(antenna1, antenna2, map_dim, any_distance):
    row1 = antenna1[0]
    row2 = antenna2[0]
    col1 = antenna1[1]
    col2 = antenna2[1]

    if not any_distance:  # Disregard resonance frequencies (part 1)
        antinode1_row = row1 + 2 * (row2 - row1)
        antinode1_col = col1 + 2 * (col2 - col1)
        antinode1 = (antinode1_row, antinode1_col)

        antinode2_row = row2 + 2 * (row1 - row2)
        antinode2_col = col2 + 2 * (col1 - col2)
        antinode2 = (antinode2_row, antinode2_col)

        return [antinode1, antinode2]

    # If resonance frequencies are taken into account (part 2)
    antinodes = []
    map_height, map_width = map_dim
    for dist in range(max(map_height, map_width)):
        antinode1_row = row1 + dist * (row2 - row1)
        antinode1_col = col1 + dist * (col2 - col1)
        antinode1 = (antinode1_row, antinode1_col)

        antinode2_row = row2 + dist * (row1 - row2)
        antinode2_col = col2 + dist * (col1 - col2)
        antinode2 = (antinode2_row, antinode2_col)

        antinodes.append(antinode1)
        antinodes.append(antinode2)

    return antinodes


def inside_map(antinode, map_dim):
    map_height, map_width = map_dim
    row, col = antinode
    if row < 0 or row >= map_height:
        return False
    elif col < 0 or col >= map_width:
        return False
    return True


def visualize(input_data, antinodes):
    for line_num, line in enumerate(input_data):
        for antinode in antinodes:
            if antinode[0] == line_num:
                antinode_col = antinode[1]
                line = line[:antinode_col] + "#" + line[antinode_col + 1 :]
        print(line)


# Part 2
def main2():
    input_data = get_input("input08.txt")
    antennas, map_dim = parse_input(input_data)
    antinodes = get_all_antinodes(antennas, map_dim, any_distance=True)
    visualize(input_data, antinodes)
    print(f"Answer 2 is: {len(antinodes)}")


if __name__ == "__main__":
    main1()
    main2()
