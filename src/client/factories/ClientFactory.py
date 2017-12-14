from src.client import client


class ClientFactory:

    @staticmethod
    def create_client(connection_socket, address):
        return client.Client(connection_socket, address)
