''' server.py - Deals with a game server '''
import sys
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


class Logger:

    def __init__(self, verbosity=0):
        self.verbosity = verbosity

    def log(self, msg, level=0):
        if level <= self.verbosity:
            print(msg)

    def log_error(self, e, stack_trace=False):
        if stack_trace:
            self.log('\n'.join(format_exception_only(type(e), e)))
        else:
            self.log(repr(e))


class ActionSocket(Logger):

    def __init__(self, frequency=0.1, buffer_size=1024, verbosity=0):
        super().__init__(verbosity=verbosity)
        self.socket = socket.socket()
        self.frequency = frequency
        self.buffer_size = buffer_size
        self.connected = False
        self.socket_free = True
        self.action_tree = {}

    # Client management

    def listen4action(self):
        ''' Deal with the incoming actions '''
        while self.connected:
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
                self.connected = False
            sleep(self.frequency)
        # Disconnect
        self.log('Disconnected')
        self.socket.close()

    # Action management

    # An action is of the form (action_word, **kwargs)
    def process_action(self, act_msg):
        act_word, kwargs = literal_eval(act_msg)
        act_func = self.action_tree[act_word]
        act_func(**kwargs)

    def send_action(self, action_word, **kwargs):
        self.send(str((action_word, kwargs)))

    # Socket management

    def connect(self, address):
        self.log('Attempting to connect to ' + str(address))
        try:
            self.socket.connect(address)
            self.connected = True
        except Exception as e:
            self.log('Unable to connect')
            raise e
        self.log('Connected to ' + str(address))
        action_listener = Thread(target=self.listen4action)
        action_listener.start()

    def disconnect(self):
        self.connected = False

    def send(self, msg):
        if not msg:  # Don't send empty messages
            return
        while not self.socket_free:
            sleep(self.frequency)
        sleep(self.frequency)
        self.socket_free = False
        try:
            self.socket.send(msg.encode())
        except Exception as e:
            self.log('Unable to send')
            self.log_error(e, stack_trace=False)
        self.socket_free = True

    def receive(self):
        try:
            return self.socket.recv(self.buffer_size).decode()
        except Exception as e:
            self.log('Unable to receive')
            self.log_error(e, stack_trace=False)


class ActionClient(ActionSocket):
    ''' Instances of Client should be run only on a client's machine and are not a part of the server '''

    def __init__(self, frequency=0.1, buffer_size=1024, verbosity=0):
        super().__init__(frequency=frequency, buffer_size=buffer_size, verbosity=verbosity)
        self.action_tree = {
            OPTIONS: self.send_options,
            REPLY: self.reply,
            ECHO: self.echo,
            EXIT: self.exit,
        }

    # Actions

    def send_options(self):
        self.send(str(*self.action_tree.keys()))

    def reply(self):
        self.send('This is a reply from a client')

    def echo(self, msg):
        self.send(msg)

    def exit(self):
        self.log('Exiting')
        self.disconnect()

    # Client management

    @abstractmethod
    def play(self):
        ''' Run the client '''


class ClientThread(ActionSocket, Thread):

    def __init__(self, server, socket, address, frequency=0.01, buffer_size=1024, verbosity=0):
        ActionSocket.__init__(self, frequency=frequency, buffer_size=buffer_size, verbosity=verbosity)
        Thread.__init__(self)
        self.server = server
        # Set connection manually
        self.socket = socket
        self.address = address
        self.connected = True
        # Set up action tree
        self.action_tree = {
            OPTIONS: self.send_options,
            REPLY: self.reply,
            ECHO: self.echo,
            EXIT: self.client_exit,
        }
        self.thread_no = ActionServer.client_no.__next__()
        self.log('Created at ' + str(address))

    # Overriding Thread.run, do not rename
    def run(self):
        self.listen4action()

    # Actions

    def send_options(self):
        self.send(str(self.action_tree.keys()))

    def reply(self):
        self.send('This is a reply from the server, you are connected at  ' + self.address)

    def echo(self, msg):
        self.send(msg)

    def client_exit(self):
        self.log('Client ended connection')
        self.connected = False
        self.socket.close()

    def log(self, msg, level=0):
        super().log('Client ' + str(self.thread_no) + '\t' + msg, level)


class ActionServer(Logger):
    ''' Runs the server and deals with clients '''

    client_no = (i for i in count())

    def __init__(self, port, client_type=ClientThread, server_type=None, frequency=0.1, backlog=32, verbosity=0):
        super().__init__(verbosity=verbosity)
        self.client_type = client_type
        self.output_free = True
        self.frequency = frequency
        self.port = port
        self.backlog = backlog
        self.socket = socket.socket()
        self.action_tree = {}
        self.log('Starting server on port: ' + str(port) + ' IP: ' + str(socket.gethostbyname(socket.gethostname())))
        self.online = True
        self.console_thread = Thread(target=self.listen4console)
        self.listen_thread = Thread(target=self.listen4client)
        self.clients = set()
        self.server_type = server_type if server_type is not None else ActionServer

    def listen4console(self):
        while self.online:
            while not self.output_free:
                sleep(self.frequency)
            try:
                self.command(input())
            except EOFError:
                self.disconnect()

    def command(self, cmd):
        if cmd in {'exit', 'done', 'disconnect', 'offline'}:
            self.disconnect()
        elif cmd in {'online', 'listen'}:
            self.listen_thread.start()
        elif cmd in {'davin'}:
            self.log('Something is happening')

    def disconnect(self):
        self.log('Going offline')
        self.online = False
        self.log('Disconnecting clients')
        for c in self.clients:
            c.connected = False
            c.socket.close()
            self.log('Disconnected client ' + str(c.thread_no))
        self.socket.close()
        self.log('Exiting')
        sleep(3)
        sys.exit(0)

    def log(self, msg, level=0):
        while not self.output_free:
            sleep(self.frequency)
        self.output_free = False
        super().log('Server\t\t' + msg, level)
        self.output_free = True

    def log_error(self, e, stack_trace=True):
        super().log_error(e, stack_trace=stack_trace)

    def listen4client(self):
        listen_address = (socket.gethostname(), self.port)
        self.socket.bind(listen_address)
        self.socket.listen(self.backlog)
        self.log('Listening on ' + str(listen_address))
        while self.online:
            try:
                client_socket, client_address = self.socket.accept()
                self.log('Accepted connection at ' + str(client_address))
                client = self.client_type(server=self, socket=client_socket, address=client_address)
                client.start()
                self.clients.add(client)
                if len(self.clients) >= 2:
                    self.server_type(self.clients)
                    self.clients = set()
            except OSError:
                self.log('Listening socket closed')
            except Exception as e:
                self.log_error(e)
