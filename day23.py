# Advent of Code 2024 - day 23
from common import get_input
from itertools import combinations


# Part 1
def main1():
    input_data = get_input("input23.txt")
    connections_per_computer = parse_input(input_data)
    three_computer_groups = get_n_computer_groups(connections_per_computer, 3)
    groups = get_groups_with_computers_starting_at("t", three_computer_groups)
    print(f"Answer 1 is: {len(groups)}")


def parse_input(input_data):
    connections_per_computer = {}
    for line in input_data:
        computer1, computer2 = line.split("-")

        if computer1 in connections_per_computer:
            connections_per_computer[computer1].add(computer2)
        else:
            connections_per_computer[computer1] = {computer2}

        if computer2 in connections_per_computer:
            connections_per_computer[computer2].add(computer1)
        else:
            connections_per_computer[computer2] = {computer1}

    return connections_per_computer


def get_n_computer_groups(connections_per_computer, n):
    groups = set()
    for computer, connections in connections_per_computer.items():
        possible_groups = combinations({computer} | connections, n)
        for group in possible_groups:
            group = list(group)
            group.sort()
            group = tuple(group)
            if fully_connected(group, connections_per_computer):
                groups.add(group)
    return groups


def fully_connected(group, connections_per_computer):
    for i, computer1 in enumerate(group):
        for j, computer2 in enumerate(group):
            if i != j and not computer2 in connections_per_computer[computer1]:
                return False
    return True


def get_groups_with_computers_starting_at(letter, groups):
    found_groups = set()
    for group in groups:
        if group_contains_computer_starting_at(group, letter):
            found_groups.add(group)
    return found_groups


def group_contains_computer_starting_at(group, letter):
    for computer in group:
        if computer[0] == letter:
            return True
    return False


# Part 2
def main2():
    input_data = get_input("input23.txt")
    connections_per_computer = parse_input(input_data)
    largest_possible_group = (
        max([len(connected) for connected in connections_per_computer.values()]) + 1
    )
    group_size = largest_possible_group
    while group_size > 0:
        found_groups = get_n_computer_groups(connections_per_computer, group_size)
        if len(found_groups) > 0:
            break
        group_size -= 1
    largest_group = found_groups.pop()
    ans = ",".join(largest_group)
    print(f"Answer 2 is: {ans}")


if __name__ == "__main__":
    main1()
    main2()
