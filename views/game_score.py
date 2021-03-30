from rgbmatrix import graphics, RGBMatrix

from data import Data
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.shapes import draw_diamond, draw_square
from mlb.constants import TEAM_ABBREVIATIONS, TEAM_COLORS
from views.base_views import BaseView


class GameScoreView(BaseView):
    _render_delay = 1

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._font, self._font_size = Font.get_font(FontStyle.SMALL)

    def _render_team_name_and_runs(self, team_name: str, runs: int, x_pos: int, y_pos: int):
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            x_pos,
            y_pos,
            Color.RED.value,
            TEAM_ABBREVIATIONS[team_name],
        )
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            x_pos+20,
            y_pos,
            Color.BLUE.value,
            str(runs),
        )

    def _render(self):
        current_game = Data.get("current_game")
        if current_game:
            self._render_team_name_and_runs(
                team_name=current_game.overview.home_team_name,
                runs=current_game.overview.home_team_runs,
                x_pos=1,
                y_pos=7,
            )
            self._render_team_name_and_runs(
                team_name=current_game.overview.away_team_name,
                runs=current_game.overview.away_team_runs,
                x_pos=1,
                y_pos=15,
            )
