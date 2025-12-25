from collections import deque
from datetime import datetime, timedelta


class TimeWindowBuffer:
    def __init__(self, window_sec: int):
        self.window = timedelta(seconds=window_sec)
        self.buffer = deque()

    def add(self, ts: datetime, value: float):
        self.buffer.append((ts, value))
        self._cleanup(ts)

    def _cleanup(self, now):
        while self.buffer and now - self.buffer[0][0] > self.window:
            self.buffer.popleft()

    def values(self):
        return [v for _, v in self.buffer]
