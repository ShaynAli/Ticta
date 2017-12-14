import unittest
from src.server.server import ServerConsole


class ServerTest(unittest.TestCase):

    def test_start(self):
        console = ServerConsole()
        self.assertEqual(console.wait_thread.is_alive(), False)
        self.assertIsNotNone(console.server)


if __name__ == '__main__':
    unittest.main()