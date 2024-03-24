import pyxel as px


def move_player_up():
    return px.btnp(px.KEY_UP) or px.btnp(px.KEY_W)

def move_player_down():
    return px.btnp(px.KEY_DOWN) or px.btnp(px.KEY_S)

def move_player_left():
    return px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_A)

def move_player_right():
    return px.btnp(px.KEY_RIGHT) or px.btnp(px.KEY_D)
