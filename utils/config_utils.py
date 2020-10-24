import json


class Config:
    def __init__(self):
        with open("./config.json") as f:
            config_data = f.read()
            self.config = json.loads(config_data)

    def get_data_center_config(self):
        host = self.config["data_center"]["host"]
        port = self.config["data_center"]["port"]
        return host, port
