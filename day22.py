# Advent of Code 2024 - day 22
from common import get_input
import math


# Part 1
def main1():
    initial_secret_numbers = get_input("input22.txt")
    initial_secret_numbers = [int(num) for num in initial_secret_numbers]
    resulting_numbers = []
    for num in initial_secret_numbers:
        resulting_numbers.append(generate_secret_number(num, 2000))

    print(f"Answer 1 is: {sum(resulting_numbers)}")


def generate_secret_number(initial_number, num_generations=1):
    prune_number = 16777216
    num = initial_number
    for _ in range(num_generations):
        num = ((num * 64) ^ num) % prune_number
        num = (math.floor(num / 32) ^ num) % prune_number
        num = ((num * 2048) ^ num) % prune_number
    return num


# Part 2
def main2():
    initial_secret_numbers = get_input("input22.txt")
    initial_secret_numbers = [int(num) for num in initial_secret_numbers]
    sequence_to_profit_map = get_sequence_to_profit_map(initial_secret_numbers)
    best_sequence = max(sequence_to_profit_map, key=lambda x: sequence_to_profit_map[x])
    max_num_bananas = sequence_to_profit_map[best_sequence]

    print(f"Answer 2 is: {max_num_bananas}")


def get_sequence_to_profit_map(initial_secret_numbers):
    sequence_to_profit_map = {}
    for num in initial_secret_numbers:
        sequence_to_price_map = get_sequence_to_price_map(num)
        for sequence in sequence_to_price_map:
            if sequence in sequence_to_profit_map:
                sequence_to_profit_map[sequence] += sequence_to_price_map[sequence]
            else:
                sequence_to_profit_map[sequence] = sequence_to_price_map[sequence]
    return sequence_to_profit_map


def get_sequence_to_price_map(initial_number, num_generations=2000):
    secret_numbers = generate_secret_numbers(initial_number, num_generations)
    prices = [num % 10 for num in secret_numbers]
    price_diffs = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]
    sequence_to_price = [
        (tuple(price_diffs[i : i + 4]), prices[i + 4])
        for i in range(len(price_diffs) - 4)
    ]
    sequence_to_price_map = {}
    for sequence, price in sequence_to_price:
        if not sequence in sequence_to_price_map:
            sequence_to_price_map[sequence] = price
    return sequence_to_price_map


def generate_secret_numbers(initial_number, num_generations):
    result = [initial_number]
    num = initial_number
    for _ in range(num_generations):
        num = generate_secret_number(num)
        result.append(num)
    return result


if __name__ == "__main__":
    main1()
    main2()
