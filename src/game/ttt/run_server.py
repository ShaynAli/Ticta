from ttt import TTTServer

server = TTTServer(port=12000)
server.console_thread.start()
server.listen_thread.start()
