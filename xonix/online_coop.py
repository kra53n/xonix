from enum import Enum
import socket
import threading

from collections import deque
from typing import Iterable

import action
import config
from enemy import Enemy
from field import Field
from player import Player, PlayerMoveStatus


class ServerState(Enum):
    pass


class Server:
    def __init__(self,
                 scenes: deque,
                 addr: str,
                 lives: int,
                 lvl: int,
                 enemies: Iterable[Enemy]):
        self.filed = Field()
        self.player1 = self.spawn_player1()
        self.player2 = self.spawn_player2()

    def draw(self):
        # self.field
        pass

    def update(self):
        pass

    def spawn_player1(self) -> Player:
        return Player(self._field.x + self._field.block_size,
                      self._field.y + self._field.block_size * 2,
                      config.PLAYER_COL,
                      config.TAIL_COL,
                      key_type)

    def spawn_player2(self) -> Player:
        return Player(self._field.x + self._field.w * self._field.block_size - self._field.block_size * 2,
                      self._field.y + self._field.block_size * 2,
                      config.TAIL_COL,
                      config.PLAYER_COL,
                      key_type)


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

    def draw(self):
        self.field.draw()
        self.player.draw()

    def update(self):
        self.update_by_local()
        self.update_by_server()

    def update_by_local(self):
        if action.move_player_up():
            self.player.move_status = PlayerMoveStatus.Up
        if action.move_player_down():
            self.player.move_status = PlayerMoveStatus.Down
        if action.move_player_left():
            self.player.move_status = PlayerMoveStatus.Left
        if action.move_player_right():
            self.player.move_status = PlayerMoveStatus.Right

    def update_by_server(self):
        pass

    def connector(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    self.state = ClientState.SENDING_SERVER
                    s.connect((self.addr, config.PORT))
                    s.sendall('(action (player (move {self.player.move_status})))'.encode())
                    self.state = ClientState.WAITING_SERVER
                    data = s.recv(1024).decode()
                    print(data)
            except ConnectionResetError:
                print('yeah')
            except ConnectionRefusedError:
                print('yeah')

    def spawn_player(self) -> Player:
        return Player(self.field.x + self.field.w * self.field.block_size - self.field.block_size * 2,
                      self.field.y + self.field.block_size * 2,
                      config.TAIL_COL,
                      config.PLAYER_COL)
