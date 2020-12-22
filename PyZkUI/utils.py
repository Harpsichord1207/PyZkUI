import time


class HostHistory:

    def __init__(self, lmt=5):
        self._data = {}

    def accept(self, host):
        self._data[host] = time.time()

    def export(self):
        ...
