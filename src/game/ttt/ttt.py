import sys
from threading import Thread
from time import sleep
sys.path.append('..\..')
from abstracts.action import ActionServer, ActionClient
from presentation.interface import TTTInterface


class TTTClient(ActionClient, TTTInterface):

    def __init__(self, listen_frequency=0.01):
        super().__init__()
        self.listen_freq = listen_frequency

    def play(self):
        # gui_thread = Thread(target=)
        # listen_thread = Thread(target=)
        # send_thread = Thread(target=)
        while not self.disconnected:
            pass

    def listen(self):
        while not self.disconnected:
            in_msg = self.receive()
            if in_msg:
                self.process_action(in_msg)
            else:
                self.exit()
            sleep(self.listen_freq)
        # Disconnect
        self.socket.close()


class TTTServer(ActionServer):

    def __init__(self, port):
        super().__init__(port)

