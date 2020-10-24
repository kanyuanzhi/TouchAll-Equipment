from apscheduler.schedulers.blocking import BlockingScheduler
from equipment import Equipment
from socket_client import Client


def register(equipment, client):
    client.send(equipment.basic_information())


def update(equipment, client):
    client.send(equipment.status())


if __name__ == "__main__":
    equipment = Equipment()
    client = Client("localhost", 9090)
