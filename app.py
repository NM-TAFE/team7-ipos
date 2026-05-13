from flask import Flask, render_template, request, redirect, url_for
from game_service import check_winner, check_draw
from src.sounds import play_sound
import functools

app = Flask(__name__)

# Initialise game board and current player
board = [' '] * 9
current_player = 'X'
x_wins = 0
o_wins = 0
draws = 0

# Player symbol
player_symbol = 'X'


def validate_move(func):
    @functools.wraps(func)
    def wrapper(cell):
        if board[cell] != ' ':
            return redirect(url_for('index'))
        return func(cell)
    return wrapper


def count_empty_spots():
    """
    Count how many empty spaces are left on the Tic Tac Toe board.

    The board is stored as a list of 9 slots.
    An empty slot = ' '

    This function uses a simple linear search.
    It checks each slot one by one and counts the slots that are empty.

    Returns: (int) The number of empty spaces left on the board.
    """
    empty_count = 0
    for cell in board:
        if cell == ' ':
            empty_count = empty_count + 1
    return empty_count


@app.route('/')
def index():
    winner = check_winner(board)
    draw = check_draw(board)

    # Get the number of empty slots so it can be shown as "moves left" on the game page.
    empty_spots = count_empty_spots()

    return render_template(
        'index.html',
        board=board,
        current_player=current_player,
        winner=winner,
        draw=draw,
        draws=draws,
        x_wins=x_wins,
        o_wins=o_wins,
        player_symbol=player_symbol,
        empty_spots=empty_spots
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
    if board[cell] == ' ' and not check_winner(board):
        board[cell] = current_player
        play_sound(current_player)
        if not check_winner(board):
            if check_draw(board):
                global draws
                draws = draws + 1
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            if current_player == "X":
                global x_wins
                x_wins = x_wins + 1
            else:
                global o_wins
                o_wins = o_wins + 1
    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    global board, current_player

    board = [' '] * 9
    current_player = player_symbol

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
