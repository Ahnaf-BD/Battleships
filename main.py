import json
from flask import Flask, jsonify, render_template, request
from components import initialise_board, create_battleships, place_battleships
from game_engine import attack
from mp_game_engine import generate_attack

initial_board = initialise_board()
ships = create_battleships()
user_board = place_battleships(initial_board, ships, algorithm='custom')
ai_board = place_battleships(initial_board, ships, algorithm='random')
players = {'User':[user_board, ships], 'AI': [ai_board, ships]}


app = Flask(__name__)

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    '''Provides user interface for user to place their battleships on the board'''
    if request.method == 'GET':
        return render_template('placement.html', ships=ships, board_size=10)
    if request.method == 'POST':
        data = request.get_json()
        with open('player_placement.json', 'w') as placement:
            json.dump(data, placement)
        return jsonify({'message': 'Received'}), 200
    return render_template('placement.html')

@app.route('/', methods=['GET'])
def root():
    '''Provides main game interface where user can view and interact with the board'''
    if request.method == 'GET':
        return render_template('main.html', player_board=user_board)

@app.route('/attack', methods=['GET'])
def process_attack():
    '''Processes attacks from user to the AI and from AI to the user'''
    if request.args:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        coordinates = (x, y)
        hit, sunk = attack(coordinates, ai_board, ships)
        ai_coordinates = generate_attack()
        i, j = ai_coordinates
        ai_hit, ai_sunk = attack(ai_coordinates, user_board, ships)

        ai_board[x][y] = 'hit' if hit else None
        user_board[i][j] = 'AI hit' if ai_hit else None

        if all(size == 0 for size in players['AI'][1].values()):
            return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': "Congratulations, you have achieved victory!"}), 200
        if all(size == 0 for size in players['User'][1].values()):
            return jsonify({'hit': True, 'AI_Turn': ai_coordinates, 'finished': "Unfortunately, you have lost against the AI."}), 200    
        return jsonify({'hit': hit, 'AI_Turn': ai_coordinates}), 200

if __name__ == '__main__':
    app.template_folder = 'templates'
    app.run()