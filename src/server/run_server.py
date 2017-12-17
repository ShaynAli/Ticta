import socket
from server import Server
# from common.constants import SERVER_PORT

server = Server(12000)
server.listen()
