from components import create_battleships, place_battleships, initialise_board
def attack(coordinates, board, battleships) -> bool:
    '''Computes an attack on the battleships and returns two boolean
       values to confirm if it hit and sunk the battleship or missed'''
    x, y = coordinates
    while x > (len(board)-1):
        x = int(input("Enter x co-ordinate but make sure it's within the board this time: "))
    while y > (len(board)-1):
        y = int(input("Enter y co-ordinate but make sure it's within the board this time: "))
    if board[x][y] in battleships: #if battleship has been hit
        hit = True
        battleship = board[x][y]
        if battleships[battleship] != 0: #Checks if the battleship has been sunk yet
            battleships[battleship] -= 1 #If not sunk, the size of the battleship decreases by 1
        board[x][y] = None
        sunk = battleships[battleship] == 0
        return hit, sunk
    
    #if battleship has not been hit
    hit = False
    sunk = False
    return hit, sunk

def cli_coordinates_input() -> tuple:
    '''Asks the user to input coordinates for their attack'''
    x = input("Enter x co-ordinate: ")
    y = input("Enter y co-ordinate: ")
    while x == '':
        x = input("Enter x co-ordinate but actually input something this time: ")
    while y == '':
        y = input("Enter y coordinate but actually input something this time: ")
    x = int(x)
    y = int(y)
    while x < 0:
        x = int(input("Enter x co-ordinate but make sure it's within the board this time: "))
    while y < 0:
        y = int(input("Enter y co-ordinate but make sure it's within the board this time: "))
    return x, y

def simple_game_loop():
    '''Single player Batlleships on the command-line interface'''
    print("Welcome to Battleships my friend!")
    empty_board = initialise_board()
    ships = create_battleships()
    board = place_battleships(empty_board, ships, algorithm='random')
    while any(ships.values()):
        coordinates = cli_coordinates_input()
        hit, sunk = attack(coordinates, board, ships)
        if hit:
            print("Hit!")
            if sunk:
                print("Battleship has been sunk!")
        else:
            print("Miss. Try again")
    
    print("Game Over")

if __name__ == '__main__':
    simple_game_loop()