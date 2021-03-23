from datetime import datetime

from rgbmatrix import graphics, RGBMatrix

from animations.outline_canvas import OutlineCanvasAnimation
from config import Config
from graphics.font import Font, FontStyle
from graphics.utils import center_text
from views.base_views import BaseView


class ClockView(BaseView):
    _render_delay = 0.05

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._last_minute = None
        self._outline_canvas_animation = OutlineCanvasAnimation(
            max_cycles=1, wait_until_armed=True
        )

    def _render_location(self):
        color = graphics.Color(*Config.get()["clock"]["location_color"])
        graphics.DrawText(
            self._offscreen_canvas, Font.get_font(FontStyle.TINY), 2, 6, color, "Tor",
        )

    def _render_time(self, time: str):
        color = graphics.Color(*Config.get()["clock"]["time_color"])
        font, font_size = Font.get_font(FontStyle.LARGE)
        x_pos = center_text(center_pos=16, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas, font, x_pos, 15, self._time_color.value, time,
        )

    def _render(self):
        # Get current date and time
        now = datetime.now()

        # Reset and arm outline animation every minute
        current_minute = now.minute
        if self._last_minute and self._last_minute != current_minute:
            self._outline_canvas_animation.reset_and_arm()
        self._last_minute = current_minute

        # Render location and time
        self._render_location()
        self._render_time(time=now.strftime("%I:%M"))

        # Render outline animation
        self._outline_canvas_animation.render(canvas=self._offscreen_canvas)
