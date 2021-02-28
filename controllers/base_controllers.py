import time
from abc import ABC, abstractmethod, abstractproperty

from common.threading import StoppableThread


class BaseController(StoppableThread, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop_count = 0
        self._current_thread = None

    def _cleanup(self):
        self._current_thread.stop()
        self._current_thread.join()

    def _set_current_thread(self, thread: StoppableThread):
        self._current_thread = thread

    def _switch_thread(self, thread):
        if self._current_thread:
            self._current_thread.stop()
            self._current_thread.join()
        thread.reset()
        thread.start()
        self._set_current_thread(thread=thread)

    @abstractmethod
    def _update_thread(self):
        pass

    def run(self):
        if not self._current_thread.is_alive():
            self._current_thread.start()

        while True:
            self._update_thread()
            time.sleep(1)
            self._loop_count += 1
            if self.stopped:
                break
