from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.text import center_text_position
from views.base_views import BaseView
from weather.open_weather import OpenWeatherDataThread


class WeatherView(BaseView):
    _render_delay = 0.05

    def __init__(
        self,
        rgb_matrix: RGBMatrix,
        temperature_color: Color = Color.BLUE,
    ):
        super().__init__(rgb_matrix)
        self._temperature_font, self._temperature_font_size = self._get_font(
            Font.MEDIUM
        )
        self._temperature_color = temperature_color
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

    def _render_temperature(self, canvas: FrameCanvas):
        weather_data = Data.get("weather")
        temperature = (
            str(Data.get("weather").current.temperature) if weather_data else "0"
        )
        x_pos = center_text_position(
            text=temperature,
            center_pos=16,
            font_width=self._temperature_font_size["width"],
        )
        graphics.DrawText(
            canvas,
            self._temperature_font,
            x_pos,
            15,
            self._temperature_color.value,
            temperature,
        )

    def _render(self):
        self._offscreen_canvas.Clear()

        self._render_temperature(canvas=self._offscreen_canvas)

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
