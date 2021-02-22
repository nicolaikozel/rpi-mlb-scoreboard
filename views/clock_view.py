from datetime import datetime

from rgbmatrix import graphics

from constants import Color
from utils import center_text_position
from views.base_views import BaseView


class ClockView(BaseView):
    def render(self):
        offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()
        font, font_size = self._get_font()
        color = Color.RED.value
        while True:
            offscreen_canvas.Clear()
            time_as_string = datetime.now().strftime("%I:%M")
            x_pos = center_text_position(text=time_as_string, center_pos=16, font_width=font_size["width"])
            graphics.DrawText(offscreen_canvas, font, x_pos, 11, color, time_as_string)
            offscreen_canvas = self._rgb_matrix.SwapOnVSync(offscreen_canvas)
            self._sleep(1)