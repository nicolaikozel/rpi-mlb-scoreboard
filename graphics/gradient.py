import math
from typing import List

from rgbmatrix import graphics


class Gradient:
    def __init__(self, colors: List[graphics.Color]):
        self._colors = colors
        self._index = 0

    def advance_color(self) -> bool:
        """
        Returns whether the gradient was reset
        as a result of advancing the color
        """
        if self._index < len(self._colors) - 1:
            self._index += 1
            return False
        else:
            self._index = 0
            return True

    def get_current_color(self, advance=False) -> graphics.Color:
        color = self._colors[self._index]
        if advance:
            self.advance_color()
        return color

    @classmethod
    def generate_gradient(
        cls,
        freq1: float,
        freq2: float,
        freq3: float,
        phase1: int,
        phase2: int,
        phase3: int,
        center: int = 128,
        width: int = 127,
        len: int = 50,
    ):
        colors = []
        for i in range(len):
            red = math.sin(freq1 * i + phase1) * width + center
            green = math.sin(freq2 * i + phase2) * width + center
            blue = math.sin(freq3 * i + phase3) * width + center
            colors.append(graphics.Color(red, green, blue))
        return cls(colors=colors)

    @classmethod
    def generate_repeating_gradient(cls, steps: int):
        freq = 2 * math.pi / steps
        return cls.generate_gradient(
            freq1=freq, freq2=freq, freq3=freq, phase1=0, phase2=2, phase3=4
        )

    @classmethod
    def generate_brightness_gradient(
        cls, color: graphics.Color, percentages=[0.25, 0.5, 1]
    ):
        colors = []
        r = color.red
        g = color.green
        b = color.blue
        for percent in sorted(percentages):
            colors.append(graphics.Color(r * percent, g * percent, b * percent))
        return cls(colors=colors)
