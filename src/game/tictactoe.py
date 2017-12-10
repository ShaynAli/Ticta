''' tictactoe.py - Runs the tic tac toe game '''


class Game:

    def __init__(self, players, board_size=3):
        '''
        Starts a tic tac toe game
        :param players: A list of player clients
        '''
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        pass

    def __repr__(self):
        pass
