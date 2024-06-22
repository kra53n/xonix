from collections import deque

import pyxel as px

import action
import config
import utils
from fonts import fonts
from single_game import SingleGame
from offline_coop import OfflineCoop
from online_coop_menu import OnlineCoopMenu
from popup_messages import About
from lvls import get_next_lvl


class MainMenu:
    def __init__(self, scenes: deque):
        self.scenes = scenes

        self.title = 'XoNix'
        self.letter_sz = fonts['inkscript'].letter_sz + 1
        w = self.letter_sz * len(self.title)
        self.x, self.y = utils.centerize_rect_in_rect(
            w, self.letter_sz,
            0, 0,
            config.WINDOW_WDT, config.WINDOW_HGT
        )

        self.options = (
            (lambda: get_next_lvl(SingleGame, self.scenes, lives=3, prev_lvl=-1), 'Play'),
            (lambda: get_next_lvl(OfflineCoop, self.scenes, lives=3, prev_lvl=-1), 'Offline coop'),
            (lambda: OnlineCoopMenu(self.scenes), 'Online coop'),
            (lambda: About(self.scenes), 'About'),
        )
        self.curr_option_idx = 0

    def draw(self):
        px.cls(config.BACKGROUND_COL)
        self._draw_title()
        self._draw_options()
        
    def update(self):
        self._update_options()
        if action.resume():
            scene, _ = self.options[self.curr_option_idx]
            self.scenes.append(scene())

    def _draw_title(self):
        off = abs(px.cos(px.frame_count * 3) * 10)
        y = int(self.y + off)
        y -= 12
        fonts['inkscript'].draw(self.x + 2, y + 2, self.title, config.TEXT2_COL)
        fonts['inkscript'].draw(self.x + 1, y + 1, self.title, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x, y, self.title, config.TEXT1_COL)
        fonts['inkscript'].draw(self.x - 1, y - 1, self.title, config.BACKGROUND_COL)
        fonts['inkscript'].draw(self.x - 2, y - 2, self.title, config.TEXT1_COL)

    def _draw_options(self):
        scene, text = self.options[self.curr_option_idx]
        w = self.letter_sz * len(text)
        x, y = utils.centerize_rect_in_rect(w, self.letter_sz, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)
        y += 24
        fonts['inkscript'].draw(x, y, text, config.TEXT1_COL)

    def _update_options(self):
        if action.move_player_up() or action.move_player_left():
            self.curr_option_idx -= 1
            if self.curr_option_idx < 0:
                self.curr_option_idx = 0
        elif action.move_player_down() or action.move_player_right():
            self.curr_option_idx += 1
            if self.curr_option_idx == len(self.options):
                self.curr_option_idx -= 1
