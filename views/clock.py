from datetime import datetime

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from animations.outline_canvas import OutlineCanvasAnimation
from constants import Color, Font
from graphics.common import get_x_pos_for_centered_text
from views.base_views import BaseView


class ClockView(BaseView):
    _render_delay = 0.05

    def __init__(
        self,
        rgb_matrix: RGBMatrix,
        loc_color: Color = Color.BLUE,
        time_color: Color = Color.RED,
    ):
        super().__init__(rgb_matrix)
        self._loc_font, _ = self._get_font(Font.TINY)
        self._loc_color = loc_color
        self._time_font, self._time_font_size = self._get_font(Font.LARGE)
        self._time_color = time_color
        self._last_minute = None
        self._outline_canvas_animation = OutlineCanvasAnimation(
            max_cycles=1, wait_until_armed=True
        )

    def _render_loc_and_time(self, canvas: FrameCanvas, time: datetime):
        time_as_string = time.strftime("%I:%M")
        graphics.DrawText(canvas, self._loc_font, 2, 6, self._loc_color.value, "Tor")
        x_pos = get_x_pos_for_centered_text(
            center_pos=16, text=time_as_string, font_width=self._time_font_size["width"]
        )
        graphics.DrawText(
            canvas, self._time_font, x_pos, 15, self._time_color.value, time_as_string
        )

    def _render(self):
        # Get current date and time
        cur_time = datetime.now()
        cur_minute = cur_time.minute
        if self._last_minute and self._last_minute != cur_minute:
            self._outline_canvas_animation.reset_and_arm()
        self._last_minute = cur_minute

        # Render location and time
        self._render_loc_and_time(canvas=self._offscreen_canvas, time=cur_time)
        # Render outline animation
        self._outline_canvas_animation.render(canvas=self._offscreen_canvas)
