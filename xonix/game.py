from collections import deque

import pyxel as px

from enemy import Enemy
from field import Field
from popup_messages import GameOverMessage
from player import Player, PlayerMoveStatus
from tail import Tail


class Game:
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._player = Player(2, 2)
        self._enemies = [Enemy(6, 6)]
        self._tail = Tail()
        self._field = Field()

        self._player.set_tail(self._tail)
        self._field.set_player(self._player)
        self._field.set_tail(self._tail)
        for enemy in self._enemies:
            enemy.set_field(self._field)
            enemy.set_tail(self._tail)
    
    def draw(self):
        px.cls(0)
        for enemy in self._enemies:
            enemy.draw()
        self._tail.draw()
        self._field.draw()
        self._player.draw()

    def update(self):
        self._field.update()
        self._player.update()
        self._tail.update()
        for enemy in self._enemies:
            enemy.update()

        if (self._player.is_stepped_on_tail or
            self._tail.have_come):
            self._scenes.append(GameOverMessage(self._scenes))

