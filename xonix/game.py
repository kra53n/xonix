from collections import deque

import pyxel as px

from enemy import Enemy
from field import Field
from popup_messages import GameOverMessage, WinMessage
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
        # self._field.set_player(self._player)
        # self._field.set_tail(self._tail)
    
    def draw(self):
        px.cls(0)
        for enemy in self._enemies:
            enemy.draw()
        self._tail.draw()
        self._field.draw()
        self._player.draw()

    def update(self):
        self.update_field()
        self._player.update()
        self._tail.update()
        for enemy in self._enemies:
            enemy.update(self._field, self._tail)

        self.update_game_status()

    def update_game_status(self):
        if (self._player.is_stepped_on_tail or
            self._tail.have_come):
            self._scenes.append(GameOverMessage(self._scenes))
        elif self._field.fullness >= 0.75:
            self.draw()
            self._scenes.append(WinMessage(self._scenes))

    def move_player(self):
        player_pos = self._field.obj_relative_pos(self._player, self._player.size)
        match self._player.move_status:
            case PlayerMoveStatus.Stop:
                pass
            case PlayerMoveStatus.Up:
                if player_pos[1] == self._field.y:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.up()
            case PlayerMoveStatus.Down:
                if player_pos[1] == self._field.h-1:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.down()
            case PlayerMoveStatus.Left:
                if player_pos[0] == self._field.x:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.left()
            case PlayerMoveStatus.Right:
                if player_pos[0] == self._field.w-1:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.right()

    def update_field(self):
        self.move_player()
        self._player.on_field = self._field.obj_on_field(self._player,
                                                         self._player.size)

        if self._player.prev_on_field == 1:
            self._tail.clear()
        elif self._player.prev_on_field == 0 and self._player.on_field == 1:
            self._player.move_status = PlayerMoveStatus.Stop
            self._field.process_filling(self._tail)
            self._tail.clear()
        self._player.prev_on_field = self._player.on_field

