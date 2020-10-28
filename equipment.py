from hardwares import cpu, disk, network, memory
import platform
import psutil
import datetime
import time
from config_utils import Config


class Equipment:
    def __init__(self):
        self._system = platform.system()
        self._cpu = cpu.CPU(self._system)
        self._disk = disk.Disk(self._system)
        self._memory = memory.Memory(self._system)
        self._network = network.Network(self._system)
        self._boot_time_in_timestamp = int(psutil.boot_time())
        config = Config()
        self._test_mode = config.get_value('test_mode')
        self._test_network_mac = config.get_value('test', 'network_mac')
        self._network_mac = self._test_network_mac if self._test_mode else self._network.basic_information()[
            'network_mac']

    def basic_information(self):
        _basic_information = {'cpu': self._cpu.basic_information(),
                              'disk': self._disk.basic_information(),
                              'memory': self._memory.basic_information(),
                              'network': self._network.basic_information(),
                              'operate_system': self._system,
                              'network_name': platform.node(),
                              'platform': platform.platform(),
                              'architecture': platform.architecture()[0],
                              'boot_time_in_timestamp': self._boot_time_in_timestamp,
                              'boot_time_in_string': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
                                  "%Y-%m-%d %H: %M: %S"),
                              'user': psutil.users()[0].name,
                              'host': psutil.users()[0].host,
                              'data_type': 30,
                              'update_time': int(time.time())}
        if self._test_mode:
            _basic_information['network']['network_mac'] = self._test_network_mac
        return _basic_information

    def status(self):
        _status = {'cpu': self._cpu.status(),
                   'disk': self._disk.status(),
                   'memory': self._memory.status(),
                   'network': self._network.status(),
                   'data_type': 31,
                   'update_time': int(time.time()),
                   'network_mac': self._network_mac,
                   'running_time': int(time.time()) - self._boot_time_in_timestamp}
        return _status


if __name__ == "__main__":
    equipment = Equipment()
    print(equipment.basic_information())
    print(equipment.status())
