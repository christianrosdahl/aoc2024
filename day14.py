# Advent of Code 2024 - day 14
from common import get_input


# Part 1
def main1():
    space_width = 101
    space_height = 103
    num_seconds = 100
    input_data = get_input("input14.txt")
    robots = parse_input(input_data, space_width, space_height)
    for _ in range(num_seconds):
        for robot in robots:
            robot.step()
    safety_factor = get_safety_factor(robots)
    print(f"Answer 1 is: {safety_factor}")


def parse_input(input_data, space_width, space_height):
    robots = []
    for line in input_data:
        pos_data, vel_data = line.split()
        x, y = pos_data.split("=")[1].split(",")
        pos = (int(x), int(y))
        v_x, v_y = vel_data.split("=")[1].split(",")
        velocity = (int(v_x), int(v_y))
        robots.append(Robot(pos, velocity, space_width, space_height))
    return robots


def get_safety_factor(robots):
    num_per_quadrant = [0, 0, 0, 0]
    for robot in robots:
        quadrant = robot.quadrant()
        if quadrant:
            num_per_quadrant[quadrant - 1] += 1

    factor = 1
    for num_in_quadrant in num_per_quadrant:
        factor *= num_in_quadrant
    return factor


class Robot:
    def __init__(self, pos, velocity, space_width, space_height):
        self.pos = pos
        self.velocity = velocity
        self.space_width = space_width
        self.space_height = space_height

    def step(self):
        x, y = self.pos
        v_x, v_y = self.velocity
        x_new = (x + v_x) % self.space_width
        y_new = (y + v_y) % self.space_height
        self.pos = (x_new, y_new)

    def quadrant(self):
        x, y = self.pos
        half_width_pos = (self.space_width - 1) / 2
        half_height_pos = (self.space_height - 1) / 2
        if x < half_width_pos and y < half_height_pos:
            return 1
        elif x > half_width_pos and y < half_height_pos:
            return 2
        elif x < half_width_pos and y > half_height_pos:
            return 3
        elif x > half_width_pos and y > half_height_pos:
            return 4
        else:
            return None


# Part 2
def main2():
    # Assumption: "Most of the robots are arranged as a christmas tree"
    # if and only if at least half of the robots have a neighbor
    space_width = 101
    space_height = 103
    max_num_seconds = 1000000
    input_data = get_input("input14.txt")
    robots = parse_input(input_data, space_width, space_height)
    max_num_robots_without_neighbors = len(robots) / 2 - 1
    for second in range(1, max_num_seconds + 1):
        for robot in robots:
            robot.step()
        if most_robots_have_neighbors(robots, max_num_robots_without_neighbors):
            display(robots, space_width, space_height)
            print(
                f"If the picture above contains a christmas tree, answer 2 is: {second}"
            )
            break


def most_robots_have_neighbors(robots, num_exceptions):
    num_without_neighbors = 0
    positions = set()
    for robot in robots:
        positions.add(robot.pos)
    for position in positions:
        x, y = position
        neighbors = {
            (x + 1, y),
            (x - 1, y),
            (x, y - 1),
            (x, y + 1),
        }
        if len(neighbors & positions) == 0:
            num_without_neighbors += 1

        if num_without_neighbors > num_exceptions:
            return False
    return True


def display(robots, space_width, space_height):
    print()
    for row_num in range(space_height):
        row = "." * space_width
        for robot in robots:
            x, y = robot.pos
            if y == row_num:
                row = row[:x] + "X" + row[x + 1 :]
        print(row)
    print()


if __name__ == "__main__":
    main1()
    main2()
