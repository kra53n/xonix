from collections import deque

import pyxel as px

from game import Game


class App:
    def __init__(self):
        px.init(80, 80, 'Xonix')

        self._scenes = deque()
        self._scenes.append(Game(self._scenes))

        px.run(self._draw, self._update)

    def _draw(self):
        self._scenes[-1].draw()

    def _update(self):
        self._scenes[-1].update()


if __name__ == '__main__':
    App()
