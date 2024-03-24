import pyxel as px


class Field:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._w = 16
        self._h = 16
        self._block_size = 8
        self._col = 3

        self._field = []
        self._init_field()

    def _init_field(self):
        for y in range(self._h):
            self._field.append([])
            for x in range(self._w):
                v = 0
                if any((x == 0, x == self._w - 1, y == 0, y == self._h - 1)):
                    v = 1
                self._field[-1].append(v)

    def _draw_field(self):
        for i, y in enumerate(self._field):
            for j, x in enumerate(y):
                if x == 0:
                    continue
                px.rect(self._x + j * self._block_size,
                        self._y + i * self._block_size,
                        self._block_size,
                        self._block_size,
                        self._col)

    def draw(self):
        self._draw_field()

    def update(self):
        pass
