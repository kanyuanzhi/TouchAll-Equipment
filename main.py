from equipment import Equipment
from socket_client import Client
from config_utils import Config
from apscheduler.schedulers.blocking import BlockingScheduler


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

    scheduler.add_job(update, 'interval', seconds=interval, max_instances=100, id='update', args=[equipment, client])
    client.update_job_started = True
    scheduler.start()

