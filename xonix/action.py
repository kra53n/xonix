import pyxel as px


def move_player_up():
    return px.btn(px.KEY_UP) or px.btn(px.KEY_W)

def move_player_down():
    return px.btn(px.KEY_DOWN) or px.btn(px.KEY_S)

def move_player_left():
    return px.btn(px.KEY_LEFT) or px.btn(px.KEY_A)

def move_player_right():
    return px.btn(px.KEY_RIGHT) or px.btn(px.KEY_D)
