from flask import Flask, render_template, request, redirect, url_for
from game_service import check_winner, check_draw
app = Flask(__name__)

# Initialise game board and current player
board = [' '] * 9
current_player = 'X'
x_wins = 0
o_wins = 0
draws = 0


@app.route('/')
def index():
    winner = check_winner(board)
    draw = check_draw(board)
    return render_template('index.html', board=board, current_player=current_player, winner=winner, draws=draws, x_wins=x_wins, o_wins=o_wins)


@app.route('/play/<int:cell>')
def play(cell):
    # breakpoint()
    global current_player
    if board[cell] == ' ' and not check_winner(board):
        board[cell] = current_player
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
    current_player = 'X'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
