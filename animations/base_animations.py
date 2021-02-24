from abc import ABC, abstractmethod


class BaseAnimation(ABC):
    @abstractmethod
    def _advance_frame(self, canvas):
        pass

    @abstractmethod
    def _render_frame(self, canvas):
        pass

    def render(self, canvas):
        self._render_frame(canvas)
        self._advance_frame(canvas)