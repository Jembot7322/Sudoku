from random import shuffle
import copy
import math


class Sudoku:
    def __init__(self, size=9):
        """
        initializes new Sudoku grid
        """
        self.size = 9
        self.resetgrid(size)
        self.cc = 17
        self.solcounter = 0
        self.grid = []

    def resetgrid(self, size):
        """
        initializes grid of zeros with input dimension
        """
        self.grid = [
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

        # for grids bigger than classic
        if size > 9:
            self.size = size
            self.cc = 55
            self.grid = [[0] * self.size for _ in range(self.size)]

    def print_grid(self):
        """
        prints the contents of the sudoku grid into a better looking format for the user
        :return: printed sudoku grids
        """
        if self.size == 16:
            print('-----------------------------------------------------------------')
            for row in self.grid:
                rows = '| '
                for x in row:
                    rows += str(x)
                    if len(str(x)) > 1:
                        rows += '| '
                    else:
                        rows += ' | '
                print(rows)
            print('-----------------------------------------------------------------')

        else:
            print('-------------------')
            for row in self.grid:
                rows = '|'
                for x in row:
                    rows += str(x)
                    rows += '|'
                print(rows)
            print('-------------------')
        return

    def get_non_empty_squares(self, grid):
        """
        returns shuffled list of numbers that are to be placed in the grid
        :param grid: list of lists representing partially filled sudoku grid
        :return:
        """
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def find_empty_square(self, grid):
        """
        return index of next empty square in grid
        :param grid: input grid
        :return: tuple containing row number and column number
        """
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    return i, j
        return

    def checkspot(self, grid, row, col, num):
        """
        Checks the row, column, and sub-box for the number to see if it can be placed
        :return: True if valid to place number there
        """
        # check row
        if num in grid[row]:
            return False
        # check column
        for x in range(self.size):
            if grid[x][col] == num:
                return False

        rowstart = row - row % (int(math.sqrt(self.size)))
        colstart = col - col % (int(math.sqrt(self.size)))
        # check sub-box
        for i in range(int(math.sqrt(self.size))):
            for j in range(int(math.sqrt(self.size))):
                if grid[i + rowstart][j + colstart] == num:
                    return False
        return True

    def generate_sol(self, grid):
        """
        generates solution with backtracking
        :param grid: partial or empty grid to be solved
        :return: completed Sudoku grid
        """
        number_list = list(range(1, self.size + 1))

        for i in range(0, self.size ** 2):
            row = i // self.size
            col = i % self.size

            # find next empty cell
            if grid[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if self.checkspot(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            self.solcounter += 1
                            return True
                        else:
                            if self.generate_sol(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def remove_numbers_from_grid(self):
        """
        removes numbers from the puzzle until minimum clues are left to solve
        :return: list of lists representing sudoku grid with partial solution
        """
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        iterations = 3

        # clue count is how many minimum spaces filled for grid size
        while iterations > 0 and non_empty_squares_count <= self.cc:
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            # might need to put the value back if there is more than one solution
            removed_square = self.grid[row][col]
            self.grid[row][col] = 0
            # make a copy of the grid to solve and test solutions
            grid_copy = copy.deepcopy(self.grid)
            # initialize solutions counter to zero
            self.solcounter = 0
            self.generate_sol(grid_copy)
            # if there is more than one solution, put the last removed cell back into the grid
            if self.solcounter != 1:
                self.grid[row][col] = removed_square
                non_empty_squares_count += 1
                iterations -= 1
        return

    def main_menu(self):
        """
        main menu for user interaction
        :return: None
        """
        print("Welcome to the Super Sudoku Solver! ")
        menuchoice = 0
        while menuchoice != 5:

            if menuchoice == 1:
                newsize = int(input("What size grid? "))
                self.resetgrid(newsize)
                self.print_grid()
            if menuchoice == 2:
                newsize = int(input("What size grid? "))
                self.resetgrid(newsize)
                self.generate_sol(self.grid)
                self.remove_numbers_from_grid()
                self.print_grid()
            if menuchoice == 3:
                self.generate_sol(self.grid)
                self.print_grid()

            print("1 - Generate Empty Puzzle\n"
                  "2 - Generate Partial Puzzle\n"
                  "3 - Solve Puzzle\n"
                  "4 - Exit")
            menuchoice = int(input("Please input choice: "))
