from equipment import Equipment
from socket_client import Client
from utils.config_utils import Config
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep


def register(equipment, client):
    client.send(equipment.basic_information())


def update(equipment, client):
    print("sending status")
    client.send(equipment.status())


if __name__ == "__main__":
    equipment = Equipment()

    config = Config()
    host, port = config.get_data_center_config()
    client = Client(host, port)
    client.connect()

    scheduler_paused = False

    # register(equipment, client)

    scheduler = BackgroundScheduler()
    scheduler.add_job(update, 'interval', seconds=1, max_instances=100, id='update', args=[equipment, client])
    scheduler.start()

    while True:
        if client.connection_refused and not scheduler_paused:
            scheduler.pause_job('update')
            client.connect()
            scheduler_paused = True
        elif not client.connection_refused and scheduler_paused:
            scheduler.resume_job('update')
            scheduler_paused = False


