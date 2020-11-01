from equipment import Equipment
from socket_client import Client
from config_utils import Config
from apscheduler.schedulers.blocking import BlockingScheduler
import json


def register(equipment, client):
    basic_information = equipment.basic_information()
    print(basic_information)
    client.send(basic_information)


def update(equipment, client):
    client.send(equipment.status())


if __name__ == "__main__":
    equipment = Equipment()

    config = Config()
    interval = config.get_value("interval")

    scheduler = BlockingScheduler()

    host, port = config.get_data_center_config()
    client = Client(host, port, scheduler)
    client.connect()

    register(equipment, client)
    message_bytes = client.conn.recv(1024)
    message_str = message_bytes.decode()
    message_json = json.loads(message_str)
    equipment.equipment_id = message_json["equipment_id"]

    scheduler.add_job(update, 'interval', seconds=interval, max_instances=100, id='update', args=[equipment, client])
    client.update_job_started = True
    scheduler.start()

