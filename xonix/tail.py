import pyxel as px

import config


class Tail(list):
    def __init__(self):
        self.size = config.BLOCK_SIZE
        self._col = config.TAIL_COL
        self.have_come = False

    def append(self, coord: tuple[int, int]):
        super().append(coord)

    def update(self):
        pass

    def draw(self):
        for coord in self:
            px.rect(coord[0], coord[1], self.size, self.size, self._col)
             
