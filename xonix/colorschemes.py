import pyxel as px

import config


palletes = (
    {
        config.BACKGROUND_COL: 0x282d3c,
        config.FIELD_COL: 0x5b5d70,
        config.PLAYER_COL: 0xf69197,
        config.TAIL_COL: 0xffc4b8,
        config.ENEMY_COL: 0xffc4b8,
        config.TEXT1_COL: 0xffc4b8,
        config.TEXT2_COL: 0xf69197,
    },
    {
        config.BACKGROUND_COL: 0x382637,
        config.FIELD_COL: 0x782f51,
        config.PLAYER_COL: 0xdea257,
        config.TAIL_COL: 0xc33149,
        config.ENEMY_COL: 0xc33149,
        config.TEXT1_COL: 0xc33149,
        config.TEXT2_COL: 0xdea257,
    },
)

def set(idx: int | None = None):
    if idx is None:
        idx = 0
    for i, col in palletes[idx].items():
        px.colors[i] = col
