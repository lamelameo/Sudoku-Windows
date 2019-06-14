""" sudoku solver using human style logic strategy """

import os

#  --------------------------------------------
# | 01 - 02 - 03 | 04 - 05 - 06 | 07 - 08 - 09 |
# |    .    .    |    .    .    |    .    .    |
# | 10 - 11 - 12 | 13 - 14 - 15 | 16 - 17 - 18 |
# |    .    .    |    .    .    |    .    .    |
# | 19 - 20 - 21 | 22 - 23 - 24 | 25 - 26 - 27 |
# |--------------|--------------|--------------|
# | 28 - 29 - 30 | 31 - 32 - 33 | 34 - 35 - 36 |
# |    .    .    |    .    .    |    .    .    |
# | 37 - 38 - 39 | 40 - 41 - 42 | 43 - 44 - 45 |
# |    .    .    |    .    .    |    .    .    |
# | 46 - 47 - 48 | 49 - 50 - 51 | 52 - 53 - 54 |
# |--------------|--------------|--------------|
# | 55 - 56 - 57 | 58 - 59 - 60 | 61 - 62 - 63 |
# |    .    .    |    .    .    |    .    .    |
# | 64 - 65 - 66 | 67 - 68 - 69 | 70 - 71 - 72 |
# |    .    .    |    .    .    |    .    .    |
# | 73 - 74 - 75 | 76 - 77 - 78 | 79 - 80 - 81 |
#  --------------------------------------------

test_grid = [5, 3, 0, 0, 7, 0, 0, 0, 0,
             6, 0, 0, 1, 9, 5, 0, 0, 0,
             0, 9, 8, 0, 0, 0, 0, 6, 0,
             8, 0, 0, 0, 6, 0, 0, 0, 3,
             4, 0, 0, 8, 0, 3, 0, 0, 1,
             7, 0, 0, 0, 2, 0, 0, 0, 6,
             0, 6, 0, 0, 0, 0, 2, 8, 0,
             0, 0, 0, 4, 1, 9, 0, 0, 5,
             0, 0, 0, 0, 8, 0, 0, 7, 9]

solved_grid = [5, 3, 4, 6, 7, 8, 9, 1, 2,
               6, 7, 2, 1, 9, 5, 3, 4, 8,
               1, 9, 8, 3, 4, 2, 5, 6, 7,
               8, 5, 9, 7, 6, 1, 4, 2, 3,
               4, 2, 6, 8, 5, 3, 7, 9, 1,
               7, 1, 3, 9, 2, 4, 8, 5, 6,
               9, 6, 1, 5, 3, 7, 2, 8, 4,
               2, 8, 7, 4, 1, 9, 6, 3, 5,
               3, 4, 5, 2, 8, 6, 1, 7, 9]


# create a save file for my sudoku game to display the outcome of the solver, to help determine what feature s
# I must implement to create a fully working solver
def solved_save_file(puzzle_num, text_file):
    # open text file full of puzzles
    file = open(text_file, 'r')
    contents = []  # list of each puzzle in the file
    for line in file:
        stripped_line = line.strip()
        contents.append(stripped_line)
    file.close()

    # create the puzzle string so we can solve it
    grid_str = contents[puzzle_num]
    grid_str = grid_str.replace(".", "0")
    grid = [int(num) for num in grid_str]
    hard_string = ""

    # solve the puzzle
    main_loop(grid)
    # for num in grid:
    #     hard_string += "set" + str(num)
    # print(hard_string)

    # save a file to be used to display the results using my sudoku game
    savegame("hard"+str(puzzle_num)+"solved", "hard", str(puzzle_num))


# TODO: put all my functions into a loop to hopefully solve a puzzle
def main_loop(puzzle_num):
    initialise(puzzle_num)
    while SudokuCell.new_values:
        check_new_vals()
        update_cell_values()
        check_group_possible_vals(SudokuCell.rows)
        check_group_possible_vals(SudokuCell.columns)
        check_group_possible_vals(SudokuCell.blocks)
        block_rowcol_conflict()
        check_group_possible_vals(SudokuCell.rows)
        check_group_possible_vals(SudokuCell.columns)
        check_group_possible_vals(SudokuCell.blocks)

        # printing out updated grid for tracking progress...
        grid = [[] for _ in range(9)]
        counter = 1
        for cell in SudokuCell.cell_list:
            row = int(counter/9.1)
            grid[row].append(cell.value)
            counter += 1
        print("updated grid")
        for row in grid:
            print(row)
    print()
    print("Correct Solution?", check_solution())

    # possible_vals = ""
    # for cell in SudokuCell.cell_list:
    #     poss_vals = cell.possible_values
    #     possible_vals += "-"
    #     for val in poss_vals:
    #         possible_vals += str(val)
    # print(possible_vals)


