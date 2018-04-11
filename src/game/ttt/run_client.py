import socket
from ttt import TTTClient

client = TTTClient()
client.connect((socket.gethostname(), 12000))
client.play()
