from datetime import datetime

from rgbmatrix import graphics

from animations.outline_canvas import OutlineCanvasAnimation
from constants import Color, Font
from graphics.text import center_text_position
from views.base_views import BaseView


class ClockView(BaseView):
    def __init__(self, rgb_matrix):
        super().__init__(rgb_matrix)
        self._loc_font, _ = self._get_font(Font.TINY) 
        self._time_font, self._time_font_size = self._get_font(Font.LARGE)

    def _render_loc_and_time(self, canvas, time):
        loc_color = Color.BLUE
        time_color = Color.RED
        time_as_string = time.strftime("%I:%M")

        graphics.DrawText(canvas, self._loc_font, 2, 6, loc_color.value, "Tor")
        x_pos = center_text_position(text=time_as_string, center_pos=16, font_width=self._time_font_size["width"])
        graphics.DrawText(canvas, self._time_font, x_pos, 15, time_color.value, time_as_string)

    def render(self):
        last_minute = None
        offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()
        outline_canvas_animation = OutlineCanvasAnimation(max_cycles=1, wait_until_armed=True)
        
        while True:
            offscreen_canvas.Clear()

            cur_time = datetime.now()
            cur_minute = cur_time.minute
            if last_minute and last_minute != cur_minute:
                outline_canvas_animation.reset_and_arm()
            last_minute = cur_minute
            outline_canvas_animation.render(canvas=offscreen_canvas)
            self._render_loc_and_time(canvas=offscreen_canvas, time=cur_time)

            offscreen_canvas = self._rgb_matrix.SwapOnVSync(offscreen_canvas)
            self._sleep(0.05)