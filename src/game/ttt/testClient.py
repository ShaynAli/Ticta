import socket


port = 12000
address = '127.0.0.1'

client_socket = socket.socket()
client_socket.bind(('127.0.0.1', 12021))
client_socket.connect((address, port))
while True:
    print(client_socket.recv(1024).decode())
    client_socket.send(input('\ninput: ').encode())
