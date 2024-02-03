import random

SPACING = '     '

"""
import_army(unit_dict, color)
:param unit_dict: a dictionary containing the the strength of all basic units on the field, as well as the number of each type
:param color: a string, either R or B, representing red or blue. this is used in making the list of representing that players army
this function takes the dictionary, and turns it into a list with x of each type of unit in it, where x is the value and the strength of each
unit is their respective key in the dictionary
{str: num} 
this is meant to be a helper method in the function init_grid(), which creates the 2d list that will handle all movement/gameplay

"""
def import_army(unit_dict, color):

    army = []

    for str_level in unit_dict.keys():

        while unit_dict[str_level] > 0 :

            army.append(color + str(str_level))

            unit_dict[str_level] -= 1

    return army


"""
init_unit_dicts(piece_file)
:param piece_file: a string containing the name of the file with the data for the pieces
this function is to pull data from the piece text file and store it in a dictionary. returns the dictionary to be used in other functions
this is intended to be a helper function for functions such as init_grid() and import_army()

"""
def init_unit_dicts(piece_file):

    unit_dict = dict()

    p_file = open(piece_file, 'r') 

    for line in p_file:

        line = line.strip() #if there is a \n, this removes it

        if len(line) == 4: # if the str level on this line is a 10 or a 1
            if line[0:2] == '10': # if the str level is a 10
                unit_dict[line[0:2]] = int(line[3:])
            else: # the str level is a 1
                unit_dict[line[0:1]] = int(line[2:])
        else: 
            unit_dict[line[0:1]] = int(line[2:])


    p_file.close()

    return unit_dict

"""
print_board(grid)
:param grid: a 2d list representing the board, containing all of its data
:param length: an int representing the length of the board
:param width: an int represengint the width of the board
this function is to be used repeatedly every turn in order to display the grid. the grid will be saved as a variable inside of tactego()
and it will constantly be updated until the game is over, and displayed using the print_board()

"""
def print_board(grid, length, width):

    for line in range(length+1):

        if line == 0: # it an axis line, print out numbers

            print('    ', end = '')

            for i in range(width):

                print(i, end = SPACING)

            print() # advance to the next line

        else: 

            # this isnt the top row, so we actually have to print out the board
            """
            HERES HOW I WANT TO HANDLE PRINTING OUT THE BOARD:
            1. PRINT OUT THE LINE NUMBER
            2. RUN THROUGH A FOR LOOP CONNECTED TO THE GRID PARAMETER TO PRINT OUT EACH TOKEN ON THAT SPECIFIED ROW OF LINE-1, OR THE LINE NUMBER
            3. PROGRESS TO THE NEXT LINE USING AN EMPTY PRINT STATEMENT
            """
            print(line-1, end = '   ')

            for token in grid[line-1]:

                if token != '':
                    print(token, end = '    ')
                else:
                    print('  ', end = '    ')
            print()


"""
init_grid(unit_dict, length, width, seed)
:param unit_dict: a dictionary with the makeup of a players starting army, created using the init_unit_dicts() func
:param length: an int representing the length of the board 
:param width: an int representing the width of the board
:param seed: a string containing a random seed for the shuffling of the red side of the board
this function is to initialize and return the board - a 2d list of length and width, contiaining randomized placements of the tokens for 
both players

"""
def init_grid(unit_dict, length, width):

    # create red and blue army lists 

    copy_unit_dict = dict(unit_dict)

    red_army = import_army(unit_dict, 'R')
    blue_army = import_army(copy_unit_dict, 'B')

    # shuffle both lists
    random.shuffle(red_army)
    random.shuffle(blue_army)
    

    the_grid = []

    # for each row inside of the boardlength, append a new row so that there can be depth
    for row in range(length):
        the_grid.append([])

    # now, we want to place the red army onto the board 

    token = 0 # this variable represents the current token from the red army we are placing on the board

    for row in range(len(the_grid)):
        for col in range(width):
            if token < len(red_army): # if the token exists
                the_grid[row].append(red_army[token])
                token += 1

    # do the same for the blue army

    token = 0 # reset token counter

    for row in range(len(the_grid)):
        for col in range(width):
            if token < len(blue_army):
                the_grid[(len(the_grid)-1) - row].append(blue_army[token])
                token += 1

    # fill the rest of the spaces up
    for row in range(length):
        
        if len(the_grid[row]) < width:

            r = length - len(the_grid[row])

            for i in range(r):

                the_grid[row].append('')

        

    return the_grid

