from datetime import datetime
from PIL import Image
from typing import Dict

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.common import center_object
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.data_classes import WeatherCondition


class InningScoreboardView(BaseView):
    _render_delay = 0.05

    def _render_pitch_count(self):
        pitch_count_string = f""
        font, font_size = self._get_font(Font.TINY)
        graphics.DrawText(
            self._offscreen_canvas, font, 1, 8, Color.YELLOW.value, pitch_count_string,
        )

    def _render(self):
        current_game = Data.get("current_game")
        if current_game:
            self._render_pitch_count()
