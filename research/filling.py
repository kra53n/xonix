import collections
import typing

import pyxel as px


WDT = 80
HGT = 60


Col = typing.NewType('Col', int)
Point = collections.namedtuple('Point', ['x', 'y'])


class Rect:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.pos = Point(x, y)
        self.size = Point(w, h)

    def drw(self, c: Col, outline: bool = False, thickness: int = 1):
        (px.rect, px.rectb)[outline](self.pos.x, self.pos.y, self.size.x, self.size.y, c)


class Player:
    def __init__(self, x: int, y: int):
        self.rect = Rect(x, y, 1, 1)
        self.footprint = []

    def drw(self):
        self.rect.drw(5)

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass



player = Player(10, 10)
field_rect = Rect(10, 10, 40, 30)



def upd():
    func = px.btnp
    btns_mapping = (
        ((px.KEY_W, px.KEY_UP), player.up),
        ((px.KEY_A, px.KEY_LEFT), player.left),
        ((px.KEY_S, px.KEY_DOWN), player.down),
        ((px.KEY_D, px.KEY_RIGHT), player.right),
    )
    for real_btns, virtual_btn in btns_mapping:
        for real_btn in real_btns:
            if func(real_btn):
                virtual_btn()


def drw():
    field_rect.drw(12, outline=True)
    player.drw()


if __name__ == '__main__':
    px.init(WDT, HGT, title='filling research', quit_key=px.KEY_Q)
    px.run(upd, drw)
