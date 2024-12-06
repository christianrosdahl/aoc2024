# Advent of Code 2024 - day 6
from common import get_input


# Part 1
def main1():
    input_data = get_input("input06.txt")
    grid = parse_input_to_grid(input_data)

    while True:
        if grid.next_pos_outside_grid(grid.direction):
            break
        while grid.next_pos_blocked(grid.direction):
            grid.rotate("right")
        grid.step()

    print(f"Answer 1 is: {len(grid.visited_pos)}")


def parse_input_to_grid(input_data):
    num_rows = len(input_data)
    num_cols = len(input_data[0])
    blocked_pos = set()
    pos_row = None
    pos_col = None
    for row in range(num_rows):
        for col in range(num_cols):
            grid_symbol = input_data[row][col]
            if grid_symbol == "#":
                blocked_pos.add((row, col))
            elif grid_symbol == "^":
                pos_row = row
                pos_col = col
    direction = "up"
    return Grid(num_rows, num_cols, blocked_pos, pos_row, pos_col, direction)


class Grid:
    def __init__(self, num_rows, num_cols, blocked_pos, pos_row, pos_col, direction):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.reset(pos_row, pos_col, direction, blocked_pos)

    def next_pos(self, direction):
        next_row = self.pos_row
        next_col = self.pos_col
        if direction == "up":
            next_row -= 1
        elif direction == "right":
            next_col += 1
        elif direction == "down":
            next_row += 1
        elif direction == "left":
            next_col -= 1
        return (next_row, next_col)

    def step(self):
        pos = self.next_pos(self.direction)
        self.pos_row = pos[0]
        self.pos_col = pos[1]
        self.visited_pos.add(pos)

    def next_pos_blocked(self, direction):
        pos = self.next_pos(direction)
        return pos in self.blocked_pos

    def next_pos_outside_grid(self, direction):
        next_row, next_col = self.next_pos(direction)
        if not (0 <= next_row < self.num_rows):
            return True
        elif not (0 <= next_col < self.num_cols):
            return True
        return False

    def rotate(self, direction):
        right_rotation = {"up": "right", "right": "down", "down": "left", "left": "up"}
        left_rotation = {"up": "left", "left": "down", "down": "right", "right": "up"}
        if direction == "right":
            self.direction = right_rotation[self.direction]
        elif direction == "left":
            self.direction = left_rotation[self.direction]

    def reset(self, pos_row, pos_col, direction, blocked_pos):
        self.pos_row = pos_row
        self.pos_col = pos_col
        self.direction = direction
        self.visited_pos = {(pos_row, pos_col)}
        self.visited_state = set()
        self.blocked_pos = blocked_pos.copy()


# Part 2
def main2():
    input_data = get_input("input06.txt")
    grid = parse_input_to_grid(input_data)
    start_row = grid.pos_row
    start_col = grid.pos_col
    start_direction = grid.direction
    start_blocked_pos = grid.blocked_pos

    num_loops = 0
    for row in range(grid.num_rows):
        for col in range(grid.num_cols):
            grid.reset(start_row, start_col, start_direction, start_blocked_pos)
            pos = (row, col)
            if pos in grid.blocked_pos or pos == (start_row, start_col):
                continue
            grid.blocked_pos.add(pos)
            if has_loop(grid):
                num_loops += 1

    print(f"Answer 2 is: {num_loops}")


def has_loop(grid):
    visited_states = set()

    while True:
        if grid.next_pos_outside_grid(grid.direction):
            return False

        while grid.next_pos_blocked(grid.direction):
            grid.rotate("right")

        grid.step()

        state = (grid.pos_row, grid.pos_col, grid.direction)
        if state in visited_states:
            return True
        visited_states.add(state)


if __name__ == "__main__":
    main1()
    main2()
