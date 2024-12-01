# Advent of Code 2024 - day 1
from common import get_input


# Part 1
def main1():
    input_data = get_input("input01.txt")

    left_list, right_list = get_sorted_lists(input_data)

    num_lines = len(left_list)
    differences = [abs(right_list[i] - left_list[i]) for i in range(num_lines)]
    print(
        f"The sum of the distances between the numbers in the sorted columns is {sum(differences)}."
    )


def get_sorted_lists(input_data):
    left_list = []
    right_list = []
    for line in input_data:
        num1, num2 = line.split()
        left_list.append(int(num1))
        right_list.append(int(num2))

    left_list.sort()
    right_list.sort()

    return left_list, right_list


# Part 2
def main2():
    input_data = get_input("input01.txt")

    left_list, right_list = get_sorted_lists(input_data)

    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_list.count(num)
    print(f"The similarity score is {similarity_score}.")


if __name__ == "__main__":
    main1()
    main2()
