""" attempt at a sudoku game """

import pygame
import sys
import os
from pygame.locals import *
import pathlib


def set_start_states(difficulty, puzzlenum):
    # given the difficulty type and puzzlenumber, set the starting state values for each Position object

    starting_state = ""

    if difficulty == 0:  # process easy puzzle selection
        # open the file and strip newline characters/whitespace for each line then append to a list
        file = open("sudoku_resources\\sudokuezpuzzles.txt", 'r')
        sudoku = []
        for line in file:
            thing = line.strip()
            sudoku.append(thing)
        file.close()

        # there are 50 easy puzzle start states, each 81 numbers of a grid is split into 10 lines
        # lines are split using \n so doesnt appear in .txt file when viewed in notepad
        # the first line is an identifier and then there are 9 lines of numbers corresponding to each row of the grid
        # concatenate all the grid rows into one 81 character string, with value of either 0 (empty) or an integer 1-9

        for puzzle_line in range(1, 10):  # loop through 9 lines, start at a value of 1 to skip the identifier line
            starting_state += sudoku[(puzzlenum - 1) * 10 + puzzle_line]  # puzzle index is 1 less than num

    elif difficulty == 1:  # process hard puzzle selection
        # open the file and strip newline characters/whitespace for each line then append to a list
        file2 = open("sudoku_resources\\hardsudokupuzzles.txt", 'r')
        sudoku = []
        for line in file2:
            stripped_line = line.strip()
            sudoku.append(stripped_line)
        file2.close()

        # the 95 hardpuzzles have the format: 1 line for each set of 81 grid numbers, each value is either an int 1-9
        # or '.' for an empty cell - replace values of '.' with '0' to be consistent with the easy puzzle format

        for value in range(81):
            position_value = sudoku[(puzzlenum - 1)][value]
            if position_value == '.':
                starting_state += '0'
            else:
                starting_state += position_value

    # set the starting state values for each grid cell using the Position class
    count = 0
    for pos in Position.positionlist:
        pos.start_state = starting_state[count]  # sets as '0' for changeable or 'int' for not
        pos.value = 'set' + starting_state[count]  # sets the position value to an integer
        count += 1


def num_pos_pic():
    pass
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


# set some constant variables for the RGB values of some standard colours
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DGRAY = (30, 30, 30)
LGRAY = (170, 170, 170)
CREAM = (249, 239, 217)


# ---------------------- MAKING POSITION CLASS AND OBJECTS -------------------------

class Position:
    positionlist = []  # list populated with all the created position objects -  used to access them
    potential_click = 0
    puzzlenumber = None
    errorPicShown = False
    delay = 0

    def __init__(self, name):
        self.name = name  # keep track of objects with name
        self.start_state = 0  # identify if position has a starting value or is changeable
        self.value = 0  # the state of the position ie an integer value or 0 as default/empty
        self.prev_state = 0  # keep track of positions changing value
        self.pencil_values = []  # 1 or 0 for each integer
        self.coordinates = []  # (x, y, w, h, xcentre, ycentre)
        self.pencil_coordinates = []  # (xcentre, ycentre) for each integers position in pencil mode
        Position.positionlist.append(self)  # add created object to list


def positionobjects():
    # make position objects named '1' - '81' from left to right, top to bottom in 9x9 grid
    for x in range(1, 82):
        Position(str(x))

    # set position coordinates
    (a, b, c, d, e, f) = (30, 30, 70, 70, 65, 65)  # (x, y, width, height, xcentre, ycentre)
    # set pencil coordinates for position objects
    # each position has 9 sets containing (x, y) coordinates
    pencil_coordinates = ((44, 44.5), (67, 44.5), (86, 44.5),
                          (44, 67), (67, 67), (86, 67),
                          (44, 89.5), (67, 89.5), (86, 89.5))

    # adding coordinates for positions and their pencil values by iterating through each cell in each row left-right
    for x1 in range(9):
        for y1 in range(9):
            index = x1*9 + y1  # the positions index in the Position list (0-80)
            # adding coordinates to the corresponding position class objects with values based on position in grid
            Position.positionlist[index].coordinates = (a + y1*70, b + x1*70, c, d, e + y1*70, f + x1*70)
            # iterate through pencil coordinates and increase the values of x or y depending on it position in the grid
            for xy_set in pencil_coordinates:
                new_coords = (xy_set[0] + (y1 * 70), xy_set[1] + (x1 * 70))
                Position.positionlist[index].pencil_coordinates.append(new_coords)


def rules():
    # checks if each group (row, column, block) contains values 1-9, if so it will return an image indicating
    # the solution is correct, else if any group doesnt pass then an error image is given
    # TODO: can change so that it only check values and make the lists after creation of position objects - is faster?

    rows = []  # list for each row, each element is a position in that row
    columns = []  # list for each column, each element is a position in that column
    blocks = []  # list for each block, each element is a position in that block

    # making rows
    counter = 0
    for num1 in range(9):
        newrow = []
        rows.append(newrow)
        for num2 in range(9):
            position_index = num1 * 9 + num2
            rows[num1].append(Position.positionlist[position_index].value)
            counter += 1

    # making columns
    for num1 in range(9):
        newcolumn = []
        columns.append(newcolumn)
        for num2 in range(9):
            newcolumn.append(rows[num2][num1])

    # making blocks
    counter2 = 0
    # append 9 blocks into block list before adding values as we add values to more than one block each loop
    for num1 in range(9):
        newblock = []
        blocks.append(newblock)
    for num1 in range(9):  # for each row
        if num1 in [0, 1, 2]:
            counter2 = 0  # for first 3 rows insert into first 3 blocks
        elif num1 in [3, 4, 5]:
            counter2 = 3  # for 2nd 3 rows insert into middle 3 blocks
        elif num1 in [6, 7, 8]:
            counter2 = 6  # for 3rd 3 rows insert into last 3 blocks
        for num2 in range(3):  # for each position in the row (3 x 3 nested loops)
            for num3 in range(3):  # append groups of 3 values from that row into 3 the blocks that overlap that row
                index = num2*3 + num3
                blocks[counter2].append(rows[num1][index])
            counter2 += 1  # change the block after 3 row values are added

    # checking position values against rules
    values = ['set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7', 'set8', 'set9']  # position values

    def check_groups(group):
        # check each list in the group to determine if values 1-9 are present and return false at 1st error
        group_counter = 1
        for listitem in group:  # for each item in the group
            for val in values:  # check for each value
                if val not in listitem:
                    print('ROW' + str(group_counter), 'ERROR')
                    return False
            group_counter += 1
        return True  # all checks were passed so return True for this group

    # if each group passed all the checks - should end game and bring up an image saying you won
    if check_groups(rows) and check_groups(columns) and check_groups(blocks):
        try:
            get_image("sudoku_resources\\sudoku_correct.png", (400, 345))
        except pygame.error as errorMessage:  # displays text only if image cant be found
            error_text = str(errorMessage)[14:]
            win_text = "YOU WIN..." + "*Missing File: " + error_text + "*"
            Position.errorPicShown = True
            get_text(28, win_text, BLACK, (346, 345), BLUE)

    else:  # error was found - display error image and message
        # TODO: highlight rows/columns/blocks with mistakes??
        print('\nCHECK FOR MISTAKES...\n')
        print('ROW 1-9: top-bottom\nCOLUMN 1-9: left-right\nBLOCK 1-9: left-right then top-bottom')
        try:
            get_image("sudoku_resources\\sudoku_error.png", (400, 345))
            Position.errorPicShown = True
        except pygame.error as errorMessage:  # display text if error picture isnt found
            print(errorMessage)
            error_text = "Check for Mistakes. " + "*Missing File: " + str(errorMessage)[14:] + "*"
            Position.errorPicShown = True
            get_text(26, error_text, BLACK, (360, 345), BLUE)


