from src.game.tictactoe import Game


class GameInterface:

    def __init__(self, number_players, board_size):
        self.game = Game(number_players, board_size)

    # todo
    def compute_turn(self, move, player):
        pass
