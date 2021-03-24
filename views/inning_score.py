from datetime import datetime
from PIL import Image
from typing import Dict

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from data import Data
from graphics.constants import Color
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
        if inning_state == InningState.TOP:
            # Arrow
            graphics.DrawLine(canvas, 25, 5, 25, 5, Color.YELLOW.value)
            graphics.DrawLine(canvas, 24, 5, 26, 5, Color.YELLOW.value)
            graphics.DrawLine(canvas, 23, 5, 27, 5, Color.YELLOW.value)
        else:
            # Upside down arrow
            graphics.DrawLine(canvas, 23, 5, 27, 5, Color.YELLOW.value)
            graphics.DrawLine(canvas, 24, 5, 26, 5, Color.YELLOW.value)
            graphics.DrawLine(canvas, 25, 5, 25, 5, Color.YELLOW.value)

    def _render_inning(self, inning: int, inning_state: InningState):
        self._render_inning_indicator()
        font, font_size = Font.get_font(FontStyle.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            28,
            5,
            Color.YELLOW.value,
            inning,
        )

    def _render(self):
        current_game = Data.get("current_game")
        if current_game:
            self._render_pitch_count(current_game.pitch_count)
            inning, inning_state = current_game.inning_and_state
            self._render_inning(inning=inning, inning_state=inning_state)
