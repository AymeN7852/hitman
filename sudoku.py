"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.0
"""

from typing import List, Tuple
import subprocess
from pprint import pprint
from itertools import combinations

# alias de types
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

example: Grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


example2: Grid = [
    [0, 0, 0, 0, 2, 7, 5, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 4, 6],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 8, 1, 0, 0, 0, 0],
    [4, 0, 6, 3, 0, 1, 0, 0, 9],
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 2, 0, 0, 0, 0, 3, 1, 0],
]


empty_grid: Grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

#### fonctions fournies


def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    return i * 81 + j * 9 + val + 1


def variable_to_cell(var: PropositionnalVariable) -> Tuple[int, int, int]:
    val = (var - 1) % 9
    return ((var - 1) // 81, ((var - 1) % 81) // 9, val)


def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    grid: Grid = empty_grid
    for var in model:
        i, j, val = variable_to_cell(var)
        grid[i][j] = val + 1
    return grid


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    clauses: Clause = []
    for i in variables:
        clauses.append(i)
    return clauses


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    clauseBase: ClauseBase = []
    clauseBase.append(at_least_one(variables))

    for i, j in combinations(variables, 2):
        clauseBase.append([-i, -j])

    return clauseBase


def create_cell_constraints() -> ClauseBase:
    clauseBase: ClauseBase = []
    for i in range(6):
        for j in range(7):
            variables: List[<PropositionnalVariable>] = []
            for val in range(9):
                variables.append(cell_to_variable(i, j, val))

            clauseBase += unique(variables)

    return clauseBase


def create_line_constraints() -> ClauseBase:
    clauseBase: ClauseBase = []

    for i in range(9):
        for val in range(9):
            variables: List[PropositionnalVariable] = []
            for j in range(9):
                variables.append(cell_to_variable(i, j, val))

            clauseBase.append(at_least_one(variables))

    return clauseBase


def create_column_constraints() -> ClauseBase:
    clauseBase: ClauseBase = []

    for j in range(9):
        for val in range(9):
            variables: List[PropositionnalVariable] = []
            for i in range(9):
                variables.append(cell_to_variable(i, j, val))

            clauseBase.append(at_least_one(variables))

    return clauseBase


def create_box_constraints() -> ClauseBase:
    clauseBase: clauseBase = []

    # for i in range(3):
    #     for j in range(3):
            


#### fonction principale


def main():
    # print(cell_to_variable(1, 3, 4))
    # print(variable_to_cell(729))
    # pprint(model_to_grid([2 * 81 + 4 * 9 + 1 + 1, 0 * 81 + 0 * 9 + 0 + 1]))
    # print(unique([200, 1, 4, 128]))
    print(create_cell_constraints())


if __name__ == "__main__":
    main()


# 1 9 possibilité par cases, 9 lignes, 9 colonnes -> 9*9*9 = 729 variables
# triplet (l,c,v) -> variable de la forme l*81 + c*9 + v + 1
# v = (n-1) % 9, c = ((n - 1)%81)//9, l = (n - 1)//81
