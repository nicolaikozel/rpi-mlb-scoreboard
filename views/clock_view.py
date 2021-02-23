from datetime import datetime

from rgbmatrix import graphics

from constants import Color, Font
from utils import center_text_position
from views.base_views import BaseView


class ClockView(BaseView):
    def _render_loc_and_time(self, canvas):
        time_font, font_size = self._get_font(Font.LARGE.value)
        time_color = Color.RED.value
        loc_font, _ = self._get_font(Font.TINY.value)
        loc_color = Color.BLUE.value
        
        time_as_string = datetime.now().strftime("%I:%M")

        x_pos = center_text_position(text=time_as_string, center_pos=16, font_width=font_size["width"])
        graphics.DrawText(canvas, time_font, x_pos, 15, time_color, time_as_string)
        graphics.DrawText(canvas, loc_font, 2, 6, loc_color, "Tor")

    def render(self):
        offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

        outline_color = Color.BLUE.value
        outline_length = 3
        outline_direction = 0
        outline_x1 = 0
        outline_y1 = 0
        outline_x2 = 0
        outline_y2 = 0

        while True:
            offscreen_canvas.Clear()
            self._render_loc_and_time(canvas=offscreen_canvas)
            
            if outline_direction == 0:
                outline_x2 = outline_x1 + outline_length
            elif outline_direction == 1:
                outline_y2 = outline_y1 + outline_length
            elif outline_direction == 2:
                outline_x2 = outline_x1 - outline_length
            elif outline_direction == 3:
                outline_y2 = outline_y1 - outline_length
            
            graphics.DrawLine(offscreen_canvas, outline_x1, outline_y1, outline_x2, outline_y2, outline_color)
            
            if outline_direction == 0:
                if outline_x2 + 1 < offscreen_canvas.width:
                    outline_x1 = outline_x2 + 1
                else:
                    outline_x1 = outline_x2 = offscreen_canvas.width - 1
                    outline_direction = 1
            elif outline_direction == 1:
                if outline_y2 + 1 < offscreen_canvas.height:
                    outline_y1 = outline_y2 + 1
                else:
                    outline_y1 = outline_y2 = offscreen_canvas.height - 1
                    outline_direction = 2
            elif outline_direction == 2:
                if outline_x2 - 1 > 0:
                    outline_x1 = outline_x2 - 1
                else:
                    outline_x1 = outline_x2 = 0
                    outline_direction = 3
            elif outline_direction == 3:
                if outline_y2 - 1 > 0:
                    outline_y1 = outline_y2 - 1
                else:
                    outline_y1 = outline_y2 = 0
                    outline_direction = 0

            offscreen_canvas = self._rgb_matrix.SwapOnVSync(offscreen_canvas)
            self._sleep(0.2)