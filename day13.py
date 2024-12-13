# Advent of Code 2024 - day 13
from common import get_input


def main(part):
    input_data = get_input("input13.txt")
    use_unit_conversion = part == 2
    machines = parse_data(input_data, use_unit_conversion)
    cost_a = 3
    cost_b = 1
    cost = 0
    for machine in machines:
        num_presses = get_num_presses(
            machine["a_coord"], machine["b_coord"], machine["prize"]
        )
        if num_presses:
            a_presses, b_presses = num_presses
            if num_presses[0].is_integer() and num_presses[1].is_integer():
                a_presses, b_presses = int(a_presses), int(b_presses)
                cost += cost_a * a_presses + cost_b * b_presses

    print(f"Answer {part} is: {cost}")


def parse_data(input_data, use_unit_conversion):
    machines = []
    machine = {}
    for line in input_data:
        if "Button A" in line:
            coord = line.split(": ")[1].split(", ")
            coord = (int(coord[0][2:]), int(coord[1][2:]))
            machine["a_coord"] = coord
        elif "Button B" in line:
            coord = line.split(": ")[1].split(", ")
            coord = (int(coord[0][2:]), int(coord[1][2:]))
            machine["b_coord"] = coord
        elif "Prize" in line:
            coord = line.split(": ")[1].split(", ")
            coord = (int(coord[0][2:]), int(coord[1][2:]))
            if use_unit_conversion:
                conversion_term = 10000000000000
                coord = (coord[0] + conversion_term, coord[1] + conversion_term)
            machine["prize"] = coord
            machines.append(machine)
            machine = {}
    return machines


def get_num_presses(a_coord, b_coord, prize):
    det = a_coord[0] * b_coord[1] - b_coord[0] * a_coord[1]
    if det == 0:
        return None
    a_presses = (b_coord[1] * prize[0] - b_coord[0] * prize[1]) / det
    b_presses = (a_coord[0] * prize[1] - a_coord[1] * prize[0]) / det
    return (a_presses, b_presses)


if __name__ == "__main__":
    main(part=1)
    main(part=2)
