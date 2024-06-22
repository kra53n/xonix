from collections import deque

import pyxel as px

import action
import config
import utils

from fonts import fonts
from popup_messages import PopupMessage


CURSOR_DATA = (
    '--',
    ' --',
    '  --',
    ' --',
    '--',
)


class Server(PopupMessage):
    def __init__(self):
        pass


class OnlineCoopMenu(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Online coop')
        self.y = 12

        self.choosed = False
        self.options = 'Wait user', 'Connect'
        self.options_pd = 6
        self.cursor_pos = 0
        self.give_options_pos()

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        self.draw_options()
        if abs(px.sin(px.frame_count * 8)) > 0.7:
            self.draw_cursor()

    def update(self):
        if action.move_player_up():
            self.cursor_pos -= 1
            if self.cursor_pos < 0:
                self.cursor_pos = 0
        if action.move_player_down():
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.options):
                self.cursor_pos = len(self.options) - 1

    def give_options_pos(self):
        self.letter_sz = fonts['inkscript'].letter_sz
        w = (self.letter_sz + 1) * max(map(len, self.options)) - 1
        h = (self.letter_sz + self.options_pd) * len(self.options) - self.options_pd
        self.options_x, self.options_y = utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)

    def draw_options(self):
        y = self.options_y
        for i, option in enumerate(self.options):
            col = config.TEXT2_COL if i == self.cursor_pos else config.TEXT1_COL
            fonts['inkscript'].draw(self.options_x, y, option, col)
            y += self.letter_sz + self.options_pd

    def draw_cursor(self):
        sz = 1
        get_x = lambda: self.options_x - max(map(len, CURSOR_DATA)) - 4
        x = get_x()
        y = self.options_y + (self.letter_sz - len(CURSOR_DATA)) // 2
        y += (self.letter_sz + self.options_pd) * self.cursor_pos
        for j, row in enumerate(CURSOR_DATA):
            for i, v in enumerate(row):
                x += sz
                if v == ' ':
                    continue
                px.rect(x, y, sz, 1, config.PLAYER_COL)
            x = get_x()
            y += 1
