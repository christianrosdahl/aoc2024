# Advent of Code 2024 - day 24
import copy
import math
import matplotlib.pyplot as plt
import random
import time
from common import get_input
from scipy import stats
from tqdm import tqdm


# Part 1
def main1():
    input_data = get_input("ex_input24.txt")
    known_signals, functions = parse_input(input_data)
    binary_num = compute(known_signals, functions)
    ans = int(binary_num, 2)
    print(f"Answer 1 is: {ans}")


def parse_input(input_data):
    known_signals = {}
    functions = []
    for line in input_data:
        if ":" in line:
            input, value = line.split(": ")
            known_signals[input] = int(value)
        elif "->" in line:
            combo, output = line.split(" -> ")
            input1, operator, input2 = combo.split()
            functions.append(
                {"inputs": (input1, input2), "operator": operator, "output": output}
            )
    return known_signals, functions


def evaluate(input_value1, input_value2, function):
    operator = function["operator"]
    if operator == "AND":
        return input_value1 & input_value2
    if operator == "XOR":
        return input_value1 ^ input_value2
    if operator == "OR":
        return input_value1 | input_value2


def compute(known_signals, functions):
    known_signals = copy.deepcopy(known_signals)
    functions = copy.deepcopy(functions)
    previous_function_len = len(functions)
    while True:
        for function in functions:
            input1, input2 = function["inputs"]
            if input1 in known_signals and input2 in known_signals:
                input_value1 = known_signals[input1]
                input_value2 = known_signals[input2]
                output_value = evaluate(input_value1, input_value2, function)
                output = function["output"]
                known_signals[output] = output_value
                functions.remove(function)
        if previous_function_len == len(functions) and len(functions) > 0:
            return None
        previous_function_len = len(functions)
        if len(functions) == 0:
            break
    sorted_signals = list(known_signals.keys())
    sorted_signals.sort()
    known_signals = {signal: known_signals[signal] for signal in sorted_signals}
    bits = []
    for signal, val in known_signals.items():
        if signal[0] == "z":
            bits.append(str(val))
    bits.reverse()
    binary_num = "".join(bits)
    return binary_num


# Part 2
"""
Method description:

The method uses the fact that in the correct system, a given output `z_i` only depends
on inputs `x_j` and `y_j` for j <= i. This means that the number of inputs that `z_i`
depends on should increase with 2 for each i, except for the last i, since
len(z) = len(x) + 1 = len(y) + 1. Thus, we should get an almost linear relation between
z_i and num_inputs(z_i) (the last i being the only exception).

Furthermore, the symmetry of the system also means that the number of gates of each
operator type that `z_i` depends on should increase linearly, with exception of the
first and last i, since the first and last numbers are special and break the symmetry.
Thus, we should expect linear relations between `z_i` and num_and(z_i), num_or(z_i) and
num_xor(z_i) for each i except i = 0 and i = len(z) - 1, where num_*(z_i) denotes the
number of operators of type * that z_i depends on.

The method thus proceeds as follows:

1. Find best pair of gates to switch by test switching each pair of gates and minimizing
    a cost. The cost is the sum of the standard errors for the by linear regression
    estimated slope between `z_i` and num_inputs(z_i), num_and(z_i), num_or(z_i) and
    num_xor(z_i), respectively, for i in [1, len(z) - 2].

2. Assuming that a unique best switch was found in 1, carry out that switch.

3. Repeat 1 and 2 two more times (until 3/4 switches are carried out).

4. Repeat 1 one more time (to find best last switch options). If a unique best switch is
    found, we are done with finding all four switches. If several best switch options
    are found, proceed to next step.

5. Find correct last switch by repeatedly feeding the system with random binary inputs
    `x` and `y` and discarding options that yield incorrect outputs `z`, until only
    one option remains.
"""


