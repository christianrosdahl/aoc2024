# Advent of Code 2024 - day 25
from common import get_input


# Part 1
def main1():
    input_data = get_input("input25.txt")
    keys, locks, max_column_size = parse_data(input_data)
    fitting_pairs = 0
    for key in keys:
        for lock in locks:
            if not overlapping(key, lock, max_column_size):
                fitting_pairs += 1

    print(f"Answer 1 is: {fitting_pairs}")


def overlapping(key, lock, max_column_size):
    for i in range(len(key)):
        if key[i] + lock[i] > max_column_size:
            return True
    return False


def parse_data(input_data):
    keys = []
    locks = []
    blocks = []
    block = []
    for i, line in enumerate(input_data):
        if len(line) == 0:
            blocks.append(block)
            block = []
        else:
            block.append(line)
    blocks.append(block)

    for block in blocks:
        columns = [[] for _ in range(len(block[0]))]
        is_lock = False
        if block[0] == "#" * len(block[0]):
            is_lock = True
        for line in block[1:-1]:
            for i, char in enumerate(line):
                columns[i].append(char)
        columns_sizes = []
        for column in columns:
            columns_sizes.append(column.count("#"))
        if is_lock:
            locks.append(columns_sizes)
        else:
            keys.append(columns_sizes)
    max_column_size = len(columns[0])
    return keys, locks, max_column_size


if __name__ == "__main__":
    main1()
