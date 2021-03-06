from datetime import datetime
from PIL import Image

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.text import center_text_position
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.data_classes import WeatherCondition
from weather.open_weather import OpenWeatherDataThread


WEATHER_CONDITION_ICON_MAP = {
    WeatherCondition.CLEAR: "sunny",
    WeatherCondition.CLOUDS: "cloudy",
    WeatherCondition.RAIN: "rainy",
    WeatherCondition.DRIZZLE: "rainy",
    WeatherCondition.THUNDERSTORM: "stormy",
    WeatherCondition.SNOW: "snowy",
}


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
        self._prev_condition = None

    def _render_temperature(self):
        weather_data = Data.get("weather")
        temperature = (
            str(weather_data.current.temperature) if weather_data else "0"
        )
        temperature = "-15"
        font, _ = self._get_font(Font.TINY)
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            17,
            11,
            self._temperature_color.value,
            temperature,
        )
        graphics.DrawCircle(self._offscreen_canvas, 29, 4, 1, self._temperature_color.value)
    
    def _render_icon(self):
        weather_data = Data.get("weather")
        condition = weather_data.current.condition if weather_data else WeatherCondition.CLOUDS
        if condition != self._prev_condition:
            icon = WEATHER_CONDITION_ICON_MAP[condition]
            self._icon = Image.open(get_abs_file_path(f"assets/{icon}.ppm")).convert('RGB')
            self._prev_condition = condition
        self._icon.resize((self._rgb_matrix.width, self._rgb_matrix.height), Image.ANTIALIAS)

        icon_width, _ = self._icon.size
        xpos = 1
        self._offscreen_canvas.SetImage(self._icon, unsafe=False)

    def _render(self):
        self._offscreen_canvas.Clear()

        self._render_icon()
        self._render_temperature()

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
