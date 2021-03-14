from enum import Enum

from rgbmatrix import graphics


class Color(Enum):
    BJ_PRIMARY = graphics.Color(19, 74, 142)
    BJ_SECONDARY = graphics.Color(29,45,92)
    BJ_TERTIARY = graphics.Color(218,41,28)
    BLUE = graphics.Color(0, 0, 255)
    GREEN = graphics.Color(0, 255, 0)
    RED = graphics.Color(255, 0, 0)
    WHITE = graphics.Color(255, 255, 255)


class Font(Enum):
    TINY = "tom-thumb"
    SMALL = "5x7"
    MEDIUM = "6x10"
    LARGE = "6x12"


class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4
