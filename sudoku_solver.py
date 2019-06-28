""" sudoku solver using human style logic strategy """

import os

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


# create a save file for my sudoku game to display the outcome of the solver, to help determine what feature s
# I must implement to create a fully working solver
def solved_save_file(puzzle_num, text_file):
    # open text file full of puzzles
    file = open("sudoku_resources\\"+text_file, 'r')
    contents = []  # list of each puzzle in the file
    for line in file:
        stripped_line = line.strip()
        contents.append(stripped_line)
    file.close()

    # create the puzzle string so we can solve it
    grid_str = contents[puzzle_num]
    grid_str = grid_str.replace(".", "0")
    grid = [int(num) for num in grid_str]

    # solve the puzzle
    solved = main_loop(grid)

    # save a file to be used to display the results using my sudoku game
    if solved:
        savegame("hard"+str(puzzle_num+1)+"solved", "hard", str(puzzle_num+1))
    else:
        savegame("hard"+str(puzzle_num+1)+"unsolved", "hard", str(puzzle_num+1))


# put all my functions into a loop to hopefully solve a puzzle, if successfully solved return True, else False
# If get stuck in loop with unchanging grid and possible values, then return False
def main_loop(puzzle_grid):
    # set starting state and remove possibilities from neighbours given those values
    initialise(puzzle_grid)
    prev_values = []
    prev_poss_values = []

    # continue looping till we have no more unset values, ie grid is solved, whether correct or not
    while SudokuCell.unset_values:
        # start by checking for any unset cells with only 1 possible value
        update_cell_values()
        # check groups for instances where the group has only 1 cell which can have a possible value
        check_group_possible_vals(SudokuCell.rows)
        check_group_possible_vals(SudokuCell.columns)
        check_group_possible_vals(SudokuCell.blocks)
        # check for cases in blocks where only 1 row or 1 column (out of the 3 overlapping) contains a possible value
        block_rowcol_conflict()
        # check for cases in rows and columns where only 1 block (of 3 overlapping) contains a possible value
        rowcol_block_conflict()
        # check for naked pairs/triples
        # naked_pairs_or_triples()
        hidden_pairs_triples()

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

        # get grid values
        values = [cell.value for cell in SudokuCell.cell_list]
        # grid values are unchanged from last loop, check if possible values are unchanged
        if prev_values == values:
            print("grid values unchanged...")
            poss_values = [cell.possible_values for cell in SudokuCell.cell_list]
            # if possible values are unchanged from last loop, we can save game state and terminate
            if prev_poss_values == poss_values:
                print("grid possible values unchanged...stuck in loop with unsolvable grid")
                return False
            else:  # update for next loop
                prev_poss_values = poss_values
        else:  # update for next loop
            prev_values = values

    print()
    print("Correct Solution?", check_solution())
    return check_solution()


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

    starting_values = []
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
                starting_values.append(cell)
            else:
                SudokuCell.unset_values.append(cell)

    # must now update all the neighbours of cells with starting values to remove possibilities
    for cell in starting_values:
        update_cell_neighbours(cell)


def update_cell_neighbours(sudoku_cell=None):
    # given a cell which has been given a new value, update its neighbours in the same row, column, block to
    # remove its value from their possible value lists
    print("\nUPDATE CELL", sudoku_cell.index, "NEIGHBOURS")

    def check_group(group, index):
        for neighbour in group[index]:
            # only check unset cells
            if neighbour.value == 0 and sudoku_cell.value in neighbour.possible_values:
                neighbour.possible_values.remove(sudoku_cell.value)
                if group == SudokuCell.rows:
                    print("updating ROW", index)
                if group == SudokuCell.columns:
                    print("updating COL", index)
                if group == SudokuCell.blocks:
                    print("updating BLOCK", index)

    # user can supply a single cell to update only its neighbours, else function tests all new cells
    check_group(SudokuCell.rows, sudoku_cell.row_index)
    check_group(SudokuCell.columns, sudoku_cell.col_index)
    check_group(SudokuCell.blocks, sudoku_cell.block_index)
    print()


def update_cell_values():
    # check the unset values possible values lists to see if they have only 1 value, then must update that value
    # call this to update cells after we have eliminated some possible values
    print("\nUPDATE CELL VALUES")
    cells_to_remove = []
    for cell in SudokuCell.unset_values:
        print("cell ", cell.index, "possible values:", cell.possible_values)
        if len(cell.possible_values) == 1:
            print("cell ", cell.index, "new value: ", cell.possible_values[0])
            cell.value = cell.possible_values[0]
            cells_to_remove.append(cell)
            update_cell_neighbours(cell)
    # TODO: unnecessary? using this because we are iterating through list while also potentially modifying it
    for cell in cells_to_remove:
        SudokuCell.unset_values.remove(cell)


