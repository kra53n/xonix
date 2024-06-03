from collections import deque

import pyxel as px

import config
import utils
from fonts import fonts


class PopupMessage:
    def __init__(self, scenes: deque, message: str):
        self._scenes = scenes
        self._message = message

    def draw(self):
        fonts['inkscript'].draw(0, 0, self._message, 0)

    def update(self):
        pass


class GameOverMessage(PopupMessage):
    def __init__(self, scenes: deque):
        self._scenes = scenes
        self._message = 'GameOver'
        letter_sz = fonts['inkscript'].letter_sz
        w = letter_sz * len(self._message)
        h = letter_sz
        self.x, self.y = utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)

    def update(self):
        super().update()
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.clear()
        if px.btnp(px.KEY_R):
            self._scenes.pop()
            self._scenes.pop()

    def draw(self):
        fonts['inkscript'].draw(self.x + 2, self.y + 2, self._message, config.TEXT2_COL)
        fonts['inkscript'].draw(self.x + 1, self.y + 1, self._message, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x, self.y, self._message, config.TEXT1_COL)
        fonts['inkscript'].draw(self.x - 1, self.y - 1, self._message, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x - 2, self.y - 2, self._message, config.TEXT1_COL)



class WinMessage(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Win')

    def update(self):
        super().update()
        if px.btnp(px.KEY_ESCAPE):
            self._scenes.clear()
        if px.btnp(px.KEY_R):
            self._scenes.pop()
