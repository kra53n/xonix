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


# Converts {'action': ('player': 'up')} to `'(action (player up))'`.
# Other examples of actions can be viewed in `utils_test.py` file.
def lispy(d: dict | str) -> str:
    match d:
        case str():
            return f'({d})'
        case tuple() | list():
            return '(' + ' '.join(map(str, d)) + ')'
    res = '('
    bracky = len(d) > 1
    for k, v in d.items():
        lhs = str(k)
        match v:
            case str():
                rhs = v
            case tuple() | list() | dict():
                rhs = lispy(v)
        i = f'{lhs} {rhs}'
        if bracky:
            i = f'({i}) '
        res += i
    if bracky:
        res = res.rstrip()
    return res + ')'


def unlispy(s: str) -> dict:
    pass
