from abc import ABC, abstractmethod, abstractproperty


class BaseAnimation(ABC):
    def __init__(self, wait_until_armed: bool = False):
        self._armed = False
        self._wait_until_armed = wait_until_armed

    @abstractproperty
    def finished(self) -> bool:
        pass

    def arm(self):
        self._armed = True

    @abstractmethod
    def _reset(self):
        pass

    def reset(self):
        self._armed = False
        self._reset()

    def reset_and_arm(self):
        self.reset()
        self.arm()

    @abstractmethod
    def _advance_frame(self, canvas):
        pass

    @abstractmethod
    def _render_frame(self, canvas):
        pass

    def render(self, canvas):
        if (self._wait_until_armed and not self._armed) or self.finished:
            return

        self._render_frame(canvas)
        self._advance_frame(canvas)
