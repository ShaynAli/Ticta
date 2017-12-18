''' client.py - Deals with a game client '''
import socket
from ast import literal_eval


class Client:

    EXIT_MSG = 'done'

    def __init__(self, verbose=True, buffer_size=1024):
        self.socket = socket.socket()
        self.buffer_size = buffer_size

    def connect(self, address):
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
            while out_msg and out_msg != Client.EXIT_MSG:
                self.send(out_msg)  # Only if a message is sent
                out_msg = input('Send to server: ')
        except EOFError:
            print('Exiting')
            self.socket.close()

    def send(self, msg):
        if not msg:
            return
        try:
            self.socket.send(msg.encode())
        except EOFError as e:
            raise e
        except Exception as e:
            print('Unable to send, ensure you\'re connected before sending')
            print(e)

    def receive(self):
        try:
            return self.socket.recv(self.buffer_size).decode()
        except(ConnectionAbortedError, EOFError):
            print('Server disconnected')
