import pyxel as px


class Player:
    def __init__(self, x: int, y: int, offset: int, size: int, col: int):
        assert offset % 2 == 0
        self._x = x
        self._y = y
        self._mx = 0
        self._my = 0
        self._offset = offset
        self._size = size
        self._col = col

    def up(self):
        self._my -= self._offset

    def down(self):
        self._my += self._offset

    def left(self):
        self._mx -= self._offset

    def right(self):
        self._mx += self._offset

    def _smooth_x_movement(self):
        vx = self._mx / 2
        self._mx = vx
        if vx == 0.5:
            self._mx = 0
            vx = 1
        self._x += vx

    def _smooth_y_movement(self):
        vy = self._my / 2
        self._my = vy
        if vy == 0.5:
            self._my = 0
            vy = 1
        self._y += vy

    def update(self):
        self._smooth_x_movement()
        self._smooth_y_movement()

    def draw(self):
        px.rect(self._x, self._y, self._size, self._size, self._col)