def main2():
    start_time = time.time()
    num_swaps = 4
    input_data = get_input("input24.txt")
    gates, zs, input_len = parse_input2(input_data)
    original_gates = copy.deepcopy(gates)

    best_swaps = []
    swapped_gates = []

    for swap_num in range(1, num_swaps + 1):
        print(
            f"Finding best swaps for swap number {swap_num}/{num_swaps} by testing all possible "
            "swaps for each gate."
        )
        best_swap_alts, cost = get_best_swaps(gates, zs, swapped_gates)
        print(
            f"Best swap alternatives (cost {cost}) for swap {swap_num}: "
            f"{best_swap_alts}"
        )

        last_swap = swap_num == num_swaps
        if not last_swap:
            error_string = (
                "Multiple best swap alternatives were found in swap number "
                f"{swap_num}. The method doesn't support this."
            )
            assert len(best_swap_alts) == 1, error_string
            best_swap = best_swap_alts[0]
        else:
            best_swap = find_last_swap(gates, best_swap_alts, input_len)

        best_swaps.append(best_swap)
        gate1, gate2 = best_swap
        swapped_gates.append(gate1)
        swapped_gates.append(gate2)
        swap_gates(gates, gate1, gate2)

    print("\nBest swaps found:", best_swaps)

    gates_to_swap = set()
    for swap in best_swaps:
        for gate in swap:
            gates_to_swap.add(gate)
    gates_to_swap = list(gates_to_swap)
    gates_to_swap.sort()
    ans = ",".join(gates_to_swap)
    print(f"Answer 2 is: {ans}")
    print_execution_time(start_time)

    plot(zs, original_gates, best_swaps)


def parse_input2(input_data):
    gates = {}
    xs = set()
    ys = set()
    zs = set()
    for line in input_data:
        if "->" in line:
            combo, output = line.split(" -> ")
            input1, operator, input2 = combo.split()
            gates[output] = {"inputs": (input1, input2), "operator": operator}
            for input in [input1, input2]:
                if input[0] == "x":
                    xs.add(input)
                elif input[0] == "y":
                    ys.add(input)
            if output[0] == "z":
                zs.add(output)
    xs = list(xs)
    ys = list(ys)
    zs = list(zs)
    xs.sort()
    ys.sort()
    zs.sort()
    assert len(xs) == len(ys), "Input lengths are different"
    input_len = len(xs)
    return gates, zs, input_len


def get_best_swaps(gates, zs, swapped_gates):
    min_cost = float("inf")
    best_swaps = []

    for i, gate1 in tqdm(enumerate(gates), desc="Swapping gates", total=len(gates)):
        for j, gate2 in enumerate(gates):
            if j <= i or gate1 in swapped_gates or gate2 in swapped_gates:
                continue

            swap_gates(gates, gate1, gate2)
            all_num_inputs = []
            all_num_and = []
            all_num_or = []
            all_num_xor = []
            bad_swap = False
            for z in zs:
                num_inputs = get_num_inputs(z, gates)
                num_and = get_num_operators("AND", z, gates)
                num_or = get_num_operators("OR", z, gates)
                num_xor = get_num_operators("XOR", z, gates)
                if (
                    num_inputs == None
                    or num_and == None
                    or num_or == None
                    or num_xor == None
                ):
                    bad_swap = True
                    break
                all_num_inputs.append(num_inputs)
                all_num_and.append(num_and)
                all_num_or.append(num_or)
                all_num_xor.append(num_xor)
            swap_gates(gates, gate2, gate1)

            if not bad_swap:
                swap = (gate1, gate2)
                cost = get_cost(all_num_inputs, all_num_and, all_num_or, all_num_xor)
                if cost == min_cost:
                    best_swaps.append(swap)
                if cost < min_cost:
                    best_swaps = [swap]
                    min_cost = cost
    return best_swaps, min_cost


def get_cost(all_num_inputs, all_num_and, all_num_or, all_num_xor):
    return (
        get_error(all_num_inputs)
        + get_error(all_num_and)
        + get_error(all_num_or)
        + get_error(all_num_xor)
    )


def get_error(values):
    values_except_ends = values[1:-1]
    indices = range(1, len(values_except_ends) + 1)
    linreg_result = stats.linregress(indices, values_except_ends)
    return linreg_result.stderr


def get_inputs(output, gates, previous=None):
    """
    Get all inputs `x_i` and `y_i` that the gate output `output` depends on.
    Returns None if path backwards from the gate output contains a loop.
    """
    if not previous:
        previous = set()
    inputs = set()
    for gate_input in gates[output]["inputs"]:
        if gate_input in previous:
            return None
        if gate_input[0] in ["x", "y"]:
            inputs.add(gate_input)
        else:
            next_inputs = get_inputs(gate_input, gates, previous | {output})
            if next_inputs == None:
                return None
            inputs |= next_inputs
    return inputs


def get_num_inputs(output, gates):
    """
    Get the number of inputs `x_i` and `y_i` that the gate output `output` depends on.
    Returns None if path backwards from the gate output contains a loop.
    """
    inputs = get_inputs(output, gates)
    if inputs == None:
        return None
    return len(inputs)


