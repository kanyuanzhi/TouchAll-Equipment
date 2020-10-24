import json
import socket
from time import sleep


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.conn = socket.socket()
        self.connection_refused = True

    def connect(self):
        count = 0
        while self.connection_refused:
            try:
                self.conn.connect((self.address, self.port))
                print("Connection success after %d reconnection(s)" % count)
                self.connection_refused = False
            except ConnectionRefusedError:
                self.conn = socket.socket()
                count += 1
                print("Connection refused, reconnecting... %d" % count)
                sleep(1)
            except Exception as e:
                self.conn = socket.socket()
                print(str(e))
                sleep(1)

    def send(self, data):
        data_json = json.dumps(data)
        data_byte = data_json.encode()
        data_byte = "header".encode() + len(data_byte).to_bytes(length=4, byteorder="big", signed=True) + data_byte
        try:
            self.conn.send(data_byte)
        except BrokenPipeError:
            self.connection_refused = True
            print("Broken pipe error, send data failed, waiting for reconnection...")
        except Exception as e:
            self.connection_refused = True
            print(str(e) + "waiting for reconnection...")
