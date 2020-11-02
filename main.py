from equipment import Equipment
from socket_client import Client
from config_utils import Config
from apscheduler.schedulers.blocking import BlockingScheduler
from json import loads
from random import randint


def register(equipment, client):
    basic_information = equipment.basic_information()
    print(basic_information)
    client.send(basic_information)


def update(equipment, client):
    client.send(equipment.status())


if __name__ == "__main__":
    config = Config()

    interval = config.get_value("interval")
    network_card = config.get_value("network_card")
    host, port = config.get_data_center_config()

    equipment = Equipment()

    scheduler = BlockingScheduler()
    client = Client(host, port, scheduler)
    client.connect()

    register(equipment, client)

    message_bytes = client.conn.recv(1024)
    message_str = message_bytes.decode()
    message_json = loads(message_str)
    use_mysql = message_json["use_mysql"]
    use_mongodb = message_json["use_mongodb"]
    if use_mysql:
        equipment.equipment_id = message_json["equipment_id"]
        text = "设备在数据中心注册成功，当前设备ID: {}"
    else:
        equipment.equipment_id = randint(65525, 70000)
        text = "当前数据中心未连接至mysql，设备无法获取正确ID，已经为设备分配临时ID: {}供测试使用"
    print(text.format(equipment.equipment_id))
    scheduler.add_job(update, 'interval', seconds=interval, max_instances=100, id='update', args=[equipment, client])
    client.update_job_started = True
    scheduler.start()
