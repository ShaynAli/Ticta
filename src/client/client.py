''' client.py - Deals with a game client '''
from src.client.abstract.AbstractClient import Client
from abc import ABCMeta, abstractmethod


class Client(Client):

    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address

    def receive_from_server(self):
        return self.client_socket.recv(1024).decode()

    def send_to_client(self, message):
        self.client_socket.send(message.encode())

    def terminator(self):
        self.client_socket.close()


host = '127.0.0.1'
port = 12000


# BUFFER_SIZE = 1024
# MESSAGE = " "
# def send_move_server(server_socket, column_number, row_number):
#     message = 'move' + ' ' + str(column_number) + ' ' + str(row_number)
#     server_socket.send(message.encode())
#
# def opponent_move():
#     pass
#
# def on_win():
#     pass
#
# def on_draw():
#     pass
#
#
# gameEnd = False
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.connect((host, port))
#
# data = server.recv(BUFFER_SIZE)
# print(data.decode())
#
# if data.decode() == 'Waiting for player to match':
#     data = server.recv(BUFFER_SIZE)
#     print(data.decode())
#
# data = data.decode()
# while data != 'end':
#
#     if data == 'Turn':
#         # will need to be user interface but console works for testing
#         column = input("Enter your column:")
#         row = input ('Enter your row:')
#         send_move_server(server, column, row)
#     if data == 'wait':
#         data = server.recv(BUFFER_SIZE)
#         if data == 'move':
#             opponent_move()
#     if data == 'win':
#         on_win()
#     if data == 'draw':
#         on_draw()
#
#
#
#
#     data = client.recv(BUFFER_SIZE)
#     print("Opponent move:", data.decode())
#     data = client.recv(BUFFER_SIZE)
#
#
#
# client.close()