class SudokuCell:
    cell_list = []  # list populated with all the created cell objects -  used to access them
    rows = [[] for _ in range(9)]
    columns = [[] for _ in range(9)]
    blocks = [[] for _ in range(9)]
    unset_values = []
    new_values = []

    def __init__(self, index):
        self.index = index  # keep track of objects with name (int: 1-81)
        self.value = 0  # the state of the position ie an integer value or 0 as default/empty
        self.start_state = 0  # identify if position has a starting value or is changeable
        self.prev_state = 0  # could use this for guessing, if it comes to that
        self.possible_values = [x for x in range(1, 10)]
        # keep track of which groups the cells are in
        self.row_index = None
        self.col_index = None
        self.block_index = None
        SudokuCell.cell_list.append(self)  # add created object to list

    def add_to_row(self, row):
        SudokuCell.rows[row].append(self)
        self.row_index = row

    def add_to_col(self, col):
        SudokuCell.columns[col].append(self)
        self.col_index = col

    def add_to_block(self, block):
        SudokuCell.blocks[block].append(self)
        self.block_index = block


def savegame(name, difficulty, puzzle_number):

    # create new text file with name entered
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    save = open(file_dir_path+'\\savefiles\\'+name+'.txt', 'w+')

    # puzzle number
    save.write(difficulty+puzzle_number+'\n')
    # game time - just set to 0
    save.write("0"+'\n')

    start_values, set_values, possible_values = "", "", ""
    for cell in SudokuCell.cell_list:
        # create string containing all starting values
        start_values += str(cell.start_state)
        # create string containing all set values
        if cell.value == "setempty":
            set_values += "set0"  # set emtpy cells values to "set0" for ease (all values 4 chars long)
        else:
            set_values += "set"+str(cell.value)
        # create string containing all pencil values for each cell
        possible_values += "-"  # separate each cells set of pencil values by "-" so we can easily distinguish them
        for value in cell.possible_values:
            possible_values += str(value)

    # write each string as a separate line in the save textfile for ease of loading
    save.write(start_values+'\n'+set_values+'\n'+possible_values)
    save.close()


def initialise(grid):
    # insert 9 cells into each row in the grid
    for row in range(9):
        for col in range(9):
            index = row * 9 + col
            # value of 0 means no starting value
            cell = SudokuCell(index)
            # add cell object to appropriate lists for future access
            cell.add_to_row(row)
            cell.add_to_col(col)
            # blocks are in a 3x3 grid which overlap multiple rows and columns...
            # cell row/col index -> block row/col index: (0,1,2)-> 0 | (3,4,5)-> 1 | (6,7,8)-> 2
            block_index = col//3 + 3*(row//3)  # block index = 0-8 from left-right, top-bottom
            cell.add_to_block(block_index)
            # set starting values
            if grid[index] != 0:
                cell.start_state = grid[index]
                cell.value = grid[index]
                SudokuCell.new_values.append(cell)
            else:
                SudokuCell.unset_values.append(cell)

    new_values = []
    for cell in SudokuCell.new_values:
        new_values.append(cell.value)
    print("new vals:", new_values)


def check_new_vals():
    # iterate through new values list to eliminate possibilities in grid for unset cells in same groups
    for cell in SudokuCell.new_values:
        # check row
        for neighbour in SudokuCell.rows[cell.row_index]:
            if neighbour.value == 0:
                print("deleting ROW possible value: ", cell.value)
                print(neighbour.possible_values)
                try:
                    neighbour.possible_values.remove(cell.value)
                except ValueError:
                    pass
        # check column
        for neighbour in SudokuCell.columns[cell.col_index]:
            if neighbour.value == 0:
                print("deleting COL possible value: ", cell.value)
                print(neighbour.possible_values)
                try:
                    neighbour.possible_values.remove(cell.value)
                except ValueError:
                    pass
        # check block
        for neighbour in SudokuCell.blocks[cell.block_index]:
            if neighbour.value == 0:
                print("deleting BLOCK possible value: ", cell.value)
                print(neighbour.possible_values)
                try:
                    neighbour.possible_values.remove(cell.value)
                except ValueError:
                    pass
        # checked all neighbours, remove value from list
        SudokuCell.new_values.remove(cell)


