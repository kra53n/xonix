import config
import utils

import pyxel as px


def center_text(text: str, col: int):
    letter_w = 3
    letter_h = 5
    letter_pd = 1
    w = (letter_w + letter_pd) * len(text) - letter_pd
    x, y = utils.centerize_rect_in_rect(w, letter_h, 0, 0, config.WINDOW_WDT, config.WINDOW_HGT)
    px.text(x, y, text, col)
