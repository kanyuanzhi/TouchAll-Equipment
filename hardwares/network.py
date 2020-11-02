import psutil
from hardwares.hardware import Hardware
from socket import AddressFamily


class Network(Hardware):
    def __init__(self, system, network_card):
        super().__init__(system)
        self._network_card = network_card
        self._network_mac = ""  # mac地址
        self._network_ip = ""
        self._network_send_gigabytes = 0
        self._network_receive_gigabytes = 0
        self._network_drop_in = 0
        self._network_drop_out = 0

    def basic_information(self):
        net_if_addrs = psutil.net_if_addrs()
        if self._system == "Windows":
            network_entries = net_if_addrs[self._network_card]
            for entry in network_entries:
                family = entry.family
                if family == AddressFamily.AF_INET:
                    self._network_ip = entry.address
                if family == AddressFamily.AF_LINK:
                    self._network_mac = entry.address
        elif self._system == "Linux":
            network_entries = net_if_addrs[self._network_card]
            for entry in network_entries:
                family = entry.family
                if family == AddressFamily.AF_INET:
                    self._network_ip = entry.address
                if family == AddressFamily.AF_PACKET:
                    self._network_mac = entry.address
        else:
            network_entries = net_if_addrs[self._network_card]
            for entry in network_entries:
                family = entry.family
                if family == AddressFamily.AF_LINK:
                    self._network_mac = entry.address
                if family == AddressFamily.AF_INET:
                    self._network_ip = entry.address

        _basic_information = {'network_mac': self._network_mac,
                              'network_ip': self._network_ip}
        return _basic_information

    def status(self):
        net_io_counters = psutil.net_io_counters(pernic=False)
        self._network_send_gigabytes = round(net_io_counters.bytes_sent / 1024 / 1024 / 1024, 1)
        self._network_receive_gigabytes = round(net_io_counters.bytes_recv / 1024 / 1024 / 1024, 1)
        self._network_drop_in = net_io_counters.dropin
        self._network_drop_out = net_io_counters.dropout
        _status = {'network_drop_in': self._network_drop_in,
                   'network_drop_out': self._network_drop_out,
                   'network_send_gigabytes': self._network_send_gigabytes,
                   'network_receive_gigabytes': self._network_receive_gigabytes}
        return _status
