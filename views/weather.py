from datetime import datetime

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
        day_of_the_week_color: Color = Color.RED,
    ):
        super().__init__(rgb_matrix)
        self._temperature_color = temperature_color
        self._day_of_the_week_color = day_of_the_week_color
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

    def _render_temperature(self):
        weather_data = Data.get("weather")
        temperature = (
            str(Data.get("weather").current.temperature) if weather_data else "0"
        )
        font, _ = self._get_font(Font.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            20,
            10,
            self._temperature_color.value,
            temperature,
        )

    def _render_day_of_the_week(self):
        day_of_the_week = datetime.now().strftime("%a")
        font, _ = self._get_font(Font.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            20,
            5,
            self._day_of_the_week_color.value,
            day_of_the_week,
        )

    def _render(self):
        self._offscreen_canvas.Clear()

        self._render_temperature()
        self._render_day_of_the_week()

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
