# Advent of Code 2024 - day 5
from common import get_input


# Part 1
def main1():
    input_rules = get_input("input05a.txt")
    input_pages = get_input("input05b.txt")
    rules = parse_rules(input_rules)
    sequences = parse_sequences(input_pages)
    middle_numbers = []
    for sequence in sequences:
        if in_right_order(sequence, rules):
            middle_numbers.append(get_middle_number(sequence))

    print(f"Answer 1 is: {sum(middle_numbers)}")


def parse_rules(input_rules):
    rules = set()
    for line in input_rules:
        page1, page2 = line.split("|")
        rules.add((page1, page2))
    return rules


def parse_sequences(input_pages):
    sequences = []
    for sequence in input_pages:
        sequences.append(sequence.split(","))
    return sequences


def in_right_order(sequence, rules):
    for index, page in enumerate(sequence):
        if not page_in_right_order(index, page, sequence, rules):
            return False
    return True


def page_in_right_order(index, page, sequence, rules):
    for index2, page2 in enumerate(sequence):
        if index2 < index:
            if not correct_order(page2, page, rules):
                return False
        elif index2 > index:
            if not correct_order(page, page2, rules):
                return False
    return True


def correct_order(page1, page2, rules):
    if (page2, page1) in rules:
        return False
    return True


def get_middle_number(sequence):
    index = int((len(sequence) - 1) / 2)
    return int(sequence[index])


# Part 2
def main2():
    input_rules = get_input("input05a.txt")
    input_pages = get_input("input05b.txt")
    rules = parse_rules(input_rules)
    sequences = parse_sequences(input_pages)
    incorrect_sequences = []
    for sequence in sequences:
        if not in_right_order(sequence, rules):
            incorrect_sequences.append(sequence)

    middle_numbers = []
    for sequence in incorrect_sequences:
        sorted_sequence = sort_sequence(sequence, rules)
        middle_numbers.append(get_middle_number(sorted_sequence))

    print(f"Answer 2 is: {sum(middle_numbers)}")


def sort_sequence(unsorted_sequence, rules):
    sequence = unsorted_sequence
    for index1 in range(len(sequence)):
        for index2 in range(index1 + 1, len(sequence)):
            page1 = sequence[index1]
            page2 = sequence[index2]
            if not correct_order(page1, page2, rules):
                sequence[index1], sequence[index2] = sequence[index2], sequence[index1]
    return sequence


if __name__ == "__main__":
    main1()
    main2()
