"""
File:    lost_and_found.py
Author: Josh Ventura
Date: 11/12/21
Section: 35
E-mail:  j246@umbc.edu
Description:
  This python program emulates a 'lost and found' game in which the objective of the game is to
  make it to the exit 'x' using the W A S D & E keys. Users must pick up required items in order to
  open locked doors, to make it to the 'x'. 

"""
# way to encode things easily to save files

import json

STARTING_LOCATION = 'start'
USE = 'e'
EMPTY = ''
FLOOR = '_'
EXIT = 'x'
DOOR = 'd'
SECRET = 's'
WALL = '*'
ITEMS = 'i'
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
PLAYER = '\u1330'


def load_map(map_file_name):
    """
        When a map file name is passed the file will load the grid and return it.
        Should you modify this function? No you shouldn't.

    :param map_file_name: a string representing the file name.
    :return: a 2D list which contains the current map.
    """
    with open(map_file_name) as map_file:
        the_map = json.loads(map_file.read())

    return the_map


def play_game(the_grid):
    """

    :param the_grid: the playable map file
    :return: nothing
    """
    inventory = []
    user_y = 0
    user_x = 0
    game_continue = False

    #secrets appear as walls until found, shouldn't appear as 's'
    #no longer secret '*' -> 'd'
    #for row_index loop

    all_items = []
    for row_index in range(len(the_grid)):
        for col_index in range(len(the_grid[row_index])):
            if row_index == user_y and col_index == user_x:
                print("\u1330", end=" ")
            elif the_grid[row_index][col_index]['items']:
                print(ITEMS, end=' ')
                #row  col dictionary ->
                #symbol: str
                #items : list[strings]
                #require: list[string]
                #start: bool T/F
                for item in the_grid[row_index][col_index]['items']:
                    all_items.append(item)
            else:
                if the_grid[row_index][col_index]['symbol']  == SECRET:
                    print(WALL,end=' ')
                else:
                    print(the_grid[row_index][col_index]['symbol'], end=' ')
        print()
    print(', '.join(all_items))
    while game_continue == False:
        user_command = input("Enter Move (wasd) (e to activate doors or secrets): ")
        temp = movement(the_grid,user_y,user_x,user_command,inventory)
        if temp is not None:
            if temp == 'GAME OVER':
                game_continue = True
            print(temp)
            user_y = temp[0]
            user_x = temp[1]
        inventory = item_get(the_grid, user_y, user_x, inventory, game_continue)