# function to check possible values in groups and check if a value appears only once in the group, then
# we can set that value in whatever cell it is in and update
def check_group_possible_vals(groups):
    #TODO: known as hidden singles
    print("\nCHECK GROUP POSSIBLE VALS")
    # check all 9 groups in the set (rows/cols/blocks)
    count = 0
    for group in groups:
        # use a dictionary to count frequency of each possible value, use a list as the value and append any cell
        # object to the list if it had that value as a possible value, list should be min 1 cell long after checking
        value_counter = {}

        for cell in group:
            # only check unset cells
            if cell.value == 0:
                for val in cell.possible_values:
                    if val in value_counter:
                        value_counter[val].append(cell)
                    else:
                        value_counter[val] = [cell]

        if groups == SudokuCell.rows:
            print("ROW", count)
        if groups == SudokuCell.columns:
            print("COL", count)
        if groups == SudokuCell.blocks:
            print("BLOCK", count)

        # print("frequencies:", value_counter)
        for value in value_counter:
            print("poss val", value, "freq:", len(value_counter[value]))

        # check if any possible values has appeared only once in group, then set that value for the cell
        for poss_val in value_counter:
            if len(value_counter[poss_val]) == 1:
                # get cell, update value, and move from unset, to new vals list
                cell = value_counter[poss_val][0]
                print("possible value", poss_val, "can only be found at cell ", cell.index)
                print(cell.possible_values)
                # for test in group:
                #     if test.value == 0:
                #         print("cell ", test.index, "poss vals:", test.possible_values)
                cell.value = poss_val
                SudokuCell.unset_values.remove(cell)
                update_cell_neighbours(cell)
        count += 1


# function to check for inferred row/col possibility remover from block
# ie all instances of a value possibility within a block are also within a single row or column, then can check
# the row/column for that value and remove from possibilities, as no matter which cell gets the value in the block
# it will remove potential throughout the row/col  @@@ can check using group_index
def block_rowcol_conflict():
    print("\nBLOCK ROWCOL CONFLICT")
    block_counter = 0
    for block in SudokuCell.blocks:
        # only want to check unset values in the block, so must track them
        vals_to_check = []
        # lists to append possible values to
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
                    if val not in vals_to_check:
                        vals_to_check.append(val)

        # blocks are in a 3x3 grid, use the block row and col index
        block_row = block_counter // 3
        block_col = block_counter % 3
        # check if values appear in only a column or only a row
        print("block:", block_counter)
        for num in vals_to_check:
            # set variables for booleans which check if value is in each row and column, only check once for each num
            in_row0 = num in rows[0]
            in_row1 = num in rows[1]
            in_row2 = num in rows[2]
            in_col0 = num in cols[0]
            in_col1 = num in cols[1]
            in_col2 = num in cols[2]

            print("value:", num)
            print("in rows 0,1,2:", in_row0, in_row1, in_row2)
            print("in cols 0,1,2:", in_col0, in_col1, in_col2)

            def check_vals_in_group(relative_index, block_index, groups, bool1, bool2, bool3):
                # check the booleans
                # if bool1 is True and bool2 is False and bool3 is False:
                if bool1 and not bool2 and not bool3:
                    # remove values from same group/different block if we find a conflict
                    group_to_check = relative_index + block_index * 3
                    count = 0
                    for cell_ in groups[group_to_check]:
                        if count == 0:
                            if groups == SudokuCell.rows:
                                print("conflict with num", num, "in block", block_counter, "row", group_to_check)
                            if groups == SudokuCell.columns:
                                print("conflict with num", num, "in block", block_counter, "col", group_to_check)
                        count += 1
                        # must ignore set values and those in the block we just checked
                        if cell_.value == 0 and (cell_.block_index != block_counter) and num in cell_.possible_values:
                            cell_.possible_values.remove(num)

            # TODO: if we find an instance of a conflict, the other group cannot have one unless it is a single possible
            # value, does this matter at all?

            # check rows/remove possible values
            check_vals_in_group(0, block_row, SudokuCell.rows, in_row0, in_row1, in_row2)
            check_vals_in_group(1, block_row, SudokuCell.rows, in_row1, in_row0, in_row2)
            check_vals_in_group(2, block_row, SudokuCell.rows, in_row2, in_row0, in_row1)
            # check columns/remove possible values
            check_vals_in_group(0, block_col, SudokuCell.columns, in_col0, in_col1, in_col2)
            check_vals_in_group(1, block_col, SudokuCell.columns, in_col1, in_col0, in_col2)
            check_vals_in_group(2, block_col, SudokuCell.columns, in_col2, in_col0, in_col1)

        print()
        block_counter += 1


