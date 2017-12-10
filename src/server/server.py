''' server.py - Deals with a game server '''
import socket
from threading import Thread


class Server(Thread):
    def __init__(self, connections):
        Thread.__init__(self)
        self.connections = connections

    def run(self):

        win = True
        while win:
            self.connections[0].send('Turn'.encode())
            self.connections[1].send('Wait'.encode())
            data = self.connections[0].recv(2048)
            print(data.decode())
            self.connections[1].send(data)

            #game logic here

            self.connections[1].send('Turn'.encode())
            self.connections[0].send('Wait'.encode())
            data = self.connections[1].recv(2048)
            print(data.decode())
            self.connections[0].send(data)

            #game logic here
        #and maybe here

        self.connections[0].send('end')
        self.connections[1].send('end')


IP = '127.0.0.1'
PORT = 12000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
connections = []

while True:
    server.listen()
    print("Waiting for connections...")
    (conn, (ip, port)) = server.accept()
    connections.append(conn)

    if len(connections) == 1:
        conn.send('Waiting for player to match'.encode())

    if len(connections) == 2:
        newthread = Server(connections)
        newthread.start()

        emptyArr = []
        connections = emptyArr
