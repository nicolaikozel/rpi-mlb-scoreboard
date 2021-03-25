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

    def _render_inning_indicator(self, inning_state: InningState):
        color = Color.YELLOW.value
        if inning_state == InningState.TOP:
            # Arrow
            graphics.DrawLine(self._offscreen_canvas, 24, 2, 24, 2, color)
            graphics.DrawLine(self._offscreen_canvas, 23, 3, 25, 3, color)
            graphics.DrawLine(self._offscreen_canvas, 22, 4, 26, 4, color)
        else:
            # Upside down arrow
            graphics.DrawLine(self._offscreen_canvas, 22, 2, 26, 2, color)
            graphics.DrawLine(self._offscreen_canvas, 23, 3, 25, 3, color)
            graphics.DrawLine(self._offscreen_canvas, 24, 4, 24, 4, color)

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

    def _render_base_runners(
        self, runner_on_1b: bool, runner_on_2b: bool, runner_on_3b: bool
    ):
        pass

    def _render_outs(self, outs: int):
        color = Color.YELLOW.value
        graphics.DrawCircle(
            self._offscreen_canvas,
            2,
            10,
            1,
            color,
        )
        graphics.DrawCircle(
            self._offscreen_canvas,
            6,
            10,
            1,
            color,
        )
        graphics.DrawCircle(
            self._offscreen_canvas,
            10,
            10,
            1,
            color,
        )

    def _render_pitch_count(self, pitch_count: str):
        font, _ = Font.get_font(FontStyle.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            1,
            8,
            Color.YELLOW.value,
            pitch_count,
        )

    def _render(self):
        current_game = Data.get("current_game")
        # if current_game:
        #    self._render_pitch_count(current_game.pitch_count)
        #    self._render_outs(outs=current_game.outs)
        #    self._render_base_runners(
        #        runner_on_1b=,
        #        runner_on_2b=,
        #        runner_on_3b=,
        #    )
        #    inning, inning_state = current_game.inning_and_state
        #    self._render_inning(inning=inning, inning_state=inning_state)
        self._render_pitch_count("1-2")
        self._render_outs(outs=1)
        self._render_base_runners(True, False, False)
        self._render_inning(inning=3, inning_state=InningState.TOP)
