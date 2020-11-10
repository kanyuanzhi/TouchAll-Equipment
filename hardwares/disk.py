import psutil
from hardwares.hardware import Hardware


class Disk(Hardware):
    def __init__(self, system):
        super().__init__(system)
        self._disk_size = 0  # 磁盘大小
        self._disk_utilization = 0  # 磁盘利用率
        self._disk_partitions = 0
        self._disk_used = 0  # 磁盘使用大小
        self._disk_available = 0  # 磁盘可用大小
        self._disk_read_bytes = 0
        self._disk_write_bytes = 0

    def basic_information(self):
        self._disk_partitions = psutil.disk_partitions(all=False)
        if self._system == "Windows":
            for partition in self._disk_partitions:
                if partition.fstype == "NTFS":
                    mount = partition.mountpoint
                    disk_usage = psutil.disk_usage(mount)
                    self._disk_size += round(disk_usage.total / 1024 / 1024 / 1024, 1)
        else:
            disk_usage = psutil.disk_usage('/')
            self._disk_size = round(disk_usage.total / 1024 / 1024 / 1024, 1)
        _basic_information = {'disk_size': self._disk_size}
        return _basic_information

    def status(self):
        self._disk_partitions = psutil.disk_partitions(all=False)
        if self._system == "Windows":
            for partition in self._disk_partitions:
                if partition.fstype == "NTFS":
                    mount = partition.mountpoint
                    disk_usage = psutil.disk_usage(mount)
                    self._disk_used += round(disk_usage.used / 1024 / 1024 / 1024, 1)
                    self._disk_available += round(disk_usage.free / 1024 / 1024 / 1024, 1)
        else:
            disk_usage = psutil.disk_usage('/')
            self._disk_used = round(disk_usage.used / 1024 / 1024 / 1024, 1)
            self._disk_available = round(disk_usage.free / 1024 / 1024 / 1024, 1)

        # disk_io_counters = psutil.disk_io_counters(perdisk=False)
        # self._disk_read_gigabytes = disk_io_counters.read_bytes / 1024 / 1024 / 1024
        # self._disk_write_gigabytes = disk_io_counters.write_bytes / 1024 / 1024 / 1024

        _status = {'disk_used': self._disk_used,
                   'disk_available': self._disk_available}
        return _status
