from rgbmatrix import graphics

from animations.base_animations import BaseAnimation
from constants import Direction
from graphics.gradient import Gradient


class OutlineCanvasAnimation(BaseAnimation):
    def __init__(
        self,
        wait_until_armed: bool = False,
        max_cycles: int = None,
        color: graphics.Color = None,
        gradient: Gradient = Gradient.generate_repeating_gradient(steps=6),
        length: int = 3,
    ):
        super().__init__(wait_until_armed)
        self._completed_cycles = 0
        self._max_cycles = max_cycles
        self._color = color
        self._gradient = gradient
        self._gradient_index = 0
        self._length = 3
        self._x1 = 0
        self._x2 = self._x1 + self._length
        self._y1 = 0
        self._y2 = 0
        self._direction = Direction.RIGHT

    @property
    def finished(self) -> bool:
        return self._completed_cycles == self._max_cycles

    def _reset(self):
        self._completed_cycles = 0

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
                if self._max_cycles:
                    self._completed_cycles += 1

    def _render_frame(self, canvas):
        if not self._color:
            color = self._gradient.get_current_color(advance=True)
        else:
            color = self._color.value
        graphics.DrawLine(canvas, self._x1, self._y1, self._x2, self._y2, color)
