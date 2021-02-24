from enum import Enum

from rgbmatrix import graphics


class Color(Enum):
    RED = graphics.Color(255, 0 , 0)
    GREEN = graphics.Color(0, 255, 0)
    BLUE = graphics.Color(0, 0, 255)


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