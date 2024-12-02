# Advent of Code 2024 - day 2
from common import get_input


# Part 1
def main1():
    input_data = get_input("input02.txt")

    num_safe_reports = 0
    for report in input_data:
        if report_is_safe(report):
            num_safe_reports += 1

    print(f"The number of safe reports is: {num_safe_reports}")


def get_diffs(line):
    line = line.split()
    return [int(line[i + 1]) - int(line[i]) for i in range(len(line) - 1)]


def report_is_safe(report):
    diffs = get_diffs(report)
    is_increasing = diffs[0] > 0
    for diff in diffs:
        if is_increasing and diff < 0:
            return False
        elif not is_increasing and diff > 0:
            return False
        elif not (1 <= abs(diff) <= 3):
            return False
    return True


# Part 2
def main2():
    input_data = get_input("input02.txt")

    num_safe_reports = 0
    for report in input_data:
        if damped_report_is_safe(report):
            num_safe_reports += 1

    print(f"The number of safe reports is: {num_safe_reports}")


def get_damped_reports(line):
    line = line.split()
    damped_reports = []
    for i in range(len(line)):
        damped_report = " ".join(line[:i] + line[i + 1 :])
        damped_reports.append(damped_report)
    return damped_reports


def damped_report_is_safe(report):
    if report_is_safe(report):
        return True
    damped_reports = get_damped_reports(report)
    for damped_report in damped_reports:
        if report_is_safe(damped_report):
            return True
    return False


if __name__ == "__main__":
    main1()
    main2()
