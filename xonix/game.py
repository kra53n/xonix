from collections import deque

import pyxel as px

from bar import Bar
from enemy import Enemy
from field import Field
from popup_messages import GameOverMessage, WinMessage
from player import Player, PlayerMoveStatus
from tail import Tail


class Game:
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._field = Field()
        self._player = Player(self._field.x + self._field.block_size,
                              self._field.y + self._field.block_size * 2)
        self._enemies = [Enemy(30, 30)]
        self._bars = (Bar(2, 2, 'fullness', 1, lambda: f'{int(self._field.fullness*100)}%', 2),)
    
    def draw(self):
        px.cls(12)
        for bar in self._bars:
            bar.draw()
        for enemy in self._enemies:
            enemy.draw()
        self._field.draw()
        self._player.draw()

    def update(self):
        self.update_field()
        self._player.update()
        for enemy in self._enemies:
            enemy.update(self._field, self._player.tail)

        self.update_game_status()

    def update_game_status(self):
        if (self._player.is_stepped_on_tail or
            self._player.tail.have_come):
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
                if self._player.y == self._field.y:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.up()
            case PlayerMoveStatus.Down:
                if self._player.y + self._player.size == self._field.y + self._field.h * self._field.block_size:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.down()
            case PlayerMoveStatus.Left:
                if self._player.x == self._field.x:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.left()
            case PlayerMoveStatus.Right:
                if self._player.x + self._player.size == self._field.x + self._field.w * self._field.block_size:
                    self._player.move_status = PlayerMoveStatus.Stop
                else:
                    self._player.right()

    def update_field(self):
        self.move_player()
        self._player.on_field = self._field.obj_on_field(self._player,
                                                         self._player.size)

        if self._player.prev_on_field == 1:
            self._player.tail.clear()
        elif self._player.prev_on_field == 0 and self._player.on_field == 1:
            self._player.move_status = PlayerMoveStatus.Stop
            self._field.process_filling(self._player.tail)
            self._player.tail.clear()
        self._player.prev_on_field = self._player.on_field
