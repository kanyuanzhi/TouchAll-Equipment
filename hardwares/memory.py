import psutil
from hardwares.hardware import Hardware


class Memory(Hardware):
    def __init__(self, system):
        super().__init__(system)
        self._memory_size = 0
        self._memory_utilization = 0
        self._memory_available = 0

    def basic_information(self):
        mem = psutil.virtual_memory()
        self._memory_size = round(mem.total / 1024 / 1024 / 1024, 1)
        _basic_information = {'memory_size': self._memory_size}
        return _basic_information

    def status(self):
        mem = psutil.virtual_memory()
        self._memory_utilization = mem.percent
        self._memory_available = round(mem.available / 1024 / 1024 / 1024, 1)
        _status = {'memory_utilization': self._memory_utilization,
                   'memory_available': self._memory_available}
        return _status
