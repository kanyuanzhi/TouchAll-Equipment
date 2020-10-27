import json


class Config:
    def __init__(self):
        with open("./equipmentStatusConfig.json") as f:
            config_data = f.read()
            self.config = json.loads(config_data)

    def get_data_center_config(self):
        host = self.config["data_center"]["host"]
        port = self.config["data_center"]["port"]
        return host, port

    def get_equipment_id(self):
        equipment_id = self.config["equipment"]["id"]
        return equipment_id

    def get_value(self, *args):
        value = self.config
        for k in args:
            value = value[k]
        return value
