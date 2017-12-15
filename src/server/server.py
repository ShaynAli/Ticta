''' server.py - Deals with a game server '''
import socket
from threading import Thread
from src.client.factories import client_factory
import sys


class Server:

    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(20)
        self.clients = []

    def wait_for_connection(self):
        while True:
            connection_socket, address = self.server_socket.accept()
            self.add_client(connection_socket, address)

    def add_client(self, connection_socket, address):
        self.clients.append(client_factory.ClientFactory.create_client(connection_socket, address))

    def terminator(self):
        for client in self.clients:
            client.terminator()


class ServerConsole:

    def __init__(self, ip='127.0.0.1', port=3030):
        self.server = Server(ip, port)
        self.wait_thread = Thread(target=self.server.wait_for_connection)

    def start_server(self):
        self.wait_thread.start()

    def console(self):
        self.start_server()
        print('Server Online, type help for commands')
        while True:
            message = input('>')
            if message == 'help':
                print('')
            elif message == 'exit':
                sys.exit()
            else:
                print('Not a valid command')


if __name__ == '__main__':
    console = ServerConsole()
    console_thread = Thread(target=console.console)
    console_thread.start()
    console_thread.join()

