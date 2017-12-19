from ttt import TTTServer

server = TTTServer(12000)
server.console_thread.start()
server.listen_thread.start()
