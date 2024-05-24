from random import choice

import pyxel as px

import config
import utils
from field import Field
from tail import Tail


class Enemy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._x_direction = choice((-1, 1))
        self._y_direction = choice((-1, 1))
        self._offset = config.BLOCK_SIZE
        self.size = config.BLOCK_SIZE
        self._col = config.ENEMY_COL
        self._field: Field = None
        self._tail: Tail = None

    def set_field(self, field: Field):
        self._field = field

    def set_tail(self, tail: Tail):
        self._tail = tail

    def _move(self):
        self.x += int(self._offset * self._x_direction)
        self.y += int(self._offset * self._y_direction)

    def _process_intersection_with_field(self):
        if self._field.intersect(self.x, self.y):
            # top left
            if (self._field.intersect(self.x + self._offset, self.y) and
                self._field.intersect(self.x, self.y + self._offset) and
                not self._field.intersect(self.x + self._offset, self.y + self._offset)):
                self.x += self._offset * 2
                self.y += self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # top right
            elif (self._field.intersect(self.x - self._offset, self.y) and
                self._field.intersect(self.x, self.y + self._offset) and
                not self._field.intersect(self.x - self._offset, self.y + self._offset)):
                self.x -= self._offset * 2
                self.y += self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # bottom left
            elif (self._field.intersect(self.x + self._offset, self.y) and
                self._field.intersect(self.x, self.y - self._offset) and
                not self._field.intersect(self.x + self._offset, self.y - self._offset)):
                self.x += self._offset * 2
                self.y -= self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # bottom right
            elif (self._field.intersect(self.x - self._offset, self.y) and
                self._field.intersect(self.x, self.y - self._offset) and
                not self._field.intersect(self.x - self._offset, self.y - self._offset)):
                self.x -= self._offset * 2
                self.y -= self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # right
            elif not self._field.intersect(self.x + self._offset, self.y):
                self.x += self._offset * 2
                self._x_direction *= -1
            # left
            elif not self._field.intersect(self.x - self._offset, self.y):
                self.x -= self._offset * 2
                self._x_direction *= -1
            # top
            elif not self._field.intersect(self.x, self.y + self._offset):
                self.y += self._offset * 2
                self._y_direction *= -1
            # bottom
            elif not self._field.intersect(self.x, self.y - self._offset):
                self.y -= self._offset * 2
                self._y_direction *= -1

    def update(self):
        if not self._tail.have_come:
            self._move()
        self._process_intersection_with_field()
        if (self.x, self.y) in self._tail:
            self._tail.have_come = True

    def draw(self):
        px.rect(self.x, self.y, self._offset, self._offset, self._col)
