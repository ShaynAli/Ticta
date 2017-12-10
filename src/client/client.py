''' client.py - Deals with a game client '''
import socket

host = '127.0.0.1'
port = 12000
BUFFER_SIZE = 1024
MESSAGE = " "

gameEnd = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

data = client.recv(BUFFER_SIZE)
print(data.decode())

if data.decode() == 'Waiting for player to match':
    data = client.recv(BUFFER_SIZE)
    print(data.decode())

#have a timer here for auto win if opponent doesnt make a move
while data != 'end':

    if data.decode() == 'Turn':
        MESSAGE = input("Enter your move or end:")
        client.send(MESSAGE.encode())

    #game logic

    if not gameEnd:
        print('Wait for opponent move')

    if MESSAGE == 'end':
        break

    data = client.recv(BUFFER_SIZE)
    data = client.recv(BUFFER_SIZE)
    print("Opponent move:", data.decode())


client.close()
