from websockets.asyncio.server import ServerConnection

class Room:
    def __init__(self, name: str, password: str, firstWebsocket: ServerConnection):
        self.name = name
        self.password = password
        self.clients: set[ServerConnection] = set()
        self.clients.add(firstWebsocket)

    def isPassword(self, string: str):
        return str == self.password

    def addClient(self, client):
        self.clients.add(client)

    def removeClient(self, client):
        self.clients.remove(client)

    def numClients(self):
        return len(self.clients)

    def handleMessageFromClient(self, client: ServerConnection, messageJson: dict):
        pass