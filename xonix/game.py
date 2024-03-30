from collections import deque

import pyxel as px

from field import Field
from popup_messages import GameOverMessage
from player import Player, PlayerMoveStatus
from tail import Tail


class Game:
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._player = Player(2, 2, 2, 2, 1)
        self._tail = Tail(2, 8)
        self._field = Field()

        self._player.set_tail(self._tail)
        self._field.set_player(self._player)
        self._field.set_tail(self._tail)
    
    def draw(self):
        px.cls(0)
        self._tail.draw()
        self._field.draw()
        self._player.draw()

    def update(self):
        self._field.update()
        self._player.update()
        self._tail.update()

        if self._player.is_stepped_on_tail:
            self._scenes.append(GameOverMessage(self._scenes))

