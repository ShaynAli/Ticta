''' tictactoe.py - Runs the tic tac toe game '''

import string
import random
from itertools import cycle


# PLAYER_SYMBOLS = string.ascii_letters
# print(PLAYER_SYMBOLS)
# symbols = list(PLAYER_SYMBOLS)
# print(symbols)
# random.shuffle(symbols)
# print(symbols)
# sym_gen = (s for s in symbols)
# print(sym_gen)
# print(list(sym_gen))


class Game:

    EMPTY = '0'
    PLAYER_SYMBOLS = string.ascii_letters

    @staticmethod
    def max_players():
        return len(Game.PLAYER_SYMBOLS)

    def __init__(self, n_players=2, board_size=3):
        '''
        Starts a tic tac toe game
        :param players: A list of Players
        '''
        if n_players > Game.max_players():
            raise RuntimeError('Too many players, can have at most ' + str(Game.max_players()))
        # Initialize board
        self.board = [[Game.EMPTY for _ in range(board_size)] for _ in range(board_size)]
        # Set up symbols for players
        symbols = list(Game.PLAYER_SYMBOLS)
        random.shuffle(symbols)
        self.symbols = (s for s in symbols)
        # Initialize players
        self.players = [Game.Player(self) for _ in range(n_players)]

    def __repr__(self):
        return '\n'.join(([' '.join(str(i) for i in row) for row in self.board]))

    def run_game(self):

        players = (p for p in cycle(self.players))

        while not self.end_of_game():
            player = players.__next__()
            print('Player ' + player.symbol + '\'s turn')
            player.turn()
            print(self.__repr__())

    def end_of_game(self):  # TODO
        pass

    def new_symbol(self):
        '''
        :return: A new symbol for a player to use to mark the positions they take
        '''
        return self.symbols.__next__()

    def n_rows(self):
        return len(self.board)

    def n_cols(self):
        return len(self.board[0])

    def valid_row_no(self, row_no):
        return 0 <= row_no < self.n_rows()

    def valid_col_no(self, col_no):
        return 0 <= col_no < self.n_cols()

    def valid_pos(self, row_no, col_no):
        return self.valid_row_no(row_no) and self.valid_col_no(col_no)

    class Player:

        def __init__(self, game):
            self.game = game
            self.symbol = self.game.new_symbol()
            pass

        def turn(self):
            row, col = self.input_turn()
            self.game.board[row][col] = self.symbol
            print('You made a move on ' + str(row) + ', ' + str(col))

        def input_turn(self):
            row, col = (self.input_row(), self.input_col())
            valid_pos, free_pos = (self.game.valid_pos(row, col), self.game.board[row][col] == self.game.EMPTY)
            while not (valid_pos and free_pos):
                if not valid_pos:
                    print('That position is invalid')
                elif not free_pos:  # Can also be an independent 'if'
                    if self.game.board[row][col] == self.symbol:
                        print('You already have that position!')
                    else:
                        print('That position has already been taken by player ' + self.game.board[row][col])
                row, col = (self.input_row(), self.input_col())
                valid_pos, free_pos = (self.game.valid_pos(row, col), self.game.board[row][col] == self.game.EMPTY)
            return row, col

        def input_row(self):
            row = input('Choose a row: ')
            while not (row.isdigit() and self.game.valid_row_no(int(row))):
                row = input('Please enter an integer from 1 to ' + str(self.game.n_rows()) + ' for the number of rows: ')
            return int(row) - 1

        def input_col(self):
            col = input('Choose a column: ')
            while not (col.isdigit() and self.game.valid_col_no(int(col))):
                col = input('Please enter an integer from 1 to ' + str(self.game.n_cols()) + ' for the number of columns: ')
            return int(col) - 1


g = Game()
print(g)
g.run_game()
