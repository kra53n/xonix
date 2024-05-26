from collections import deque

import pyxel as px


class PopupMessage:
    def __init__(self, scenes: deque, message: str):
        self._scenes = scenes
        self._message = message

    def draw(self):
        px.text(0, 0, self._message, 5)

    def update(self):
        pass


class GameOverMessage(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Game over')

    def update(self):
        super().update()
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.clear()
        if px.btnp(px.KEY_R):
            self._scenes.pop()
            self._scenes.pop()


class WinMessage(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Win')

    def update(self):
        super().update()
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.clear()
        if px.btnp(px.KEY_R):
            self._scenes.pop()
            self._scenes.pop()
