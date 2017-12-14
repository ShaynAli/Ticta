''' client.py - Deals with a game client '''
import socket

host = '127.0.0.1'
port = 12000
BUFFER_SIZE = 1024
MESSAGE = " "


def send_move_server(server_socket, column_number, row_number):
    message = 'move' + ' ' + str(column_number) + ' ' + str(row_number)
    server_socket.send(message.encode())

def opponent_move():
    pass

def on_win():
    pass

def on_draw():
    pass


gameEnd = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))

data = server.recv(BUFFER_SIZE)
print(data.decode())

if data.decode() == 'Waiting for player to match':
    data = server.recv(BUFFER_SIZE)
    print(data.decode())

data = data.decode()
while data != 'end':

    if data == 'Turn':
        # will need to be user interface but console works for testing
        column = input("Enter your column:")
        row = input ('Enter your row:')
        send_move_server(server, column, row)
    if data == 'wait':
        data = server.recv(BUFFER_SIZE)
        if data == 'move':
            opponent_move()
    if data == 'win':
        on_win()
    if data == 'draw':
        on_draw()



<<<<<<< HEAD
    data = client.recv(BUFFER_SIZE)
    print("Opponent move:", data.decode())
    data = client.recv(BUFFER_SIZE)
=======
>>>>>>> 1cc1ab0ec56c8aee663a43f2bfc4d6a07d8ad596


client.close()
