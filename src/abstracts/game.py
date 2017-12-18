''' game.py - Classes and functions for game flow '''
from abc import ABC, abstractmethod


class GameServer(ABC):

    @abstractmethod
    def __init__(self):
        ''' Initialize the server '''

    @abstractmethod
    def run_game(self):
        ''' Run the game '''

    @abstractmethod
    def restart(self):
        ''' Restart the game '''

    def action(self, player, act, **kwargs):
        ''' Allows a player to perform an action '''


class GameClient(ABC):

    @abstractmethod
    def __init__(self):
        ''' Initialize the client '''

    @abstractmethod
    def action(self, act, **kwargs):
        ''' Do some action in the game '''
