from flask import Flask, render_template, request, redirect, url_for
from src.sounds import play_sound

app = Flask(__name__)

# Initialise game board and current player
board = [' '] * 9
current_player = 'X'

# Player symbol
player_symbol = 'X'


def validate_move(func):
    def wrapper(cell):
        if board[cell] != ' ':
            return redirect(url_for('index'))
        return func(cell)
    return wrapper


def check_winner():
    # Winning combinations
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)  # Diagonal
    ]

    for combination in win_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != ' ':
            return board[combination[0]]

    return None


def check_draw():
    return ' ' not in board


@app.route('/')
def index():
    winner = check_winner()
    draw = check_draw()

    return render_template(
        'index.html',
        board=board,
        current_player=current_player,
        winner=winner,
        draw=draw,
        player_symbol=player_symbol
    )


# Set player symbol
@app.route('/set_symbol', methods=['POST'])
def set_symbol():
    global current_player, player_symbol

    selected_symbol = request.form['symbol']

    player_symbol = selected_symbol
    current_player = selected_symbol

    return redirect(url_for('index'))


@app.route('/play/<int:cell>')
@validate_move
def play(cell):
    global current_player

    if board[cell] == ' ':
        board[cell] = current_player
feature/player-choose-symbol
play_sound(current_player)
  
        if not check_winner():
            current_player = 'O' if current_player == 'X' else 'X'

    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    global board, current_player

    board = [' '] * 9
    current_player = player_symbol

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
