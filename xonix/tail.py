import pyxel as px


class Tail(list):
    def __init__(self, size: int, col: int):
        self.size = size
        self._col = col

    def append(self, coord: tuple[int, int]):
        super().append(coord)

    def update(self):
        pass

    def draw(self):
        for coord in self:
            px.rect(coord[0], coord[1], self.size, self.size, self._col)
             
