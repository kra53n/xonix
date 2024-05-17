from random import choice

import pyxel as px

import config
from field import Field


class Enemy:
    def __init__(self, x: int, y: int):
        self.x = 20
        self.y = 20
        self._x_direction = choice((-1, 1))
        self._y_direction = choice((-1, 1))
        self._offset = config.BLOCK_SIZE
        self.size = config.BLOCK_SIZE
        self._col = config.ENEMY_COL
        self._field: Field = None

    def set_field(self, field: Field):
        self._field = field

    def _move(self):
        self.x += int(self._offset * self._x_direction)
        self.y += int(self._offset * self._y_direction)

    def update(self):
        self._move()

        if self._field.intersect(self.x, self.y):
            if (not self._field.intersect(self.x - self._offset, self.y) and
                not self._field.intersect(self.x, self.y - self._offset)):
                self.x += self._offset
                self.y += self._offset
                self._x_direction *= -1
                self._y_direction *= -1
            elif (not self._field.intersect(self.x + self._offset, self.y) and
                not self._field.intersect(self.x, self.y + self._offset)):
                self.x -= self._offset
                self.y -= self._offset
                self._x_direction *= -1
                self._y_direction *= -1
            elif not self._field.intersect(self.x + self._offset, self.y):
                self.x += self._offset
                self._x_direction *= -1
            elif not self._field.intersect(self.x - self._offset, self.y):
                self.x -= self._offset
                self._x_direction *= -1
            elif not self._field.intersect(self.x, self.y + self._offset):
                self.y += self._offset
                self._y_direction *= -1
            elif not self._field.intersect(self.x, self.y - self._offset):
                self.y -= self._offset
                self._y_direction *= -1

    def draw(self):
        px.rect(self.x, self.y, self._offset, self._offset, self._col)
