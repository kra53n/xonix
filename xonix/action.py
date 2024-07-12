import pyxel as px

import config


def move_player_up(key_type: int = config.KEY_MOVE_TYPE_ANY) -> bool:
    key_type_keys = ((config.KEY_MOVE_TYPE_WASD, px.KEY_W),
                     (config.KEY_MOVE_TYPE_ARROWS, px.KEY_UP),
                     (config.KEY_MOVE_TYPE_GAMEPAD, px.GAMEPAD1_BUTTON_DPAD_UP))
    for kt, key in key_type_keys:
        if px.btnp(key) and key_type in (kt, config.KEY_MOVE_TYPE_ANY):
            return True
    return False


def move_player_down(key_type: int = config.KEY_MOVE_TYPE_ANY) -> bool:
    key_type_keys = ((config.KEY_MOVE_TYPE_WASD, px.KEY_S),
                     (config.KEY_MOVE_TYPE_ARROWS, px.KEY_DOWN),
                     (config.KEY_MOVE_TYPE_GAMEPAD, px.GAMEPAD1_BUTTON_DPAD_DOWN))
    for kt, key in key_type_keys:
        if px.btnp(key) and key_type in (kt, config.KEY_MOVE_TYPE_ANY):
            return True
    return False


def move_player_left(key_type: int = config.KEY_MOVE_TYPE_ANY) -> bool:
    key_type_keys = ((config.KEY_MOVE_TYPE_WASD, px.KEY_A),
                     (config.KEY_MOVE_TYPE_ARROWS, px.KEY_LEFT),
                     (config.KEY_MOVE_TYPE_GAMEPAD, px.GAMEPAD1_BUTTON_DPAD_LEFT))
    for kt, key in key_type_keys:
        if px.btnp(key) and key_type in (kt, config.KEY_MOVE_TYPE_ANY):
            return True
    return False


def move_player_right(key_type: int = config.KEY_MOVE_TYPE_ANY) -> bool:
    key_type_keys = ((config.KEY_MOVE_TYPE_WASD, px.KEY_D),
                     (config.KEY_MOVE_TYPE_ARROWS, px.KEY_RIGHT),
                     (config.KEY_MOVE_TYPE_GAMEPAD, px.GAMEPAD1_BUTTON_DPAD_RIGHT))
    for kt, key in key_type_keys:
        if px.btnp(key) and key_type in (kt, config.KEY_MOVE_TYPE_ANY):
            return True
    return False


def resume() -> bool:
    return (px.btnp(px.KEY_SPACE) or
            px.btnp(px.KEY_RETURN) or
            px.btnp(px.GAMEPAD1_BUTTON_X) or
            px.btnp(px.GAMEPAD1_BUTTON_A))
