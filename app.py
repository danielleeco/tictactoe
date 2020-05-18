from flask import Flask, current_app, request, session
from flask import jsonify

import game
import logging
import random
import time


app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('index.html')


@app.route('/get_state')
def get_state():
    if 'username' not in session:
        username = str(random.random())
        session['username'] = username
    username = session['username']

    # обновить время последней активности
    if username in game.active_users:
        game.active_users[username] = time.time()

    # проверка активности юзеров, удаление, если активных давно не было
    for user, last_time in list(game.active_users.items()):
        if time.time() - last_time > 5:  # тогда игрок пропал, удаляем и рестарт
            game.restart()

    # если есть свободный слот -- добавить юзера
    if username not in game.active_users and len(game.free_slots):
        game.active_users[username] = time.time()  # посл. время активности
        game.name2slot[username] = game.free_slots[0]
        game.free_slots.pop(0)

    return jsonify(game.state(username))


@app.route('/click', methods=['POST'])
def click():
    if 'username' in session:
        content = request.json
        username = session['username']
        i = content["i"]
        j = content["j"]
        game.tap(username, i, j)
    return ""


if __name__ == '__main__':
    app.secret_key = str(random.random())
    app.run()
