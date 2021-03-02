from datetime import datetime
from PIL import Image

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.text import center_text_position
from utils import get_abs_file_path
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
        self._icon = None

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
    
    def _render_icon(self):
        if not self._icon:
            self._icon = Image.open(get_abs_file_path("assets/partially_cloudy.ppm")).convert('RGB')
        self._icon.resize((self._rgb_matrix.width, self._rgb_matrix.height), Image.ANTIALIAS)

        icon_width, _ = self._icon.size
        xpos = 1
        self._offscreen_canvas.SetImage(self._icon, unsafe=False)
        self._offscreen_canvas.SetImage(self._icon, unsafe=False)

    def _render(self):
        self._offscreen_canvas.Clear()

        self._render_icon()
        self._render_temperature()
        self._render_day_of_the_week()

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
