import unittest
from ...server.server import Server


class ServerTest(unittest.TestCase):

    def test_constructor(self):
        server = Server('localhost', 3030)
        self.assertEqual(server.clients, [])

    def test_connectClient:



if __name__ == '__main__':
    unittest.main()