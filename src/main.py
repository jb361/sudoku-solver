# main.py
#
# This program implements a sudoku solver that finds the unique solution for a sudoku puzzle 
# using a depth-first search with constraint propagation. The search tree is pruned at the start 
# of the solve and after each guess by checking solved neighbours and removing any digits that are 
# no longer valid possibilities.

import time
import numpy as np

from solver import Solver

def main():
    """
    Test the solver with sample sudoku puzzles of various difficulties.
    """
    solver = Solver()
    difficulties = ['easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"../data/{difficulty}_puzzle.npy")
        solutions = np.load(f"../data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = solver.solve(sudoku)
            end_time = time.process_time()

            print(f"This is the solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is the solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

if __name__ == "__main__":
    main()