"""
combat(attacker, defender)
:param attacker: a string representing a token. this is the attacking token. it will be passed in in token format ('R2', 'B5')
:param defender: same thing as attacker, but it is the defending token
this function is used to simulate combat. 
it will return a 1 if the attacker strength is greater than or equal to the defender strength, and a 0 otherwise 

"""
def combat(attacker, defender):

    at_str = int(attacker[1:])
    def_str = int(defender[1:])

    if at_str >= def_str:
        return 1
    return 0

"""
move(grid, select, target)
:param grid: you already know what this is by now. the grid that stores the boards data
:param select: a coordinate set pointing to the selected space in c format (row col) that represents whatever is on the selected space. 
               this is already valid
:param target: a coordinate set pointing to the desired movement space in c format (row col) that represents whatever is on the movement space.
               this is already valid

"""
def move(grid, select, target):

    select_row = int(select[0:1])
    select_col = int(select[2:])
    target_row = int(target[0:1])
    target_col = int(target[2:])

    grid[target_row][target_col] = grid[select_row][select_col]

    grid[select_row][select_col] = ''

"""
take_turn(grid, turn)
:param grid: the grid that handles all changes to the board, the skeleton of the board, whatever you wanna call it. its a 2d list containing
             the places of all tokens 
:turn: a bool. if false, it is red turn. if true, its blue turn. 
this function is to handle movement and combat, ending the turn if all is valid, repeating it if all is not
returns an updated grid

"""

def take_turn(grid, turn):

    repeat = True # if repeat is true, repeat the turn. when the turn has met all valid states, then set repeat to false

    player = 'R' # red turn

    if turn: # blue turn 

        player = 'B' # blue turn

    turn = True
    while turn: # this while loop controls the turn. while the player still has to do their turn, keep on looping. 
        select_pos = ''
        select_cord = []

        while repeat: # this first while loop handles getting the selection input for what token the player wants to move

            select_pos = input("select a token to move my tile (row col) >> ")
            select_cord = select_pos.split(' ')
            
            if len(select_cord) != 2:
                print("please enter something in the correct format. restarting...")
            elif ((0 > int(select_cord[0])) or (int(select_cord[0]) >= len(grid))) or ((0 > int(select_cord[1])) or (int(select_cord[1]) >= len(grid[int(select_cord[0])]))):
                print("thats out of bounds. restarting...")
            elif grid[int(select_cord[0])][int(select_cord[1])] == '' or grid[int(select_cord[0])][int(select_cord[1])][1:] == 'F':
                print("please do not select an empty space or a flag. restarting...")
            elif grid[int(select_cord[0])][int(select_cord[1])][0:1] != player:
                print("please select a token you own. restarting")
            else: # since the player has selected a valid token (one that exists and that they own), move on
                repeat = False 
            
        repeat = True

        move_pos = ''
        move_cord = []

        while repeat:

            move_pos = input("select a tile to move to (row col) >> ")
            move_cord = move_pos.split(' ') # move_cord[0] is the row that the player selected, move_cord[1] is the col

            if len(move_cord) == 2:
                move_row = int(move_cord[0])
                move_col = int(move_cord[1])
                if move_row < 0 or move_row >= len(grid) or move_col < 0 or move_col >= len(grid[move_row]): # if its not in bounds
                    print("that's out of bounds. restarting.")
                elif not (-1 <= move_row - int(select_cord[0]) <= 1 and -1 <= move_col - int(select_cord[1]) <= 1): # if the move is too far
                    print('thats too far. restarting')
                elif grid[move_row][move_col] != '': # if its not an empty space 
                    if grid[move_row][move_col][0:1] == player: # if the token on the target tile is allied
                        print("you cant move there, theres an allied token on that tile")
                    else: # so its not an allied tile, but theres dfinitely a tile where you want to move
                        if grid[move_row][move_col][1:] != 'F': # if that tile isnt a flag
                            result = combat(grid[int(select_cord[0])][int(select_cord[1])], grid[move_row][move_col]) # make the two units fight
                            if result == 1: # if the attacker wins, move attacker onto target tile
                                move(grid, select_pos, move_pos)
                            else: # the attacker lost, so delete them
                                grid[int(select_cord[0])][int(select_cord[1])] = ''
                            
                            repeat = False 
                            turn = False
                        else: # the tile on the target is an enemy flag, so you get to take it without any repurcussions
                            move(grid, select_pos, move_pos)
                            repeat = False
                            turn = False
                else: # so it is an empty space. move in without any repurcussions. 
                    move(grid, select_pos, move_pos)
                    repeat = False
                    turn = False
            else: # the player didnt enter their input in the right format
                print("pleae enter something in the correct format. restarting...")


            
        


