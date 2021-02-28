import time
import os
from abc import ABC, abstractmethod

from rgbmatrix import graphics

from common.threading import StoppableThread
from constants import Font
from utils import get_abs_file_path


class BaseView(StoppableThread, ABC):
    _font_cache = {}
    _default_font_name = Font.SMALL
    _render_delay = 1

    def __init__(self, rgb_matrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix

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
    def _render(self):
        pass

    def run(self):
        while True:
            self._render()
            time.sleep(self._render_delay)
            if self.stopped:
                break


class RestartableView:
    def __init__(self, view, *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        self._view = view
        self.reset()

    def is_alive(self):
        return self._instance.is_alive()

    def reset(self):
        self._instance = self._view(*self._args, **self._kwargs)

    def start(self):
        self._instance.start()
    
    def join(self):
        self._instance.join()
    
    def stop(self):
        self._instance.stop()