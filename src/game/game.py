''' game.py - Classes and functions for game flow '''


class Game:

    pass


class Player:

    def __init__(self):
        pass

    def prompt(self, first_prompt, condition, second_prompt=None):
        '''
        Prompts the user until they respond with an input that meets some condition
        :param first_prompt: A prompt for the user to enter information after
        :param condition: A condition function for the user's input to meet - note that input will be in a string
        format
        :param second_prompt: A follow-up prompt for the following times the user tries to provide input
        :return:
        '''
        user_input = input(first_prompt)
        if condition(user_input):
            return user_input
        else:  # Prompt again
            if second_prompt is None:
                return self.prompt(first_prompt, condition)
            else:
                return self.prompt(second_prompt, condition)
