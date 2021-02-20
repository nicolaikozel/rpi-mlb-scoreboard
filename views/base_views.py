import time
from abc import ABC, abstractmethod


class BaseView(ABC):
    def __init__(self, rgb_matrix):
        self._rgb_matrix = rgb_matrix

    def _usleep(self, value):
        time.sleep(value/1000000.0)

    @abstractmethod
    def render(self):
        pass
