from collections import deque
from typing import Iterable

import pyxel as px

import action
import config
import utils

from fonts import fonts
from popup_messages import PopupMessage


class Server(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Waiting user')
        self.y = 12
        self.addrs = self.get_addrs()
        self.cursor_pos = 0

        self.letter_w = 3
        self.letter_h = 5
        self.addr_x, self.addr_y = self.get_addr_pos()
        self.addr_pd = 12

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        px.text(self.addr_x, self.addr_y, self.addrs[self.cursor_pos], config.TEXT2_COL)
        if self.cursor_pos > 0:
            px.text(
                self.addr_x + self.addr_pd // 2,
                self.addr_y - self.addr_pd, self.addrs[self.cursor_pos-1], config.TEXT1_COL)
        if self.cursor_pos < len(self.addrs):
            px.text(
                self.addr_x + self.addr_pd // 2,
                self.addr_y + self.addr_pd, self.addrs[self.cursor_pos+1], config.TEXT1_COL)
        if utils.flicker(0.7):
            utils.draw_selection_cursor(
                self.addr_x - 8,
                self.addr_y - (self.letter_h - len(config.SELECTION_CURSOR_DATA)) // 2,
                1)

    def update(self):
        if action.move_player_up():
            self.cursor_pos -= 1
            if self.cursor_pos < 0:
                self.cursor_pos = 0
        if action.move_player_down():
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.addrs):
                self.cursor_pos = len(self.addrs) - 1
        if action.resume():
            pass

    def get_addrs(self) -> Iterable[str]:
        return ['192.168.103.' + str(i) for i in range(100, 256)]

    def get_addr_pos(self) -> (int, int):
        w = (self.letter_w + 1) * len('192.168.101.101') - 1
        return utils.centerize_rect_in_rect(
            w, self.letter_h,
            0, 0,
            config.WINDOW_WDT, config.WINDOW_HGT)


class OnlineCoopMenu(PopupMessage):
    def __init__(self, scenes: deque):
        super().__init__(scenes, 'Online coop')
        self.y = 12

        self.choosed = False
        self.options = (
            ('Wait user', lambda: self._scenes.append(Server(self._scenes))),
            ('Connect', lambda: print('connection menu')),
        )
        self.option_names = tuple(i[0] for i in self.options)
        self.options_pd = 6
        self.cursor_pos = 0
        self.options_x, self.options_y = self.get_options_pos()

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        super().draw()
        self.draw_options()
        if utils.flicker(0.7):
            utils.draw_selection_cursor(
                self.options_x - max(map(len, config.SELECTION_CURSOR_DATA)) - 4,
                self.options_y + (self.letter_sz - len(config.SELECTION_CURSOR_DATA)) // 2 + (self.letter_sz + self.options_pd) * self.cursor_pos,
                1)

    def update(self):
        if action.move_player_up():
            self.cursor_pos -= 1
            if self.cursor_pos < 0:
                self.cursor_pos = 0
        if action.move_player_down():
            self.cursor_pos += 1
            if self.cursor_pos >= len(self.options):
                self.cursor_pos = len(self.options) - 1
        if action.resume():
            actn = self.options[self.cursor_pos][1]
            actn()

    def get_options_pos(self) -> (int, int):
        self.letter_sz = fonts['inkscript'].letter_sz
        w = (self.letter_sz + 1) * max(map(len, self.option_names)) - 1
        h = (self.letter_sz + self.options_pd) * len(self.option_names) - self.options_pd
        return utils.centerize_rect_in_rect(w, h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)

    def draw_options(self):
        y = self.options_y
        for i, option_name in enumerate(self.option_names):
            col = config.TEXT2_COL if i == self.cursor_pos else config.TEXT1_COL
            fonts['inkscript'].draw(self.options_x, y, option_name, col)
            y += self.letter_sz + self.options_pd
