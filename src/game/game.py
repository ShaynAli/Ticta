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

    def action(self, player, action):
        ''' Allows a player to perform an action '''


class GameClient(ABC):

    @abstractmethod
    def __init__(self):
        ''' Initialize the client '''

    @abstractmethod
    def action(self, act, kwargs):
        ''' Do some action in the game '''


class Player:

    def __init__(self):
        pass

    def prompt(self, first_prompt, condition=None, second_prompt=None):
        '''
        Prompts the user until they respond with an input that meets some condition
        :param first_prompt: A prompt for the user to enter information after
        :param condition: A condition function for the user's input to meet. The condition function should take a string
            and return True (or a Python equivalent) if the string is a valid user input and False otherwise
        :param second_prompt: A follow-up prompt for the following times the user tries to provide input
        :return: The user input, subject to the condition if one is provided
        '''
        user_input = input(first_prompt)
        if condition is not None:
            if condition(user_input):
                return user_input
            # Prompt again
            if second_prompt is None:
                return self.prompt(first_prompt, condition)
            return self.prompt(second_prompt, condition)
        # Without a condition the user input is always returned
        return user_input
