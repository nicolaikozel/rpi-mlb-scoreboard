import time
from abc import ABC, abstractmethod
from typing import Type

from threading import Event, Thread


class StoppableThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def _cleanup(self):
        pass

    def stop(self):
        self._cleanup()
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        return self._stop_event.is_set()


class RestartableThread:
    def __init__(self, thread: Type[StoppableThread], *args, **kwargs):
        self._args, self._kwargs = args, kwargs
        self._thread = thread
        self.reset()

    def is_alive(self) -> bool:
        return self.instance.is_alive()

    def reset(self):
        self.instance = self._thread(*self._args, **self._kwargs)

    def start(self):
        self.instance.start()

    def join(self):
        self.instance.join()

    def stop(self):
        self.instance.stop()


class DataThread(StoppableThread, ABC):
    def __init__(self, refresh_rate: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._refresh_rate = refresh_rate
        self._data = None

    @property
    def data(self) -> object:
        return self._data

    @abstractmethod
    def _fetch_data(self) -> object:
        pass

    def run(self):
        while True:
            self._data = self._fetch_data()
            time.sleep(self._refresh_rate)
            if self.stopped:
                break
