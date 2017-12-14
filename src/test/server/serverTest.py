import unittest
from src.server.server import Server
from threading import Thread
import socket
from time import sleep


class ServerTest(unittest.TestCase):

    def test_constructor(self):
        server = Server('localhost', 3030)
        self.assertEqual(server.clients, [])

    def test_add_client(self):
        server = Server('localhost', 3030)
        dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.add_client(dummy_socket, ('127.0.0.1', 20121))
        self.assertEqual(len(server.clients), 1)


if __name__ == '__main__':
    unittest.main()
