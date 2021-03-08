import time
import os
from typing import Dict, Optional, Tuple
from abc import ABC, abstractmethod

from rgbmatrix import graphics, RGBMatrix

from common.threading import StoppableThread
from constants import Font
from utils import get_abs_file_path


class BaseView(StoppableThread, ABC):
    _font_cache = {}
    _default_font_name = Font.SMALL
    _render_delay = 1

    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

    def _get_font(self, font_name: Font = None) -> Tuple[graphics.Font, Optional[Dict]]:
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
                size = None
                if font_name.startswith("tom"):
                    size = dict(width=4, height=6)
                else:
                    dimensions = font_name.split("x", 1)
                    if len(dimensions) == 2:
                        size = dict(width=int(dimensions[0]), height=int(dimensions[1]))
                ret = (font, size)
                self._font_cache[font_name] = ret
                return ret

    @abstractmethod
    def _render(self):
        pass

    def run(self):
        while True:
            self._offscreen_canvas.Clear()
            self._render()
            self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                self._offscreen_canvas
            )
            time.sleep(self._render_delay)
            if self.stopped:
                break
