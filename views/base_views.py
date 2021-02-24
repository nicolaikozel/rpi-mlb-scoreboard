import time
import os
from abc import ABC, abstractmethod

from rgbmatrix import graphics

from constants import Font
from utils import get_abs_file_path


class BaseView(ABC):
    _font_cache = {}
    _default_font_name = Font.SMALL

    def __init__(self, rgb_matrix):
        self._rgb_matrix = rgb_matrix

    def _sleep(self, value):
        time.sleep(value)

    def _get_font(self, font_name=None):
        if not font_name:
            font_name = self._default_font_name

        font_name = font_name.value

        if font_name in self._font_cache:
            return self._font_cache[font_name]

        font_paths = ["rpi-rgb-led-matrix/fonts"]
        for font_path in font_paths:
            path = get_abs_file_path(f"{font_path}/{font_name}.bdf")
            if os.path.isfile(path):
                font = graphics.Font()
                font.LoadFont(path)
                dimensions = font_name.split("x", 1)
                size = None
                if len(dimensions) == 2:
                    size = dict(width=int(dimensions[0]), height=int(dimensions[1]))
                ret = (font, size)
                self._font_cache[font_name] = ret
                return ret

    @abstractmethod
    def render(self):
        pass