def clear_states():
    # clear values for all positions if they are not starting values, leave pencil values unchanged
    # TODO: add option for removing pencil states
    for pos in Position.positionlist:
        if pos.start_state == '0':
            pos.value = 'set0'  # reset value
            positiontext(pos)  # redraw graphics so it is empty
        else:
            pass


# ---------------------------- MAKING BUTTONS CLASS AND GRAPHICS ---------------------------------

class Button:
    buttondict = {}
    startbuttons = []
    startbutdict = {}
    activestate = None
    pencilstate = None
    potential_click = 0
    prev_hover = None

    def __init__(self, name):
        self.name = name
        self.state = 0  # default state, 1 = active
        self.was_hovered = False
        self.coordinates = (0, 0, 0, 0, 0, 0)
        self.textcoords = ()
        self.text = name

    def add_dict(self):
        Button.buttondict[self.name] = self  # add button to a dictionary with key as name and value as object

    def add_startlist(self):
        Button.startbuttons.append(self)  # add start buttons to list sequentially - 0-49=easy, 49-139=hard

    def add_startdict(self):
        Button.startbutdict[self.name] = self  # add button to a dictionary with key as name and value as object
        pass

    def clicked(self):
        # change state to clicked or unclicked
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0


def buttonobjects():

    int_list = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    buttonlist = ['setempty', 'set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7',
                  'set8', 'set9', 'pencil', 'clear', 'check', 'save', 'savetextbox']
    # list of coordinates for each button: (xorigin, yorigin, width, height, xcentre, ycentre)
    coordinateslist = [(720, 100, 65, 70, 752.5, 135), (785, 100, 65, 70, 817.5, 135),
                       (720, 170, 65, 70, 752.5, 205), (785, 170, 65, 70, 817.5, 205),
                       (720, 240, 65, 70, 752.5, 275), (785, 240, 65, 70, 817.5, 275),
                       (720, 310, 65, 70, 752.5, 345), (785, 310, 65, 70, 817.5, 345),
                       (720, 380, 65, 70, 752.5, 415), (785, 380, 65, 70, 817.5, 415),
                       (720, 460, 130, 30, 785, 475), (720, 500, 130, 30, 785, 515),
                       (720, 540, 130, 30, 785, 555), (720, 580, 130, 30, 785, 595),
                       (720, 620, 130, 30, 785, 635)]

    # create class objects for buttons
    integer = 0
    for name in buttonlist:
        newbutton = Button(name)
        newbutton.add_dict()
        Button.buttondict[name].coordinates = coordinateslist[integer]
        integer += 1
    # change text for integer buttons - dont want the names to appear on the button graphic just the integer
    integer = 0
    for name in buttonlist[:10]:
        Button.buttondict[name].text = int_list[integer]
        integer += 1

    Button.buttondict['savetextbox'].text = 'Enter File Name'


def get_text(size, text, text_col, coords, back_col=None, align=None):
    # draws the given text (with set size and colour) onto the gamescreen
    text_obj = pygame.font.Font('freesansbold.ttf', size)
    surface_obj = text_obj.render(text, True, text_col, back_col)
    rect_obj = surface_obj.get_rect()
    # TODO: doesnt support all alignments
    if align == "midleft":
        rect_obj.midleft = coords
    else:
        rect_obj.center = coords
    GAMESCREEN.blit(surface_obj, rect_obj)


def get_image(file_path, coords):
    # draws an image onto the gamescreen given a filepath and coordinates
    image_obj = pygame.image.load(file_path)
    rect_obj = image_obj.get_rect()
    rect_obj.center = coords
    GAMESCREEN.blit(image_obj, rect_obj)


def drawbutton(button, fill=BLACK, size=22):
    # general function to draw/redraw a button given coordinates and colours
    x = button.coordinates[0] + 1
    y = button.coordinates[1] + 1
    width = button.coordinates[2] - 2
    height = button.coordinates[3] - 2
    button_centre = (button.coordinates[4], button.coordinates[5])

    # first, draw the button fill (for all button types)
    pygame.draw.rect(GAMESCREEN, fill, [x, y, width, height])

    # draw the button text
    if button.name == 'setempty':
        try:  # try load eraser image else use text for button
            get_image("sudoku_resources\\eraser3.png", (752.5, 135))
        # couldnt find image, use text instead, give warning
        except pygame.error as image_error:
            print("Warning - Missing Button Image File: " + str(image_error)[14:])
            # set default eraser object as text
            get_text(14, "del", BLUE, (752.5, 135))

    elif button.name == 'savetextbox':
        if button.state == 1:  # if textbox is active (clicked) draw text in white
            get_text(14, button.text, WHITE, button_centre)
        else:  # if inactive, draw over default black fill then draw black text
            pygame.draw.rect(GAMESCREEN, DGRAY, [x, y, width, height])  # draw box
            get_text(14, button.text, BLACK, button_centre)  # draw text

    elif button.name in ('pencil', 'clear', 'check', 'save'):
        get_text(size, button.text, LGRAY, button_centre)  # draw text in light gray

    else:  # for integer buttons draw text in blue
        get_text(size, button.text, BLUE, button_centre)  # draw text in light gray


def index_in_grid(event_pos, xlower, xupper, ylower, yupper, cell_size, num_cols):
    # determine what index in a grid an event occurred in, given the grid region's x and y bounds and the event position
    # return that index if the event occured in the grid, else return nothing
    if xlower < event_pos[0] < xupper and ylower < event_pos[1] < yupper:
        # gives the row and column index of the button in the easy grid
        grid_col = (event_pos[0] - xlower) // cell_size
        grid_row = (event_pos[1] - ylower) // cell_size
        # if the remainder of the division of position by grid size is 0, then the mouse is on an edge
        col_remainder = (event_pos[0] - xlower) % cell_size
        row_remainder = (event_pos[1] - ylower) % cell_size
        # calculate the index of the button in the grid of buttons, assuming a left-right, top-bottom indexing
        grid_index = grid_col + grid_row * num_cols
        # the mouse is hovering a button, not on a row or column edge
        if col_remainder != 0 and row_remainder != 0:
            return grid_index  # return the index


