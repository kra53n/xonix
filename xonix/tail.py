import pyxel as px

import config


class Tail(list):
    def __init__(self, col: int = config.TAIL_COL):
        self.size = config.BLOCK_SIZE
        self._col = col
        self.have_come = False

    def append(self, coord: tuple[int, int]):
        super().append(coord)

    def update(self):
        pass

    def draw(self):
        for coord in self:
            px.rect(coord[0], coord[1], self.size, self.size, self._col)
             