# Inverse of block rowcol conflict - If a row or column can only have a possible value in cells within 1 of the 3
# possible intersecting blocks, then no matter where in that row/column it is placed, it cannot be placed anywhere else
# in that block, so we can remove it from the possible values of the remaining cells in that block
def rowcol_block_conflict():
    print("\nROWCOL BLOCK CONFLICT")
    rows_and_cols = [SudokuCell.rows, SudokuCell.columns]
    checking_rows = True
    for groups in rows_and_cols:
        group_counter = 0
        for sub_group in groups:
            # only check the possible values and not the ones already set in that group
            vals_to_check = []
            # lists to append possible values to - each group has 3 blocks it intersects with
            blocks = [[], [], []]
            block_indexes = []
            counter = 0
            for cell in sub_group:
                # save the block indexes for when we have to remove values from the block - useful for columns
                if counter % 3 == 0:
                    block_indexes.append(cell.block_index)
                counter += 1
                # for unset values, check the possible values and add to the relative block lists
                if cell.value == 0:
                    # relative block index depends on if we are checking row or column, as they increment differently
                    if checking_rows:  # increments by 1 each new block
                        relative_block_index = cell.block_index % 3
                    else:  # increments by 3 each new block
                        relative_block_index = cell.block_index // 3
                    for val in cell.possible_values:
                        blocks[relative_block_index].append(val)
                        if val not in vals_to_check:
                            vals_to_check.append(val)

            for num in vals_to_check:
                # set variables for booleans which check if value is in each block, essentially using an exclusive or
                in_block0 = num in blocks[0]
                in_block1 = num in blocks[1]
                in_block2 = num in blocks[2]

                def check_vals_in_blocks(block_index, bool1, bool2, bool3):
                    # check the booleans
                    if bool1 and not bool2 and not bool3:
                        # remove values from same block if we find a conflict
                        for cell_ in SudokuCell.blocks[block_index]:
                            # must check the row/col index for the cell to ignore the cells in row/col we are checking
                            if checking_rows:
                                cell_group_index = cell.row_index
                                print("conflict with num", num, "in block", block_index, "row", group_counter)
                            else:
                                cell_group_index = cell.col_index
                                print("conflict with num", num, "in block", block_index, "col", group_counter)
                            # ignore set values and those in the row we are checking, and cells without the poss value
                            if cell_.value == 0 and (cell_group_index != group_counter) and num in cell_.possible_values:
                                cell_.possible_values.remove(num)

                # check rows/remove possible values
                check_vals_in_blocks(block_indexes[0], in_block0, in_block1, in_block2)
                check_vals_in_blocks(block_indexes[1], in_block1, in_block0, in_block2)
                check_vals_in_blocks(block_indexes[2], in_block2, in_block0, in_block1)

            print()
            group_counter += 1
        # update before moving to columns
        checking_rows = False


def naked_pairs_or_triples():
    # check all groups for naked pairs/triples
    for group in [SudokuCell.rows, SudokuCell.columns, SudokuCell.blocks]:
        for subgroup in group:
            # count number of times any unique pair or triple is seen - no bugs are possible with equivalent pairs eg.
            # (1,2) or (2,1), as possible values are all in order, so any pair or triple will be in same order\
            pairs = {}
            triples = {}

            def check_pair_triple(dictionary, length):
                # Save any pair seen in a dict, the key being the values as a string, the value being a list which
                # contains the cell. Another cell with the same possible values is added to the same dict entry.
                # TODO: could search through group only once to count pairs and triples, but unsure if they can mess
                # TODO: with each other...so just search and process each separately
                for cell_ in subgroup:
                    # only check unset cells
                    if cell_.value == 0:
                        poss_vals = cell_.possible_values
                        if len(poss_vals) == length:
                            if str(poss_vals) in dictionary:
                                dictionary[str(poss_vals)].append(cell_)
                            else:
                                dictionary[str(poss_vals)] = [cell_]

                # For a naked pair/triple, the dict value will be a list of cells of length 2 or 3, respectively.
                # Remove the pair/triple possible values from all unset cells which are not part of the pair/triple.
                for combination in dictionary:
                    if len(dictionary[combination]) == length:
                        # get the combo cells and values and then remove the values from any other cell in the group
                        combo_cells = dictionary[combination]
                        combo_vals = combo_cells[0].possible_values
                        for cell_ in subgroup:
                            # make sure cell is unset and not in the combo
                            if cell_.value == 0 and cell_ not in combo_cells:
                                for poss_val in combo_vals:
                                    if poss_val in cell_.possible_values:
                                        cell_.possible_values.remove(poss_val)
            check_pair_triple(pairs, 2)
            check_pair_triple(triples, 3)


