from flask import Flask, render_template, request, redirect, url_for
from game_service import check_winner, check_draw
from src.sounds import play_sound

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
    def wrapper(cell):
        if board[cell] != ' ':
            return redirect(url_for('index'))
        return func(cell)
    return wrapper


@app.route('/')
def index():
    winner = check_winner(board)
    draw = check_draw(board)

    return render_template(
        'index.html',
        board=board,
        current_player=current_player,
        winner=winner,
        draws=draws,
        x_wins=x_wins,
        o_wins=o_wins,
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
