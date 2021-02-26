from threading import Event, Thread


class StoppableThread(Thread):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def _cleanup(self):
        pass

    def stop(self):
        self._cleanup()
        self._stop_event.set()

    @property
    def stopped(self):
        return self._stop_event.is_set()
    