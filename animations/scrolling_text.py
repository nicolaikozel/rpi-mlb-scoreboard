from typing import Dict

from rgbmatrix import graphics

from animations.base_animations import BaseAnimation
from constants import Direction, Font


class ScrollingTextAnimation(BaseAnimation):
    def __init__(
        self,
        text: str,
        font: graphics.Font,
        font_size: Dict,
        starting_x_pos: int,
        starting_y_pos: int,
        color: graphics.Color = None,
        wait_until_armed: bool = False,
    ):
        super().__init__(wait_until_armed)
        self._text = text
        self._font = font
        self._font_size = font_size
        self._color = color
        self._starting_x_pos = starting_x_pos
        self._starting_y_pos = starting_y_pos
        self._x_pos = self._starting_x_pos
        self._y_pos = self._starting_y_pos
        self._direction = Direction.LEFT

    @property
    def finished(self) -> bool:
        return False

    def _reset(self):
        self._x_pos = self._starting_x_pos
        self._y_pos = self._starting_y_pos

    def _advance_frame(self, canvas):
        if self._direction == Direction.LEFT:
            self._x_pos -= 1
            if self._x_pos < -(len(self._text)*self._font_size["width"]):
                self._reset()

    def _render_frame(self, canvas):
        graphics.DrawText(
            canvas,
            self._font,
            self._x_pos,
            self._y_pos,
            self._color.value,
            self._text,
        )
