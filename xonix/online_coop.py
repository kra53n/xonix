import socket

from collections import deque
from typing import Iterable

import action
import config
from enemy import Enemy


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
