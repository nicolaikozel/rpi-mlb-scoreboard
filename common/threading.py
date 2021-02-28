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
        return self._instance.is_alive()

    def reset(self):
        self._instance = self._thread(*self._args, **self._kwargs)

    def start(self):
        self._instance.start()

    def join(self):
        self._instance.join()

    def stop(self):
        self._instance.stop()
