# solver.py
#
# This program implements a sudoku solver that finds the unique solution for a sudoku puzzle 
# using a depth-first search with constraint propagation. The search tree is pruned at the start 
# of the solve and after each guess by checking solved neighbours and removing any digits that are 
# no longer valid possibilities.

import numpy as np

class Solver:
    """
    Find the unique solution for a sudoku puzzle using a depth-first search with
    constraint propagation.
    """
    def __init__(self):
        """
        Initialise variables and create a LUT of neighbour cells (i.e. cells in the same row,
        column or subgrid as each cell in the puzzle).
        """
        self.digits = '123456789'
        self.no_solution = np.full((9, 9), -1)
        self.cells = [x + y for x in self.digits for y in self.digits]

        rows = [[x + y for x in r for y in self.digits] for r in self.digits]
        columns = [[x + y for x in self.digits for y in c] for c in self.digits]

        subgrids = [[x + y for x in r for y in c] for r in ['123', '456', '789'] 
            for c in ['123', '456', '789']]
        permutations = dict((c, [p for p in list(rows + columns + subgrids) if c in p]) 
            for c in self.cells)

        self.neighbours = dict((c, set(sum(permutations[c], [])) - {c}) for c in self.cells)

    def to_dictionary(self, numpy_array, empty_cell):
        """
        Convert a 9x9 numpy array of integers to a dictionary of strings and replace empty
        cells with possible values (i.e. digits in the range 1 to 9).
        """
        dictionary = dict(zip(self.cells, numpy_array.flatten()))

        for key, value in dictionary.items():
            str_value = str(value)
            dictionary[key] = str_value

            if str_value == empty_cell:
                dictionary[key] = self.digits

        return dictionary

    def to_numpy_array(self, dictionary):
        """
        Convert a dictionary of strings to a 9x9 numpy array of integers.
        """
        for key, value in dictionary.items():
            dictionary[key] = int(value)

        return np.array(list(dictionary.values())).reshape((9, 9))

    def is_valid_puzzle(self, sudoku):
        """
        Check that a sudoku puzzle is 9x9 and contains numbers in the range 0 to 9.
        """
        if sudoku.shape != (9, 9):
            return False

        for i in range(9):
            for j in range(9):
                if sudoku[i, j] < 0 or sudoku[i, j] > 9:
                    return False

        return True

    def is_valid_solution(self, sudoku):
        """
        Check that the solution contains columns that add up to 45 (i.e. the sum of the 
        digits 1 to 9).
        """
        return np.sum(np.sum(sudoku, axis=0)) == 9 * 45

    def propagate(self, sudoku):
        """
        Find the unique solution for a sudoku puzzle using a depth-first search with 
        constraint propagation. The search tree is pruned at the start and after each guess 
        by checking solved neighbours and removing any digits that are no longer valid 
        possibilities.
        """
        while True:
            prev_solved = len([c for c in sudoku.keys() if len(sudoku[c]) == 1])

            # Remove any digits that appear in solved neighbours.
            for key, value in sudoku.items():
                if len(value) != 1:
                    solved_neighbours = set([sudoku[k] for k in self.neighbours[key] 
                        if len(sudoku[k]) == 1])
                    
                    sudoku[key] = ''.join(set(sudoku[key]) - solved_neighbours)

            # Exit the loop if no more cells were solved.
            if prev_solved == len([c for c in sudoku.keys() if len(sudoku[c]) == 1]):
                break

            # Return false if the puzzle is unsolvable (i.e. there is a cell with 0 digits).
            if len([c for c in sudoku.keys() if len(sudoku[c]) == 0]):
                return False

        # Return the solution if the puzzle is solved (i.e. all cells contain a single digit).
        if all(len(value) == 1 for key, value in sudoku.items()):
            return sudoku

        # Process the unsolved cell with the fewest possibilities.
        length, min_key = min((len(value), key) for key, value in sudoku.items() 
            if len(value) > 1)

        for digit in sudoku[min_key]:
            next_state = dict(sudoku)
            next_state[min_key] = digit

            next_solve = self.solve(next_state)

            if next_solve:
                return next_solve

    def solve(self, sudoku):
        """
        Solve a Sudoku puzzle and return its unique solution as a 9x9 numpy array of integers. 
        If there is no solution, all array entries will be -1.
        """
        if not self.is_valid_puzzle(sudoku):
            return self.no_solution

        solution_dict = self.propagate(self.to_dictionary(sudoku, '0'))
        if not solution_dict:
            return self.no_solution

        solution_array = self.to_numpy_array(solution_dict)
        if not self.is_valid_solution(solution_array):
            return self.no_solution

        return solution_array
