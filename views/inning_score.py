from datetime import datetime
from PIL import Image
from typing import Dict

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from data import Data
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.utils import center_object
from mlb.constants import InningState
from utils import get_abs_file_path
from views.base_views import BaseView


class InningScoreView(BaseView):
    _render_delay = 1

    def _render_pitch_count(self, pitch_count: str):
        font, font_size = Font.get_font(FontStyle.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            1,
            8,
            Color.YELLOW.value,
            pitch_count,
        )

    def _render_inning_indicator(self, inning_state: InningState):
        color = Color.YELLOW.value
        if inning_state == InningState.TOP:
            # Arrow
            graphics.DrawLine(self._offscreen_canvas, 25, 5, 25, 5, color)
            graphics.DrawLine(self._offscreen_canvas, 24, 6, 26, 6, color)
            graphics.DrawLine(self._offscreen_canvas, 23, 7, 27, 7, color)
        else:
            # Upside down arrow
            graphics.DrawLine(self._offscreen_canvas, 23, 5, 27, 5, color)
            graphics.DrawLine(self._offscreen_canvas, 24, 6, 26, 6, color)
            graphics.DrawLine(self._offscreen_canvas, 25, 7, 25, 7, color)

    def _render_inning(self, inning: int, inning_state: InningState):
        color = Color.YELLOW.value
        self._render_inning_indicator(inning_state=inning_state)
        font, _ = Font.get_font(FontStyle.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            28,
            5,
            color,
            str(inning),
        )

    def _render(self):
        current_game = Data.get("current_game")
        if current_game:
            self._render_pitch_count(current_game.pitch_count)
            inning, inning_state = current_game.inning_and_state
            self._render_inning(inning=inning, inning_state=inning_state)
