import sys
from threading import Thread
from time import sleep
import string
from random import shuffle
sys.path.append('..\..')
from abstracts.action import ActionServer, ActionClient
from presentation.interface import TTTGUI

NEW_GAME = 'new-game'
MOVE = 'move'
DISCONNECT = 'disconnect'
QUIT = 'quit'


class TTTClient(ActionClient, TTTGUI):

    def __init__(self):
        super().__init__()
        self.action_tree = {
            NEW_GAME: ' ',
            MOVE: ' ',
            DISCONNECT: ' ',
            QUIT: ' ',
        }

    def play(self):
        self.log('Playing')
        # gui_thread = Thread(target=)
        listen_thread = Thread(target=self.listen4action)
        # send_thread = Thread(target=)
        listen_thread.start()
        tick = 0
        while self.connected:
            i = tick % 10
            if i:
                self.log('Connected')
            sleep(self.frequency)

    def new_game(self, event):
        pass

    def move(self, event, row, col):
        pass

    def quit(self, event):
        pass


class TTTServer(ActionServer):

    # Behind the scenes, letters are used to represent players
    EMPTY = '0'
    PLAYER_SYMBOLS = string.ascii_letters
    SYM_ATTR = 'symbol'

    @staticmethod
    def max_players():
        return len(TTTServer.PLAYER_SYMBOLS)

    def __init__(self, players, board_size=3, auto_restart=False, port=12000):
        super().__init__(port)
        if len(players) > TTTServer.max_players():
            raise RuntimeError('Too many players, can have at most ' + str(TTTServer.max_players()))
        self.board_size = board_size
        self.board = self.init_board(self.board_size)
        self.players = players
        symbols = list(TTTServer.PLAYER_SYMBOLS)
        shuffle(symbols)
        self.symbol = {p: s for p, s in zip(players, symbols)}
        self.turns = []
        self.auto_restart = auto_restart
        self.current_player = None

    def reinit(self, players=None, board_size=None, auto_restart=None):
        '''
        Re-initializes the game
        :param board_size: A new board size to change the game to, set to None to use the same size as before
        :param players: Use a new set of players, set to None to use the same players before
        :param auto_restart: Restart the game immediately after it ends
        '''
        self.board_size = board_size if board_size is not None else self.board_size
        self.board = self.init_board(self.board_size)
        self.players = players if players is not None else self.players
        self.turns = []
        self.auto_restart = auto_restart if auto_restart is not None else self.auto_restart

    def init_board(self, board_size):
        '''
        FIlls Produces an empty board
        :param board_size: The dimensions of the board such that the board will have dimensions board_size x board_size
        :return: An empty board
        '''
        return [[TTTServer.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]

    def run_game(self):
        players = (p for p in cycle(self.players))
        win, tie = False, False
        while not (win or tie):
            self.current_player = players.__next__()
            self.disp_all_board()  # TODO: Remove
            self.disp_all('Player ' + self.symbol[player] + '\'s turn')  # TODO: Change to set message
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
            row, col = (self.input_row(player), self.input_col(player))
            while not (self.take(player, row, col)):
                if not self.valid_pos(row, col):
                    self.disp(player, 'That position is invalid')
                elif self.board[row][col] == self.symbol[player]:
                    self.disp(player, 'You already have that position!')
                else:
                    self.disp(player, 'That position has already been taken by player ' + self.board[row][col])
                row, col = (self.input_row(player), self.input_col(player))
            self.disp(player, 'You made a move on ' + str(row + 1) + ', ' + str(col + 1))
            self.turns.append((player, (row, col)))
            return row, col
        raise RuntimeWarning('Player ' + str(player) + ' attempted turn when not current player')

    def disp(self, player, string):
        player.display(string)

    def disp_board(self, player):
        self.disp(player, self.__repr__())

    def disp_all(self, string):
        for p in self.players:
            self.disp(p, string)

    def disp_all_board(self):
        self.disp_all(self.__repr__())

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

    def take(self, player, row, col):
        '''
        Allows the player to take a position if that position is valid
        :param player: The player making the move
        :param row: The row to try and take
        :param col: The column to try and take
        :return: Returns True if the position is taken and False is the move was invalid, i.e. the position was not on
            the board or the position was taken
        '''
        if player is self.current_player and self.takeable(row, col):  # Take if you can
            self.board[row][col] = self.symbol[player]
            return True  # Success
        return False  # Failure

    def win(self, player):
        self.disp_all('Player ' + self.symbol[player] + ' wins!')

    def tie(self):
        self.disp_all('Tie game.py!')

    def restart(self):
        self.disp_all('Restarting...')
        self.reinit()
        self.welcome()
        self.run_game()

    def input_row(self, player):
        return int(player.prompt('Choose a row: ',
                                 lambda row: row.isdigit() and self.valid_row_no(int(row) - 1),
                                 'Please enter an integer from 1 to ' + str(self.n_rows()) +
                                 ' for the row number: ')) - 1

    def input_col(self, player):
        return int(player.prompt('Choose a column: ',
                                 lambda col: col.isdigit() and self.valid_col_no(int(col) - 1),
                                 'Please enter an integer from 1 to ' + str(self.n_cols()) +
                                 ' for the column number: ')) - 1

