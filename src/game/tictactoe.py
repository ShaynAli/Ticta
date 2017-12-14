''' tictactoe.py - Runs the tic tac toe game '''

import string
import random
from itertools import cycle

SYM_ATTR = 'symbol'


class TicTacToe:

    EMPTY = '0'
    PLAYER_SYMBOLS = string.ascii_letters

    @staticmethod
    def max_players():
        return len(TicTacToe.PLAYER_SYMBOLS)

    def __init__(self, players, board_size=3):
        '''
        Starts a tic tac toe game
        :param players: A list of Players
        '''
        if len(players) > TicTacToe.max_players():
            raise RuntimeError('Too many players, can have at most ' + str(TicTacToe.max_players()))
        self.board_size = board_size
        self.board = self.init_board(self.board_size)
        self.players = self.init_players(players)
        self.welcome()

    def welcome(self):
        print('Welcome to a new game of Tic Tac Toe!')

    def init_board(self, board_size):
        return [[TicTacToe.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]

    def init_players(self, players):
        # Set up symbols for players
        symbols = list(TicTacToe.PLAYER_SYMBOLS)
        random.shuffle(symbols)
        symbols = (s for s in symbols)
        # Initialize players
        self.players = players
        for player in players:
            setattr(player, SYM_ATTR, symbols.__next__())
        return players

    def symbol(self, player):
        return getattr(player, SYM_ATTR)

    def __repr__(self):
        return '\n'.join(([' '.join(str(i) for i in row) for row in self.board]))

    def display(self):
        print(self.__repr__())

    def take(self, player, row, col):
        if self.valid_pos(row, col) and not self.taken_pos(row, col):
            self.board[row][col] = self.symbol(player)
            return True
        else:
            return False

    def run_game(self):
        self.display()
        players = (p for p in cycle(self.players))
        player = players.__next__()
        while not self.winning_move(player, *self.turn(player)):
            player = players.__next__()
            self.display()
        self.win(player)
        self.display()
        self.restart()

    def reinit(self, board_size=None, players=None):
        if board_size is not None:
            self.board_size = board_size
        self.board = self.init_board(self.board_size)
        if players is not None:
            self.players = self.init_players(players)

    def restart(self):
        print('Restarting...')
        self.reinit()
        self.welcome()
        self.run_game()

    def turn(self, player):
        print('Player ' + getattr(player, SYM_ATTR) + '\'s turn')
        row, col = (self.input_row(player), self.input_col(player))
        while not (self.take(player, row, col)):
            if not self.valid_pos(row, col):
                print('That position is invalid')
            elif self.board[row][col] == getattr(player, SYM_ATTR):
                print('You already have that position!')
            else:
                print('That position has already been taken by player ' + self.board[row][col])
            row, col = (self.input_row(player), self.input_col(player))
        print('You made a move on ' + str(row + 1) + ', ' + str(col + 1))
        return row, col

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

    def winning_move(self, player, row, col):
        # Check row, columns, and diagonals
        sym = self.symbol(player)
        row_win = all([self.board[row][i] == sym for i in range(self.n_cols())])
        col_win = all([self.board[i][col] == sym for i in range(self.n_rows())])
        maj_diag_win = row == col \
            and all([self.board[i][i] == sym for i in range(min(self.n_rows(), self.n_cols()))])
        min_diag_win = (row + col == self.n_rows() or row + col == self.n_cols()) \
            and all([self.board[-i-1][i] == sym for i in range(min(self.n_rows(), self.n_cols()))])
        if any([row_win, col_win, maj_diag_win, min_diag_win]):
            return True

    def win(self, player):
        print('Player ' + self.symbol(player) + ' wins!')

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


N_PLAYERS = 2
BOARD_SIZE = 3

from game import Player
players = [Player() for _ in range(N_PLAYERS)]
g = TicTacToe(players, BOARD_SIZE)
g.run_game()
