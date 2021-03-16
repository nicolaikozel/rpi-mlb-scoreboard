from abc import ABC, abstractmethod, abstractproperty


class BaseAnimation(ABC):
    def __init__(self, max_cycles: int = None, wait_until_armed: bool = False):
        self._completed_cycles = 0
        self._max_cycles = max_cycles
        self._armed = False
        self._wait_until_armed = wait_until_armed

    @property
    def finished(self) -> bool:
        return self._completed_cycles == self._max_cycles

    def increment_completed_cycles(self):
        if self._max_cycles:
            self._completed_cycles += 1

    def arm(self):
        self._armed = True

    def _reset(self):
        pass

    def reset(self):
        self._armed = False
        self._completed_cycles = 0
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
