from collections import deque

import pyxel as px

import config
import fonts
import single_game
import colorschemes
from main_menu import MainMenu


class App:
    def __init__(self):
        px.init(config.WINDOW_WDT, config.WINDOW_HGT, config.WINDOW_TITLE, quit_key=False)
        fonts.load()
        colorschemes.set()

        self._scenes = deque()
        self._scenes.append(MainMenu(self._scenes))

        px.run(self._draw, self._update)

    def _draw(self):
        self._scenes[-1].draw()

    def _update(self):
        self._scenes[-1].update()


if __name__ == '__main__':
    App()
