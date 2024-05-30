import threading

class Timer:
    def __init__(self, duration_ms):
        self.duration_ms = duration_ms
        self.timeUp = False
        self._timer = None

    def _time_up(self):
        self.timeUp = True

    def start(self):
        self._timer = threading.Timer(self.duration_ms / 1000, self._time_up)
        self._timer.start()

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()
        self.timeUp = False

    def is_time_up(self):
        return self.timeUp