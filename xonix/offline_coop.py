from collections import deque
from typing import Iterable
from random import randrange

import pyxel as px

import colorschemes
import config

from bar import Bar
from enemy import Enemy
from fonts import fonts
from field import Field
from popup_messages import GameOverMessage, WinMessage, GetPlayersInput
from player import Player, PlayerMoveStatus
from lvls import get_next_lvl
from tail import Tail


class OfflineCoop:
    def __init__(
            self,
            scenes: deque,
            lives: int,
            lvl: int,
            enemies: Iterable[Enemy],
            player1_keys: tuple | None = None,
            player2_keys: tuple | None = None,
    ):
        self._scenes = scenes
        self._field = Field()
        self._player = self.spawn_player()
        self._enemies = enemies
        self.lives = lives
        self.lvl = lvl
        self._bars = self.spawn_bars()

        # the values setting after PlayerInput execution if they are None
        self.player1_keys: tuple | None = player1_keys
        self.player2_keys: tuple | None = player2_keys
        
        # execute functions in deque when update function calling
        self.exec_later = deque([
            lambda lvl=self.lvl: colorschemes.set(lvl % len(colorschemes.palletes)),
        ])
        if not (self.player1_keys and self.player2_keys):
            self.exec_later.append(lambda: self._scenes.append(GetPlayersInput(self._scenes)))
    
    def draw(self):
        px.cls(config.BACKGROUND_COL)
        for bar in self._bars:
            bar.draw()
        for enemy in self._enemies:
            enemy.draw()
        self._field.draw()
        self._player.draw()

    def update(self):
        while self.exec_later:
            self.exec_later.pop()()

        self.update_field()
        self._player.update()
        for enemy in self._enemies:
            enemy.update(self._field, self._player.tail)

        self.update_game_status()

    def update_game_status(self):
        # lose the live
        if ((self._player.is_stepped_on_tail or
             self._player.tail.have_come) and
            self.lives > 1):
            self.lives -= 1
            self._player = self.spawn_player()
        # game over
        elif (self._player.is_stepped_on_tail or
            self._player.tail.have_come):
            self._scenes.append(GameOverMessage(self._scenes))
        # win
        elif self._field.fullness >= 0.75:
            self.draw()
            self._scenes.pop()
            self._scenes.append(get_next_lvl(
                OfflineCoop,
                self._scenes,
                self.lives,
                self.lvl,
                player1_keys=self.player1_keys,
                player2_keys=self.player2_keys,
            ))
            self._scenes.append(WinMessage(self._scenes))


    def spawn_player(self) -> Player:
        return Player(self._field.x + self._field.block_size,
                      self._field.y + self._field.block_size * 2)

    def spawn_bars(self) -> Iterable[Bar]:
        bars = (Bar(2, 0, 'fullness', config.TEXT1_COL, lambda: f'{int(self._field.fullness*100)}%', config.TEXT2_COL),
                Bar(2, 0, 'lives', config.TEXT1_COL, lambda: str(self.lives), config.TEXT2_COL),
                Bar(2, 0, 'lvl', config.TEXT1_COL, lambda: str(self.lvl+1), config.TEXT2_COL))
        letter_sz = fonts['inkscript'].letter_sz
        off = 2
        for i, bar in enumerate(bars):
            bar.y = (off + letter_sz) * i + off
        return bars

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
