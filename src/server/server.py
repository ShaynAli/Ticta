''' server.py - Deals with a game server '''
import socket
from threading import Thread

from src.game import interaface


<<<<<<< HEAD
class Client(Thread):
    def __init__(self, connections):
=======
class Server(Thread):
    def __init__(self, connections, number_players, board_size):
>>>>>>> 1cc1ab0ec56c8aee663a43f2bfc4d6a07d8ad596
        Thread.__init__(self)
        self.connections = connections
        self.number_players = number_players
        self.board_size = board_size
        self.game = interaface.GameInterface(number_players, board_size)

    def game_logic(self, move, player):
        return self.game.computeTurn(move, player)

    def turn(self, turn):
        for i in range(0, len(self.connections)-1):
            if i == turn:
                self.connections[i].send('turn'.encode())
            else:
                self.connections[i].send('wait'.encode())
        data = self.connections[turn].recv(2048)
        print(data.decode())
        for i in range(0, len(self.connections)-1):
            if i != turn:
                self.connections[i].send(data)
        return data.decode

    # todo
    '''
    Custom win condition - probably send the data to the player so that it can be properly displayed to the player
    :param player_number: number of the player who won
    :param win_type: either column, row, diagonal or timeout
    :param column_row_number: the number of the column, row or diagonal that the win occured on
    '''
    def on_win(self, player_number, win_type, column_row_number):
        if win_type == 'column':
            pass
        if win_type == 'row':
            pass
        if win_type == 'diagonal':
            pass
        if win_type == 'timeout':
            pass

    # todo
    '''
    Custom draw condition - send draw to players probably
    '''
    def on_draw(self):
        pass

    def run(self):

        win = True
        while win:
            for i in range(0, len(self.number_players)-1):
                success = 0
                while success == 0:
                    data = self.turn(i)
                    message = self.game_logic(data, turn).split
                    success = message[0]
                if success == 2:
                    win = false
                    if message[1] == 'win':
                        self.on_win(message[2], message[3], message[4])
                    if message[2] == 'draw':
                        self.on_draw()
                    break
        # end of game here
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
    print(port)
    connections.append(conn)

    if len(connections) == 1:
        conn.send('Waiting for player to match'.encode())

    if len(connections) == 2:
        newthread = Client(connections)
        newthread.start()

        emptyArr = []
        connections = emptyArr
