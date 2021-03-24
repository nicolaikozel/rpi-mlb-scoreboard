import mlbgame
from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from animations.controllers.looping_animations import LoopingAnimationsController
from animations.outline_canvas import OutlineCanvasAnimation
from animations.pulsing_text import PulsingTextAnimation
from animations.scrolling_text import ScrollingTextAnimation
from config import Config
from data import Data
from graphics.font import Font, FontStyle
from graphics.gradient import Gradient
from graphics.utils import center_text
from views.base_views import BaseView


class UpcomingGameView(BaseView):
    _render_delay = 0.05

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        game = Data.get("games_today").upcoming_game
        pulsing_text = "Gameday!"
        team_names_color = graphics.Color(
            *Config.get()["upcoming_game"]["team_names_color"]
        )
        font, font_size = Font.get_font(FontStyle.TINY)
        self._looping_animations_controller = LoopingAnimationsController(
            animations=[
                PulsingTextAnimation(
                    text=pulsing_text,
                    font=font,
                    x_pos=1
                    + center_text(
                        center_pos=16, text=pulsing_text, font_width=font_size["width"]
                    ),
                    y_pos=1 + font_size["height"],
                    gradient=Gradient.generate_brightness_gradient(
                        color=team_names_color
                    ),
                    max_cycles=10,
                ),
                ScrollingTextAnimation(
                    text=f"{game.away_team} at {game.home_team}",
                    font=font,
                    font_size=font_size,
                    color=team_names_color,
                    starting_x_pos=self._offscreen_canvas.width,
                    starting_y_pos=1 + font_size["height"],
                    max_cycles=1,
                ),
            ]
        )
        outline_animation_gradient = graphics.Color(
            *Config.get()["upcoming_game"]["team_names_color"]
        )
        self._outline_canvas_animation = OutlineCanvasAnimation(
            gradient=Gradient(
                colors=[
                    graphics.Color(*color)
                    for color in Config.get()["upcoming_game"][
                        "outline_animation_gradient"
                    ]
                ],
            ),
        )

    def _render_game_time(self, time: str):
        color = graphics.Color(*Config.get()["upcoming_game"]["game_time_color"])
        font, font_size = Font.get_font(FontStyle.SMALL)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            center_text(center_pos=16, text=time, font_width=font_size["width"]),
            15,
            color,
            time,
        )

    def _render(self):
        game = Data.get("games_today").upcoming_game
        if game:
            self._looping_animations_controller.render(canvas=self._offscreen_canvas)
            self._render_game_time(time=game.game_start_time.split(" ", 1)[0])
            self._outline_canvas_animation.render(canvas=self._offscreen_canvas)