def movement(map_file,user_y,user_x,user_command,inventory):
    if user_command != UP and user_command != DOWN and user_command != LEFT and user_command != RIGHT and user_command != USE:
        print("Invalid Command!")

        return None

    else:
        if user_command == UP:
            if (user_y - 1) > 0:
                if map_file[user_y - 1][user_x]['symbol'] == DOOR:
                    print("That's a door")
                    print_grid(map_file)
                    return None
                elif map_file[user_y - 1][user_x]['symbol'] == WALL:
                    print("Thats a wall")
                    print_grid(map_file)
                    return None
                else:
                    if map_file[user_y - 1][user_x]['symbol'] == EXIT:
                        print("You win!")
                        print_grid(map_file)
                        return 'GAME OVER'
                    map_file[user_y - 1][user_x]['symbol'] = PLAYER
                    map_file[user_y][user_x]['symbol'] = FLOOR
                    print_grid(map_file)
                    return [user_y - 1, user_x]
            else:
                print("Invalid Command!")
                print_grid(map_file)
                return None

        elif user_command == DOWN:
            if (user_y + 1) < len(map_file):
                if map_file[user_y + 1][user_x]['symbol'] == DOOR:
                    print("That's a door")
                    print_grid(map_file)
                    return None
                elif map_file[user_y + 1][user_x]['symbol'] == WALL:
                    print("Thats a wall")
                    print_grid(map_file)
                    return None
                else:
                    if map_file[user_y + 1][user_x]['symbol'] == EXIT:
                        print("You win!")
                        print_grid(map_file)
                        return 'GAME OVER'
                    map_file[user_y + 1][user_x]['symbol'] = PLAYER
                    map_file[user_y][user_x]['symbol'] = FLOOR
                    print_grid(map_file)
                    return [user_y + 1, user_x]
            else:
                print("Invalid Command!")
                print_grid(map_file)
                return None
        elif user_command == LEFT:
            if (user_x - 1) >= 0:
                if map_file[user_y][user_x - 1]['symbol'] == DOOR:
                    print("That's a door")
                    print_grid(map_file)
                    return None
                elif map_file[user_y][user_x - 1]['symbol'] == WALL:
                    print("Thats a wall")
                    print_grid(map_file)
                    return None
                else:
                    if map_file[user_y][user_x -1]['symbol'] == EXIT:
                        print("You win!")
                        print_grid(map_file)
                        return 'GAME OVER'
                    map_file[user_y][user_x - 1]['symbol'] = PLAYER
                    map_file[user_y][user_x]['symbol'] = FLOOR
                    print_grid(map_file)
                    return [user_y, user_x -1]
            else:
                print("Invalid Command!")
            print_grid(map_file)
            return None
        elif user_command == RIGHT:
            if (user_x +1) < len(map_file[user_y]):
                if map_file[user_y][user_x + 1 ]['symbol'] == DOOR:
                    print("That's a door")
                    print_grid(map_file)
                    return None
                elif map_file[user_y][user_x + 1]['symbol'] == WALL:
                    print("Thats a wall")
                    print_grid(map_file)
                    return None
                else:
                    if map_file[user_y][user_x + 1]['symbol'] == EXIT:
                        print("You win!")
                        print_grid(map_file)
                        return 'GAME OVER'
                    map_file[user_y][user_x + 1]['symbol'] = PLAYER
                    map_file[user_y][user_x]['symbol'] = FLOOR
                    print_grid(map_file)
                    return [user_y, user_x + 1]
        elif user_command == USE:
            if map_file[user_y-1][user_x]['symbol'] == DOOR: #checks above
                if 'requires' in map_file[user_y - 1][user_x]:
                    for item in map_file[user_y - 1][user_x]['requires']:
                        if item in inventory:
                            print("You used your", item, "to open the door!")
                            map_file[user_y -1][user_x]['requires'].remove(item)
                            inventory.remove(item)
                            map_file[user_y - 1][user_x].update({'symbol': "_"})
                        else:
                            print("You need a ", item, "to open this door!")
                else:
                    print("You opened the door!")
                    map_file[user_y-1][user_x]['symbol']= "_"

            if map_file[user_y + 1][user_x]['symbol'] == DOOR:  # checks below
                if 'requires' in map_file[user_y + 1][user_x]:
                    for item in map_file[user_y + 1][user_x]['requires']:
                        if item in inventory:
                            print("You used your", item, "to open the door!")
                            map_file[user_y + 1][user_x]['requires'].remove(item)
                            inventory.remove(item)
                            map_file[user_y + 1][user_x].update({'symbol': "_"})
                        else:
                            print("You need a ", item, "to open this door!")
                else:
                    print("You opened the door!")
                    map_file[user_y + 1][user_x]['symbol'] = "_"

            if user_x+1 < len(map_file[user_y]):
                if map_file[user_y][user_x+1]['symbol'] == DOOR: #check right
                    if 'requires' in map_file[user_y][user_x+1]:
                        for item in map_file[user_y][user_x+1]['requires']:
                            if item in inventory:
                                print("You used your", item, "to open the door!")
                                map_file[user_y][user_x+1]['requires'].remove(item)
                                inventory.remove(item)
                                map_file[user_y][user_x+1].update({'symbol': "_"})
                            else:
                                print("You need a ", item, "to open this door!")
                    else:
                        print("You opened the door!")
                        map_file[user_y][user_x+1]['symbol']= "_"

            if user_x+1 < len(map_file[user_y]):
                if map_file[user_y][user_x-1]['symbol'] == DOOR: #check right
                    if 'requires' in map_file[user_y][user_x-1]:
                        for item in map_file[user_y][user_x-1]['requires']:
                            if item in inventory:
                                print("You used your", item, "to open the door!")
                                map_file[user_y][user_x-1]['requires'].remove(item)
                                inventory.remove(item)
                                map_file[user_y][user_x-1].update({'symbol': "_"})
                            else:
                                print("You need a ", item, "to open this door!")
                    else:
                        print("You opened the door!")
                        map_file[user_y][user_x-1]['symbol']= "_"

            elif map_file[user_y -1][user_x]['symbol']== SECRET:
                print("Secret passage revealed!")
                map_file[user_y - 1][user_x].update({'symbol':"d"})
            elif map_file[user_y+1][user_x]['symbol']== SECRET:
                print("Secret passage revealed!")
                map_file[user_y+1][user_x].update({'symbol':"d"})



            else:
                print("Invalid Command!")

        print_grid(map_file)
        return None


def print_grid(the_grid):
    for row_index in range(len(the_grid)):
        for col_index in range(len(the_grid[row_index])):
            if the_grid[row_index][col_index]['items']:
                print(ITEMS, end=' ')
                #row  col dictionary ->
                #symbol: str
                #items : list[strings]
                #require: list[string]
                #start: bool T/F
            else:
                if the_grid[row_index][col_index]['symbol']  == SECRET:
                    print(WALL,end=' ')
                else:
                    print(the_grid[row_index][col_index]['symbol'], end=' ')
        print()
def item_get(map_file, row_index, col_index, inventory, game_continue):
    """

    :param map_file: The map_file
    :param  user_x: The user's x position
    :param user_y: The user's y position
    :param inventory: The user's inventory list to appear below map
    :return: Updated inventory
    """
    if game_continue == False:
        if map_file[row_index][col_index]['items'] != []:
            if map_file[row_index][col_index]['items'][0] not in inventory:
                for items in map_file[row_index][col_index]['items']:
                    inventory.append((items))
        print("Current inventory: ", inventory)
        return inventory

if __name__ == '__main__':
    map_file_name = input('What map do you want to load? ')
    the_game_map = load_map(map_file_name)
    if the_game_map:
        play_game(the_game_map)

