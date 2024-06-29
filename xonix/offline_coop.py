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
    def __init__(self,
                 scenes: deque,
                 lives: int,
                 lvl: int,
                 enemies: Iterable[Enemy],
                 player1_keys: tuple | None = None,
                 player2_keys: tuple | None = None):
        self._scenes = scenes
        self._field = Field()
        self._player1 = self.spawn_player1()
        self._player2 = self.spawn_player2()
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
        self._player1.draw_tail()
        self._player2.draw_tail()
        self._field.draw()
        self._player1.draw_only_player()
        self._player2.draw_only_player()

    def update(self):
        while self.exec_later:
            self.exec_later.pop()()

        self.update_field()
        for enemy in self._enemies:
            enemy.update(self._field, self._player1.tail)

        self.update_game_status()

    def update_game_status(self):
        someone_has_touched_someone = (self._player1.is_stepped_on_tail or
                                       self._player1.tail.have_come or
                                       self._player1.is_stepped_on_other_tail(self._player2.tail) or
                                       self._player2.is_stepped_on_tail or
                                       self._player2.tail.have_come or
                                       self._player2.is_stepped_on_other_tail(self._player1.tail))
        # lose the live
        if someone_has_touched_someone and self.lives > 1:
            self.lives -= 1
            self._player1 = self.spawn_player1()
            self._player2 = self.spawn_player2()
        # game over
        elif someone_has_touched_someone:
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


    def spawn_player1(self) -> Player:
        return Player(self._field.x + self._field.block_size,
                      self._field.y + self._field.block_size * 2,
                      config.PLAYER_COL,
                      config.TAIL_COL)

    def spawn_player2(self) -> Player:
        return Player(self._field.x + self._field.w * self._field.block_size - self._field.block_size * 2,
                      self._field.y + self._field.block_size * 2,
                      config.TAIL_COL,
                      config.PLAYER_COL)

    def spawn_bars(self) -> Iterable[Bar]:
        bars = (Bar(2, 0, 'fullness', config.TEXT1_COL, lambda: f'{int(self._field.fullness*100)}%', config.TEXT2_COL),
                Bar(2, 0, 'lives', config.TEXT1_COL, lambda: str(self.lives), config.TEXT2_COL),
                Bar(2, 0, 'lvl', config.TEXT1_COL, lambda: str(self.lvl+1), config.TEXT2_COL))
        letter_sz = fonts['inkscript'].letter_sz
        off = 2
        for i, bar in enumerate(bars):
            bar.y = (off + letter_sz) * i + off
        return bars

    def move_player(self, player: Player):
        player_pos = self._field.obj_relative_pos(player, player.size)
        match player.move_status:
            case PlayerMoveStatus.Stop:
                pass
            case PlayerMoveStatus.Up:
                if player.y == self._field.y:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.up()
            case PlayerMoveStatus.Down:
                if player.y + player.size == self._field.y + self._field.h * self._field.block_size:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.down()
            case PlayerMoveStatus.Left:
                if player.x == self._field.x:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.left()
            case PlayerMoveStatus.Right:
                if player.x + player.size == self._field.x + self._field.w * self._field.block_size:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.right()

    def move_players(self):
        if self.player1_keys is None or self.player2_keys is None:
            return
        for player1_key in self.player1_keys:
            if px.btnp(player1_key):
                self._player1.update()
                break
        for player2_key in self.player2_keys:
            if px.btnp(player2_key):
                self._player2.update()
                break
        self.move_player(self._player1)
        self.move_player(self._player2)

    def update_player(self, player: Player):
        player.on_field = self._field.obj_on_field(player,
                                                   player.size)

        if player.prev_on_field == 1:
            player.tail.clear()
        elif player.prev_on_field == 0 and player.on_field == 1:
            player.move_status = PlayerMoveStatus.Stop
            self._field.process_filling(player.tail)
            player.tail.clear()
        player.prev_on_field = player.on_field

    def update_field(self):
        self.move_players()
        self.update_player(self._player1)
        self.update_player(self._player2)
