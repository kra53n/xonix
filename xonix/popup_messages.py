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
        w = (letter_sz + 1) * len(self._message) - 1
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



class GetPlayersInput(PopupMessage):
    """
    Define players input for offline coop
    """
    def __init__(self, scenes: deque):
        self.scenes = scenes

        self.possible_keys = {
            (px.KEY_W, px.KEY_A, px.KEY_S, px.KEY_D): 'wasd',
            (px.KEY_UP, px.KEY_LEFT, px.KEY_DOWN, px.KEY_RIGHT): 'arrows',
            (px.GAMEPAD1_BUTTON_DPAD_UP, px.GAMEPAD1_BUTTON_DPAD_LEFT, px.GAMEPAD1_BUTTON_DPAD_DOWN, px.GAMEPAD1_BUTTON_DPAD_RIGHT): 'gamepad',
        }
        self.player1: tuple | None = None
        self.player2: tuple | None = None
        self.curr_keys: tuple | None = None
        self.keys_r_busy: bool = False

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        self.draw_title()
        self.draw_info_bar()

    def update(self):
        for keys in self.possible_keys.keys():
            for key in keys:
                if px.btnp(key):
                    self.curr_keys = keys
                    self.keys_r_busy = False
                    break

        if action.resume() and self.curr_keys and self.player1 is None:
            self.player1 = self.curr_keys
            self.curr_keys = None
        elif action.resume() and self.curr_keys:
            if self.player1 == self.curr_keys:
                self.keys_r_busy = True
                return
            self.player2 = self.curr_keys
            self.finish()

    def finish(self):
        self.scenes.pop()
        offline_coop = self.scenes[-1]
        offline_coop.player1_keys = self.player1
        offline_coop.player2_keys = self.player2

    def draw_title(self):
        msg = self._get_title()
        w = len(msg) * 4 - 1
        h = 15
        x, y = utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)
        px.text(x, y, msg, config.TEXT1_COL)

    def draw_info_bar(self):
        msg = ('Non selected'
               if self.curr_keys is None
               else 'Keys already was selected'
               if self.keys_r_busy
               else self.possible_keys[self.curr_keys])
        w = len(msg) * 4 - 1
        h = 15
        x, y = utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)
        y += 8
        px.text(x, y, msg, config.TEXT2_COL)

    def _get_title(self) -> str:
        return 'Select keys for player' + ('2' if self.player1 else '1')
