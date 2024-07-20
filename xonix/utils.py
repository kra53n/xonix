import pyxel as px

import config


def point_in_rect(r_x1: int, r_y1: int, r_x2: int, r_y2: int, p_x: int, p_y: int):
    return (r_x1 <= p_x <= r_x2 and
            r_y1 <= p_y <= r_y2)


def centerize_rect_in_rect(w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> (int, int):
    return x2 - (w1 - w2) // 2, y2 - (h1 - h2) // 2


def draw_selection_cursor(x: int, y: int, pd: int):
    _x = x
    for j, row in enumerate(config.SELECTION_CURSOR_DATA):
        for i, v in enumerate(row):
            _x += pd
            if v == ' ':
                continue
            px.rect(_x, y, pd, 1, config.PLAYER_COL)
        _x = x
        y += 1


def flicker(v: float) -> bool:
    return abs(px.sin(px.frame_count * 8)) > v
