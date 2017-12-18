''' server.py - Deals with a game server '''
import socket
from threading import Thread
from itertools import count
from time import sleep
from ast import literal_eval
from traceback import format_exception_only
from abc import abstractmethod

OPTIONS = 'options'
REPLY = 'reply'
ECHO = 'echo'
EXIT = 'exit'


class ActionClient:
    ''' Instances of Client should be run only on a client's machine and are not a part of the server '''

    def __init__(self, buffer_size=1024):
        self.socket = socket.socket()
        self.buffer_size = buffer_size
        self.disconnected = False
        self.action_tree = {
            OPTIONS: self.send_options,
            REPLY: self.reply,
            ECHO: self.echo,
            EXIT: self.exit,
        }

    # Actions

    def send_options(self):
        self.send(str(self.action_tree.keys()))

    def reply(self):
        self.send('This is a reply from a client')

    def echo(self, msg):
        self.send(msg)

    def exit(self):
        self.log('Exiting')
        self.send_action(EXIT)
        self.socket.close()
        self.disconnected = True

    # Client management

    @abstractmethod
    def play(self):
        ''' Run the client '''

    # Action management

    # An action is of the form (action_word, **kwargs)
    def action(self, act_msg):
        act_word, kwargs = literal_eval(act_msg)
        act_func = self.action_tree[act_word]
        act_func(**kwargs)

    def send_action(self, action_word, **kwargs):
        self.send(str(action_word) + str(kwargs.items()))

    # Socket management

    def connect(self, address):
        self.log('Attempting to connect to ' + str(address))
        try:
            self.socket.connect(address)
        except Exception as e:
            self.log('Unable to connect')
            raise e
        self.log('Connected to ' + str(address))
        self.log('Type ' + ActionClient.EXIT_MSG + ' to exit at any time')

    def send(self, msg):
        if not msg:  # Don't send empty messages
            return
        try:
            self.socket.send(msg.encode())
        except EOFError as e:
            raise e
        except Exception as e:
            self.log('Unable to send, ensure you\'re connected before sending')
            self.log_error(e)

    def receive(self):
        try:
            return self.socket.recv(self.buffer_size).decode()
        except(ConnectionAbortedError, EOFError):
            self.log('Server disconnected')

    def log(self, msg, level=0):
        if level <= self.verbosity:
            print(msg)

    def log_error(self, e, log_stack_trace=False):
        self.log('Encountered an error: ' + repr(e))
        if log_stack_trace:
            self.log('\n'.join(format_exception_only(type(e), e)))


class ActionServer:
    ''' Runs the server and deals with clients '''

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
            client = ActionServer.ClientThread(self, client_socket, client_address, self.verbosity // 2)
            client.start()

    def log(self, msg, level=0):
        if level <= self.verbosity:
            print(msg)

    class ClientThread(Thread):

        thread_no = (i for i in count())

        def __init__(self, server, socket, address, frequency=0.01, buffer_size=1024, verbosity=0):
            self.server = server
            super().__init__()
            self.thread_no = ActionServer.ClientThread.thread_no.__next__()
            self.socket = socket
            self.address = address
            self.disconnected = False
            self.frequency = frequency
            self.buffer_size = buffer_size
            self.verbosity = verbosity
            self.log('ClientThread ' + str(self.thread_no) + ' created at ' + str(address))
            self.action_tree = {
                OPTIONS: self.send_options,
                REPLY: self.reply,
                ECHO: self.echo,
                EXIT: self.exit,
            }

        # Actions

        def send_options(self):
            self.send(str(self.action_tree.keys()))

        def reply(self):
            self.send('This is a reply from the server, you are connected at  ' + self.address)

        def echo(self, msg):
            self.send(msg)

        def exit(self):
            self.log('Client ended connection')
            self.disconnected = True

        # Overriding Thread.run, do not rename
        def run(self):
            self.play()

        # Client management

        @abstractmethod
        def play(self):
            ''' Deal with the client's actions '''
            while not self.disconnected:
                in_msg = self.receive()
                if in_msg:
                    try:
                        self.process_action(in_msg)
                        self.log('Completed action: ' + in_msg)
                    except(SyntaxError, TypeError, KeyError, ValueError) as e:
                        self.log('Received non-action message: ' + in_msg)
                    except Exception as e:
                        raise e
                else:
                    self.exit()
                sleep(self.frequency)
            # Disconnect
            self.socket.close()

        # Action management

        # An action is of the form (action_word, **kwargs)
        def process_action(self, act_msg):
            act_word, kwargs = literal_eval(act_msg)
            act_func = self.action_tree[act_word]
            act_func(**kwargs)

        def send_action(self, action_word, **kwargs):
            self.send(str(action_word) + str(kwargs.items()))

        # Socket management

        def send(self, msg):
            if not msg:  # Don't send empty messages
                return
            try:
                self.socket.send(msg.encode())
            except Exception as e:
                self.log('Unable to send to client')
                self.log_error(e)

        def receive(self):
            try:
                return self.socket.recv(self.buffer_size).decode()
            except Exception as e:
                self.log('Unable to receive from client')
                self.log_error(e)

        # Logging

        def log(self, msg, level=0):
            if level <= self.verbosity:
                print('ClientThread ' + str(self.thread_no) + ': ' + str(msg))

        def log_error(self, e, log_stack_trace=False):
            self.log('Encountered an error: ' + repr(e))
            if log_stack_trace:
                self.log('\n'.join(format_exception_only(type(e), e)))
