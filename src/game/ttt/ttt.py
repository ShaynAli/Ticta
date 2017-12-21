import sys
from os.path import sep
from threading import Thread
from time import sleep
import string
import socket
from random import shuffle
from itertools import cycle
from threading import Semaphore
sys.path.append('..' + sep + '..')
from abstracts.action import ActionServer, ActionClient, ClientThread
from presentation.interface import TTTGUI

NEW_GAME = 'new-game'
MOVE = 'move'
DISCONNECT = 'disconnect'
QUIT = 'quit'

SET_TITLE = 'set-title'
SET_MSG = 'set-msg'
SET_PLAYERS = 'set-players'
SET_BOARD = 'set-board'

PLAY = 'play'

# PROMPT = 'prompt'
# GET_ROW = 'get-row'
# GET_COL = 'get-col'

class TTTClient(ActionClient, TTTGUI):

    def __init__(self):
        ActionClient.__init__(self)
        TTTGUI.__init__(self)
        self.action_tree = {
            SET_MSG: self.set_message,
            SET_TITLE: self.set_title,
            SET_PLAYERS: self.set_players,
            SET_BOARD: self.set_board,
            PLAY: self.play,
        }
        self.running = False
        self.output_free = True

    def run_gui(self):
        self.running = True
        self.log('GUI running')
        self.start()

    def play(self):
        self.log('Playing')
        action_in_thread = Thread(target=self.listen4action)
        action_in_thread.start()
        # game_thread = Thread(target=self.game_loop)
        # game_thread.start()
        self.run_gui()  # This call eats babies

    def game_loop(self):
        while not self.running:
            sleep(self.frequency)
        self.log('Game running')
        while self.connected:
            sleep(self.frequency)

    def new_game(self):
        self.log('Attempting to start new game')
        self.send_action(NEW_GAME)

    def move(self, row, col):
        self.log('Attempting move at ' + str((row, col)))
        self.send_action(MOVE, row=row, col=col)

    def quit(self):
        global root
        self.log('Quitting')
        root.quit()
        sys.exit()

    def disconnect(self):
        self.log('Disconnecting')
        self.running = False
        self.send_action(DISCONNECT)

    def log(self, msg, level=0):
        while not self.output_free:
            sleep(self.frequency)
        self.output_free = False
        super().log(msg, level)
        self.output_free = True


