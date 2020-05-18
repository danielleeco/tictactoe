import logging


def clear_field(n=3):
    return [[''] * n for i in range(n)]


size_of_field = 3
size_of_win = 3
field = clear_field(size_of_field)

is_over = False
current_player = 'X'  # чей ход
name2slot = {}  # name -> X|O
message = f'Ход {current_player}'

free_slots = ['X', 'O']  # свободные слоты для игры
active_users = {}  # username, last_request_time


def restart():
    global field, is_over, free_slots, active_users, name2slot
    field = clear_field(size_of_field)
    is_over = False
    free_slots = ['X', 'O']
    active_users = {}
    name2slot = {}


def check_win():
    result = 0

    def _check(x):
        if 'X' * size_of_win in x:
            return 1
        if 'O' * size_of_win in x:
            return -1
        return 0

    for i in range(0, size_of_field):
        row = ''.join(map(lambda j: field[i][j], range(0, size_of_field)))
        column = ''.join(map(lambda j: field[j][i], range(0, size_of_field)))
        result += _check(row)
        result += _check(column)
    diag1 = ''.join(map(lambda j: field[j][j], range(0, size_of_field)))
    diag2 = ''.join(map(lambda j: field[2-j][j], range(0, size_of_field)))
    result += (_check(diag1) + _check(diag2))
    return result


def state(username=None):
    global is_over
    is_win = check_win()
    if is_win:
        is_over = True
    return {
        "field": field,
        "player": current_player,
        "ready": len(name2slot) == 2,
        "is_win": is_win,
        "is_over": is_over,
        "you": name2slot.get(username, "")
    }


def tap(player, i, j):
    global current_player, field, is_over
    i = int(i)
    j = int(j)
    if len(name2slot) < 2:
        if player not in name2slot:
            name2slot[player] = len(name2slot)
        else:
            return "Not enough players"

    if is_over:
        restart()

    if name2slot[player] != current_player:
        return "Not your turn"

    if not (0 <= i < len(field)) or not (0 <= j < len(field[0])):
        return "Not in the field"

    if field[i][j] != '':
        return "Almost placed"

    field[i][j] = current_player
    current_player = 'X' if current_player == 'O' else 'O'

    count_null = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == '':
                count_null += 1
    if count_null == len(field) * len(field[0]):
        is_over = True
