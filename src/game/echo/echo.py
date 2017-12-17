import sys
import socket
from select import select
from threading import Thread
from itertools import count


# TODO: Write for logging, should be able to log ClientThreads, Server, Games, etc to console and file
class Logger:
    pass


# TODO: Commentify


BUFFER_SIZE = 1024
SERVER_IP = socket.gethostname()
SERVER_PORT = 12000


class Client:

    EXIT_MSG = 'done'

    def __init__(self):
        self.socket = socket.socket()

    def connect(self, address=(SERVER_IP, SERVER_PORT)):
        print('Attempting to connect to ' + str(address))
        try:
            self.socket.connect(address)
        except Exception as e:
            print('Unable to connect')
            raise e
        print('Connected to ' + str(address))
        print('Type ' + Client.EXIT_MSG + ' to exit at any time')

    def play(self):
        try:
            out_msg = input('Send to server: ')
            while out_msg != Client.EXIT_MSG:
                if self.send(out_msg):  # Only if a message is sent
                    print('Waiting on reply')
                    in_msg = self.receive()
                    print('Server reply: ' + in_msg)
                out_msg = input('Send to server: ')
        except EOFError:
            print('Exiting')

    def send(self, msg):
        try:
            self.socket.send(msg.encode())
            return True
        except EOFError:
            return False
            # TODO: Deal with exit with EOF
        except Exception as e:
            print('Unable to send, ensure you\'re connected before sending')
            print(e)

    def receive(self):
        try:
            return self.socket.recv(BUFFER_SIZE).decode()
        except ConnectionAbortedError:
            print('Server disconnected')


class Server:

    EXIT_MSG = 'done'

    def __init__(self, port=SERVER_PORT, backlog=32):
        print('Starting server')
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket()
        self.online = True

    def exit(self, c_in):
        return c_in != Server.EXIT_MSG

    def listen(self):
        listen_address = (socket.gethostname(), self.port)
        self.socket.bind(listen_address)
        self.socket.listen(self.backlog)
        print('Listening on ' + str(listen_address))
        while self.online:
            client_socket, client_address = self.socket.accept()
            print('Accepted connection at ' + str(client_address))
            client = Server.ClientThread(client_socket, client_address)
            client.start()

    def log(self, msg):
        print(msg)

    class ClientThread(Thread):

        thread_no = (i for i in count())

        def __init__(self, socket, address):
            super().__init__()
            self.thread_no = Server.ClientThread.thread_no.__next__()
            self.socket = socket
            self.address = address
            self.disconnected = False
            print('ClientThread ' + str(self.thread_no) + ' created at ', str(address))

        def send(self, msg):
            if not msg:
                return
            try:
                self.socket.send(msg.encode())
            except Exception as e:
                print('Unable to send to client')
                print(e)

        def receive(self):
            try:
                return self.socket.recv(BUFFER_SIZE).decode()
            except ConnectionAbortedError:
                self.log('Client disconnected')
                self.disconnected = True

        def run(self):
            # TODO - Detect disconnection, possibly with select
            # See Socket Programming HOWTO by McMillan
            while not self.disconnected:
                self.reply_to(self.receive())

        def reply_to(self, msg):
            self.log('Received: ' + str(msg))
            self.send('You sent: ' + str(msg))

        def log(self, msg):
            print('ClientThread ' + str(self.thread_no) + ': ' + str(msg))
