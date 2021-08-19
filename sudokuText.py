"""Sudoku generator"""
import random
import numpy as np


class Sudoku:
    """Sudoku class"""
    def __init__(self):
        self.sudoku = np.full((9, 9), 0)
        self.size = 9

    def draw(self):
        """draw sudoku"""
        self.generate()
        for row in range(self.size):
            for col in range(self.size):
                print(self.sudoku[row, col], end=" ")
                if (col + 1)/3 == 1 or (col + 1)/3 == 2:
                    print(" | ", end="")
            if (row + 1) / 3 == 1 or (row + 1) / 3 == 2:
                print("\n-----------------------")
            else:
                print()

    def generate(self):
        """generate sudoku"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for col in range(self.size):
            num = random.choice(numbers)
            self.sudoku[0, col] = num
            numbers.remove(num)

        self.sudoku[1, 0:3] = self.sudoku[0, 3:6]
        self.sudoku[1, 3:6] = self.sudoku[0, 6:10]
        self.sudoku[1, 6:10] = self.sudoku[0, 0:3]

        self.sudoku[2, 0:3] = self.sudoku[1, 3:6]
        self.sudoku[2, 3:6] = self.sudoku[1, 6:10]
        self.sudoku[2, 6:10] = self.sudoku[1, 0:3]


        self.sudoku[3:6, 0] = self.sudoku[0:3, 1]
        self.sudoku[3:6, 1] = self.sudoku[0:3, 2]
        self.sudoku[3:6, 2] = self.sudoku[0:3, 0]

        self.sudoku[3:6, 3] = self.sudoku[0:3, 4]
        self.sudoku[3:6, 4] = self.sudoku[0:3, 5]
        self.sudoku[3:6, 5] = self.sudoku[0:3, 3]

        self.sudoku[3:6, 6] = self.sudoku[0:3, 7]
        self.sudoku[3:6, 7] = self.sudoku[0:3, 8]
        self.sudoku[3:6, 8] = self.sudoku[0:3, 6]

        self.sudoku[6:10, 0] = self.sudoku[3:6, 1]
        self.sudoku[6:10, 1] = self.sudoku[3:6, 2]
        self.sudoku[6:10, 2] = self.sudoku[3:6, 0]

        self.sudoku[6:10, 0] = self.sudoku[3:6, 1]
        self.sudoku[6:10, 1] = self.sudoku[3:6, 2]
        self.sudoku[6:10, 2] = self.sudoku[3:6, 0]

        self.sudoku[6:10, 3] = self.sudoku[3:6, 4]
        self.sudoku[6:10, 4] = self.sudoku[3:6, 5]
        self.sudoku[6:10, 5] = self.sudoku[3:6, 3]

        self.sudoku[6:10, 6] = self.sudoku[3:6, 7]
        self.sudoku[6:10, 7] = self.sudoku[3:6, 8]
        self.sudoku[6:10, 8] = self.sudoku[3:6, 6]



if __name__ == '__main__':
    Sudoku().draw()
