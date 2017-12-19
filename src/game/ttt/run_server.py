from ttt import TTTServer

server = TTTServer(['player1', 'player2'])
server.console_thread.start()
server.listen_thread.start()
