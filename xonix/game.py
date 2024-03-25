from collections import deque

import pyxel as px

import action
from field import Field
from player import Player, PlayerMoveStatus


class Game:
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._player = Player(2, 2, 2, 2, 1)
        self._field = Field(self._player)
    
    def draw(self):
        px.cls(0)
        self._field.draw()
        self._player.draw()

    def update(self):
        self._field.update()
        self._player.update()

        if (action.move_player_up() and
            self._player.move_status != PlayerMoveStatus.Down):
            self._player.move_status = PlayerMoveStatus.Up

        if (action.move_player_down() and
            self._player.move_status != PlayerMoveStatus.Up):
            self._player.move_status = PlayerMoveStatus.Down

        if (action.move_player_left() and
            self._player.move_status != PlayerMoveStatus.Right):
            self._player.move_status = PlayerMoveStatus.Left

        if (action.move_player_right() and
            self._player.move_status != PlayerMoveStatus.Left):
            self._player.move_status = PlayerMoveStatus.Right
