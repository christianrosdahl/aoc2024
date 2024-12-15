# Advent of Code 2024 - day 15
from common import get_input


# Part 1
def main1():
    map_data = get_input("input15a.txt")
    movement_data = get_input("input15b.txt")
    warehouse, movements = parse_input(map_data, movement_data)

    for movement in movements:
        warehouse.move(movement)

    print(f"Answer 1 is: {warehouse.get_gps_sum()}")


def parse_input(map_data, movement_data):
    robot_pos, boxes, walls = parse_map(map_data)
    movements = parse_movements(movement_data)
    return Warehouse(robot_pos, boxes, walls), movements


def parse_map(map_data):
    robot_pos = None
    boxes = []
    walls = []
    for row, line in enumerate(map_data):
        for col, symbol in enumerate(line):
            if symbol == "#":
                walls.append((row, col))
            elif symbol == "O":
                boxes.append((row, col))
            elif symbol == "@":
                robot_pos = (row, col)
    return robot_pos, boxes, walls


def parse_movements(movement_data):
    movements = []
    for line in movement_data:
        for symbol in line:
            movement = None
            if symbol == "<":
                movement = (0, -1)
            elif symbol == ">":
                movement = (0, 1)
            elif symbol == "^":
                movement = (-1, 0)
            elif symbol == "v":
                movement = (1, 0)
            if movement:
                movements.append(movement)
    return movements


class Warehouse:
    def __init__(self, robot_pos, boxes, walls):
        self.robot_pos = robot_pos
        self.boxes = boxes
        self.walls = walls

    def move(self, direction):
        if self.can_move(self.robot_pos, direction):
            new_pos, has_box_to_move = self.move_robot(direction)
            while has_box_to_move:
                new_pos, has_box_to_move = self.move_box(new_pos, direction)

    def get_new_pos(self, pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def can_move(self, pos, direction):
        new_pos = self.get_new_pos(pos, direction)
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes:
            if not self.can_move(new_pos, direction):
                return False
        return True

    def move_robot(self, direction):
        new_pos = self.get_new_pos(self.robot_pos, direction)
        self.robot_pos = new_pos
        has_box_to_move = new_pos in self.boxes
        return new_pos, has_box_to_move

    def move_box(self, pos, direction):
        self.boxes.remove(pos)
        new_pos = self.get_new_pos(pos, direction)
        has_box_to_move = new_pos in self.boxes
        self.boxes.append(new_pos)
        return new_pos, has_box_to_move

    def get_gps_sum(self):
        sum = 0
        for box in self.boxes:
            sum += 100 * box[0] + box[1]
        return sum


# Part 2
def main2():
    map_data = get_input("input15a.txt")
    movement_data = get_input("input15b.txt")
    visualize = False
    height, width = len(map_data), 2 * len(map_data[0])
    warehouse, movements = parse_input2(map_data, movement_data)
    if visualize:
        display(warehouse, height, width)

    for movement in movements:
        warehouse.move(movement)
        if visualize:
            display(warehouse, height, width)

    print(f"Answer 2 is: {warehouse.get_gps_sum()}")


def parse_input2(map_data, movement_data):
    robot_pos, boxes, walls = parse_map2(map_data)
    movements = parse_movements(movement_data)
    return Warehouse2(robot_pos, boxes, walls), movements


def parse_map2(map_data):
    robot_pos = None
    boxes = []
    walls = []
    for row, line in enumerate(map_data):
        for col, symbol in enumerate(line):
            if symbol == "#":
                walls.append((row, 2 * col))
                walls.append((row, 2 * col + 1))
            elif symbol == "O":
                boxes.append((row, 2 * col))
            elif symbol == "@":
                robot_pos = (row, 2 * col)
    return robot_pos, boxes, walls


def display(warehouse, height, width):
    print()
    for row in range(height):
        line = "." * width
        for col in range(width):
            if (row, col) in warehouse.walls:
                line = line[:col] + "#" + line[col + 1 :]
            if (row, col) in warehouse.boxes:
                line = line[:col] + "[" + line[col + 1 :]
                line = line[: col + 1] + "]" + line[col + 2 :]
            if (row, col) == warehouse.robot_pos:
                line = line[:col] + "@" + line[col + 1 :]
        print(line)


class Warehouse2(Warehouse):
    def __init__(self, robot_pos, boxes, walls):
        super().__init__(robot_pos, boxes, walls)

    def move(self, direction):
        if self.can_move_robot(self.robot_pos, direction):
            box_in_pos = self.move_robot(direction)
            boxes_in_pos = set()
            if box_in_pos:
                boxes_in_pos.add(box_in_pos)

            while boxes_in_pos:
                all_new_boxes_in_pos = set()
                for box_in_pos in boxes_in_pos:
                    new_boxes_in_pos = self.move_box(box_in_pos, direction)
                    all_new_boxes_in_pos |= new_boxes_in_pos
                boxes_in_pos = all_new_boxes_in_pos

    def can_move_robot(self, pos, direction):
        new_pos = self.get_new_pos(pos, direction)
        if new_pos in self.walls:
            return False
        box_in_pos = self.get_box_in_pos(new_pos)
        if box_in_pos:
            if not self.can_move_box(box_in_pos, direction):
                return False
        return True

    def can_move_box(self, box, direction):
        for box_position in self.get_box_positions(box):
            new_pos = self.get_new_pos(box_position, direction)
            if new_pos in self.walls:
                return False
            box_in_pos = self.get_box_in_pos(new_pos)
            another_box_in_pos = box_in_pos and not box_in_pos == box
            if another_box_in_pos:
                if not self.can_move_box(box_in_pos, direction):
                    return False
        return True

    def move_robot(self, direction):
        new_pos = self.get_new_pos(self.robot_pos, direction)
        self.robot_pos = new_pos
        box_in_pos = self.get_box_in_pos(new_pos)
        return box_in_pos

    def move_box(self, pos, direction):
        self.boxes.remove(pos)
        boxes_in_pos = set()
        new_pos = self.get_new_pos(pos, direction)
        new_box_positions = self.get_box_positions(new_pos)
        for new_box_pos in new_box_positions:
            box_in_pos = self.get_box_in_pos(new_box_pos)
            if box_in_pos:
                boxes_in_pos.add(box_in_pos)
        self.boxes.append(new_pos)
        return boxes_in_pos

    def get_box_in_pos(self, pos):
        for box in self.boxes:
            if pos in self.get_box_positions(box):
                return box
        return None

    def get_box_positions(self, box):
        return [box, self.get_new_pos(box, (0, 1))]


if __name__ == "__main__":
    main1()
    main2()