class TTTServer(ActionServer):

    # Behind the scenes, letters are used to represent players
    EMPTY = '0'
    PLAYER_SYMBOLS = string.ascii_letters
    SYM_ATTR = 'symbol'

    @staticmethod
    def max_players():
        return len(TTTServer.PLAYER_SYMBOLS)

    def __init__(self, players=None, board_size=3, auto_restart=False, port=12000, master_server = None):
        super().__init__(port, client_type=TTTClientThread, server_type=TTTServer)
        self.board_size = board_size
        self.board = self.new_board(self.board_size)
        symbols = list(TTTServer.PLAYER_SYMBOLS)
        shuffle(symbols)
        self.symbol = {}
        self.turns = []
        self.auto_restart = auto_restart
        self.row = None
        self.col = None
        self.finished = Semaphore(0)
        self.start = Semaphore(1)
        self.players = players
        self.master_server = master_server
        if players is not None:
            if len(players) > TTTServer.max_players():
                raise RuntimeError('Too many players, can have at most ' + str(TTTServer.max_players()))
            self.current_player_number = None
            self.current_player = None
            for p in players:
                p.server = self
            self.players = players
            self.symbol = {p: s for p, s in zip(self.players, symbols)}
            for p in self.players:
                p.send_action(SET_PLAYERS, players=[v for k, v in self.symbol.items()])
                p.send_action(PLAY)
            self.game_thread = Thread(target=self.run_game)
            self.game_thread.start()

    def reinit(self, players=None, board_size=None, auto_restart=None):
        '''
        Re-initializes the game
        :param board_size: A new board size to change the game to, set to None to use the same size as before
        :param players: Use a new set of players, set to None to use the same players before
        :param auto_restart: Restart the game immediately after it ends
        '''
        self.board_size = board_size if board_size is not None else self.board_size
        self.board = self.new_board(self.board_size)
        self.players = players if players is not None else self.players
        self.turns = []
        self.auto_restart = auto_restart if auto_restart is not None else self.auto_restart

    def new_board(self, board_size):
        '''
        Produces an empty board
        :param board_size: The dimensions of the board such that the board will have dimensions board_size x board_size
        :return: An empty board
        '''
        return [[TTTServer.EMPTY for _ in range(board_size)] for _ in range(board_size)]

    def run_game(self):
        players = (p for p in cycle(self.players))
        win, tie = False, False
        while not (win or tie):
            self.current_player = players.__next__()
            self.start.release()
            # self.disp_all_board()  # TODO: Remove
            # self.disp_all('Player ' + self.symbol[self.current_player] + '\'s turn')  # TODO: Change to set message
            win = self.check_win(self.current_player, *self.turn(self.current_player))
            tie = self.check_tie()
        if win:
            self.win(self.current_player)
        elif tie:
            self.tie()
        else:
            raise RuntimeError('Game is finished but not won or tied')
        self.disp_all_board()
        if self.auto_restart:
            self.restart()
        # TODO: Add prompt to restart

    def turn(self, player):
        if player is self.current_player:
            player.send_action(SET_TITLE, text='Your turn!')
            sleep(0.05)
            player.send_action(SET_MSG, text='Click on a board position to take it')
            self.finished.acquire()
            row = self.row
            col = self.col

            # row, col = (self.input_row(player), self.input_col(player))  # TODO: Change
            # while not (self.take(player, row, col)):
            #     if not self.valid_pos(row, col):
            #         player.send_action(SET_MSG, text='That position is invalid')
            #     elif self.board[row][col] == self.symbol[player]:
            #         player.send_action(SET_MSG, text='You already have that position!')
            #     else:
            #         player.send_action(SET_MSG, text='That position has already been taken by player ' + self.board[row][col])
            #         # self.update_player_board(player, 'That position has already been taken by player ' + self.board[row][col])  # TODO: Change
            #     row, col = (self.input_row(player), self.input_col(player))
            player.send_action(SET_MSG, text='You made a move on ' + str(row + 1) + ', ' + str(col + 1))
            for p in self.players:
                p.send_action(SET_TITLE, text='Waiting')
                sleep(0.05)
                self.set_board(p, row, col)
            self.turns.append((player, (row, col)))
            return row, col
        player.send_action(SET_MSG, text='It\'s not your turn yet!')
        self.log_error(RuntimeWarning('Player ' + str(player) + ' attempted turn when not current player'))

    def set_board(self, player, row, col):
        player.send_action(SET_BOARD, player=self.board[row][col], row=row, col=col)

    # def update_player_board(self, player):
    #     for i in range(self.board_size):
    #         for j in range(self.board_size):
    #             player.send_action(SET_BOARD, player=self.board[i][j], row=i, col=j)

    # def disp_board(self, player):  # TODO: Remove
    #     self.update_player_board(player, self.__repr__())
    #
    # def disp_all(self, string):  # TODO: Remove
    #     for p in self.players:
    #         self.update_player_board(p, string)
    #
    # def disp_all_board(self):  # TODO: Remove
    #     self.disp_all(self.__repr__())

    def check_win(self, player, row, col):
        '''
        Checks if a given move was a winning move
        :param player: The player making the move
        :param row: The row the move was made on
        :param col: The column the move was made on
        '''
        # Check row, columns, and diagonals
        move = (player, row, col)
        return any([self.maj_diag_win(*move), self.min_diag_win(*move), self.row_win(*move), self.col_win(*move)])

    def maj_diag_win(self, player, row, col):
        return row == col and \
               all([self.board[i][i] == self.symbol[player] for i in range(min(self.n_rows(), self.n_cols()))])

    def min_diag_win(self, player, row, col):
        return (row + col == self.n_rows() or row + col == self.n_cols()) \
               and all([self.board[-i-1][i] == self.symbol[player] for i in range(min(self.n_rows(), self.n_cols()))])

    def row_win(self, player, row, col):
        return all([self.board[row][i] == self.symbol[player] for i in range(self.n_cols())])

    def col_win(self, player, row, col):
        return all([self.board[i][col] == self.symbol[player] for i in range(self.n_rows())])

    def check_tie(self):
        return len(self.turns) >= self.board_size**2  # Fewer turns have been played than the numbers of positions

    def n_rows(self):
        return self.board_size

    def n_cols(self):
        return self.board_size

    def valid_row_no(self, row_no):
        return 0 <= row_no < self.n_rows()

    def valid_col_no(self, col_no):
        return 0 <= col_no < self.n_cols()

    def valid_pos(self, row_no, col_no):
        return self.valid_row_no(row_no) and self.valid_col_no(col_no)

    def taken_pos(self, row, col):
        return True if not self.valid_pos(row, col) else self.board[row][col] != self.EMPTY

    def takeable(self, row, col):
        return self.valid_pos(row, col) and not self.taken_pos(row, col)

    def take(self, player, row, col):  # TODO: Change
        '''
        Allows the player to take a position if that position is valid
        :param player: The player making the move
        :param row: The row to try and take
        :param col: The column to try and take
        :return: Returns True if the position is taken and False is the move was invalid, i.e. the position was not on
            the board or the position was taken
        '''
        if self.players is None:
            return False
        row = int(row)
        col = int(col)
        self.start.acquire()
        if player is self.current_player and self.takeable(row, col):
            self.board[row][col] = self.symbol[player]
            self.row = row
            self.col = col
            self.finished.release()
            return True  # Success
        self.start.release()
        return False  # Failure

    def win(self, player):
        sleep(0.1)
        for p in self.players:
            if p == self.current_player:
                msg = 'win'
            else:
                msg = 'lose'
            p.send_action(SET_TITLE, text=msg)
            p.send_action(SET_MSG, text='You ' + msg+ '!')



    def tie(self):
        sleep(0.1)
        for p in self.players:
            p.send_action(SET_TITLE, text='Draw')
            p.send_action(SET_MSG, text="It's a tie!")


    def restart(self):
        self.disp_all('Restarting...')
        self.reinit()
        self.welcome()
        self.run_game()

    def input_row(self, player):  # TODO: Remove
        return int(player.prompt('Choose a row: ',
                                 lambda row: row.isdigit() and self.valid_row_no(int(row) - 1),
                                 'Please enter an integer from 1 to ' + str(self.n_rows()) +
                                 ' for the row number: ')) - 1

    def input_col(self, player):  # TODO: Remove
        return int(player.prompt('Choose a column: ',
                                 lambda col: col.isdigit() and self.valid_col_no(int(col) - 1),
                                 'Please enter an integer from 1 to ' + str(self.n_cols()) +
                                 ' for the column number: ')) - 1

    def listen4client(self):
        listen_address = (socket.gethostname(), self.port)
        self.socket.bind(listen_address)
        self.socket.listen(self.backlog)
        self.log('Listening on ' + str(listen_address))
        i = 0
        while self.online:
            try:
                client_socket, client_address = self.socket.accept()
                self.log('Accepted connection at ' + str(client_address))
                client = self.client_type(server=self, socket=client_socket, address=client_address)
                client.start()
                self.clients.add(client)
                i += 1
                if len(self.clients) >= 2:
                    self.server_type(self.clients, master_server=self)
                    self.clients = set()
            except OSError:
                self.log('Listening socket closed')
            except Exception as e:
                self.log_error(e)


class TTTClientThread(ClientThread):

    def __init__(self, server, socket, address, players=[], frequency=0.01, buffer_size=1024, verbosity=0):
        ClientThread.__init__(self, server, socket, address,
                              frequency=frequency, buffer_size=buffer_size, verbosity=verbosity)
        self.action_tree = {  # TODO: Implement
            NEW_GAME: self.new_game,
            MOVE: self.move,
            DISCONNECT: self.disconnect,
            QUIT: self.quit,
        }

    def process_action(self, act_msg):
        self.log('Processing action: ' + act_msg)
        super().process_action(act_msg)

    def new_game(self):
        pass

    def move(self, row, col):
        if self.server.take(self, row, col):
            self.send_action(SET_BOARD, row=row, col=col, player=self.server.symbol[self])

    def disconnect(self):
        pass
        # self.server.end_game('Player disconnected')  # TODO: Implement

    # def send_players(self, players):
    #     self.send_action(SET_PLAYERS, players=players)

    def quit(self):
        pass  # TODO
