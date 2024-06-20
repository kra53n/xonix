from collections import deque
from random import randrange

import config
from enemy import Enemy


def get_next_lvl(game_class, scenes: deque, lives: int, prev_lvl: int, **kw):
    """
    game_class: OfflineCoop, OnlineCoop
    """
    lvl = prev_lvl + 1
    common = {'scenes': scenes, 'lives': lives, 'lvl': lvl} | kw
    x_enemy = lambda: randrange(config.BORDER_THICKNESS, config.FIELD_WDT, config.BLOCK_SIZE)
    y_enemy = lambda: randrange(config.FIELD_Y_OFF + config.BORDER_THICKNESS, config.FIELD_HGT, config.BLOCK_SIZE)
    lvls = [
        lambda: game_class(
            **common,
            enemies=(Enemy(x_enemy(), y_enemy(), min_delay=12, max_delay=12),)
        ),
        lambda: game_class(
            **common,
            enemies=(
                Enemy(x_enemy(), y_enemy(), min_delay=10, max_delay=10),
                Enemy(x_enemy(), y_enemy(), min_delay=10, max_delay=10),
            )
        ),
    ]
    # NOTE: level generation was not written in the proper way, after
    # implementing othe stuff may be possible to rewrite it
    for i in range(3, 20):
        lvls.append(lambda i=i: game_class(
            **common,
            enemies=tuple(Enemy(x_enemy(), y_enemy(), min_delay=1, max_delay=randrange(1, 11))
                          for _ in range(i)),
        ))
    game = lvls[lvl] if lvl < len(lvls) else lvls[-1]
    return game()
