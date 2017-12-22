import socket
from ttt import TTTClient

client = TTTClient()
client.connect(("https://ticta-shaynali.c9users.io", 12000))
client.play()