"""
victory_check(grid)
:param grid: the grid. the board. the thing. stores information of the boards data
this function handles victory checks. its going to loop through the grid to look for flags. 
if it sees a flag, it adds it to a list called flags. When its done looking for flags, its going to look to see whats in the array
if the length of the flags list is 2, there are 2 flags, and we already know the game hasnt ended yet so return 2
if the length of the flags list is 1, there is only one flag on the board, so look into it to see what it is. 
if the flag is a blue flag, blue team won. if the flag is a red flag, red team one.
return 1 for a blue victory, and 0 for a red victory. 

"""
def victory_check(grid):

    flags = []

    for row in range(len(grid)):  
        for col in range(len(grid[row])):
            if grid[row][col][1:] == 'F':
                flags.append(grid[row][col])

    if len(flags) != 2:
        if flags[0][0:1] == 'B':
            return 1
        else: 
            return 0
    else: 
        return 2
"""
tactego(length, width, seed, piece_file)
:param grid: the grid, the board, you already know what this is. stores the board data. 
:param length: the length of the board, an int
:param width: the width of the board, an int. 
:param seed: the random seed to be used in the generation of the red side of the board. 
thi is the function that puts everything together and makes the game run. it handles the main loop of the game, utilizing the 
other functions I made earlier as helper functions
Heres the plan: 
1. using the seed, initialize the board using the piece_file and the helper functions made to do that
2. then save the new board to a variable called grid or something
3. start a while loop connected to a flag variable.
4. at the start of each iteration, run a victory check. if the flag returns an int > -1, set the flag variable to false. 
5. create a variable to keep track of turns (before the loop starts). itll be a bool: false for red turn, true for blue turn. 
6. print board, take turn, swap turns. 

"""
def tactego(length, width, piece_file):

    if length > 0 and width > 0 and seed != '' and piece_file != '':

        ud = init_unit_dicts(piece_file)

        board = init_grid(ud, length, width)

        turn = False

        run = True

        while run:

            print_board(board, length, width)
            take_turn(board, turn)

            if not turn:
                turn = True
            else: 
                turn = False 

            if victory_check(board) > -1:
                if victory_check(board) == 0: 
                    print("red won")
                    run = False
                elif victory_check(board) == 1:
                    print("blue won")
                    run = False
                else:
                    print("it was a tie")
    
    else: 
        print("one of your inputs were invalid. terminating...")


if __name__ == '__main__':

    seed = input("seed? ")
    random.seed(seed)
    file_name = "project 2\\" + input("pieces file name? ")
    length = int(input("board length? "))
    width = int(input("board width? "))

    tactego(length, width, file_name)
