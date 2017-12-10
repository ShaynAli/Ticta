''' tictactoe.py - Runs the tic tac toe game '''

from itertools import zip_longest


class Game:

    EMPTY = '0'

    def __init__(self, n_players=2, board_size=3):
        '''
        Starts a tic tac toe game
        :param players: A list of Players
        '''
        self.board = [[Game.EMPTY for _ in range(board_size)] for _ in range(board_size)]
        self.players = [Game.Player(self) for _ in range(n_players)]
        self.run_game()

    def __repr__(self):
        return '\n'.join(([' '.join(str(i) for i in row) for row in self.board]))

    def run_game(self):

        player_no = 0

        while not self.end_of_game():
            self.players[player_no].turn()

    def end_of_game(self):
        pass

    def n_rows(self):
        return len(self.board)

    def n_cols(self):
        return len(self.board[0])

    def valid_row_no(self, row_no):
        return 0 <= row_no < self.n_rows()

    def valid_col_no(self, col_no):
        return 0 <= col_no < self.n_cols()

    class Player:

        def __init__(self, game):
            self.game = game
            pass

        def turn(self):
            pass

        def prompt_for_turn(self):
            valid_pos = False
            while not valid_pos:
                row = input('Choose a row')
                while not (row.isdigit() and self.game.valid_row_no(int(row))):
                    row = input('Please enter an integer from 1 to ' + self.game.n_rows() + ' for the number of rows')
                row = int(row) - 1
                col = input('Choose a column')
                while not (col.isdigit() and self.game.valid_col_no(int(col))):
                    col = input('Please enter an integer from 1 to ' + self.game.n_cols() + ' for the number of columns')
                col = int(col) - 1
                valid_pos = self.game.board[row][col] == self.game.EMPTY
            # print('You take ')





g = Game()
print(g)
