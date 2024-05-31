import pyxel as px


class Font:
    def __init__(self,
                 img: int,
                 filename: str,
                 letter_sz: int,
                 start_sym: str,
                 row_end_sym: str,
                 font_col: int,
                 colkey: int):
        assert len(start_sym) == 1, 'must have 1 symbol'
        assert len(row_end_sym) == 1, 'must have 1 symbol'
        px.images[img].load(0, 0, filename)
        self._img = img
        self._row = ord(row_end_sym)+1 - ord(start_sym)
        self._font_col = font_col
        self._colkey = colkey
        self.letter_sz = letter_sz
        self._letter_off = letter_sz + 1

    def _recolor(self, x: int, y: int, w: int, h: int, col: int):
        for _x in range(x, w):
            for _y in range(y, h):
                if px.pget(_x, _y) != self._font_col:
                    continue
                px.pset(_x, _y, col)

    def draw(self, x: int, y: int, s: str, col: int):
        x_off = 0
        y_off = 0
        for c in s:
            if c == '\n':
                x_off = 0
                y_off += self._letter_off
                continue
            c = ord(c)
            u = (c % self._row) * self._letter_off
            v = (c // self._row - 1) * self._letter_off
            px.blt(x_off + x, y_off + y, self._img, u, v, self.letter_sz, self.letter_sz, self._colkey)
            x_off += self._letter_off
        self._recolor(x, y, x_off + x + self.letter_sz, y_off + y + self.letter_sz, col)


# wrap all fonts with lambda for the fonts initialization after the
# pyxel initialization by calling `load` function
fonts = {'inkscript': lambda: Font(0, 'assets/fonts/Inkscript.png', 7, ' ', '?', 0, 7)}


def load():
    for i, v in fonts.items():
        fonts[i] = v()
