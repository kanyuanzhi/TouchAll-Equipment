import json
import socket


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.conn = socket.socket()
        self.conn.connect((address, port))

    def send(self, data):
        data_json = json.dumps(data)
        data_byte = data_json.encode()
        data_byte = "header".encode() + len(data_byte).to_bytes(length=4, byteorder="big", signed=True) + data_byte
        self.conn.send(data_byte)

