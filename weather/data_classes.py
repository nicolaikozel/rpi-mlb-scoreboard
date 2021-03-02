class Weather:
    def __init__(self, temperature: int, weather_type: str):
        self.temperature = temperature
        self.weather_type = weather_type


class WeatherData:
    def __init__(self, current: Weather):
        self.current = current
