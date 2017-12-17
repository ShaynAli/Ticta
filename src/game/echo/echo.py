import sys
import socket
from threading import Thread
from itertools import count
# sys.path.append('..')


# TODO: Write for logging, should be able to log ClientThreads, Server, Games, etc to console and file
class Logger:
    pass


BUFFER_SIZE = 1024


class Client:

    def __init__(self):
        self.socket = socket.socket()

    def connect(self, address):
        try:
            self.socket.connect(address)
        except Exception as e:
            print('Unable to connect')
            print(e)
        finally:
            self.socket.close()

    def send(self, msg):
        try:
            self.socket.send(msg.encode())
        except Exception as e:
            print('Unable to send, ensure you\'re connected before sending')
            print(e)

    def recieve(self):
        print(self.socket.recv(BUFFER_SIZE))


class EchoServer:

    def __init__(self, port, backlog):
        self.socket = socket.socket()
        self.socket.bind((socket.gethostname(), port))
        self.backlog = backlog

    def listen(self):
        self.socket.listen(self.backlog)
        while True:
            client_socket, address = self.socket.accept()
            ClientThread(client_socket, address)

    def log(self, msg):
        print(msg)

    class ClientThread(Thread):

        thread_no = (i for i in count())

        def __init__(self, socket, address):
            super().__init__()
            self.thread_no = ClientThread.thread_no.__next__()
            self.socket = socket
            self.address = address
            print('ClientThread ', str(self.thread_no), ' created at ', str((socket, address)))
            self.start()

        def run(self):
            while True:
                client_msg = self.socket.recv(BUFFER_SIZE).decode()
                self.log('Client sent: ' + str(client_msg))
                self.socket.send(b'You sent: ' + client_msg.encode())

        def log(self, msg):
            print('ClientThread ' + str(self.thread_no) + ': ' + str(msg))

# class EchoServer:
#
#     def __init__(self, clients, backlog=32):
#         self.clients = clients
#         self.backlog = backlog
#         self.messages = []
#         self.action_tree = {
#             'msg': add_msg
#         }
#         self.listen_thread = Thread(target=self.listen, kwargs={'port': port})
#
#     def listen(self, port):
#         access_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         access_socket.bind((socket.gethostname(), port))
#         access_socket.listen(self.backlog)
#         while True:
#             t = Thread()
#
#     def run_game(self):
#         for c in cycle(self.clients):
#             pass
#
#     def restart(self):
#         pass
#
#     def add_msg(self, msg):
#         self.messages.append(msg)
#         print('Received ' + msg)
#
#     def add_msgs(self):
#         for msg in self.messages:
#             self.add_msg(msg)
#
#     def action(self, client, action, args):
#         if action in self.action_tree:
#             self.action_tree[action](*args)
