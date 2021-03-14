import mlbgame
from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from views.base_views import BaseView


class UpcomingGameView(BaseView):
    _render_delay = 0.05

    def __init__(
        self,
        rgb_matrix: RGBMatrix,
        game: mlbgame.game.GameScoreboard,
    ):
        super().__init__(rgb_matrix)
        self._game = game

    def _render(self):
        font, _ = self._get_font(Font.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            10,
            10,
            Color.BLUE.value,
            self._game.game_start_time,
        )
