''' server.py - Deals with a game server '''
import socket
from threading import Thread
from itertools import count
from time import sleep


class Server:

    def __init__(self, port, backlog=32, verbosity=0):
        self.verbosity = verbosity
        self.log('Starting server')
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket()
        self.online = True

    def listen(self):
        listen_address = (socket.gethostname(), self.port)
        self.socket.bind(listen_address)
        self.socket.listen(self.backlog)
        self.log('Listening on ' + str(listen_address))
        while self.online:
            client_socket, client_address = self.socket.accept()
            self.log('Accepted connection at ' + str(client_address))
            client = Server.ClientThread(self, client_socket, client_address, self.verbosity//2)
            client.start()

    def log(self, msg, level=0):
        if level <= self.verbosity:
            print(msg)

    class ClientThread(Thread):

        thread_no = (i for i in count())

        def __init__(self, server, socket, address, frequency=0.02, buffer_size=1024, verbosity=0):
            self.server = server
            super().__init__()
            self.thread_no = Server.ClientThread.thread_no.__next__()
            self.socket = socket
            self.address = address
            self.disconnected = False
            self.frequency = frequency
            self.buffer_size = buffer_size
            self.verbosity = verbosity
            self.log('ClientThread ' + str(self.thread_no) + ' created at ' + str(address))

        def send(self, msg):
            if not msg:
                return
            try:
                self.socket.send(msg.encode())
            except Exception as e:
                self.log('Unable to send to client')
                raise e

        def receive(self):
            try:
                return self.socket.recv(self.buffer_size).decode()
            except Exception as e:
                self.log('Unable to receive from client')
                raise e

        def run(self):
            while not self.disconnected:
                self.action(self.receive())
                sleep(self.frequency)

        def action(self, msg):
            if msg:
                self.log('Received: ' + str(msg))

        def log(self, msg, level=0):
            if level <= self.verbosity:
                print('ClientThread ' + str(self.thread_no) + ': ' + str(msg))
