from autobahn.twisted.websocket import WebSocketServerFactory


class XSiteBroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url, reactor, stateObject, clientConnectedHandler, clientDisconnectedHandler):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.stateObject = stateObject
        self.reactor = reactor
        self.clientConnectedHandler = clientConnectedHandler
        self.clientDisconnectedHandler = clientDisconnectedHandler

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)
            self.clientConnectedHandler(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)
            self.clientDisconnectedHandler(client)
