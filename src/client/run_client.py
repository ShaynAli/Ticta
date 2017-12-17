import socket
from client import Client

client = Client()
client.connect((socket.gethostname(), 12000))
client.play()
