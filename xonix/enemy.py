from random import choice, randint

import pyxel as px

import config
import utils
from field import Field
from tail import Tail


class Enemy:
    def __init__(self, x: int, y: int, min_delay:int, max_delay: int):
        self.x = x
        self.y = y
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.curr_delay = self._get_random_delay()
        self._x_direction = choice((-1, 1))
        self._y_direction = choice((-1, 1))
        self._offset = config.BLOCK_SIZE
        self.size = config.BLOCK_SIZE
        self._col = config.ENEMY_COL

    def _get_random_delay(self) -> int:
        return randint(self.min_delay, self.max_delay)

    def _move(self):
        if px.frame_count % self.curr_delay:
            return
        self.x += self._offset * self._x_direction
        self.y += self._offset * self._y_direction

    def _process_intersection_with_field(self, field: Field):
        if field.intersect(self.x, self.y, self.size):
            self.curr_delay = self._get_random_delay()

            # top left
            if (field.intersect(self.x + self._offset, self.y, self.size) and
                field.intersect(self.x, self.y + self._offset, self.size) and
                not field.intersect(self.x + self._offset, self.y + self._offset, self.size)):
                self.x += self._offset * 2
                self.y += self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # top right
            elif (field.intersect(self.x - self._offset, self.y, self.size) and
                field.intersect(self.x, self.y + self._offset, self.size) and
                not field.intersect(self.x - self._offset, self.y + self._offset, self.size)):
                self.x -= self._offset * 2
                self.y += self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # bottom left
            elif (field.intersect(self.x + self._offset, self.y, self.size) and
                field.intersect(self.x, self.y - self._offset, self.size) and
                not field.intersect(self.x + self._offset, self.y - self._offset, self.size)):
                self.x += self._offset * 2
                self.y -= self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # bottom right
            elif (field.intersect(self.x - self._offset, self.y, self.size) and
                field.intersect(self.x, self.y - self._offset, self.size) and
                not field.intersect(self.x - self._offset, self.y - self._offset, self.size)):
                self.x -= self._offset * 2
                self.y -= self._offset * 2
                self._x_direction *= -1
                self._y_direction *= -1
            # right
            elif not field.intersect(self.x + self._offset, self.y, self.size):
                self.x += self._offset * 2
                self._x_direction *= -1
            # left
            elif not field.intersect(self.x - self._offset, self.y, self.size):
                self.x -= self._offset * 2
                self._x_direction *= -1
            # top
            elif not field.intersect(self.x, self.y + self._offset, self.size):
                self.y += self._offset * 2
                self._y_direction *= -1
            # bottom
            elif not field.intersect(self.x, self.y - self._offset, self.size):
                self.y -= self._offset * 2
                self._y_direction *= -1

    def _process_stuck(self, field: Field):
        if field.intersect(self.x, self.y, self.size):
            self.x, self.y = choice(field.get_empty_cells_coords())

    def update(self, field: Field, tail: Tail):
        if not tail.have_come:
            self._move()
        self._process_intersection_with_field(field)
        self._process_stuck(field)
        if (self.x, self.y) in tail:
            tail.have_come = True

    def draw(self):
        px.rect(self.x, self.y, self._offset, self._offset, self._col)
