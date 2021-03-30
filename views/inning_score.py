from rgbmatrix import graphics

from data import Data
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.shapes import draw_diamond, draw_square
from mlb.constants import Base, InningState
from views.base_views import BaseView


class InningScoreView(BaseView):
    _render_delay = 1

    def _render_inning_indicator(self, inning_state: InningState):
        color = Color.YELLOW.value
        if inning_state == InningState.TOP:
            # Arrow
            graphics.DrawLine(self._offscreen_canvas, 25, 2, 25, 2, color)
            graphics.DrawLine(self._offscreen_canvas, 24, 3, 26, 3, color)
            graphics.DrawLine(self._offscreen_canvas, 23, 4, 27, 4, color)
        else:
            # Upside down arrow
            graphics.DrawLine(self._offscreen_canvas, 23, 2, 27, 2, color)
            graphics.DrawLine(self._offscreen_canvas, 24, 3, 26, 3, color)
            graphics.DrawLine(self._offscreen_canvas, 25, 4, 25, 4, color)

    def _render_inning(self, inning: int, inning_state: InningState):
        color = Color.YELLOW.value
        self._render_inning_indicator(inning_state=inning_state)
        font, _ = Font.get_font(FontStyle.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            29,
            5,
            color,
            str(inning),
        )

    def _render_base_runners(
        self, runner_on_1b: bool, runner_on_2b: bool, runner_on_3b: bool
    ):
        color = Color.YELLOW.value
        draw_diamond(
            canvas=self._offscreen_canvas,
            x_pos=16,
            y_pos=8,
            size=7,
            color=color,
            outline_only=not runner_on_3b,
        )
        draw_diamond(
            canvas=self._offscreen_canvas,
            x_pos=21,
            y_pos=4,
            size=7,
            color=color,
            outline_only=not runner_on_2b,
        )
        draw_diamond(
            canvas=self._offscreen_canvas,
            x_pos=26,
            y_pos=8,
            size=7,
            color=color,
            outline_only=not runner_on_1b,
        )

    def _render_outs(self, outs: int):
        color = Color.YELLOW.value
        draw_square(
            canvas=self._offscreen_canvas,
            x_pos=1,
            y_pos=10,
            size=3,
            color=color,
            outline_only=outs < 1,
        )
        draw_square(
            canvas=self._offscreen_canvas,
            x_pos=5,
            y_pos=10,
            size=3,
            color=color,
            outline_only=outs < 2,
        )
        draw_square(
            canvas=self._offscreen_canvas,
            x_pos=9,
            y_pos=10,
            size=3,
            color=color,
            outline_only=outs < 3,
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
        if current_game:
            self._render_pitch_count(pitch_count=current_game.formatted_pitch_count)
            self._render_outs(outs=current_game.overview.outs)
            self._render_base_runners(
                runner_on_1b=current_game.is_runner_on_base(base=Base.FIRST),
                runner_on_2b=current_game.is_runner_on_base(base=Base.SECOND),
                runner_on_3b=current_game.is_runner_on_base(base=Base.THIRD),
            )
            inning, inning_state = current_game.inning_and_state
            self._render_inning(inning=inning, inning_state=inning_state)
