from datetime import datetime
from PIL import Image
from typing import Dict

from rgbmatrix import FrameCanvas, graphics, RGBMatrix

from constants import Color, Font
from data import Data
from graphics.common import get_x_pos_for_centered_obj
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.data_classes import WeatherCondition
from weather.open_weather import OpenWeatherDataThread

CELCIUS_INDICATOR_WIDTH = 3
CONDITION_ICON_TEMP_MARGIN = 3
CONDITION_ICON_WIDTH = 15
WEATHER_CONDITION_ICON_MAP = {
    WeatherCondition.CLEAR: dict(
        name="sunny",
        x_offset=-1,
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
        self._icon_name = None
        self._temperature_color = temperature_color

    def _render_temperature(
        self, temperature: str, font: Font, font_size: Dict, x_pos: int
    ):
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            11,
            self._temperature_color.value,
            temperature,
        )
        graphics.DrawCircle(
            self._offscreen_canvas,
            x_pos + len(temperature) * font_size["width"],
            4,
            1,
            self._temperature_color.value,
        )

    def _render_condition(self, icon_name: str, x_pos: int, y_pos: int):
        if icon_name != self._icon_name:
            self._icon = Image.open(
                get_abs_file_path(f"assets/{icon_name}.ppm")
            ).convert("RGB")
            self._icon_name = icon_name
        self._icon.resize(
            (self._rgb_matrix.width, self._rgb_matrix.height), Image.ANTIALIAS
        )
        self._offscreen_canvas.SetImage(self._icon, x_pos, y_pos, unsafe=False)

    def _render(self):
        self._offscreen_canvas.Clear()
        # Get weather data
        weather_data = Data.get("weather")
        temperature = "0"
        condition = WeatherCondition.CLOUDS
        if weather_data:
            temperature = str(weather_data.current.temperature)
            condition = weather_data.current.condition

        # Get condition icon data and determine x_pos
        condition_icon_data = WEATHER_CONDITION_ICON_MAP[condition]
        font, size = self._get_font(Font.TINY)
        font_width = len(temperature) * size["width"]
        margin_width = (
            CONDITION_ICON_TEMP_MARGIN - 1
            if temperature.startswith("-")
            else CONDITION_ICON_TEMP_MARGIN
        )
        x_pos = (
            get_x_pos_for_centered_obj(
                center_pos=16,
                obj_width=CONDITION_ICON_WIDTH
                + margin_width
                + font_width
                + CELCIUS_INDICATOR_WIDTH,
            )
            + condition_icon_data.get("x_offset", 0)
        )

        # Render condition icon and temperature
        self._render_condition(
            icon_name=condition_icon_data["name"],
            x_pos=x_pos,
            y_pos=condition_icon_data.get("y_offset", 0),
        )
        self._render_temperature(
            temperature=temperature,
            font=font,
            font_size=size,
            x_pos=x_pos + CONDITION_ICON_WIDTH + margin_width,
        )

        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(self._offscreen_canvas)