def hidden_pairs_triples():
    for group in [SudokuCell.rows, SudokuCell.columns, SudokuCell.blocks]:
        for subgroup in group:
            # TODO: check each cell, if poss vals > 1 check all combinations (p/t), add to dict,
            # after all cells checked we have frequency of each combination, if = 2/3 then we have hidden combo
            # TODO: this should find any naked pairs too?? hidden have to be only instances of values in group,
            # naked can have extras, as long as only those values are in the pair/triple cells, could distinguish after
            # finding them though, ie go through determining combos, then do checks to determine if its hidden/naked

            # count number of times any unique pair or triple is seen - no bugs are possible with equivalent pairs eg.
            # (1,2) or (2,1), as possible values are all in order, so any pair or triple will be in same order\
            triples = {}
            pairs = {}

            def check_pair_triple(length, dictionary):
                # Save any pair seen in a dict, the key being the values as a string, the value being a list which
                # contains the cell. Another cell with the same possible values is added to the same dict entry.

                # frequencies must be re-initialised as we call function separately for pairs and triples
                val_frequencies = {}
                for cell_ in subgroup:
                    # only check unset cells
                    if cell_.value == 0:
                        poss_vals = cell_.possible_values
                        if len(poss_vals) >= length:
                            # TODO: current method, need to count freq of each poss val, in case there is extra nums
                            # TODO: freq of vals. Need to check only 2 of each in pair in group, of 3 for triples...
                            # OTHERWISE: create combos and check each
                            pair_list = []
                            triple_list = []
                            # determines pair combinations - only looking for ordered combos, so just check all values
                            # after the current
                            for index, val in enumerate(poss_vals):
                                # count frequencies of each possible value for each cell in group
                                if val in val_frequencies:
                                    val_frequencies[val] += 1
                                else:
                                    val_frequencies[val] = 1
                                # take combinations with values in front of current only - dont want reversed combos
                                for combo_val in poss_vals[index+1:]:
                                    pair_list.append([val, combo_val])
                            # skip triples if we only have 2 values, add pairs to dict first, then move to next cell
                            if length == 2:
                                # add pairs to dictionary, with the pair as index 0, for ease of access later
                                for pair in pair_list:
                                    if str(pair) in pairs:
                                        pairs[str(pair)].append(cell_)
                                    else:
                                        pairs[str(pair)] = [pair, cell_]
                                continue
                            # determines triple combinations by using each pair and adding each of the next values
                            for pair in pair_list:
                                # index of next value after pair is equal to the 2nd value - start here and increment
                                combo_val_index = pair[-1]
                                for combo_val in poss_vals[combo_val_index:]:
                                    triple_list.append(pair + [combo_val])
                            # add pairs to dictionary
                            for triple in triple_list:
                                if str(triple) in triples:
                                    triples[str(triple)].append(cell_)
                                else:
                                    triples[str(triple)] = [triple, cell_]

                # For a hidden pair/triple, the dict value will be a list of cells of length 3 or 4, respectively.
                # Index 0 is the pair/triple for access here, so makes the list 1 longer
                # The frequency of the possible values must be 2 or 3, respectively, else is not a hidden pair/triple.
                # Remove the pair/triple possible values from all unset cells which are not part of the pair/triple.
                for combination in dictionary:
                    if len(dictionary[combination]) - 1 == length:
                        # get the pair/triple values and check the frequencies of each value, if any are not 2 or 3
                        # then move to next combination, as this is not a viable hidden pair/triple
                        combo_vals = dictionary[combination][0]
                        hidden_combo = True
                        for value in combo_vals:
                            if val_frequencies[value] != length:
                                hidden_combo = False
                        if not hidden_combo:
                            continue
                        # Valid hidden pair/triple - process rest of the possible values in the pair/triple cells
                        combo_cells = dictionary[combination][1:]
                        for cell_ in combo_cells:
                            for poss_val in cell_.possible_values:
                                if poss_val not in combo_vals:
                                    cell_.possible_values.remove(poss_val)

            check_pair_triple(2, pairs)
            check_pair_triple(3, triples)


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


solved_save_file(89, "hardsudokupuzzles.txt")

