import time
from abc import ABC, abstractmethod, abstractproperty

from common.threading import StoppableThread


class BaseController(StoppableThread, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop_count = 0

    @abstractproperty
    def current_thread(self) -> StoppableThread:
        pass

    def _cleanup(self):
        self.current_thread.stop()
        self.current_thread.join()

    def _switch_thread(self, thread):
        if self.current_thread:
            self.current_thread.stop()
            self.current_thread.join()
        thread.reset()
        thread.start()

    @abstractmethod
    def _update_thread(self):
        pass

    def run(self):
        if not self.current_thread.is_alive():
            self.current_thread.start()

        while True:
            self._update_thread()
            time.sleep(1)
            self._loop_count += 1
            if self.stopped:
                break
