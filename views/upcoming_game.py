import mlbgame
from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from animations.controllers.looping_animations import LoopingAnimationsController
from animations.outline_canvas import OutlineCanvasAnimation
from animations.pulsing_text import PulsingTextAnimation
from animations.scrolling_text import ScrollingTextAnimation
from constants import Color, Font
from data import Data
from graphics.common import center_text
from graphics.gradient import Gradient
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

        gameday_text = "Gameday!"
        font, font_size = self._get_font(Font.TINY)
        self._looping_animations_controller = LoopingAnimationsController(
            animations=[
                PulsingTextAnimation(
                    text=gameday_text,
                    font=font,
                    x_pos=1
                    + center_text(
                        center_pos=16, text=gameday_text, font_width=font_size["width"]
                    ),
                    y_pos=1 + font_size["height"],
                    gradient=Gradient.generate_brightness_gradient(color=Color.BLUE),
                    max_cycles=10,
                ),
                ScrollingTextAnimation(
                    text=f"{self._game.away_team} at {self._game.home_team}",
                    font=font,
                    font_size=font_size,
                    color=Color.BLUE,
                    starting_x_pos=self._offscreen_canvas.width,
                    starting_y_pos=1 + font_size["height"],
                    max_cycles=1,
                ),
            ]
        )
        self._outline_canvas_animation = OutlineCanvasAnimation(
            gradient=Gradient(
                colors=[
                    Color.WHITE.value,
                    Color.BJ_PRIMARY.value,
                    Color.BJ_SECONDARY.value,
                ]
            ),
        )

    def _render_game_time(self):
        font, font_size = self._get_font(Font.SMALL)
        time = self._game.game_start_time.split(" ", 1)[0]
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            center_text(center_pos=16, text=time, font_width=font_size["width"]),
            15,
            Color.BJ_TERTIARY.value,
            time,
        )

    def _render(self):
        self._looping_animations_controller.render(canvas=self._offscreen_canvas)
        self._render_game_time()
        self._outline_canvas_animation.render(canvas=self._offscreen_canvas)
