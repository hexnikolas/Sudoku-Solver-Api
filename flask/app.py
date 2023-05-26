import os
import time

import sqlite3
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for, redirect
from flask_mysqldb import MySQL
from datetime import datetime

from notgraphical import Sudoku

app = Flask(__name__)
conn = None

app.config["MYSQL_USER"] = "flask-app"
app.config["MYSQL_PASSWORD"] = "kolhfgh124"
app.config["MYSQL_DB"] = "sudoku"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# function to return the tab icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/test')
def test():
    puzzletext = '.8..1......5....3.......4.....6.5.7.89....2.....3.....2.....1.9..67........4.....'
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM Puzzles where Puzzle = %s", (puzzletext,))
        rv = cur.fetchall()
        print(str(rv))
        return str(rv)
    # ip = request.remote_addr return('Script started') cur = mysql.connection.cursor() asd = f"insert into Puzzles (
    # Puzzle, Submited, ip) values ('.8..1......5....3.......4.....6.5.7.89....2.....3.....2.....1.9..67........4
    # .....', '123', {ip})" cur.execute('''SELECT * FROM Puzzles''') rv = cur.fetchall() return str(ip)

    # cur.execute("INSERT INTO Puzzles(Puzzle, Submited, ip) VALUES (%s, %s, %s)",
    # ('.8..1......5....3.......4.....6.5.7.89....2.....3.....2.....1.9..67........4.....', '123',
    # ip)) mysql.connection.commit() cur.close() return 'success'


# index
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/solve', methods=['POST'])
def solver():
    start = time.time()
    dict_to_return = dict()

    puzzletext = request.form['puzzle']
    try:
        check_input(puzzletext)
    except IndexError:
        error = 'Provided puzzle is not the correct length'
        return redirect(url_for('home', error=error))
    except TypeError:
        error = 'Provided puzzle contains wrong symbols'
        return redirect(url_for('home', error=error))

    puzzle = Sudoku()

    ip = request.remote_addr
    write_to_db(puzzletext, ip)

    ## TODO: all of these to be integrated into a function
    puzzle.create_sudoku_puzzle(puzzletext)
    puzzle.first_stage()
    puzzle.second_stage()
    puzzle.third_stage()
    if puzzle.unsolved != 0:
        print('fourth stage')
        puzzle.fourth_stage()
    if puzzle.unsolved != 0:
        print('fifth stage')
        puzzle.fifth_stage()
    puzzle.show_puzzle()
    last_puzzle = puzzle.return_result()

    results = []
    for i in last_puzzle:
        if isinstance(i, list):
            results.append(' ')
        else:
            results.append(i)

    dict_to_return['starting_puzzle'] = puzzletext
    time_elapsed = format(time.time() - start, '.3f')
    dict_to_return['time_elapsed'] = f'{time_elapsed} sec'
    dict_to_return['final_result'] = results
    dict_to_return['unsolved_spots'] = puzzle.unsolved
    if puzzle.unsolved == 0:
        dict_to_return['solved'] = True
    else:
        dict_to_return['solved'] = False
    # return json.dumps(dict_to_return)
    # return str(result)
    return render_template('result.html', dict_to_return=dict_to_return)


@app.route('/cache-me')
def cache():
    return "nginx will cache this response"


@app.route('/history')
def history():
    puzzles = read_from_db()
    return render_template('history.html', puzzles=puzzles)


@app.route('/info')
def info():
    resp = {
        'connecting_ip': request.headers['X-Real-IP'],
        'proxy_ip': request.headers['X-Forwarded-For'],
        'host': request.headers['Host'],
        'user-agent': request.headers['User-Agent']
    }

    return jsonify(resp)


@app.route('/flask-health-check')
def flask_health_check():
    return "success"


def check_input(puzzletext):
    if len(puzzletext) != 81:
        print('damn true')
        raise IndexError
    okchars = '0123456789.'
    if not (all(c in okchars for c in puzzletext)):
        raise TypeError


def write_to_db(puzzletext, ip):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM Puzzles where Puzzle = %s", (puzzletext,))
        rv = cur.fetchall()
        if len(rv) == 0:
            cur.execute("INSERT INTO Puzzles(Puzzle, Submited, ip) VALUES (%s, %s, %s)",
                        (puzzletext, datetime.now(), ip))
            mysql.connection.commit()


def read_from_db():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM Puzzles")
        rv = cur.fetchall()
        return str(rv)
