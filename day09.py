# Advent of Code 2024 - day 9
from common import get_input


# Part 1
def main1():
    input_data = get_input("input09.txt")[0]
    disk_map = format_disk_map(input_data)
    disk_map = rearrange(disk_map)
    checksum = get_checksum(disk_map)

    print(f"Answer 1 is: {checksum}")


def format_disk_map(input_data):
    disk_map = []
    id_number = 0
    for i, number in enumerate(input_data):
        number = int(number)
        if i % 2 == 0:
            disk_map += [id_number] * number
            id_number += 1
        else:
            disk_map += ["."] * number
    return disk_map


def rearrange(disk_map):
    disk_map = remove_dots_from_end(disk_map)
    while not is_done(disk_map):
        last_entry = disk_map[-1]
        disk_map = disk_map[:-1]
        if last_entry == ".":
            continue
        else:
            first_dot_index = disk_map.index(".")
            disk_map[first_dot_index] = last_entry
    return disk_map


def remove_dots_from_end(old_disk_map):
    disk_map = old_disk_map
    while True:
        if disk_map[-1] == ".":
            disk_map = disk_map[:-1]
        else:
            break
    return disk_map


def is_done(disk_map):
    return not "." in disk_map


def get_checksum(disk_map):
    checksum = 0
    for i, num in enumerate(disk_map):
        if not num == ".":
            checksum += i * num
    return checksum


# Part 2
def main2():
    input_data = get_input("input09.txt")[0]
    files, free_spaces = parse_input(input_data)
    moved_files = get_moved_files(files, free_spaces)
    new_disk_map = get_new_disk_map(files, free_spaces, moved_files)
    checksum = get_checksum(new_disk_map)
    print(f"Answer 2 is: {checksum}")


def parse_input(input_data):
    files = []
    free_spaces = []
    id_number = 0
    for i, number in enumerate(input_data):
        number = int(number)
        if i % 2 == 0:
            files.append((id_number, number))
            id_number += 1
        else:
            free_spaces.append(number)
    return files, free_spaces


def get_moved_files(files, free_spaces):
    moved_files = {}
    for file in reversed(files):
        file_size = file[1]
        free_space_index = move_to_free_space(file, free_spaces)
        if free_space_index >= 0:
            if free_space_index in moved_files:
                moved_files[free_space_index].append(file)
            else:
                moved_files[free_space_index] = [file]
            free_spaces[free_space_index] -= file_size
    return moved_files


def move_to_free_space(file, free_spaces):
    file_index, file_size = file
    for space_index, space in enumerate(free_spaces[:-1]):
        if file_index > space_index and space >= file_size:
            return space_index
    return -1


def get_new_disk_map(files, free_spaces, moved_files):
    all_moved_files = []
    for moved_files_list in moved_files.values():
        all_moved_files += moved_files_list

    disk_map = []
    for file in files:
        file_index, file_size = file
        if not file in all_moved_files:
            disk_map += [file_index] * file_size
        else:
            disk_map += ["."] * file_size
        if file_index in moved_files:
            for file in moved_files[file_index]:
                moved_file_index, moved_file_size = file
                disk_map += [moved_file_index] * moved_file_size
        if file_index < len(free_spaces):
            disk_map += ["."] * free_spaces[file_index]

    return disk_map


if __name__ == "__main__":
    main1()
    main2()
