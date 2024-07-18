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
#
# The `lispy` function uses for sending information between client and
# server. We could send just the Python type like dict apllyied with
# `str` but this solution has disadvantage:
#
# >>> len("{'action': {'player': 'up'}}")
# 28
# >>> len('(action (player up))')
# 20
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
            case str() | int():
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
    stack = []
    res = {}
    word = ''
    i = 0
    while i < len(s):
        match s[i]:
            case '(':
                stack.append(0)
                i += 1
                continue
            case ')':
                if word:
                    stack.append(word)
                    word = ''
                i += 1
                stack.append(1)
                continue
            case ' ':
                while i < len(s) and s[i] == ' ':
                    i += 1
                if word:
                    stack.append(word)
                    word = ''
                continue
        word += s[i]
        i += 1
    return _unlispy_recursion(stack)


def _unlispy_recursion(l: list):
    if len(l) > 2:
        if l[0] == 0 and l[1] == 0:
            res = {}
            start = 0
            while start < len(l):
                if l[start] == 0 and l[start+1] != 0:
                    end = start + 2
                    while end < len(l) and l[end] != 1:
                        end += 1
                    res[l[start+1]] = _unlispy_recursion(l[start+2:end])
                    start = end
                start += 1
            return res
        if l[-1] != 1:
            return l[1:]
        if l[0] == 0:
            # start here
            return {l[1]: _unlispy_recursion(l[2:-1])}
    elif len(l) == 1:
        return l[0]
