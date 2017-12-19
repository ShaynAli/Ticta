import sys
from threading import Thread
from time import sleep
sys.path.append('..\..')
from abstracts.action import ActionServer, ActionClient
from presentation.interface import TTTGUI


class TTTClient(ActionClient, TTTGUI):

    def __init__(self):
        super().__init__()

    def play(self):
        self.log('Playing')
        # gui_thread = Thread(target=)
        listen_thread = Thread(target=self.listen4action)
        # send_thread = Thread(target=)
        listen_thread.start()
        tick = 0
        while self.connected:
            i = tick % 10
            if i:
                self.log('Connected')
            sleep(self.frequency)


class TTTServer(ActionServer):

    def __init__(self, port):
        super().__init__(port)


