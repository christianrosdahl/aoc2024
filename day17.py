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
    def __init__(self, regA, regB, regC):
        self.regA = regA
        self.regB = regB
        self.regC = regC
        self.instruction_pointer = 0
        self.output = []

    def __call__(self, program):
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]
            self.run_instruction(opcode, operand)
        output = self.output
        output = [str(num) for num in output]
        return ",".join(output)

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


if __name__ == "__main__":
    main1()
