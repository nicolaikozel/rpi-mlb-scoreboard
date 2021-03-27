from enum import Enum

from rgbmatrix import graphics


class Color(Enum):
    RED = graphics.Color(255, 0, 0)
    GREEN = graphics.Color(0, 255, 0)
    BLUE = graphics.Color(0, 0, 255)
    YELLOW = graphics.Color(255, 255, 0)
