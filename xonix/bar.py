from typing import Callable

from fonts import fonts


class Bar:
    def __init__(self, x: int, y: int, key: str, key_col: int, val: Callable, val_col: int):
        self.x = x
        self.y = y
        self.key = key
        self.key_col = key_col
        self.val = val
        self.val_col = val_col

    def draw(self):
        letter_sz = fonts['inkscript'].letter_sz
        fonts['inkscript'].draw(self.x, self.y, self.key, self.key_col)
        fonts['inkscript'].draw(self.x + (letter_sz+1) * len(self.key), self.y, self.val(), self.val_col)
