# Advent of Code 2024 - day 4
from common import get_input


# Part 1
def main1():
    grid = get_input("input04.txt")
    num_rows = len(grid)
    num_cols = len(grid[0])
    num_matches = 0
    for row in range(num_rows):
        for col in range(num_cols):
            num_matches += search_from_pos(grid, row, col)
    print(f"Answer 1 is: {num_matches}")


def search_from_pos(grid, row, col):
    num_steps = len("XMAS") - 1
    num_rows = len(grid)
    num_cols = len(grid[0])
    num_matches = 0
    for row_dir in [-1, 0, 1]:
        for col_dir in [-1, 0, 1]:
            if row + row_dir * num_steps < 0:
                continue
            elif row + row_dir * num_steps >= num_rows:
                continue
            elif col + col_dir * num_steps < 0:
                continue
            elif col + col_dir * num_steps >= num_cols:
                continue
            if has_word_in_direction(grid, row, col, row_dir, col_dir):
                num_matches += 1
    return num_matches


def has_word_in_direction(grid, row, col, row_dir, col_dir):
    for i, letter in enumerate("XMAS"):
        if not grid[row + i * row_dir][col + i * col_dir] == letter:
            return False
    return True


# Part 2
def main2():
    grid = get_input("input04.txt")
    num_rows = len(grid)
    num_cols = len(grid[0])
    num_matches = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if is_feasible_middle_pos(grid, row, col):
                if is_middle_of_x_mas(grid, row, col):
                    num_matches += 1

    print(f"Answer 2 is: {num_matches}")


def is_feasible_middle_pos(grid, row, col):
    num_rows = len(grid)
    num_cols = len(grid[0])
    if not (1 <= row < num_rows - 1):
        return False
    if not (1 <= col < num_cols - 1):
        return False
    return True


def is_middle_of_x_mas(grid, row, col):
    word1 = grid[row - 1][col - 1] + grid[row][col] + grid[row + 1][col + 1]
    word2 = grid[row + 1][col - 1] + grid[row][col] + grid[row - 1][col + 1]
    if not word1 in ["MAS", "SAM"]:
        return False
    if not word2 in ["MAS", "SAM"]:
        return False
    return True


if __name__ == "__main__":
    main1()
    main2()
