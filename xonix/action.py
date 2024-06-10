import pyxel as px


def move_player_up():
    return (px.btnp(px.KEY_UP) or
            px.btnp(px.KEY_W) or
            px.btnp(px.GAMEPAD1_BUTTON_DPAD_UP))

def move_player_down():
    return (px.btnp(px.KEY_DOWN) or
            px.btnp(px.KEY_S) or
            px.btnp(px.GAMEPAD1_BUTTON_DPAD_DOWN))

def move_player_left():
    return (px.btnp(px.KEY_LEFT) or
            px.btnp(px.KEY_A) or
            px.btnp(px.GAMEPAD1_BUTTON_DPAD_LEFT))

def move_player_right():
    return (px.btnp(px.KEY_RIGHT) or
            px.btnp(px.KEY_D) or
            px.btnp(px.GAMEPAD1_BUTTON_DPAD_RIGHT))


def resume():
    return (px.btnp(px.KEY_SPACE) or
            px.btnp(px.KEY_RETURN) or
            px.btnp(px.GAMEPAD1_BUTTON_X) or
            px.btnp(px.GAMEPAD1_BUTTON_A))
