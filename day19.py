# Advent of Code 2024 - day 19
from common import get_input


# Part 1
def main1():
    input_data = get_input("input19.txt")
    towels, patterns = parse_input(input_data)

    num_possible = 0
    for pattern in patterns:
        if possible(pattern, towels):
            num_possible += 1

    print(f"Answer 1 is: {num_possible}")


def parse_input(input_data):
    towels = input_data[0].split(", ")
    patterns = []
    for line in input_data[2:]:
        patterns.append(line)
    return towels, patterns


def possible(pattern, towels):
    for towel in towels:
        num_stripes = len(towel)
        if pattern == towel:
            return True
        elif len(pattern) >= num_stripes and pattern[:num_stripes] == towel:
            if possible(pattern[num_stripes:], towels):
                return True
    return False


# Part 2
def main2():
    input_data = get_input("input19.txt")
    towels, patterns = parse_input(input_data)

    total_num_possible_arrangements = 0
    for pattern in patterns:
        cache = {}
        total_num_possible_arrangements += num_possible_arrangements(
            pattern, towels, cache
        )

    print(f"Answer 2 is: {total_num_possible_arrangements}")


def num_possible_arrangements(pattern, towels, cache):
    if pattern in cache:
        return cache[pattern]
    result = 0
    for i, towel in enumerate(towels):
        num_stripes = len(towel)
        if pattern == towel:
            result += 1
        elif len(pattern) >= num_stripes and pattern[:num_stripes] == towel:
            result += num_possible_arrangements(pattern[num_stripes:], towels, cache)
    cache[pattern] = result
    return result


if __name__ == "__main__":
    main1()
    main2()