def startscreenhover():
    # This function processes the following button hover related events:
    # || no buttons hovered -> button hovered || button hover -> still hovered ||
    # || button hover -> different button hovered || button hover -> button unhovered ||
    # determines which button is hovered using its position in its regions grid (easy/hard/search results)

    mouse_pos = pygame.mouse.get_pos()

    def hoveroutline(hovered_button, hover_outline):
        # processes confirmed hover events on buttons by updating the currently hovered buttons outline
        # and updating previously hovered buttons outline (depending on which are necessary)
        if not hovered_button.was_hovered:  # button wasnt hovered last frame so must update outline
            # skipped over the edge to new button - have to reset prev outline
            clearhovered()
            # update hover trackers for current button for next frame
            hovered_button.was_hovered = True
            Button.prev_hover = hovered_button
            # redraw the outline to hover colour
            pygame.draw.rect(GAMESCREEN, hover_outline, hovered_button.coordinates[:4], 1)

    def clearhovered():
        # if no button is hovered, then have to check for a previous frame hover and update the buttons outline
        if Button.prev_hover is not None:
            # print('no current hover - but previous')
            if Button.prev_hover.name[:4] == "load":  # redraw load outlines black
                pygame.draw.rect(GAMESCREEN, BLACK, Button.prev_hover.coordinates[:4], 1)
            else:  # redraw default outlines gray
                pygame.draw.rect(GAMESCREEN, GRAY, Button.prev_hover.coordinates[:4], 1)
            Button.prev_hover.was_hovered = False

    def searchhovered(xlower, xupper, ylower, yupper):
        # determine if the mouse is hovering a button in the search area, is so return True, else return False
        if xlower < mouse_pos[0] < xupper and ylower < mouse_pos[1] < yupper:
            # search box/button and load button have white hover outline
            hover_outline = WHITE
            if 281 < mouse_pos[0] < 495 and 191 < mouse_pos[1] < 235:  # search box
                button_key = "searchbox"
            elif 495 < mouse_pos[0] < 539 and 191 < mouse_pos[1] < 235:  # search button
                button_key = "searchbutton"
            elif 235 < mouse_pos[1] < 610:  # load buttons
                # determines which load button and converts to the corresponding key
                button_key = "load" + str((mouse_pos[1] - 235) // 25 + 1)
                hover_outline = BLUE  # search results have blue outline
                # only allow for hover on search result button areas if a result is displayed
                if '.txt' not in Button.startbutdict[button_key].text:
                    return False
            elif 610 < mouse_pos[1] < 639:  # load button
                button_key = "fileload"
            else:  # edges
                return False
            # all confirmed hovers fall through and are processed here given the set key and outline
            hoveroutline(Button.startbutdict[button_key], hover_outline)
            return True
        return False  # hover not in the region will fall all the way through to here without returning a value

    # determine if a hover was in the easy or hard grid, if it was the variable will be the index in the grid else None
    easy_index = index_in_grid(mouse_pos, 45, 270, 190, 640, 45, 5)
    hard_index = index_in_grid(mouse_pos, 550, 955, 190, 640, 45, 9)
    # check if a hover occurred in any region and process it, else clear hover from previous frame
    if easy_index is not None:
        hoveroutline(Button.startbuttons[easy_index], RED)
    elif hard_index is not None:
        hoveroutline(Button.startbuttons[50 + hard_index], GREEN)
    elif searchhovered(280, 540, 190, 650):
        pass  # function processes a hover
    else:
        clearhovered()


def buttonhover(button, default_outline=BLUE, hover_outline=WHITE):
    # redraws a buttons outline if hovered, can give outline colours for hovered/unhovered states
    # just checks every button till it finds the one corresponding to the hover

    # only redraw if change of state
    mouse_pos = pygame.mouse.get_pos()
    bx = button.coordinates[0]
    by = button.coordinates[1]
    bw = button.coordinates[2]
    bh = button.coordinates[3]

    # if button is hovered...ie mouse x is between button x->x+width and mouse y between button y->y+height
    if bx < mouse_pos[0] < (bx + bw) and by < mouse_pos[1] < (by + bh):
        if not button.was_hovered:  # button was not previously hovered so update outline
            button.was_hovered = True  # updates hovered for next frame
            pygame.draw.rect(GAMESCREEN, hover_outline, [bx, by, bw, bh], 1)  # redraw hover outline
    else:  # if button not hovered but was last frame, then update outline
        if button.was_hovered:
            button.was_hovered = False  # reset prev state for next frame
            pygame.draw.rect(GAMESCREEN, default_outline, [bx, by, bw, bh], 1)  # redraw default outline


def positiontext(position, default_colour=BLUE):
    # draw values/pencil for positions
    xcentre = position.coordinates[4]
    ycentre = position.coordinates[5]
    buttonnames = ['set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7',
                   'set8', 'set9']

    # We have just changed the positions integer value
    if position.value in buttonnames:
        text = position.value[-1]
        position.prev_state = position.value  # update prev_state as position value has changed
        # renders box over top of pencil values and draw position value
        get_text(60, "   ", default_colour, (xcentre, ycentre), BLACK)
        get_text(28, text, default_colour, (xcentre, ycentre), BLACK)

    # check if position value is to be removed this frame, if so - remove value and show pencil states (if any)
    elif position.value in ['setempty', 'set0']:
        if position.prev_state in buttonnames:  # value has been cleared
            position.prev_state = position.value  # update prev_state for next frame
            get_text(28, "  ", default_colour, (xcentre, ycentre), BLACK)  # clear prev value by redrawing background
            for value in position.pencil_values:  # draw pencil states
                penciltext(position, mode='load', value=value)


def penciltext(position, mode=None, default_colour=BLUE, size=12, value=None):
    # draws pencil text in gamescreen - called if a pencil value is added or removed or loading a game

    if position.value in ['set0', 'setempty', 0]:  # position is empty of a value so pencil values should be visible
        # adding a new pencil value
        if mode == 'add':
            lastvalue = position.pencil_values[-1]  # last value in pencil__values - in the form 'set1'
            coordindex = int(lastvalue[-1]) - 1  # lastvalues corresponding index in position.pencil_coordinates
            xcentre = position.pencil_coordinates[coordindex][0]
            ycentre = position.pencil_coordinates[coordindex][1]
            text = lastvalue[-1]  # text set to string of integer being added - taking only the integer part of string
        # removing a pencil value
        elif mode == 'delete':
            coordindex = int(Button.activestate[-1]) - 1  # deleted values coord index in position.pencil_coordinates
            xcentre = position.pencil_coordinates[coordindex][0]
            ycentre = position.pencil_coordinates[coordindex][1]
            text = '   '  # text set to empty string to draw a cream box to remove the integer
        # loading a saved file
        elif mode == 'load':
            coordindex = int(value[-1]) - 1
            text = value[-1]
            xcentre = position.pencil_coordinates[coordindex][0]
            ycentre = position.pencil_coordinates[coordindex][1]
        else:  # setempty has been pressed so erase all pencil values by redrawing with cream box
            text = '   '
            size = 60
            xcentre = position.coordinates[4]
            ycentre = position.coordinates[5]

        # draw the text to gamescreen
        get_text(size, text, default_colour, (xcentre, ycentre), BLACK)


def draw_startbuttons(textcolour=BLACK, boxcolour=None, text1=None, size=16, textcoords=None,
                      boxcoords=None, textalign=None, boxfill=None):
    # TODO: redundant function?
    # draws a button outline
    if boxcoords is not None:
        if boxfill is not None:
            pygame.draw.rect(GAMESCREEN, boxfill, boxcoords)
        if boxcolour is not None:
            pygame.draw.rect(GAMESCREEN, boxcolour, boxcoords, 1)
    # draws button text
    if textcoords is not None:
        if textalign == 'midleft':  # align button text to left of box
            get_text(size, text1, textcolour, textcoords, align="midleft")
        else:  # default text align is centre
            get_text(size, text1, textcolour, textcoords)


def startscreenbuttons():
    # function creates all the buttons in the startscreen

    def incrementbuttons(boxcoords, textcoords, numboxes, colour, text):

        [a, b, c, d] = boxcoords
        [e, f] = textcoords
        counter = 1
        # make a button object for each puzzle number (1-50), add its coordinates, and draw the button
        for x in range(10):
            for y in range(int(numboxes/10)):
                buttontext = text + str(counter)
                newbutt = Button(buttontext)
                Button.add_startlist(newbutt)
                newbutt.coordinates = [a, b, c, d]
                draw_startbuttons(text1=buttontext[4:], boxcolour=GRAY, textcolour=colour,
                                  textcoords=[e, f], boxcoords=[a, b, c, d])
                counter += 1
                a += 45
                e += 45
            a = boxcoords[0]
            e = textcoords[0]
            b += 45
            f += 45

    # draws easy and hard puzzle boxes and text
    incrementbuttons([45, 190, 45, 45], [67.5, 212.5], 50, GREEN, "easy")
    incrementbuttons([550, 190, 45, 45], [572.5, 212.5], 90, RED, "hard")

    # -------- draw loadgame boxes and text ----------

    # make savefile search box
    newbutt = Button('searchbox')
    newbutt.add_startdict()
    newbutt.coordinates = [281, 191, 214, 44]
    newbutt.textcoords = [288, 212.5]
    newbutt.text = 'Search Files'
    draw_startbuttons(textcolour=GRAY, text1=newbutt.text, textcoords=[288, 212.5], textalign='midleft',
                      boxcolour=GRAY, boxcoords=[281, 191, 214, 44])

    # make clickable image button for search box
    newbutt = Button('searchbutton')
    newbutt.add_startdict()
    newbutt.coordinates = [495, 191, 44, 44]
    draw_startbuttons(boxcolour=GRAY, boxcoords=[495, 191, 44, 44])

    try:  # set search button image, if image missing use text
        get_image("sudoku_resources\\searchimage.png", (517, 213))
    except pygame.error as search_error:
        error_text = str(search_error)[14:]
        print("*Missing Search Image Button File: " + error_text + "*")
        get_text(20, "Go.", GRAY, (516, 213))

    # make load button
    newbutt = Button('fileload')
    newbutt.add_startdict()
    newbutt.coordinates = [280, 610, 260, 29]
    newbutt.text = "LOAD"
    draw_startbuttons(textcolour=GRAY, text1=newbutt.text, textcoords=[400, 625],
                      boxcolour=GRAY, boxcoords=[280, 610, 260, 29])
    # load button area outline box
    draw_startbuttons(boxcolour=GRAY, boxcoords=[280, 190, 260, 450])

    # make button objects for each load space (15 max shown at any time)
    [a, b, c, d] = [281, 235, 258, 25]
    [e, f] = [290, 247.5]

    for x in range(1, 16):
        newbutt = Button("load"+str(x))
        Button.add_startdict(newbutt)
        newbutt.coordinates = [a, b, c, d]
        newbutt.textcoords = [e, f]
        b += 25
        f += 25


def searchfiles(searchterm):
    # TODO: bug - search test and no results appear, when clearly i have files with test in the name

    # created save folder when game is started if the folder doesnt already exist
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    savedir = pathlib.WindowsPath(file_dir_path+"\\savefiles")
    # saves = [child.name for child in savedir.iterdir() if child.suffix == '.txt']
    saves = []  # an empty list to append searched files

    # draw over previous loadfile buttons
    for x in range(1, 16):
        loadbutton = Button.startbutdict["load"+str(x)]
        loadbutton.text = loadbutton.name  # reset text so buttons cannot be hovered unless more text is entered
        draw_startbuttons(boxfill=BLACK, boxcoords=loadbutton.coordinates)

    for child in savedir.iterdir():
        # open textfiles and check if they are valid save files
        if child.suffix == '.txt':
            opensave = open(child, 'r')
            puzzname = opensave.readline()
            opensave.close()
        else:  # if a non text file type is found skip this file
            continue

        if searchterm == '!easy' or '!hard':  # codes to search for puzzles of given difficulty
            try:  # display the first 15 (max) easy/hard puzzle savefiles in the directory
                if searchterm[1:] in puzzname:
                    textshown = child.name + '  ¦¦  ' + puzzname[:-1]
                    saves.append(textshown)
            except IndexError:
                pass

        else:  # for any other term search for any file with that string in the name
            try:
                if searchterm in child.name:
                    textshown = child.name + '  ¦¦  ' + puzzname[:-1]
                    saves.append(textshown)
            except IndexError:  # stuff
                pass

    # set the loadfile buttons to show the text for the savefiles that were found with the search
    for filetext in saves:
        counter = saves.index(filetext) + 1
        if counter < 15:  # can only show 15 max as only 15 buttons
            Button.startbutdict['load' + str(counter)].text = filetext
            draw_startbuttons(textcolour=GRAY, boxcolour=None,
                              text1=Button.startbutdict['load' + str(counter)].text,
                              textcoords=Button.startbutdict['load' + str(counter)].textcoords,
                              boxcoords=None, textalign='midleft')


# ---------------------- DRAWING THE SUDOKU GAME BOARD --------------------------------------
#                       630 x 630 size is divisible by 9

def drawboard(back_colour=BLACK, line_colour=BLACK):
    # board background colour
    pygame.draw.rect(GAMESCREEN, back_colour, [20, 20, 650, 650])
    # bold outer/block lines
    lines = [(30, 30), (30, 660), (240, 30), (240, 660), (450, 30), (450, 660), (660, 30), (660, 660),
             (30, 30), (660, 30), (30, 240), (660, 240), (30, 450), (660, 450), (30, 660), (660, 660)]
    # thin inner row/column lines
    lines2 = [(100, 30), (100, 660), (170, 30), (170, 660), (310, 30), (310, 660), (380, 30), (380, 660),
              (520, 30), (520, 660), (590, 30), (590, 660),
              (30, 100), (660, 100), (30, 170), (660, 170), (30, 310), (660, 310), (30, 380), (660, 380),
              (30, 520), (660, 520), (30, 590), (660, 590)]

    y = 1
    for x in range(0, 15, 2):
        pygame.draw.line(GAMESCREEN, line_colour, lines[x], lines[y], 4)
        y = y + 2
    y = 1
    for x in range(0, 23, 2):
        pygame.draw.line(GAMESCREEN, line_colour, lines2[x], lines2[y], 1)
        y = y + 2


def gametimer(mins, secs, paused=False):

    # TODO: does not support 1h+ times

    # if hrs == '0':
    #     h = '  '
    # else:
    #     h = hrs + 'h:'
    if mins == '0':
        m = '     : '
    elif len(mins) == 1:
        m = '  ' + mins + 'm: '
    else:
        m = ' ' + mins + 'm: '
    if secs == '0':
        s = '    '
    elif len(secs) == 1:
        s = '' + secs + 's '
    else:
        s = '' + secs + 's '
    timestring = m + s

    # draw the fill outline and text of the timer
    pygame.draw.rect(GAMESCREEN, BLACK, [720, 45, 130, 40])
    pygame.draw.rect(GAMESCREEN, BLUE, [720, 50, 130, 40], 1)
    get_text(24, timestring, WHITE, (785, 70))


# TODO: ------------------------------ CHECKLIST ----------------------------------

# highlight rows/columns of position hovered?

# MOVE EVENT PROCESSING CODE TO CLASS METHODS??????

# make it so clear and check dont interrupt other active buttons???


# ---------------------------- START SCREEN AND GAME LOOP ----------------------------------


def pyinit():

    pygame.init()
    # Centring the game window using os module
    os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 35'
    # print(pygame.display.get_driver())

    # set game icon as a small sudoku image
    try:
        icon = pygame.image.load('sudoku_resources\\sudoku_icon.bmp')
        pygame.display.set_icon(icon)
    except pygame.error as error_message:
        print(error_message)
    # set name in window tab
    pygame.display.set_caption('Lameo Sudoku')

    # global variables
    global GAMESCREEN, CLOCK
    GAMESCREEN = pygame.display.set_mode((1000, 690))
    CLOCK = pygame.time.Clock()
    # background_image = pygame.image.load('sudoku_resources\\gridpaper.bmp').convert() #not big enough image..


def startscreen():

    # draws all the components of the start screen
    startscreenbuttons()
    draw_startbuttons(text1='LAMEO SUDOKU', textcolour=BLUE, textcoords=[500, 80], size=70)
    draw_startbuttons(text1='easy', textcolour=GREEN, textcoords=[157, 170], size=28)
    draw_startbuttons(text1='hard', textcolour=RED, textcoords=[751, 170], size=28)
    draw_startbuttons(text1='load', textcolour=GRAY, textcoords=[410, 170], size=28)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # process downclicks on
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # encompasses all easy state buttons
                if 45 < event.pos[0] < 270 and 190 < event.pos[1] < 640:
                    # click is on a button with this index, or is None if on an edge
                    easy_index = index_in_grid(event.pos, 45, 270, 190, 640, 45, 5)
                    if easy_index is not None:
                        # determine puzzle number and set starting states using that information
                        num = easy_index + 1  # puzzlenum is 1 greater than index
                        set_start_states(0, num)
                        Position.puzzlenumber = 'easy' + str(num)
                        return  # return from function to continue to main loop after setting starting state of game

                # encompasses all hard state buttons, same function as easy
                elif 550 < event.pos[0] < 955 and 190 < event.pos[1] < 640:
                    hard_index = index_in_grid(event.pos, 550, 955, 190, 640, 45, 9)
                    if hard_index is not None:
                        num = hard_index + 1
                        set_start_states(1, num)
                        Position.puzzlenumber = 'hard' + str(num)
                        return

                # encompasses all load buttons - must confirm upclick on these buttons
                elif 281 < event.pos[0] < 539 and 191 < event.pos[1] < 656:
                    for buttonkey in Button.startbutdict:
                        button = Button.startbutdict[buttonkey]
                        bx = button.coordinates[0]
                        by = button.coordinates[1]
                        bw = button.coordinates[2]
                        bh = button.coordinates[3]
                        if bx < event.pos[0] < (bx + bw) and by < event.pos[1] < (by + bh):
                            Button.potential_click = button
                            break  # break for loop as clicked button was found

                else:  # for a click outside of any button, must reset search box
                    searchbox = Button.startbutdict['searchbox']
                    searchbox.state = 0
                    # coords alters coordinates so the boxfill wont draw over the outline - which it does otherwise
                    coords = [searchbox.coordinates[0] + 1, searchbox.coordinates[1] + 1,
                              searchbox.coordinates[2] - 2, searchbox.coordinates[3] - 2]
                    if searchbox.text == '':  # reset the search box text if empty
                        searchbox.text = 'Search Files'
                        draw_startbuttons(textcolour=GRAY, text1=searchbox.text, textcoords=searchbox.textcoords,
                                          textalign='midleft')
                    else:  # keep search box text but redraw in gray to show inactive
                        draw_startbuttons(textcolour=GRAY, text1=searchbox.text, textcoords=searchbox.textcoords,
                                          textalign='midleft', boxcoords=coords, boxfill=BLACK)

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                # only have to deal with load game buttons as others direct straight to mainloop upon downclick
                if isinstance(Button.potential_click, Button):
                    b = Button.potential_click  # button object that has been downclicked
                    bx = b.coordinates[0]
                    by = b.coordinates[1]
                    bw = b.coordinates[2]
                    bh = b.coordinates[3]
                    if bx < event.pos[0] < (bx + bw) and by < event.pos[1] < (by + bh):
                        if b.name == 'fileload':
                            # if clicked - if a loadfile is selected - load that file - if not, do nothing
                            # can be active while other button is active?
                            if Button.activestate is not None:
                                try:  # load the starting state from the filename linked to the active load button
                                    loadgame(Button.startbutdict[Button.activestate].text)
                                except (IndexError, ValueError) as errors:
                                    # if file contents are not in the correct format as per the save function
                                    # trying to load likely gives an index or value error as it tries to
                                    # load values from lines in the text file
                                    print('File contains incorrect data...Please delete or move.')
                                    print('Error:', errors)

                        elif b.name == 'searchbox':
                            # redraw previously active loadfile button
                            if Button.activestate is not None:
                                prevbut = Button.startbutdict[Button.activestate]
                                draw_startbuttons(text1=prevbut.text, textcolour=GRAY, textcoords=prevbut.textcoords,
                                                  textalign='midleft', boxcoords=prevbut.coordinates, boxfill=BLACK)
                            # activate and redraw the searchbox
                            b.state = 1
                            Button.activestate = b.name
                            draw_startbuttons(textcolour=WHITE, text1=b.text, textcoords=b.textcoords,
                                              textalign='midleft', boxcoords=b.coordinates, boxfill=BLACK,
                                              boxcolour=WHITE)

                        elif b.name == 'searchbutton':
                            # should call function to search the save directory for the search term
                            if Button.startbutdict['searchbox'].text != 'Search Files':
                                searchfiles(Button.startbutdict['searchbox'].text)
                            # should flash or something to show it clicked

                        else:  # clicked on loadfile button
                            if b.text == b.name:
                                # if no file has been linked to the button then it cant become active
                                pass
                            else:  # text has been linked to a button so it should be clickable
                                b.clicked()
                                if Button.activestate is None:  # if no button was active:
                                    Button.activestate = b.name  # set active to clicked button
                                    # redraw the button
                                    draw_startbuttons(textcolour=WHITE, text1=b.text, textcoords=b.textcoords,
                                                      boxcolour=WHITE, boxcoords=b.coordinates, textalign='midleft',
                                                      boxfill=BLUE)

                                elif Button.activestate is not None:  # if a button was active
                                    if Button.activestate == b.name:  # if clicked button is active
                                        Button.activestate = None  # turn it off
                                        # redraw the button
                                        draw_startbuttons(textcolour=GRAY, text1=b.text, textcoords=b.textcoords,
                                                          boxcolour=BLUE, boxcoords=b.coordinates,
                                                          textalign='midleft', boxfill=BLACK)

                                    else:  # if another button was active
                                        prevbut = Button.startbutdict[Button.activestate]
                                        if prevbut.name == 'searchbox':
                                            # separate as need to change coords to not draw over outline
                                            coords = [prevbut.coordinates[0] + 1, prevbut.coordinates[1] + 1,
                                                      prevbut.coordinates[2] - 2, prevbut.coordinates[3] - 2]
                                            draw_startbuttons(textcolour=GRAY, text1=prevbut.text,
                                                              textcoords=prevbut.textcoords, boxcolour=BLACK,
                                                              boxcoords=coords, textalign='midleft',
                                                              boxfill=BLACK)
                                        else:  # redraw previous active loadfile button
                                            draw_startbuttons(textcolour=GRAY, text1=prevbut.text, textalign='midleft',
                                                              textcoords=prevbut.textcoords, boxcolour=BLACK,
                                                              boxcoords=prevbut.coordinates, boxfill=BLACK)
                                        prevbut.clicked()  # reset previous active button
                                        Button.activestate = b.name  # turn on clicked button
                                        # draw active button
                                        draw_startbuttons(textcolour=WHITE, text1=b.text, textcoords=b.textcoords,
                                                          boxcolour=WHITE, boxcoords=b.coordinates,
                                                          textalign='midleft', boxfill=BLUE)

            elif event.type == KEYDOWN:
                # processing key presses for the load search box
                searchbox = Button.startbutdict['searchbox']
                if searchbox.state == 1:  # if active
                    if searchbox.text == 'Search Files':
                        searchbox.text = ''  # remove the text so it can be changed by user

                    if event.key in range(32, 127):  # includes all standard characters on a keyboard
                        if len(searchbox.text) < 12:
                            searchbox.text += event.unicode
                            coords = [searchbox.coordinates[0] + 1, searchbox.coordinates[1] + 1,
                                      searchbox.coordinates[2] - 2, searchbox.coordinates[3] - 2]
                            draw_startbuttons(text1=searchbox.text, textcoords=searchbox.textcoords, textcolour=WHITE,
                                              textalign='midleft', boxcoords=coords, boxfill=BLACK)
                        else:
                            print('File name 12 characters max!')
                    elif event.key == 8:  # if backspace pressed remove last character
                        searchbox.text = searchbox.text[:-1]
                        coords = [searchbox.coordinates[0] + 1, searchbox.coordinates[1] + 1,
                                  searchbox.coordinates[2] - 2, searchbox.coordinates[3] - 2]
                        draw_startbuttons(text1=searchbox.text, textcoords=searchbox.textcoords, textcolour=WHITE,
                                          textalign='midleft', boxcoords=coords, boxfill=BLACK)
                    elif event.key == 13:  # if enter pressed provides same functionality as hitting search
                        if Button.startbutdict['searchbox'].text != 'Search Files':
                            searchfiles(Button.startbutdict['searchbox'].text)
                    else:
                        # print(event.key)
                        print('Invalid character...')

        # draw different box colours if hovered for easy puzzle boxes - only redraws on hover/unhover
        startscreenhover()

        CLOCK.tick(30)  # set maximum fps to 30
        # updates the full screen every frame..docs say better to use on a full list than keep calling the function
        # TODO: MAKE A LIST CONTAINING ALL OBJECTS TO BE RENDERED THIS FRAME TO PASS IN THIS FUNCTION EACH FRAME??
        pygame.display.update()


def savegame(name, time):

    # create new text file with name entered
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    save = open(file_dir_path+'\\savefiles\\'+name+'.txt', 'w+')

    # get puzzle number and difficulty
    puzzle_number = Position.puzzlenumber
    save.write(puzzle_number+'\n')
    # get current game time
    gametime = str(time)
    save.write(gametime+'\n')

    start_values, set_values, pencil_values = "", "", ""
    for pos in Position.positionlist:
        # create string containing all starting values
        start_values += pos.start_state
        # create string containing all set values
        if pos.value == "setempty":
            set_values += "set0"  # set emtpy cells values to "set0" for ease (all values 4 chars long)
        else:
            set_values += pos.value
        # create string containing all pencil values for each cell
        pencil_values += "-"  # separate each cells set of pencil values by "-" so we can easily distinguish them
        for value in pos.pencil_values:
            pencil_values += value[-1]

    # write each string as a separate line in the save textfile for ease of loading
    save.write(start_values+'\n'+set_values+'\n'+pencil_values)
    save.close()


def loadgame(savefile):
    # takes the given text linked to the load button and uses the filename section to open that file and load the
    # game data (values, pencil, and timer) for the game and starts the main loop

    nameindex = savefile.index('¦') - 2  # is preceeded by two spaces and then the file name
    filename = savefile[:nameindex]  # takes only the filename as in the directory

    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    test = open(file_dir_path+"\\savefiles\\"+filename, 'r')
    lines = (test.readlines())  # reads each line 1 at a time

    puzzlename = lines[0]  # string with puzzle difficulty and number
    gametime = int(lines[1])  # string of the game time in seconds when saved
    start_values = lines[2]  # string 81 chars long with an integer for each position starting value
    pos_values = lines[3]  # string with 'setx' to signify the position values
    pencil_vals = lines[4]  # string with - before each list of pencil values for each position -empty list = dash only
    test.close()

    # takes values from the pencil line from the savefile and puts all the values for each position into its own
    # element in a list to then be used to load the values into positions when loading a saved game
    pencil_list = []
    index = -1
    for value in pencil_vals:
        if value == '-':
            pencil_list.append([])
            index += 1
        elif value == '\n':
            pass  # otherwise will get ['set\n'] for the last value in the list
        else:
            pencil_list[index].append('set'+value)  # add in 'set' part of string again so it can draw the text

    # Initialising the saved data into a new pygame instance from the chosen savefile
    Position.puzzlenumber = puzzlename[:-1]  # puzzle difficulty/number - last character is '\n' so leave this out
    for count, posi in enumerate(Position.positionlist):
        posi.start_state = start_values[count]  # sets start values
        # step by 4 characters each position value as it is in the form 'set0'
        posi.value = pos_values[count*4:(count*4) + 4]  # sets position values
        posi.pencil_values = pencil_list[count]  # sets pencil values
    print('loaded file...', filename)
    mainloop(gametime, load=True)  # starts the gameloop using the saved time


def resetboard():
    # remove error pic
    drawboard(BLACK, BLUE)
    # redraw position values
    for pos in Position.positionlist:
        if pos.start_state != '0':
            positiontext(pos, WHITE)
        elif pos.start_state == '0':
            if pos.value == 'set0':
                if pos.pencil_values is not []:  # have pencil values
                    for val2 in pos.pencil_values:
                        penciltext(pos, mode='load', value=val2)
            else:
                positiontext(pos, BLUE)


def mainloop(timer=0, load=False):

    # resize screen to fit smaller game elements better - can just move stuff instead
    pygame.display.set_mode((900, 690))
    # background images that dont need redrawing each loop:
    GAMESCREEN.fill(BLACK)  # draws over the startscreen graphics for a black background
    drawboard(BLACK, BLUE)  # draws game board

    # reset active button to none so no errors occur in event processing a new active button for first time in new loop
    Button.activestate = None

    # drawing text to display the puzzle number/difficulty
    # pygame.draw.rect(gamescreen, GRAY, [700, 620, 170, 30])
    get_text(19, "Puzzle: "+Position.puzzlenumber, BLUE, (785, 30))

    # draw clock
    mins = str(timer//60)
    secs = str(timer % 60)
    gametimer(mins, secs)
    # initialising time for clock
    counting = 0

    # drawing all buttons which arent redrawn till a change occurs
    for button in Button.buttondict:
        # draw the button text and fill
        drawbutton(Button.buttondict[button])
        b = Button.buttondict[button]
        bx = b.coordinates[0]
        by = b.coordinates[1]
        bw = b.coordinates[2]
        bh = b.coordinates[3]
        # draw the button outlines
        pygame.draw.rect(GAMESCREEN, BLUE, [bx, by, bw, bh], 1)

    # drawing starting state and/or loaded values which are set/loaded into the class attributes from startscreen
    if load is False:
        # drawing starting state position text - these positions are never redrawn
        for pos in Position.positionlist:
            positiontext(pos, WHITE)
    elif load is True:
        for pos in Position.positionlist:
            # starting values drawn
            if pos.start_state != '0':
                positiontext(pos, WHITE)
            # loaded changeable values and pencil values drawn
            elif pos.start_state == '0':
                # if no position value, check for pencil values to be drawn
                if pos.value == 'set0':
                    if pos.pencil_values is not []:  # no pencil values
                        for val in pos.pencil_values:
                            penciltext(pos, mode='load', value=val)
                else:  # position has value to be drawn
                    positiontext(pos, BLUE)

    # main game loop starts here with a while loop that is broken by returning False
    while True:

        def event_check():  # Function that checks and processes events during game loop - eg clicks/typing
            # code was getting big so put in its own function

            # TODO: ------ SET EACH TYPE OF EVENT CHECK TO ITS OWN FUNCTION OUTSIDE OF LOOP AND CALL ??? ------

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # First checking for a left downclick in a button or position then for an upclick
                # Functionality: A (left) mouseclick interacts with a button/position object only if the downclick
                # and then corresponding upclick occur in the object; other mouseclicks wont register as
                # either downclicks or upclicks. Long holds register as 1 click, upclicks outside the object
                # do not register (for change of mind), and downclick outside the object followed by upclick
                # inside the object do not register

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # TODO: could change to methods in classes eg onDown, onUp
                    skip = 0
                    # check if board is displaying error pic to be removed on board click and redraw position values
                    if Position.errorPicShown:
                        # if clicked on board
                        if 20 < event.pos[0] < 670 and 20 < event.pos[1] < 670:
                            # reset relevant attributes/graphics
                            Position.delay = 0
                            resetboard()
                            Position.errorPicShown = False  # reset attribute
                            skip = 1

                    # check for each button, if it was clicked
                    for but in Button.buttondict:
                        b = Button.buttondict[but]
                        x = b.coordinates[0]
                        y = b.coordinates[1]
                        w = b.coordinates[2]
                        h = b.coordinates[3]
                        if x < event.pos[0] < x + w and y < event.pos[1] < y + h:
                            Button.potential_click = b  # set to remove unnecessary checks through
                            # buttondict on every mouse upclick - same as for position
                            skip = 1  # set skip to 1 if button set active so positions arent also checked
                            break  # stop searching buttons as only one is active each frame

                    # check if any position was clicked only if a button is active, and there was no click on a button
                    if Button.activestate is not None and skip == 0:
                        pos_index = index_in_grid(event.pos, 30, 660, 30, 660, 70, 9)
                        if pos_index is not None:
                            clicked_pos = Position.positionlist[pos_index]
                            # set a variable in Position class only for changeable positions so upclicks can be
                            # rejected if they did not pass all these checks for a click on a position
                            if clicked_pos.start_state == '0':
                                Position.potential_click = clicked_pos

                # Checks if a left mouse button upclick occurs. Process button/position clicks only if a potential click
                # has been registered from a downclick in the Position/Button classes. Do not have to check
                # for button.activestate as downclick is only confirmed if activestate is not None. Deactivate the
                # save text box if the upclick occurred anywhere outside of it.
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    # track the state of save text box, if any click outside of it occurs, then make it inactive
                    textbox_active = False
                    # If a downclick occurred on a Position object, it will be stored in the potential_click variable
                    # else it will be None, isinstance checks this and removes IDE warnings when using that variable
                    if isinstance(Position.potential_click, Position):
                        p = Position.potential_click  # the position object which has been clicked (as set above)
                        x1 = p.coordinates[0]
                        y1 = p.coordinates[1]
                        w1 = p.coordinates[2]
                        h1 = p.coordinates[3]
                        # if the upclick occurs in the same Position as downclicked, then it is a confirmed click
                        if x1 < event.pos[0] < x1 + w1 and y1 < event.pos[1] < y1 + h1:
                            if Button.pencilstate == 1:  # pencil button is active, change Position pencil value
                                if Button.activestate == 'setempty':  # eraser is active, remove all pencil values
                                    p.pencil_values = []
                                    penciltext(p)
                                else:  # if an integer button is active
                                    if Button.activestate in p.pencil_values:  # remove pencil int if in position
                                        penciltext(p, 'delete')
                                        # remove value after redrawing as function needs the pencilvalue index
                                        p.pencil_values.remove(Button.activestate)
                                    else:  # add pencil int if not in position
                                        p.pencil_values.append(Button.activestate)
                                        penciltext(p, 'add')  # draw after adding
                            else:  # inactive pencil button, change Position value
                                if p.value == 'set0':  # position empty, add the value of the active button
                                    p.value = Button.activestate
                                elif p.value == Button.activestate:  # position value same as button, clear Position
                                    p.value = 'set0'
                                else:  # position value different to the active button state, change to button value
                                    p.value = Button.activestate
                                # redraws the position text if a state change has occurred (calls penciltext if needed)
                                positiontext(p)

                        # reset potential click regardless of outcome as full click rotation has occurred
                        Position.potential_click = 0

                    elif Button.potential_click != 0:
                        b = Button.potential_click  # the button object which has been downclicked (as set above)
                        x = b.coordinates[0]
                        y = b.coordinates[1]
                        w = b.coordinates[2]
                        h = b.coordinates[3]
                        # upclick occurred in same button as downclick, process confirmed click
                        if x < event.pos[0] < x + w and y < event.pos[1] < y + h:
                            if b.name == 'pencil':  # pencil code is separate so can be on at same time as other buttons
                                b.clicked()  # change state of button
                                if b.state == 1:  # pencil button now active, update object and graphic
                                    Button.pencilstate = 1
                                    drawbutton(b, fill=DGRAY)
                                else:  # pencil button now inactive
                                    Button.pencilstate = None
                                    drawbutton(b)
                            elif b.name == 'savetextbox':  # save text box can also be active at same time as others
                                textbox_active = True
                                if b.state != 1:  # if it is not active, make it, else leave it active
                                    b.state = 1
                                    # Button.buttondict['savetextbox'].text = ''
                                    drawbutton(b, BLUE)
                            else:  # for the remaining buttons, only one can be active at a time
                                b.clicked()
                                if Button.activestate is None:  # if no button was active:
                                    Button.activestate = b.name  # set active to clicked button
                                    drawbutton(b, fill=DGRAY)
                                elif Button.activestate is not None:  # if a button was active
                                    if Button.activestate == b.name:  # if clicked button is active
                                        Button.activestate = None  # turn it off
                                        drawbutton(b)
                                    else:  # another button was active, reset/redraw it before updating clicked Button
                                        Button.buttondict[Button.activestate].clicked()  # previous
                                        drawbutton(Button.buttondict[Button.activestate])  # previous
                                        Button.activestate = b.name  # turn on clicked button
                                        drawbutton(b, fill=DGRAY)

                        # reset potential click to 0 as a full click has occurred
                        # and need to be able to change to 1 to signify a new button click
                        Button.potential_click = 0

                    # if a click occurred outside of save text box, then deactivate it
                    if not textbox_active:
                        Button.buttondict['savetextbox'].state = 0
                        if Button.buttondict['savetextbox'].text == '':
                            Button.buttondict['savetextbox'].text = 'Enter File Name'
                            drawbutton(Button.buttondict['savetextbox'], DGRAY)
                        else:
                            drawbutton(Button.buttondict['savetextbox'], DGRAY)

                # functionality to change button state using integer keys
                elif event.type == KEYDOWN:
                    savebox = Button.buttondict['savetextbox']
                    # textbox to enter a file name
                    if savebox.state == 1:
                        # remove default message when clicked, so user can enter a file name
                        if savebox.text == 'Enter File Name':
                            savebox.text = ''
                        # update the text box as user enters characters
                        if event.key in range(32, 127):  # includes all standard characters on a keyboard
                            if len(savebox.text) < 12:
                                savebox.text += event.unicode
                                drawbutton(savebox, BLUE)
                            else:
                                print('File name 12 characters max!')
                        elif event.key == 8:  # if backspace pressed remove last character
                            savebox.text = savebox.text[:-1]
                            drawbutton(savebox, BLUE)
                        else:
                            print('Invalid character...')
                    else:  # interaction with number keys to change active button
                        try:
                            i = int(event.unicode)
                        except ValueError:
                            break

                        numlist = ['setempty', 'set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7',
                                   'set8', 'set9']
                        b = Button.buttondict[numlist[i]]
                        b.clicked()
                        if Button.activestate is None:  # if no button was active:
                            Button.activestate = b.name  # set active to clicked button
                            drawbutton(b, fill=DGRAY)
                        elif Button.activestate is not None:  # if a button was active
                            if Button.activestate == b.name:  # if clicked button is active
                                Button.activestate = None  # turn it off
                                drawbutton(b)
                            else:  # if another button was active
                                Button.buttondict[Button.activestate].clicked()  # reset previous active button
                                drawbutton(Button.buttondict[Button.activestate])  # redraw previous active button
                                Button.activestate = b.name  # turn on clicked button
                                drawbutton(b, fill=DGRAY)

        event_check()

        # --- no button click graphic can change ----
        if Button.activestate == 'check':
            # if check button is clicked then check if the game has been completed successfully
            rules()
            # reset the button state so it isnt able to be kept active only clicked
            Button.buttondict[Button.activestate].state = 0
            # reset the Button class activestate so the mouseclick processing works properly next frame
            Button.activestate = None
            drawbutton(Button.buttondict['check'])  # redraw button

        # TODO: ---------- HOW TO MAKE A BUTTON FLASH FOR ONE OR A FEW FRAMES FOR A CLICK ??? ------------
        #   Make delay function that ticks every 30frames (or whatever fps set to)

        elif Button.activestate == 'clear':
            # if clear button is clicked then clear the states of changeable positions (and update graphics)
            clear_states()
            # reset the button state so it isnt able to be kept active only clicked
            Button.buttondict[Button.activestate].state = 0
            # reset the Button class activestate so the mouseclick processing works properly next frame
            Button.activestate = None
            drawbutton(Button.buttondict['clear'])  # redraw button

        # button hover graphics
        for button in Button.buttondict:
            b = Button.buttondict[button]
            buttonhover(b)

        # timer function: every frame increments counter then resets to 0 at 30 (change for diff fps)
        if counting == 30:
            timer += 1
            # hours = str(timer//3600)
            minutes = str(timer // 60)
            seconds = str(timer % 60)
            gametimer(minutes, seconds)
            counting = 0
        counting += 1

        # automatically reset board ~4s after error pic shown, if board not clicked (also resets0
        if Position.errorPicShown:
            Position.delay += 1
            if Position.delay == 120:  # 4s x 30fps = 120
                Position.delay = 0
                resetboard()
                Position.errorPicShown = False

        # save function
        if Button.activestate == 'save':
            if Button.buttondict['savetextbox'].text != ('' or 'Enter File Name'):
                # add to save class
                savegame(Button.buttondict['savetextbox'].text, timer)
                print('SAVED!')
            else:
                print('NO FILENAME ENTERED.')
            Button.activestate = None
            drawbutton(Button.buttondict['save'])

        pygame.display.update()

        CLOCK.tick(30)
        # checking efficiency by measuring how long a frame takes compared to set fps
        # print(clock.get_rawtime())


def main():

    # TODO: could just give an error if savefiles doesnt exist rather than blindly making folder
    # create savefile folder if not already made
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    savefolderexists = os.path.exists(file_dir_path+"\\savefiles")
    if not savefolderexists:
        os.mkdir(file_dir_path+"\\savefiles")

    # create class objects
    positionobjects()
    buttonobjects()

    # start game
    pyinit()
    startscreen()
    # startscreen exits while loop/finishes executing upon selection - mainloop now to be called to start game
    mainloop()


main()

