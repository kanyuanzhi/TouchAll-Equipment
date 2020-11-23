import json
import socket
from time import sleep


class Client:
    def __init__(self, address, port, scheduler):
        self.address = address
        self.port = port
        self.scheduler = scheduler
        self.conn = socket.socket()
        self.is_reconnecting = False
        self.update_job_started = False

    def connect(self):
        count = 0
        while True:
            try:
                self.conn.connect((self.address, self.port))
                self.is_reconnecting = False
                print("Connection success after %d reconnection(s)" % count)
                if self.update_job_started:
                    self.scheduler.resume_job('update')
                return
            except Exception as e:
                self.is_reconnecting = True
                self.conn = socket.socket()
                count += 1
                print(str(e) + ": %d" % count)
                sleep(1)

    def send(self, data):
        data_json = json.dumps(data)
        data_byte = data_json.encode()
        data_byte = "header".encode() + len(data_byte).to_bytes(length=4, byteorder="little", signed=True) + data_byte
        if self.is_reconnecting:
            return
        else:
            try:
                self.conn.send(data_byte)
                print(data)
            except Exception as e:
                print(str(e) + ": Reconnecting...\n")
                self.scheduler.pause_job('update')
                self.conn = socket.socket()
                self.connect()
