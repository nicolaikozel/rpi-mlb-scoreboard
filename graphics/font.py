import os
from typing import Dict, Optional, Tuple

from enum import Enum

from rgbmatrix import graphics

from utils import get_abs_file_path


class FontStyle(Enum):
    TINY = "tom-thumb"
    SMALL = "5x7"
    MEDIUM = "6x10"
    LARGE = "6x12"


class Font:
    _font_cache = {}

    @classmethod
    def get_font(cls, font_style: FontStyle) -> Tuple[graphics.Font, Optional[Dict]]:
        font_name = font_style.value
        if font_name in cls._font_cache:
            return cls._font_cache[font_name]

        font_paths = ["rpi-rgb-led-matrix/fonts"]
        for font_path in font_paths:
            path = get_abs_file_path(f"{font_path}/{font_name}.bdf")
            if os.path.isfile(path):
                font = graphics.Font()
                font.LoadFont(path)
                size = None
                if font_name.startswith("tom"):
                    size = dict(width=4, height=6)
                else:
                    dimensions = font_name.split("x", 1)
                    if len(dimensions) == 2:
                        size = dict(width=int(dimensions[0]), height=int(dimensions[1]))
                ret = (font, size)
                cls._font_cache[font_name] = ret
                return ret

        raise ValueError(f"Could not find a font for {font_name}!")
