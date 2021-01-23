# Name: Elena Rangelov
# Date: 12.2.2020
import os, time


def solve(puzzle, neighbors):
    variables = initial_variables(puzzle, neighbors)
    csp_table = sudoku_csp()
    return recursive_backtracking(puzzle, variables, csp_table, neighbors)


def sudoku_neighbors(csp_table):
    neighbors = {}
    for i in range(81):
        neighbors[i] = []
        for block in csp_table:
            if i in block:
                for val in block:
                    if val != i:
                        neighbors[i] += [val]
    return neighbors

def check_complete(assignment, csp_table):
    if assignment.find('.') != -1: return False
    for hexa in csp_table:
        if len(set([assignment[i] for i in hexa])) != 9: return False
    return True


def select_unassigned_var(assignment, variables, csp_table, neighbors):
    mrv = 10
    for var in variables:
        count = len(variables[var])
        if count == 1:
            return var
        if min(mrv, count) == count:
            mrv = count
            ret = var
    return ret



def isValid(value, var_index, assignment, variables, csp_table, neighbors):
    for n in neighbors[var_index]:
        if assignment[n] == value:
            return False
    for v, vals in variables.items():
        if len(vals) == 0: return False

    return True


def ordered_domain(var_index, assignment, variables, csp_table, neighbors):
    temp = {x:0 for x in variables[var_index]}
    for var in assignment:
        if var in temp: temp[var] = temp[var]+1
    temp2 = sorted([(var1, value) for value, var1 in temp.items()], reverse=True)
    return [val for var1, val in temp2]


def update_variables(value, var_index, assignment, variables, csp_table, neighbors):
    variables_copy = {k: vals[:] for k, vals in variables.items() if k != var_index}
    for n in neighbors[var_index]:
        if n in variables_copy:
            if value in variables_copy[n]:
                variables_copy[n].remove(int(value))
    return variables_copy



def recursive_backtracking(assignment, variables, csp_table, neighbors):
    if check_complete(assignment, csp_table): return assignment

    var = select_unassigned_var(assignment, variables, csp_table, neighbors)
    dom = ordered_domain(var, assignment, variables, csp_table, neighbors)
    # print(dom)
    for value in dom:
        if isValid(str(value), var, assignment, variables, csp_table, neighbors):
            assignment = assignment[:var] + str(value) + assignment[var + 1:]
            variables_copy = update_variables(value, var, assignment, variables, csp_table, neighbors)
            result = recursive_backtracking(assignment, variables_copy, csp_table, neighbors)
            if not result == None:
                return result
            assignment = assignment[:var] + "." + assignment[var + 1:]
    return None


def display(solution):
    ret = ""
    for z in range(0, 3):
        for y in range(0, 3):
            for x in range(0, 3):
                ret += " ".join(solution[27 * z + 9 * y + 3 * x:27 * z + 9 * y + 3 * x + 3])
                ret += "\t"
            ret += "\n"
        ret += "\n"
    return ret


def initial_variables(puzzle, neighbors):
    ret = {}
    for x in range(0, len(puzzle)):
        if puzzle[x] == ".":
            ret[x] = []
            for val in range(1, 10):
                b = True
                for n in neighbors[x]:
                    if puzzle[n] == str(val): b = False
                if b: ret[x] += [val]
    return ret


def sudoku_csp(n=9):
    csp_table = [[k for k in range(i * n, (i + 1) * n)] for i in range(n)]  # rows
    csp_table += [[k for k in range(i, n * n, n)] for i in range(n)]  # cols
    temp = [0, 1, 2, 9, 10, 11, 18, 19, 20]
    csp_table += [[i + k for k in temp] for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]]  # sub_blocks
    return csp_table


def checksum(solution):
    return sum([ord(c) for c in solution]) - 48 * 81  # One easy way to check a valid solution


def main():
    filename = input("file name: ")
    if not os.path.isfile(filename):
        filename = "puzzles.txt"
    csp_table = sudoku_csp()  # rows, cols, and sub_blocks
    neighbors = sudoku_neighbors(csp_table)  # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
    start_time = time.time()
    for line, puzzle in enumerate(open(filename).readlines()):
        # if line == 50: break  # check point: goal is less than 0.5 sec
        line, puzzle = line + 1, puzzle.rstrip()
        print("Line {}: {}".format(line, puzzle))
        solution = solve(puzzle, neighbors)
        if solution == None: print("No solution found."); break
        print("{}({}, {})".format(" " * (len(str(line)) + 1), checksum(solution), solution))
    print("Duration:", (time.time() - start_time))


if __name__ == '__main__': main()
