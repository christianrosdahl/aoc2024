# Common functions, used in several of the solutions
def get_input(path):
    file = open(path,'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    file.close()
    return lines
