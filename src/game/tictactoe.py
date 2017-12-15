''' tictactoe.py - Runs the tic tac toe game '''

import string
import random
from itertools import cycle

# Future TODO: Check if game will end in a tie


class TicTacToe:

    EMPTY = '0'
    PLAYER_SYMBOLS = string.ascii_letters
    SYM_ATTR = 'symbol'

    @staticmethod
    def max_players():
        return len(TicTacToe.PLAYER_SYMBOLS)

    def __init__(self, players, board_size=3, auto_restart=False):
        '''
        Starts a tic tac toe game
        :param players: A list of Players
        '''
        if len(players) > TicTacToe.max_players():
            raise RuntimeError('Too many players, can have at most ' + str(TicTacToe.max_players()))
        self.board_size = board_size
        self.board = self.init_board(self.board_size)
        self.players = self.init_players(players)
        self.turns = []
        self.auto_restart = auto_restart
        self.welcome()

    # Initialization

    def init_board(self, board_size):
        '''
        FIlls Produces an empty board
        :param board_size: The dimensions of the board such that the board will have dimensions board_size x board_size
        :return: An empty board
        '''
        return [[TicTacToe.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]

    def init_players(self, players):
        '''
        Initializes the players, providing them with symbols
        :param players: A list of Player objects from the game module
        :return: The provided player list after initialization
        '''
        # Set up symbols for players
        symbols = list(TicTacToe.PLAYER_SYMBOLS)
        random.shuffle(symbols)
        symbols = (s for s in symbols)
        # Initialize players
        self.players = players
        for player in players:
            setattr(player, TicTacToe.SYM_ATTR, symbols.__next__())
        return players

    def reinit(self, players=None, board_size=None, auto_restart=None):
        '''
        Re-initializes the game
        :param board_size: A new board size to change the game to, set to None to use the same size as before
        :param players: Use a new set of players, set to None to use the same players before
        '''
        self.board_size = board_size if board_size is not None else self.board_size
        self.board = self.init_board(self.board_size)
        self.players = self.init_players(players) if players is not None else self.players
        self.turns = []
        self.auto_restart = auto_restart if auto_restart is not None else self.auto_restart

    # Game flow

    def welcome(self):
        print('Welcome to a new game of Tic Tac Toe!')

    def run_game(self):
        players = (p for p in cycle(self.players))
        player = players.__next__()
        win, tie = False, False
        while not (win or tie):
            player = players.__next__()
            self.display()
            win = self.check_win(player, *self.turn(player))
            tie = self.check_tie()
        if win:
            self.win(player)
        elif tie:
            self.tie()
        else:
            raise RuntimeError('Game is finished but not won or tied')
        self.display()
        if self.auto_restart:
            self.restart()
        # TODO: Add prompt to restart

    def turn(self, player):
        print('Player ' + self.symbol(player) + '\'s turn')
        row, col = (self.input_row(player), self.input_col(player))
        while not (self.take(player, row, col)):
            if not self.valid_pos(row, col):
                print('That position is invalid')
            elif self.board[row][col] == self.symbol(player):
                print('You already have that position!')
            else:
                print('That position has already been taken by player ' + self.board[row][col])
            row, col = (self.input_row(player), self.input_col(player))
        print('You made a move on ' + str(row + 1) + ', ' + str(col + 1))
        self.turns.append((player, (row, col)))
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

    def take(self, player, row, col):
        if self.valid_pos(row, col) and not self.taken_pos(row, col):
            self.board[row][col] = self.symbol(player)
            return True
        return False

    def win(self, player):
        print('Player ' + self.symbol(player) + ' wins!')

    def tie(self):
        print('Tie game!')

    def restart(self):
        print('Restarting...')
        self.reinit()
        self.welcome()
        self.run_game()

    # Utilities

    def symbol(self, player):
        '''
        Get the symbol of a player
        :param player: The player whose symbol will be retrieved
        :return: A character, representing the symbol of the given player
        '''
        return getattr(player, TicTacToe.SYM_ATTR)

    def __repr__(self):
        return '\n'.join(([' '.join(str(i) for i in row) for row in self.board]))

    def display(self):
        print(self.__repr__())

    # Checks

    def check_win(self, player, row, col):
        '''
        Checks if a given move was a winning move
        :param player: The player making the move
        :param row: The row the move was made on
        :param col: The column the move was made on
        '''
        # Check row, columns, and diagonals
        move = (player, row, col)
        li = [self.maj_diag_win(*move), self.min_diag_win(*move), self.row_win(*move), self.col_win(*move)]
        return any(li)

    def maj_diag_win(self, player, row, col):
        return row == col and \
               all([self.board[i][i] == self.symbol(player) for i in range(min(self.n_rows(), self.n_cols()))])

    def min_diag_win(self, player, row, col):
        return (row + col == self.n_rows() or row + col == self.n_cols()) \
               and all([self.board[-i-1][i] == self.symbol(player) for i in range(min(self.n_rows(), self.n_cols()))])

    def row_win(self, player, row, col):
        return all([self.board[row][i] == self.symbol(player) for i in range(self.n_cols())])

    def col_win(self, player, row, col):
        return all([self.board[i][col] == self.symbol(player) for i in range(self.n_rows())])

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


N_PLAYERS = 1
BOARD_SIZE = 5

from game import Player
players = [Player() for _ in range(N_PLAYERS)]
g = TicTacToe(players, BOARD_SIZE)
g.run_game()
