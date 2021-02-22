from enum import Enum

from rgbmatrix import graphics


class Color(Enum):
    RED = graphics.Color(255, 0 , 0)


class Font(Enum):
    MEDIUM = "6x9"