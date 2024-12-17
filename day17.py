# Advent of Code 2024 - day 17
from common import get_input
import math


# Part 1
def main1():
    input_data = get_input("input17.txt")
    regA, regB, regC, program = parse_input(input_data)
    computer = Computer(regA, regB, regC)
    output = computer(program)

    print(f"Answer 1 is: {output}")


def parse_input(input_data):
    for line in input_data:
        if "Register A" in line:
            regA = int(line.split(": ")[1])
        elif "Register B" in line:
            regB = int(line.split(": ")[1])
        elif "Register C" in line:
            regC = int(line.split(": ")[1])
        elif "Program" in line:
            program = line.split(": ")[1]
            program = program.split(",")
            program = [int(num) for num in program]
    return regA, regB, regC, program


class Computer:
    def __init__(self, regA, regB, regC, output_string=True):
        self.regA = regA
        self.regB = regB
        self.regC = regC
        self.output_string = output_string
        self.instruction_pointer = 0
        self.output = []

    def __call__(self, program):
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]
            self.run_instruction(opcode, operand)
        output = self.output
        if self.output_string:
            output = [str(num) for num in output]
            return ",".join(output)
        return output

    def run_instruction(self, opcode, operand):
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)

    def combo(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.regA
        elif operand == 5:
            return self.regB
        elif operand == 6:
            return self.regC

    def adv(self, operand):
        self.regA = math.trunc(self.regA / (2 ** self.combo(operand)))
        self.instruction_pointer += 2

    def bxl(self, operand):
        self.regB = self.regB ^ operand
        self.instruction_pointer += 2

    def bst(self, operand):
        self.regB = self.combo(operand) % 8
        self.instruction_pointer += 2

    def jnz(self, operand):
        if self.regA == 0:
            self.instruction_pointer += 2
            return
        self.instruction_pointer = operand

    def bxc(self, operand):
        self.regB = self.regB ^ self.regC
        self.instruction_pointer += 2

    def out(self, operand):
        self.output.append(self.combo(operand) % 8)
        self.instruction_pointer += 2

    def bdv(self, operand):
        self.regB = math.trunc(self.regA / (2 ** self.combo(operand)))
        self.instruction_pointer += 2

    def cdv(self, operand):
        self.regC = math.trunc(self.regA / (2 ** self.combo(operand)))
        self.instruction_pointer += 2


# Part 2
def main2():
    """
    By observing the outputs for a range of regA values, we see that the length of the output vector seems to be
    monotonically non-decreasing. Furthermore, digit i in the vector seems to vary slower than digit i-1 for all i,
    and digit i doesn't seem to come back to a previous value while the digits at indices > i are constant.
    Based on these observations, we define a similarity measure between the output vector and the program vector.
    If they have different lengths, the similarity is -1, and otherwise it is in the interval [0, 1]. If the similarity
    is 1, the vectors are equal. If it is 0, the last digit in the vectors are different. A number in-between indicates
    the ratio of the number of consecutive last digits in the vector that are equal.

    The used method works as follows: regA starts out with its lowest allowed value. It is then increased in steps
    given by the specified step size until a positive similarity is found. Then, we jump back one step size, multiply
    the step size with a specified step decrease factor so that it is decreased, and continue the stepping with the
    new smaller step size. When a higher similarity value than before is found, we again take one step back and continue
    from there with a smaller step size. This process is repeated until the step size is 1. Then, we continue stepping
    until the similarity is 1.

    In order for the method to work, the step size has to be sufficiently small for all steps. If the method doesn't
    converge, a smaller initial step size should be selected.
    """
    input_data = get_input("input17.txt")
    regA, regB, regC, program = parse_input(input_data)

    regA = 1
    step_size = 100000000000
    step_decrease_factor = 0.1
    max_similarity = -1
    while True:
        regA_old = regA
        regA += step_size
        computer = Computer(regA, regB, regC, output_string=False)
        output = computer(program)
        similarity = get_similarity(program, output)
        print(f"Similarity = {similarity} for regA = {regA}")

        if similarity == 1:
            print(f"Answer 2 is: {regA}")
            break

        if similarity > max_similarity:
            max_similarity = similarity
            regA = regA_old
            step_size = int(max(step_size * step_decrease_factor, 1))


def get_similarity(program, output):
    if len(program) != len(output):
        return -1
    result = 0
    for i in range(len(program)):
        if program[-1 - i] == output[-1 - i]:
            result += 1
        else:
            break
    return result / len(output)


if __name__ == "__main__":
    main1()
    main2()
