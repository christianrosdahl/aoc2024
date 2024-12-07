# Advent of Code 2024 - day 7
from common import get_input


# Part 1
def main1():
    input_data = get_input("input07.txt")
    equations = parse_input(input_data)
    operator_types = ["+", "*"]
    result = 0
    for equation in equations:
        test_value, numbers = equation
        if can_be_true(test_value, numbers, operator_types):
            result += test_value

    print(f"Answer 1 is: {result}")


def parse_input(input_data):
    equations = []
    for line in input_data:
        test_value, numbers_string = line.split(": ")
        numbers = numbers_string.split()

        test_value = int(test_value)
        numbers = [int(number) for number in numbers]

        equations.append((test_value, numbers))
    return equations


def can_be_true(test_value, numbers, operator_types):
    num_operators = len(numbers) - 1
    operator_combinations = get_operator_combinations(num_operators, operator_types)
    for operators in operator_combinations:
        if equation_is_true(test_value, numbers, operators):
            return True
    return False


def get_operator_combinations(num_operators, operator_types):
    if num_operators == 1:
        return [[operator_type] for operator_type in operator_types]
    else:
        rest_combinations = get_operator_combinations(num_operators - 1, operator_types)
        combinations = []
        for rest_combination in rest_combinations:
            for operator in operator_types:
                combinations.append([operator] + rest_combination)
        return combinations


def equation_is_true(test_value, numbers, operators):
    result = numbers[0]
    for i, operator in enumerate(operators, 1):
        if operator == "+":
            result += numbers[i]
        elif operator == "*":
            result *= numbers[i]
        elif operator == "||":
            result = int(str(result) + str(numbers[i]))
        if result > test_value:
            return False
    if result == test_value:
        return True
    return False


# Part 2
def main2():
    input_data = get_input("input07.txt")
    equations = parse_input(input_data)
    operator_types = ["+", "*", "||"]
    result = 0
    for equation in equations:
        test_value, numbers = equation
        if can_be_true(test_value, numbers, operator_types):
            result += test_value

    print(f"Answer 2 is: {result}")


if __name__ == "__main__":
    main1()
    main2()
