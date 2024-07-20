from dataclasses import dataclass
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

        self.message = ''
        self.sockets: deque[socket.socket] = deque()

    def process_received(self, data: str):
        print(data)
        data = data.split()
        if not data:
            return
        match data[0]:
            case 'player':
                match data[1]:
                    case 'up':
                        self.player2.move_status = PlayerMoveStatus.Up
                    case 'down':
                        self.player2.move_status = PlayerMoveStatus.Down
                    case 'left':
                        self.player2.move_status = PlayerMoveStatus.Left
                    case 'right':
                        self.player2.move_status = PlayerMoveStatus.Right

    def connector(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.addr, config.PORT))
            except OSError as e:
                print('OSError', e)
                s.close()
                self.connector()
                return
            s.listen(1)
            print('1')
            while True:
                conn, addr = s.accept()
                print('2')
                with conn:
                    print('3')
                    self.process_received(conn.recv(1024).decode())
                    print('4')
                    if not self.message:
                        self.message = '0'
                    conn.sendall(self.message.encode())
                    print('5')
                    self.message = ''
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
            self.message = f'field {self.field._field}'
        player.prev_on_field = player.on_field

    def update_field(self):
        self.move_player(self.player1)
        self.move_player(self.player2)
        self.player1.update()
        # for the player2 updating we should wait for the client message
        self.update_player(self.player1)
        self.update_player(self.player2)
        if not 'field' in self.message:
            self.message = f'players {self.player1.x} {self.player1.y} {self.player2.x} {self.player2.y}'


class ClientState(Enum):
    WAITING_SERVER = 1
    RECIEVED_FROM_SERVER = 2
    SENDING_SERVER = 3


class Client:
    def __init__(self, scenes: deque, addr: str):
        self.scenes = scenes
        self.addr = addr
        self.state = ClientState.WAITING_SERVER
        self.field = Field()
        self.player1 = self.spawn_player1()
        self.player2 = self.spawn_player2()

        t = threading.Thread(target=self.connector)
        t.start()

        self.message = ''

    def connector(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    self.state = ClientState.WAITING_SERVER
                    print(1)
                    s.connect((self.addr, config.PORT))
                    if not self.message:
                        self.message = '0'
                    s.sendall(self.message.encode())
                    print(2)
                    data = ''
                    while (buf := s.recv(1024).decode()):
                        data += buf
                    print('wtf')
                    self.state = ClientState.RECIEVED_FROM_SERVER
                    data_unpack(data, self)
            except ConnectionResetError as e:
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
        self.update_by_local()
        # self.update_by_server()

    def update_by_local(self):
        message = ''
        if action.move_player_up():
            message = f'player up'
        if action.move_player_down():
            message = f'player down'
        if action.move_player_left():
            message = f'player left'
        if action.move_player_right():
            message = f'player right'
        self.message = message

    def update_by_server(self):
        pass

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


def data_pack(s: Server) -> str:
    return str({
        'action': {
            'field': s.field._field,
            'player1': (s.player1.x, s.player1.y),
            'player2': (s.player2.x, s.player2.y),
            'lives': s.lives,
            'lvl': s.lvl,
        },
    })


def data_unpack(data: str, c: Client):
    data = data.split()
    if not data:
        return
    print(data)
    match data[0]:
        case 'players':
            c.player1.x = int(data[1])
            c.player1.y = int(data[2])
            c.player2.x = int(data[3])
            c.player2.y = int(data[4])
            print(c.player1.x, c.player1.y)
    # match data:
    #     case {'action': dict() as action}:
    #         if 'field' in action:
    #             c.field._field = ction['field']
    #         if 'player1' in action:
    #             c.player1.x = action['player1'][0]
    #             c.player1.y = action['player1'][1]
    #         if 'player2' in action:
    #             c.player2.x = action['player2'][0]
    #             c.player2.y = action['player2'][1]
    #             # c.playe1.x 
    # # print(c.field._field)
