from collections import deque

import pyxel as px

import config
import fonts
import game


class App:
    def __init__(self):
        px.init(config.WINDOW_WDT, config.WINDOW_HGT, config.WINDOW_TITLE)
        fonts.load()

        self._scenes = deque()
        self._scenes.append(game.get_next_lvl(
            scenes=self._scenes,
            lives=3,
            prev_lvl=-1))

        px.run(self._draw, self._update)

    def _draw(self):
        self._scenes[-1].draw()

    def _update(self):
        self._scenes[-1].update()


if __name__ == '__main__':
    App()
