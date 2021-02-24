import math

from rgbmatrix import graphics


class Gradient:
    def __init__(self, colors):
        self._colors = colors
        self._index = 0

    def advance_color(self):
        if self._index < len(self._colors) - 1:
            self._index += 1 
        else:
            self._index = 0

    def get_current_color(self, advance=False):
        color = self._colors[self._index]
        if advance:
            self.advance_color()
        return color


def generate_gradient(freq1, freq2, freq3, phase1, phase2, phase3, center=128, width=127, len=50):
    colors = []
    for i in range(len):
        red = math.sin(freq1*i + phase1) * width + center
        green = math.sin(freq2*i + phase2) * width + center
        blue = math.sin(freq3*i + phase3) * width + center
        colors.append(graphics.Color(red, green, blue))
    return Gradient(colors=colors)


def generate_repeating_gradient(steps):
    freq = 2*math.pi / steps
    return generate_gradient(freq1=freq, freq2=freq, freq3=freq, phase1=0, phase2=2, phase3=4)