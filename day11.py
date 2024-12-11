# Advent of Code 2024 - day 11
from common import get_input


# Part 1
def main1():
    input_data = get_input("input11.txt")[0]
    stones = input_data.split()
    num_blinks = 25
    for blink in range(num_blinks):
        new_stones = []
        for stone in stones:
            new_stones += get_new_stones(stone)
        stones = new_stones
    print(f"Answer 1 is: {len(stones)}")


def get_new_stones(stone):
    if stone == "0":
        return ["1"]
    elif len(stone) % 2 == 0:
        num_digits = len(stone)
        new_num1 = str(int(stone[: int(num_digits / 2)]))
        new_num2 = str(int(stone[int(num_digits / 2) :]))
        return [new_num1, new_num2]
    else:
        return [str(int(stone) * 2024)]


# Part 2
def main2():
    input_data = get_input("input11.txt")[0]
    stones = input_data.split()
    num_blinks_left = 75
    new_stones_dict = {}
    num_stones_generated_dict = {}
    result = 0
    for stone in stones:
        state = (stone, num_blinks_left)
        result += num_of_stones_generated(
            state, num_stones_generated_dict, new_stones_dict
        )
    print(f"Answer 1 is: {result}")


def num_of_stones_generated(state, num_stones_generated_dict, new_stones_dict):
    stone, num_blinks_left = state
    if num_blinks_left == 0:
        return 1

    state = (stone, num_blinks_left)
    if state in num_stones_generated_dict:
        return num_stones_generated_dict[state]

    result = 0
    new_stones = get_new_stones2(stone, new_stones_dict)
    for new_stone in new_stones:
        new_state = (new_stone, num_blinks_left - 1)
        num_of_stones = num_of_stones_generated(
            new_state, num_stones_generated_dict, new_stones_dict
        )
        result += num_of_stones
        num_stones_generated_dict[new_state] = num_of_stones
    return result


def get_new_stones2(stone, new_stones_dict):
    if stone in new_stones_dict:
        return new_stones_dict[stone]

    if stone == "0":
        new_stones_dict["0"] = ["1"]
    elif len(stone) % 2 == 0:
        num_digits = len(stone)
        new_num1 = str(int(stone[: int(num_digits / 2)]))
        new_num2 = str(int(stone[int(num_digits / 2) :]))
        new_stones_dict[stone] = [new_num1, new_num2]
    else:
        new_stones_dict[stone] = [str(int(stone) * 2024)]

    return new_stones_dict[stone]


if __name__ == "__main__":
    main1()
    main2()
