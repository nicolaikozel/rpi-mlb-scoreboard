from rgbmatrix import graphics, RGBMatrix

from data import Data
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.shapes import draw_diamond, draw_square
from mlb.constants import TEAM_ABBREVIATIONS, TEAM_COLORS
from views.base_views import BaseView


class GameScoreView(BaseView):
    _render_delay = 5

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._font, self._font_size = Font.get_font(FontStyle.SMALL)

    def _render_score_for_team(
        self, team_name: str, runs: int, x_pos: int, y_pos: int, height: int, width: int
    ):
        team_colors = TEAM_COLORS[team_name]

        # Draw background
        accent_color_rgb = team_colors.get("accent", {"r": 0, "g": 0, "b": 0})
        for i in range(x_pos, width):
            for j in range(y_pos, y_pos + height):
                self._offscreen_canvas.SetPixel(
                    i,
                    j,
                    accent_color_rgb["r"],
                    accent_color_rgb["g"],
                    accent_color_rgb["b"],
                )

        # Draw team name and runs
        text_color_rgb = team_colors.get("text", {"r": 255, "g": 255, "b": 255})
        text_color = graphics.Color(
            text_color_rgb["r"], text_color_rgb["g"], text_color_rgb["b"]
        )
        text_x_pos = x_pos + 1
        text_y_pos = y_pos + height - 1
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            text_x_pos,
            text_y_pos,
            text_color,
            TEAM_ABBREVIATIONS[team_name],
        )
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            text_x_pos + 20,
            text_y_pos,
            text_color,
            str(runs),
        )

    def _render(self):
        current_game = Data.get("current_game")
        if current_game:
            half_height = int(self._offscreen_canvas.height / 2)
            self._render_score_for_team(
                team_name=current_game.overview.home_team_name,
                runs=current_game.overview.home_team_runs,
                x_pos=0,
                y_pos=0,
                height=half_height,
                width=self._offscreen_canvas.width,
            )
            self._render_score_for_team(
                team_name=current_game.overview.away_team_name,
                runs=current_game.overview.away_team_runs,
                x_pos=0,
                y_pos=half_height,
                height=half_height,
                width=self._offscreen_canvas.width,
            )
