from enum import Enum
import socket
import threading

from collections import deque
from typing import Iterable

import pyxel as px

import action
import config
from bar import Bar
from enemy import Enemy
from fonts import fonts
from field import Field
from player import Player, PlayerMoveStatus
from utils import lispy, unlispy


class ServerState(Enum):
    pass


class Server:
    def __init__(self,
                 scenes: deque,
                 addr: str,
                 lives: int,
                 lvl: int,
                 enemies: Iterable[Enemy]):
        self.scenes = scenes
        self.addr = addr
        self.field = Field()
        self.player1 = self.spawn_player1()
        self.player2 = self.spawn_player2()
        self.enemies = enemies
        self.lives = lives
        self.lvl = lvl
        self.bars = self.spawn_bars()

        t = threading.Thread(target=self.connector)
        t.start()

        self.sockets: deque[socket.socket] = deque()

    def connector(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.addr, config.PORT))
            except OSError:
                s.close()
                self.connector()
                return
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    print(data)
                    conn.sendall(data_pack(self).encode())
            s.close()

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        self.field.draw()
        for enemy in self.enemies:
            enemy.draw()
        self.player1.draw()
        self.player2.draw()
        for bar in self.bars:
            bar.draw()

    def update(self):
        self.player1.update()
        self.update_field()
        for enemy in self.enemies:
            enemy.update(self.field, self.player1.tail)
            enemy.update(self.field, self.player2.tail)

    def spawn_player1(self) -> Player:
        return Player(self.field.x + self.field.block_size,
                      self.field.y + self.field.block_size * 2,
                      config.PLAYER_COL,
                      config.TAIL_COL)

    def spawn_player2(self) -> Player:
        return Player(self.field.x + self.field.w * self.field.block_size - self.field.block_size * 2,
                      self.field.y + self.field.block_size * 2,
                      config.TAIL_COL,
                      config.PLAYER_COL)

    def spawn_bars(self) -> Iterable[Bar]:
        bars = (Bar(2, 0, 'fullness', config.TEXT1_COL, lambda: f'{int(self.field.fullness*100)}%', config.TEXT2_COL),
                Bar(2, 0, 'lives', config.TEXT1_COL, lambda: str(self.lives), config.TEXT2_COL),
                Bar(2, 0, 'lvl', config.TEXT1_COL, lambda: str(self.lvl+1), config.TEXT2_COL))
        letter_sz = fonts['inkscript'].letter_sz
        off = 2
        for i, bar in enumerate(bars):
            bar.y = (off + letter_sz) * i + off
        return bars

    def move_player(self, player: Player):
        player_pos = self.field.obj_relative_pos(player, player.size)
        match player.move_status:
            case PlayerMoveStatus.Stop:
                pass
            case PlayerMoveStatus.Up:
                if player.y == self.field.y:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.up()
            case PlayerMoveStatus.Down:
                if player.y + player.size == self.field.y + self.field.h * self.field.block_size:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.down()
            case PlayerMoveStatus.Left:
                if player.x == self.field.x:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.left()
            case PlayerMoveStatus.Right:
                if player.x + player.size == self.field.x + self.field.w * self.field.block_size:
                    player.move_status = PlayerMoveStatus.Stop
                else:
                    player.right()

    def update_player(self, player: Player):
        player.on_field = self.field.obj_on_field(player,
                                                  player.size)

        if player.prev_on_field == 1:
            player.tail.clear()
        elif player.prev_on_field == 0 and player.on_field == 1:
            player.move_status = PlayerMoveStatus.Stop
            self.field.process_filling(player.tail)
            player.tail.clear()
        player.prev_on_field = player.on_field

    def update_field(self):
        self.move_player(self.player1)
        self.move_player(self.player2)
        self.player1.update()
        # for the player2 updating we should wait for the client message
        self.update_player(self.player1)
        self.update_player(self.player2)


# class ClientState(Enum):
#     SENDING_SERVER = 1
#     WAITING_SERVER = 2
#     RECIEVED_FROM_SERVER = 3


class Client:
    def __init__(self, scenes: deque, addr: str):
        self.scenes = scenes
        self.addr = addr
        # self.state = ClientState.WAITING_SERVER
        self.field: Field | None = None
        self.player1: Player | None = None
        self.player2: Player | None = None

        t = threading.Thread(target=self.connector)
        t.start()

    def connector(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # self.state = ClientState.SENDING_SERVER
                    s.connect((self.addr, config.PORT))
                    s.sendall(f'(wait)'.encode())
                    # self.state = ClientState.WAITING_SERVER
                    data = ''
                    while (buf := s.recv(1024).decode()):
                        data += buf
                    print(data)
            except ConnectionResetError:
                print('ConnectionResetError')
            except ConnectionRefusedError:
                print('ConnectionRefusedError')

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        objs = (self.field, self.player1, self.player2)
        for obj in objs:
            if obj:
                obj.draw()

    def update(self):
        # self.update_by_local()
        # self.update_by_server()
        pass

    def update_by_local(self):
        # if action.move_player_up():
        #     self.player.move_status = PlayerMoveStatus.Up
        # if action.move_player_down():
        #     self.player.move_status = PlayerMoveStatus.Down
        # if action.move_player_left():
        #     self.player.move_status = PlayerMoveStatus.Left
        # if action.move_player_right():
        #     self.player.move_status = PlayerMoveStatus.Right
        pass

    def update_by_server(self):
        pass

    def spawn_player(self) -> Player:
        return Player(self.field.x + self.field.w * self.field.block_size - self.field.block_size * 2,
                      self.field.y + self.field.block_size * 2,
                      config.TAIL_COL,
                      config.PLAYER_COL)


def data_unpack(c: Client):
    pass


def data_pack(s: Server) -> str:
    return lispy({
        'data': {
            'field': s.field._field,
            'player1': (s.player1.x, s.player1.y),
            'player2': (s.player2.x, s.player2.y),
            'lives': s.lives,
            'lvl': s.lvl,
        },
    })
