# Advent of Code 2024 - day 21
from common import get_input


def main(part=1, num_remotes_used_by_robots=2):
    codes = get_input("input21.txt")
    keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]
    remote = [["#", "^", "A"], ["<", "v", ">"]]
    data = {
        "cache": {},
        "keypad_key_to_pos": get_key_to_pos(keypad),
        "remote_key_to_pos": get_key_to_pos(remote),
        "num_remotes": num_remotes_used_by_robots + 1,
    }
    ans = 0
    for code in codes:
        sequence_cost = get_sequence_cost(code, data)
        numeric_part_of_code = int(code[:-1])
        ans += sequence_cost * numeric_part_of_code
    print(f"Answer {part} is: {ans}")


def get_key_to_pos(keypad):
    key_to_pos = {}
    for row, line in enumerate(keypad):
        for col, char in enumerate(line):
            key_to_pos[char] = (row, col)
    return key_to_pos


def get_sequence_cost(sequence, data, level=1):
    cache = data["cache"]
    movement = (level, sequence)
    if movement in cache:
        return cache[movement]
    cost = 0
    previous_key = "A"
    for key in sequence:
        cost += get_movement_and_activation_cost(previous_key, key, data, level)
        previous_key = key
    cache[movement] = cost
    return cost


def get_movement_and_activation_cost(key1, key2, data, level):
    cache = data["cache"]
    movement = (level, key1, key2)
    if movement in cache:
        return cache[movement]
    if level == data["num_remotes"]:
        movement_cost = get_distance(key1, key2, data["remote_key_to_pos"])
        activation_cost = 1
        min_cost = movement_cost + activation_cost
    else:
        if level == 1:
            options = get_movement_options(key1, key2, data["keypad_key_to_pos"])
        else:
            options = get_movement_options(key1, key2, data["remote_key_to_pos"])
        min_cost = None
        for option in options:
            movement_and_activation_option = option + "A"
            cost = get_sequence_cost(movement_and_activation_option, data, level + 1)
            if not min_cost or cost < min_cost:
                min_cost = cost
    cache[movement] = min_cost
    return min_cost


def get_distance(key1, key2, key_to_pos):
    pos1 = key_to_pos[key1]
    pos2 = key_to_pos[key2]
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])


def get_movement_options(key, next_key, key_to_pos):
    pos1 = key_to_pos[key]
    pos2 = key_to_pos[next_key]
    forbidden_pos = key_to_pos["#"]
    d_row = pos2[0] - pos1[0]
    d_col = pos2[1] - pos1[1]
    if d_row > 0:
        vertical_movement_type = "v"
    else:
        vertical_movement_type = "^"
    if d_col > 0:
        horizontal_movement_type = ">"
    else:
        horizontal_movement_type = "<"
    num_vertical_steps = abs(d_row)
    num_horizontal_steps = abs(d_col)
    sequences = get_combinations(num_vertical_steps, num_horizontal_steps)
    sequences = [
        sequence.replace("v", vertical_movement_type).replace(
            "h", horizontal_movement_type
        )
        for sequence in sequences
    ]
    remove_forbidden_sequence(sequences, pos1, forbidden_pos)
    return sequences


def get_combinations(num_vertical_steps, num_horizontal_steps):
    combinations = []
    if num_vertical_steps == 0:
        return ["h" * num_horizontal_steps]
    if num_horizontal_steps == 0:
        return ["v" * num_vertical_steps]
    combinations += [
        "v" + rest
        for rest in get_combinations(num_vertical_steps - 1, num_horizontal_steps)
    ]
    combinations += [
        "h" + rest
        for rest in get_combinations(num_vertical_steps, num_horizontal_steps - 1)
    ]
    return combinations


def remove_forbidden_sequence(sequences, start_pos, forbidden_pos):
    sequences_to_remove = []
    for sequence in sequences:
        if is_forbidden_sequence(sequence, start_pos, forbidden_pos):
            sequences_to_remove.append(sequence)
    for sequence in sequences_to_remove:
        sequences.remove(sequence)


def is_forbidden_sequence(sequence, start_pos, forbidden_pos):
    pos = start_pos
    command_to_change = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for command in sequence:
        change = command_to_change[command]
        pos = (pos[0] + change[0], pos[1] + change[1])
        if pos == forbidden_pos:
            return True
    return False


if __name__ == "__main__":
    main(part=1, num_remotes_used_by_robots=2)
    main(part=2, num_remotes_used_by_robots=25)
