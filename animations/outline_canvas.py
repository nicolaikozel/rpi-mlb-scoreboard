from rgbmatrix import graphics

from animations.base_animations import BaseAnimation
from constants import Direction
from graphics.gradient import generate_repeating_gradient


class OutlineCanvasAnimation(BaseAnimation):
    def __init__(self, color=None, gradient=None, length=3):
        self._color = color
        if not gradient:
            gradient = generate_repeating_gradient(steps=6)
        self._gradient = gradient
        self._gradient_index = 0
        self._length = 3
        self._x1 = 0
        self._x2 = self._x1 + self._length
        self._y1 = 0
        self._y2 = 0
        self._direction = Direction.RIGHT

    def _advance_frame(self, canvas):
        if self._direction == Direction.RIGHT:
            if self._x2 + 1 < canvas.width:
                self._x1 = self._x2 + 1
                self._x2 += self._length + 1
            else:
                self._x1 = self._x2 = canvas.width - 1
                self._y2 += self._length
                self._direction = Direction.DOWN
        elif self._direction == Direction.DOWN:
            if self._y2 + 1 < canvas.height:
                self._y1 = self._y2 + 1
                self._y2 += self._length + 1
            else:
                self._y1 = self._y2 = canvas.height - 1
                self._x2 -= self._length
                self._direction = Direction.LEFT
        elif self._direction == Direction.LEFT:
            if self._x2 - 1 > 0:
                self._x1 = self._x2 - 1
                self._x2 -= self._length + 1 
            else:
                self._x1 = self._x2 = 0
                self._y2 -= self._length
                self._direction = Direction.UP
        elif self._direction == Direction.UP:
            if self._y2 - 1 > 0:
                self._y1 = self._y2 - 1
                self._y2 -= self._length + 1
            else:
                self._y1 = self._y2 = 0
                self._x2 += self._length
                self._direction = Direction.RIGHT

    def _render_frame(self, canvas):
        if not self._color:
            color = self._gradient.get_current_color(advance=True)
        else:
            color = self._color.value
        graphics.DrawLine(canvas, self._x1, self._y1, self._x2, self._y2, color)