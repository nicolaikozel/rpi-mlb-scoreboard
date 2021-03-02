import time
from typing import List

from common.threading import RestartableThread
from controllers.base_controllers import BaseController


class LoopingThreadsController(BaseController):
    def __init__(
        self,
        threads: List[RestartableThread],
        thread_change_delay: int,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._threads = threads
        self._thread_index = 0
        self._thread_change_delay = thread_change_delay
        self._set_current_thread(thread=self._threads[self._thread_index])

    def _switch_to_next_thread(self):
        next_thread_index = self._thread_index + 1
        if next_thread_index == len(self._threads):
            next_thread_index = 0
        self._switch_thread(thread=self._threads[next_thread_index])
        self._thread_index = next_thread_index
        self._loop_count = 0

    def _update_thread(self):
        if self._loop_count == self._thread_change_delay:
            self._switch_to_next_thread()
