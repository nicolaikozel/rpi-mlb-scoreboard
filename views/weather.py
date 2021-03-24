from PIL import Image
from typing import Dict

from rgbmatrix import graphics, RGBMatrix

from config import Config
from data import Data
from graphics.font import Font, FontStyle
from graphics.utils import center_object
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.constants import WeatherCondition

CELCIUS_INDICATOR_WIDTH = 3
CONDITION_ICON_WIDTH = 15
MARGIN_WIDTH = 3
WEATHER_CONDITION_ICON_MAP = {
    WeatherCondition.CLEAR: dict(name="sunny", x_offset=-1, y_offset=1),
    WeatherCondition.CLOUDS: dict(name="cloudy", y_offset=1),
    WeatherCondition.RAIN: dict(name="rainy", x_offset=-1),
    WeatherCondition.DRIZZLE: dict(name="rainy", x_offset=-1),
    WeatherCondition.THUNDERSTORM: dict(name="stormy", x_offset=-1),
    WeatherCondition.SNOW: dict(name="snowy", x_offset=-1),
}


class WeatherView(BaseView):
    _render_delay = 0.05

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._icon = None
        self._icon_name = None
        self._font, self._font_size = Font.get_font(FontStyle.TINY)

    def _render_temperature(self, temperature: str, x_pos: int, y_pos: int):
        color = graphics.Color(*Config.get()["weather"]["temperature_color"])
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            x_pos,
            y_pos + self._font_size["height"],
            color,
            temperature,
        )
        graphics.DrawCircle(
            self._offscreen_canvas,
            x_pos + len(temperature) * self._font_size["width"] + 1,
            y_pos,
            1,
            color,
        )

    def _render_condition_icon(self, icon_name: str, x_pos: int, y_pos: int):
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
        # Get weather data
        weather_data = Data.get("weather")
        condition = WeatherCondition.CLOUDS
        temperature = "0"
        if weather_data:
            temperature = str(weather_data.current.temperature)
            condition = weather_data.current.condition

        # Determine x position of condition icon
        condition_icon_data = WEATHER_CONDITION_ICON_MAP[condition]
        font_width = len(temperature) * self._font_size["width"]
        margin_width = MARGIN_WIDTH - 1 if temperature.startswith("-") else MARGIN_WIDTH
        x_pos = (
            center_object(
                center_pos=16,
                obj_length=CONDITION_ICON_WIDTH
                + margin_width
                + font_width
                + CELCIUS_INDICATOR_WIDTH,
            )
            + condition_icon_data.get("x_offset", 0)
        )

        # Render condition icon and temperature
        self._render_condition_icon(
            icon_name=condition_icon_data["name"],
            x_pos=x_pos,
            y_pos=center_object(center_pos=8, obj_length=16)
            + condition_icon_data.get("y_offset", 0),
        )
        self._render_temperature(
            temperature=temperature,
            x_pos=x_pos + CONDITION_ICON_WIDTH + margin_width,
            y_pos=center_object(center_pos=8, obj_length=self._font_size["height"]),
        )
