from datetime import datetime

from rgbmatrix import graphics

from constants import Color, Font
from utils import center_text_position
from animations.outline_canvas import OutlineCanvasAnimation
from views.base_views import BaseView


class ClockView(BaseView):
    def _render_loc_and_time(self, canvas):
        time_font, font_size = self._get_font(Font.LARGE)
        time_color = Color.RED
        loc_font, _ = self._get_font(Font.TINY)
        loc_color = Color.BLUE
        
        time_as_string = datetime.now().strftime("%I:%M")

        x_pos = center_text_position(text=time_as_string, center_pos=16, font_width=font_size["width"])
        graphics.DrawText(canvas, time_font, x_pos, 15, time_color.value, time_as_string)
        graphics.DrawText(canvas, loc_font, 2, 6, loc_color.value, "Tor")

    def render(self):
        offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()
        outline_canvas_animation = OutlineCanvasAnimation(color=Color.BLUE)
        
        while True:
            offscreen_canvas.Clear()
            self._render_loc_and_time(canvas=offscreen_canvas)
            outline_canvas_animation.render(canvas=offscreen_canvas)
            offscreen_canvas = self._rgb_matrix.SwapOnVSync(offscreen_canvas)
            self._sleep(0.03)