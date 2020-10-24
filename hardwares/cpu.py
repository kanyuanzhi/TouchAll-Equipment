import psutil
from hardwares.hardware import Hardware


class CPU(Hardware):
    def __init__(self, system):
        super().__init__(system)
        self._cpu_count = 0
        self._cpu_per_utilization = []
        self._cpu_average_utilization = 0
        self._cpu_time = 0

    def basic_information(self):
        self._cpu_count = psutil.cpu_count(logical=True)
        _basic_information = {"cpu_count": self._cpu_count}
        return _basic_information

    def status(self):
        self._cpu_per_utilization = psutil.cpu_percent(interval=1, percpu=True)
        self._cpu_average_utilization = psutil.cpu_percent(interval=1, percpu=False)
        _status = {'cpu_per_utilization': self._cpu_per_utilization,
                   'cpu_average_utilization': self._cpu_average_utilization}
        return _status

