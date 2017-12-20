from ttt import TTTServer

server = TTTServer()
server.console_thread.start()
server.listen_thread.start()