def get_num_operators(operator_type, output, gates, previous=None):
    """
    Get the number of operators of type `operator_type` that the output `output`
    depends on. Returns None if path backwards from the gate output contains a loop.
    """
    if not previous:
        previous = set()
    num_operators = 0
    operator = gates[output]["operator"]
    if operator == operator_type:
        num_operators += 1
    for gate_input in gates[output]["inputs"]:
        if gate_input in previous:
            return None
        if not gate_input[0] in ["x", "y"]:
            new_num_operators = get_num_operators(
                operator_type, gate_input, gates, previous | {output}
            )
            if new_num_operators == None:
                return None
            num_operators += new_num_operators
    return num_operators


def swap_gates(gates, output1, output2):
    gates[output1], gates[output2] = gates[output2], gates[output1]


def find_last_swap(gates, last_swap_alts, input_len):
    """
    Find last swap among alternatives by repeatedly testing each resulting network with
    random inputs and discarding options that yield incorrect output until only one
    option remains.
    """
    gates_alts = []
    for last_swap_alt in last_swap_alts:
        gates_alts.append(copy.deepcopy(gates))
        gate1, gate2 = last_swap_alt
        swap_gates(gates_alts[-1], gate1, gate2)

    discarded_alts = []
    while len(discarded_alts) < len(gates_alts) - 1:
        for i, gates_alt in enumerate(gates_alts):
            if i in discarded_alts:
                continue
            if not test_random_addition(gates_alt, input_len):
                discarded_alts.append(i)
                if len(discarded_alts) == len(gates_alts) - 1:
                    break

    for i in range(len(gates_alt)):
        if i not in discarded_alts:
            return last_swap_alts[i]


def test_random_addition(gates, input_len):
    output_len = input_len + 1
    functions = []
    for output, gate_info in gates.items():
        functions.append(
            {
                "inputs": gate_info["inputs"],
                "operator": gate_info["operator"],
                "output": output,
            }
        )
    x = random_binary_string(input_len)
    y = random_binary_string(input_len)
    z = compute2(x, y, functions)
    if z == None:
        return False
    z_expected = bin(int(x, 2) + int(y, 2))[2:].zfill(output_len)
    if not z == z_expected:
        return False
    return True


def random_binary_string(size):
    num = ""
    for _ in range(size):
        num += str(random.randint(0, 1))
    return num


def compute2(x, y, functions):
    input_signals = get_input_signals(x, y)
    return compute(input_signals, functions)


def get_input_signals(x, y):
    input_signals = {}
    input_signals.update(get_bits(x, "x"))
    input_signals.update(get_bits(y, "y"))
    return input_signals


def get_bits(signal, signal_name):
    bits = {}
    for i, signal_i in enumerate(reversed(signal)):
        bit_name = signal_name + str(i).zfill(2)
        bits[bit_name] = int(signal_i)
    return bits


def print_execution_time(start_time):
    print(
        "Execution time:",
        math.floor((time.time() - start_time) / 60),
        "min,",
        int(round((time.time() - start_time) % 60)),
        "s",
    )


def plot(zs, gates, swaps):
    num_swaps = len(swaps)
    fig, axs = plt.subplots(1, num_swaps + 1)
    for i in range(num_swaps + 1):
        all_num_inputs = []
        all_num_and = []
        all_num_or = []
        all_num_xor = []
        for z in zs:
            num_inputs = get_num_inputs(z, gates)
            num_and = get_num_operators("AND", z, gates)
            num_or = get_num_operators("OR", z, gates)
            num_xor = get_num_operators("XOR", z, gates)
            all_num_inputs.append(num_inputs)
            all_num_and.append(num_and)
            all_num_or.append(num_or)
            all_num_xor.append(num_xor)

        ax = axs[i]
        ax.set_title(f"After {i} swaps")
        ax.set_xlabel("$z_i$")
        ax.plot(all_num_inputs, label=r"num_inputs($z_i$)")
        ax.plot(all_num_and, label=r"num_and($z_i$)")
        ax.plot(all_num_or, label=r"num_or($z_i$)")
        ax.plot(all_num_xor, label=r"num_xor($z_i$)")

        if i < num_swaps:
            swap = swaps[i]
            gate1, gate2 = swap
            swap_gates(gates, gate1, gate2)

    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4)
    plt.show()


if __name__ == "__main__":
    main1()
    main2()