def update_cell_values():
    for cell in SudokuCell.unset_values:
        print("possible values", cell.possible_values)
        if len(cell.possible_values) == 1:
            print("new value")
            cell.value = cell.possible_values[0]
            SudokuCell.unset_values.remove(cell)
            SudokuCell.new_values.append(cell)


# TODO: need function to check possible values in groups and check if a value appears only once in the group, then
# we can set that value in whatever cell it is in and update
def check_group_possible_vals(groups):
    # check all 9 groups in the set (rows/cols/blocks)
    for group in groups:
        # use a dictionary to count frequency of each possible value, use a list as the value and append the cell
        # object to the list if it had that value as a possible value
        value_counter = {str(num): [] for num in range(1, 10)}

        for cell in group:
            if cell.value == 0:
                for val in cell.possible_values:
                    value_counter[str(val)].append(cell)

        # check if any of the possible values only has appeared once in group, and then set that value for the cell
        for poss_val in value_counter:
            if len(value_counter[poss_val]) == 1:
                # get cell, update value, and move from unset, to new vals list
                cell = value_counter[poss_val][0]
                cell.value = int(poss_val)
                SudokuCell.unset_values.remove(cell)
                SudokuCell.new_values.append(cell)


# TODO: need function to check for inferred row/col possibility remover from block
# ie all instances of a value possibility within a block are also within a single row or column, then can check
# the row/column for that value and remove from possibilities, as no matter which cell gets the value in the block
# it will remove potential throughout the row/col  @@@ can check using group_index
def block_rowcol_conflict():
    block_counter = 0
    for block in SudokuCell.blocks:
        rows = [[], [], []]
        cols = [[], [], []]
        # put each cell in a list for its row and column
        for cell in block:
            if cell.value == 0:
                # add all the possible values to the row list
                for val in cell.possible_values:
                    # use row/col index relative to the block, ie block 3 (top right) will have columns 6,7,8,
                    # which we will convert to 0,1,2, whereas rows are 0,1,2 already
                    relative_row_index = cell.row_index % 3
                    relative_col_index = cell.col_index % 3
                    rows[relative_row_index].append(val)
                    cols[relative_col_index].append(val)
        # check if values appear in only a column or only a row
        # TODO: check all values, see if in
        for num in range(1, 10):
            # remove values from same group if we find a conflict
            block_row = block_counter // 3
            block_col = block_counter % 3

            # check if value is in each row and column
            in_row0 = num in rows[0]
            in_row1 = num in rows[1]
            in_row2 = num in rows[2]
            in_col0 = num in cols[0]
            in_col1 = num in cols[1]
            in_col2 = num in cols[2]

            def check_vals_in_group(relative_index, block_index, bool1, bool2, bool3):
                if bool1 and not bool2 and not bool3:
                    print("row0")
                    row_to_check = relative_index + block_index * 3
                    for cell_ in SudokuCell.rows[row_to_check]:
                        if cell_.value == 0 and num in cell_.possible_values:
                            cell_.possible_values.remove(num)
            # check rows/remove possible values
            check_vals_in_group(0, block_row, in_row0, in_row1, in_row2)
            check_vals_in_group(1, block_row, in_row1, in_row0, in_row2)
            check_vals_in_group(2, block_row, in_row2, in_row0, in_row1)
            # check columns/remove possible values
            check_vals_in_group(0, block_col, in_col0, in_col1, in_col2)
            check_vals_in_group(0, block_col, in_col1, in_col0, in_col2)
            check_vals_in_group(0, block_col, in_col2, in_col0, in_col1)

    block_counter += 1


def check_solution():

    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # position values

    def check_groups(groups):
        # check each list in the group to determine if values 1-9 are present and return false at 1st error
        group_counter = 1
        for group in groups:  # for each item in the group
            group_values = []
            for cell in group:
                group_values.append(cell.value)
            for val in values:  # check for each value
                if val not in group_values:
                    print('ROW' + str(group_counter), 'ERROR')
                    return False
            group_counter += 1
        return True  # all checks were passed so return True for this group

        # if each group passed all the checks - should end game and bring up an image saying you won

    if check_groups(SudokuCell.rows) and check_groups(SudokuCell.columns) and check_groups(SudokuCell.blocks):
        return True
    else:
        return False


solved_save_file(0, "hardsudokupuzzles.txt")

