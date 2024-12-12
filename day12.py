# Advent of Code 2024 - day 12
from common import get_input


# Part 1
def main1():
    grid = get_input("input12.txt")
    grid_height = len(grid)
    grid_width = len(grid[0])

    positions_to_check = {
        (row, col) for row in range(grid_height) for col in range(grid_width)
    }

    regions = []
    while not len(positions_to_check) == 0:
        pos = positions_to_check.pop()
        region_positions = get_region_positions(pos, grid)
        positions_to_check -= region_positions
        regions.append(region_positions)

    price = 0
    for region in regions:
        price += cost(region)

    print(f"Answer 1 is: {price}")


def get_region_positions(pos, grid):
    grid_positions = {pos}
    positions_to_check = {pos}
    checked_positions = set()
    while len(positions_to_check) > 0:
        pos = positions_to_check.pop()
        neighbors = get_same_type_neighbors(pos, grid)
        grid_positions |= neighbors
        checked_positions.add(pos)
        for neighbor in neighbors:
            if neighbor not in checked_positions:
                positions_to_check.add(neighbor)
    return grid_positions


def get_same_type_neighbors(pos, grid):
    letter = grid[pos[0]][pos[1]]
    connected = set()
    for d_pos in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (pos[0] + d_pos[0], pos[1] + d_pos[1])
        if not allowed_position(new_pos, grid):
            continue
        new_letter = grid[new_pos[0]][new_pos[1]]
        if new_letter == letter:
            connected.add(new_pos)
    return connected


def allowed_position(pos, grid):
    grid_height = len(grid)
    grid_width = len(grid[0])
    if not (0 <= pos[0] < grid_height):
        return False
    if not (0 <= pos[1] < grid_width):
        return False
    return True


def cost(region):
    area = len(region)
    perimeter = 0
    for pos in region:
        perimeter += 4 - num_neighbors_in_region(pos, region)
    return area * perimeter


def num_neighbors_in_region(pos, region):
    num = 0
    for d_pos in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (pos[0] + d_pos[0], pos[1] + d_pos[1])
        if new_pos in region:
            num += 1
    return num


if __name__ == "__main__":
    main1()
