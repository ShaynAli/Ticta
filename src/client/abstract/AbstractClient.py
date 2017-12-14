''' Abstract Client '''
from abc import ABCMeta, abstractmethod


class Client(metaclass=ABCMeta):

    def receive_from_client(self):
        pass

    def send_to_client(self):
        pass

