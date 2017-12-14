''' server.py - Deals with a game server '''
import socket
from threading import Thread
from ..client.factories import ClientFactory
import sys


IP = '127.0.0.1'
port = 2020


class Server(Thread):

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, port))
        self.clients = []
        self.wait_for_connection()

    def wait_for_connection(self):
        while True:
            connection_socket, address = self.server_socket.accept()
            self.clients.append(ClientFactory.ClientFactory.create_client(connection_socket, address))

    def terminator(self):
        for client in self.clients:
            client.terminator()


server = Server()
print('Server Online, type help for commands')
while True:
    message = input()
    if message == 'help':
        print('')
    if message == 'exit':
        server.terminator()
        sys.exit()
    else:
        print('Not a valid command')


