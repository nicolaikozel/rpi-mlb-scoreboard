import time
from typing import Dict

from common.threading import RestartableThread
from views.controllers.base_controllers import BaseController


class LoopingThreadsController(BaseController):
    def __init__(self, threads: Dict, thread_change_delay: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._threads = threads
        self._thread_index = 0
        self._thread_change_delay = thread_change_delay
        self._set_current_thread(
            thread=self._get_thread_instance(index=self._thread_index)
        )

    def _get_thread_instance(self, index: int) -> RestartableThread:
        return self._threads[index]["instance"]

    def _switch_to_next_thread(self):
        next_thread_index = self._thread_index + 1
        if next_thread_index >= len(self._threads):
            next_thread_index = 0
        self._switch_thread(thread=self._get_thread_instance(index=next_thread_index))
        self._thread_index = next_thread_index
        self._loop_count = 0

    def _update_thread(self):
        if self._loop_count == self._thread_change_delay:
            self._switch_to_next_thread()

    def _find_thread_by_key(self, key: str) -> int:
        for index, thread in enumerate(self._threads):
            if thread["key"] == key:
                return index
        return -1

    def add_thread(self, thread: Dict):
        self._threads.append(thread)

    def remove_thread(self, key: str):
        thread_index = self._find_thread_by_key(key=key)
        if self._thread_index == thread_index:
            self._switch_to_next_thread()
        del self._threads[thread_index]

    def has_thread_for_key(self, key: str) -> bool:
        thread_index = self._find_thread_by_key(key=key)
        return not thread_index == -1
