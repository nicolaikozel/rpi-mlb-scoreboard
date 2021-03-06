from datetime import datetime
from PIL import Image
from typing import Dict

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.common import get_x_pos_for_centered_text_and_obj
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.data_classes import WeatherCondition
from weather.open_weather import OpenWeatherDataThread

ICON_WIDTH = 19
WEATHER_CONDITION_ICON_MAP = {
    WeatherCondition.CLEAR: dict(
        name="sunny",
        y_offset=1,
    ),
    WeatherCondition.CLOUDS: dict(
        name="cloudy",
    ),
    WeatherCondition.RAIN: dict(
        name="rainy",
    ),
    WeatherCondition.DRIZZLE: dict(
        name="rainy",
    ),
    WeatherCondition.THUNDERSTORM: dict(
        name="stormy",
    ),
    WeatherCondition.SNOW: dict(
        name="snowy",
    ),
}


class WeatherView(BaseView):
    _render_delay = 0.05

    def __init__(
        self,
        rgb_matrix: RGBMatrix,
        temperature_color: Color = Color.BLUE,
    ):
        super().__init__(rgb_matrix)
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()
        self._icon = None
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self._condition = None
        self._temperature_color = temperature_color

    def _render_temperature(self, temperature: str, font: Font, font_size: Dict, x_pos: int):
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            11,
            self._temperature_color.value,
            temperature,
        )
        graphics.DrawCircle(self._offscreen_canvas, x_pos+len(temperature)*font_size["width"], 4, 1, self._temperature_color.value)
    
    def _render_condition(self, condition: WeatherCondition, x_pos: int):
        if condition != self._condition:
            icon_data = WEATHER_CONDITION_ICON_MAP[condition]
            self._icon = Image.open(get_abs_file_path(f"assets/{icon_data['name']}.ppm")).convert('RGB')
            self._icon_x_offset = icon_data.get("x_offset", 0)
            self._icon_y_offset = icon_data.get("y_offset", 0)
            self._condition = condition
        self._icon.resize((self._rgb_matrix.width, self._rgb_matrix.height), Image.ANTIALIAS)
        self._offscreen_canvas.SetImage(self._icon, x_pos+self._icon_x_offset, self._icon_y_offset, unsafe=False)

    def _render(self):
        self._offscreen_canvas.Clear()

        weather_data = Data.get("weather")
        temperature = "-10"
        condition = WeatherCondition.CLOUDS
        if weather_data:
            #temperature = str(weather_data.current.temperature)
            condition = weather_data.current.condition
        font, size = self._get_font(Font.TINY)
        x_pos = get_x_pos_for_centered_text_and_obj(center_pos=16, text=temperature, font_width=size["width"], obj_width=ICON_WIDTH) - 1
        self._render_condition(condition=condition, x_pos=x_pos)
        self._render_temperature(temperature=temperature, font=font, font_size=size, x_pos=x_pos+ICON_WIDTH-1)

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
