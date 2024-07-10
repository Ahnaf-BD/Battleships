import random
import json
def initialise_board(size=10) -> list:
    '''Initialises the board with the provided size 
       with no battleships on it'''
    board_state = [[None]*size for x in range(size)]
    return board_state

def create_battleships(filename='battleships.txt') -> dict:
    '''Accesses the types and sizes of the battleships
       from the file provided and stores it in a dictionary'''
    battleships = {}
    with open(filename, 'r') as file:
        for line in file:
            new_line = line.split(':')
            name, size = map(str.strip, new_line) #Removes all the leading and trailing whitespaces
            battleships[name] = int(size)
    return battleships

def place_battleships(board, ships, algorithm='simple') -> list:
    '''Places the battleships on the board
       according to the algorithm user chooses'''
    if algorithm == 'simple':
        return place_battleships_simple(board, ships)
    if algorithm == 'random':
        return place_battleships_random(board, ships)
    if algorithm == 'custom':
        return place_battleships_custom(board, ships)
    raise ValueError("Invalid argument. Only 'simple', 'random' or 'custom' are allowed for algorithm")
def place_battleships_simple(board, ships):
    '''Places battleships horizontally in consecutive lines
       from coordinates (0, 0)'''
    i = 0
    for ship, size in ships.items():
        for j in range(size):
            board[i][j] = ship
        i += 1
    return board
def place_battleships_random(board, ships):
    '''Places battleships in random coordinates
       either horizontally or vertically'''
    board_length = len(board)-1
    x = random.randint(0, board_length)
    y = random.randint(0, board_length)
    orientation = random.choice(['h', 'v'])
    for ship, size in ships.items():
        for i in range(size):
            if orientation == 'h':
                while (y + i) > board_length: #Checks if y coordinate goes beyond the board
                    y = random.randint(0, board_length)
                board[x][y + i] = ship
            if orientation == 'v':
                while (x + i) > board_length: #Checks if x coordinate goes beyond the board 
                    x = random.randint(0, board_length)
                board[x + i][y] = ship
        x = random.randint(0, board_length)
        y = random.randint(0, board_length)
    return board
def place_battleships_custom(board, ships):
    '''Places battleships in coordinates and orientations
       specified in the given placement file'''
    with open('placement.txt', 'r') as file:
        placement = json.load(file)
        for ship, size in ships.items():
            x = int(placement[ship][0])
            y = int(placement[ship][1])
            orientation = placement[ship][2]

            for i in range(size):
                if orientation == 'h':
                    board[x][y + i] = ship
                if orientation == 'v':
                    board[x + i][y] = ship
    return board