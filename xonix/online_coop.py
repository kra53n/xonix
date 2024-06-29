import socket

from collections import deque
from typing import Iterable

import action
import config
from enemy import Enemy


def connect_to_server(host: str, port: int = config.PORT) -> socket.socket:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        return sock


class Client:
    def __init__(self, scenes: deque):
        pass



class Server:
    def __init__(self,
                 scenes: deque,
                 lives: int,
                 lvl: int,
                 enemies: Iterable[Enemy]):
        pass
