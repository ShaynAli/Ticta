''' server.py - Deals with a game server '''
import socket
from threading import Thread
from itertools import count
from time import sleep
from ast import literal_eval


class Server:

    def __init__(self, port, backlog=32, verbosity=0):
        self.verbosity = verbosity
        self.log('Starting server')
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket()
        self.online = True

    def listen(self):
        listen_address = (socket.gethostname(), self.port)
        self.socket.bind(listen_address)
        self.socket.listen(self.backlog)
        self.log('Listening on ' + str(listen_address))
        while self.online:
            client_socket, client_address = self.socket.accept()
            self.log('Accepted connection at ' + str(client_address))
            client = Server.ClientThread(self, client_socket, client_address, self.verbosity//2)
            client.start()

    def log(self, msg, level=0):
        if level <= self.verbosity:
            print(msg)

    class ClientThread(Thread):

        thread_no = (i for i in count())

        def __init__(self, server, socket, address, frequency=0.02, buffer_size=1024, verbosity=0):
            self.server = server
            super().__init__()
            self.thread_no = Server.ClientThread.thread_no.__next__()
            self.socket = socket
            self.address = address
            self.disconnected = False
            self.frequency = frequency
            self.buffer_size = buffer_size
            self.verbosity = verbosity
            self.log('ClientThread ' + str(self.thread_no) + ' created at ' + str(address))
            self.action_tree = {
                'reply': self.reply,
                'echo': self.echo,
                'exit': self.exit,
            }

        # Overriding Thread.run, do not rename
        def run(self):
            self.play()

        def play(self):
            while not self.disconnected:
                in_msg = self.receive()
                if self.is_action(in_msg):
                    self.action(*in_msg)
                else:
                    self.log('Received message: ' + in_msg)
                    self.is_action(in_msg, log_errors=True)
                sleep(self.frequency)

        # Socket management

        def send(self, msg, log=False):
            if not msg:
                return
            try:
                self.socket.send(msg.encode())
            except Exception as e:
                self.log('Unable to send to client')
                raise e

        def receive(self, log=False):
            try:
                return self.socket.recv(self.buffer_size).decode()
            except Exception as e:
                self.log('Unable to receive from client')
                raise e

        # Action management

        # An action is of the form (action_word, **kwargs)
        def action(self, act_msg):
            act = literal_eval(act_msg)
            action_word, kwargs = act
            self.action_tree[action_word](**kwargs)

        def send_action(self, action):
            self.send(str(action))

        def is_action(self, msg, log_errors=False):
            try:
                action_word, params = literal_eval(msg)
                if action_word not in self.action_tree:  # Check word
                    if log_errors:
                        self.log('Action word not in action tree')
                    return False
                else:  # Check parameters
                    pass
            except(TypeError, ValueError) as e:
                self.log('Encountered ' + type(e) + ' while processing action word')
                self.log(repr(e))
                return False

        # Actions

        def reply(self):
            self.send('This is a reply from the server, you are connected at  ' + self.address)

        def echo(self, msg):
            self.send(msg)

        def exit(self):
            self.log('Client ended connection')
            self.disconnected = True

        # Helper functions

        @staticmethod
        def non_none(first, second):
            return first if first is not None else second

        # Logging

        def log(self, msg, level=0):
            if level <= self.verbosity:
                print('ClientThread ' + str(self.thread_no) + ': ' + str(msg))
