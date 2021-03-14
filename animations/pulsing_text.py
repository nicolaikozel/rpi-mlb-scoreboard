from rgbmatrix import graphics

from animations.base_animations import BaseAnimation
from constants import Font
from graphics.gradient import Gradient


class PulsingTextAnimation(BaseAnimation):
    def __init__(
        self,
        text: str,
        font: graphics.Font,
        gradient: Gradient,
        x_pos: int,
        y_pos: int,
        wait_until_armed: bool = False,
    ):
        super().__init__(wait_until_armed)
        self._text = text
        self._font = font
        self._gradient = gradient
        self._x_pos = x_pos
        self._y_pos = y_pos

    @property
    def finished(self) -> bool:
        return False

    def _reset(self):
        pass

    def _advance_frame(self, canvas):
        self._gradient.advance_color()

    def _render_frame(self, canvas):
        color = self._gradient.get_current_color()
        graphics.DrawText(
            canvas,
            self._font,
            self._x_pos,
            self._y_pos,
            color,
            self._text,
        )
