import random
from components import create_battleships, place_battleships, initialise_board
from game_engine import attack, cli_coordinates_input
user_board = place_battleships(initialise_board(), create_battleships(), algorithm='custom')
ai_board = place_battleships(initialise_board(), create_battleships(), algorithm='random')
ships = create_battleships()
players = {'User':[user_board, ships], 'AI': [ai_board, ships]}
def generate_attack() -> tuple:
    '''Generates coordinates for the AI to attack'''
    x = random.randint(0, (len(user_board)-1))
    y = random.randint(0, (len(user_board)-1))
    return x, y

def ai_opponent_game_loop():
    '''Multiplayer Battleships with a human user against an AI
       on the command-line interface'''
    print("Welcome to Battleships my friend!")
    while any(players['User'][1].values()) and any(players['AI'][1].values()):
        print("User's turn:")
        coordinates = cli_coordinates_input()
        hit, sunk = attack(coordinates, players['AI'][0], players['AI'][1])
        if hit:
            print("Bullseye! You got a hit!")
            if sunk:
                print("Battleship has been sunk!")
        else:
            print("Unlucky mate, you have missed.")   
        if all(size == 0 for size in players['AI'][1].values()):
            print("Congratulations, you have achieved victory!")
            break
    
        print("AI's turn:")
        ai_coordinates = generate_attack()
        ai_hit, ai_sunk = attack(ai_coordinates, players['User'][0], players['User'][1])
        if ai_hit:
            print("AI has hit")
            if ai_sunk:
                print("AI has sunk your battleship.")
        else:
            print("AI has missed!")
        if all(size == 0 for size in players['User'][1].values()):
            print("Unfortunately, you have lost against the AI.")
            break

    print("Game Over")

if __name__ == '__main__':
    ai_opponent_game_loop()