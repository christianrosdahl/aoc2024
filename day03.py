# Advent of Code 2024 - day 3
from common import get_input
import re


# Part 1
def main1():
    input_data = get_input("input03.txt")
    text = "".join(input_data)
    sum = sum_multiplications(text)
    print(f"Answer 1 is: {sum}")


def sum_multiplications(string):
    multiplications = re.findall("mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\)", string)
    sum = 0
    for multiplication in multiplications:
        num1, num2 = re.split("mul\(|,|\)", multiplication)[1:3]
        num1, num2 = int(num1), int(num2)
        sum += num1 * num2
    return sum


# Part 2
def main2():
    input_data = get_input("input03.txt")
    text = "".join(input_data)
    text = get_enabled_part_of_string(text)
    sum = sum_multiplications(text)
    print(f"Answer 2 is: {sum}")


def get_enabled_part_of_string(text):
    activated = True
    text_to_save = ""
    while True:
        if activated:
            i = text.find("don't()")
            if i < 0:
                text_to_save += text
                break
            text_to_save += text[:i]
            text = text[i:]
            activated = False
        else:
            i = text.find("do()")
            if i < 0:
                break
            text = text[i + len("do()") :]
            activated = True
    return text_to_save


if __name__ == "__main__":
    main1()
    main2()
