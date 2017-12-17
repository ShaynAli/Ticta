''' client.py - Deals with a game client '''
import socket
sys.path.append('..')
from common.constants import SERVER_HOST, SERVER_PORT, CLIENT_PORT_RANGE


class Client:
    ''' A class for the client to communicate with the server '''

    def __init__(self, buffer_size=1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = buffer_size

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, data):
        self.socket.send(str(data).encode())

    def receive(self):
        self.socket.recv(self.buffer_size)

    def disconnect(self):
        self.socket.close()
