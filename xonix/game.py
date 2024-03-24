from collections import deque

import pyxel as px

import action
from field import Field
from player import Player


class Game:
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._player = Player(8, 8, 8, 8, 1)
        self._field = Field()
    
    def draw(self):
        px.cls(0)
        self._field.draw()
        self._player.draw()

    def update(self):
        self._field.update()
        self._player.update()

        if action.move_player_up():
            self._player.up()

        if action.move_player_down():
            self._player.down()

        if action.move_player_left():
            self._player.left()

        if action.move_player_right():
            self._player.right()
