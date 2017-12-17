''' server.py - Deals with a game server '''
import sys, socket, socketserver, time
from threading import Thread
from multiprocessing.pool import ThreadPool
from ast import literal_eval
sys.path.append('..')
from common.constants import SERVER_HOST, SERVER_PORT, CLIENT_PORT_RANGE

# TODO: Detect when a client disconnects and react accordingly


class Client:
    ''' A class for the server to deal with connected client '''
    BUFFER_SIZE = 1024

    def __init__(self, socket):
        self.socket = socket

    def send(self, data):
        self.socket.send(str(data).encode())

    def receive(self):
        return self.socket.receive(BUFFER_SIZE).decode()

    def disconnect(self):
        self.socket.close()


class Server:

    SOCKET_BACKLOG = 32
    SLEEP = 0.2

    def __init__(self, port):
        # Set up the listening thread
        self.listening_thread = Thread(target=self.listen, kwargs={'port': port})
        self.wait_queue = []
        self.clients = set()

    def listen(self, port):
        access_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        access_socket.bind((socket.gethostname(), port))
        access_socket.listen(Server.SOCKET_BACKLOG)
        while True:
            self.add_client(access_socket.accept()[0])  # accept() returns (socket, address), we just want the socket
            time.sleep(Server.SLEEP)

    def add_client(self, socket):
        client = Client(socket)
        self.wait_queue.append(client)
        self.clients.add(client)

    def disconnect_all(self):
        for client in self.clients:
            client.disconnect()

    class MMServer:
        ''' A matchmaking server '''
        pass

    class GameServer:
        ''' A server running a game.py '''
        def __init__(self, game):
            self.game = game

        def action(self):
            '''
            Process an action from the client
            '''
            pass
