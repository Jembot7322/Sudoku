from sudoku import Sudoku

print("Welcome to the Super Sudoku Solver! ")
menuchoice = 0
s1 = Sudoku()
while menuchoice != 5:

    if menuchoice == 1:
        # generate blank grid
        newsize = int(input("What size grid? "))
        s1.resetgrid(newsize)
        s1.print_grid()
    if menuchoice == 2:
        newsize = int(input("What size grid? "))
        s1.resetgrid(newsize)
        # generate filled grid then remove until clue minimum is reached
        s1.generate_sol(s1.grid)
        s1.remove_numbers_from_grid()
        s1.print_grid()
    if menuchoice == 3:
        # complete partial or empty grid
        s1.generate_sol(s1.grid)
        s1.print_grid()

    print("1 - Generate Empty Puzzle\n"
          "2 - Generate Partial Puzzle\n"
          "3 - Solve Puzzle\n"
          "4 - Exit")
    menuchoice = int(input("Please input choice: "))
