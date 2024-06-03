from collections import deque

import pyxel as px

import action
import config
import utils
import single_game
from fonts import fonts


class PopupMessage:
    def __init__(self, scenes: deque, message: str):
        self._scenes = scenes
        self._message = message
        letter_sz = fonts['inkscript'].letter_sz
        w = letter_sz * len(self._message)
        h = letter_sz
        self.x, self.y = utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)

    def draw(self):
        fonts['inkscript'].draw(self.x + 2, self.y + 2, self._message, config.TEXT2_COL)
        fonts['inkscript'].draw(self.x + 1, self.y + 1, self._message, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x, self.y, self._message, config.TEXT1_COL)
        fonts['inkscript'].draw(self.x - 1, self.y - 1, self._message, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x - 2, self.y - 2, self._message, config.TEXT1_COL)

    def update(self):
        pass


class GameOverMessage(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'GameOver')

    def update(self):
        super().update()

        if px.btnp(px.KEY_ESCAPE):
            while len(self._scenes) != 1:
                self._scenes.pop()

        if px.btnp(px.KEY_R):
            self._scenes.pop()
            scene = self._scenes.pop()
            match type(scene):
                case single_game.SingleGame:
                    self._scenes.append(single_game.get_next_lvl(
                        self._scenes,
                        3,
                        -1,
                    ))


class WinMessage(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, '=Win=')

    def update(self):
        super().update()
        if action.resume():
            self._scenes.pop()

        if px.btnp(px.KEY_ESCAPE):
            self._scenes.pop()
            self._scenes.pop()
            self._scenes.pop()


class About:
    def __init__(self, scenes: deque):
        self.scenes = scenes

    def update(self):
        if px.btnp(px.KEY_ESCAPE) or action.resume():
            while len(self.scenes) != 1:
                self.scenes.pop()


    def draw(self):
        px.cls(config.BACKGROUND_COL)
        px.text(
            0, 0,
            '''




    Hello everyone! I create
    this clone game because it
    is not possible to find
    normal Xonix game. I am
    going to implement offline
    coop for this game and try
    to make online coop.
    Have fun!
        kra53n
            ''',
            config.TEXT1_COL,
        )
