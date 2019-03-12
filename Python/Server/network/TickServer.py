import sys

from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

import json


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            # self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def disconnectClient(self):
        self.sendClose(1000, 'please leave')


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url, reactor, getValues, clientConnectedHandler, clientDisconnectedHandler):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0
        self.getValues = getValues
        self.tick()
        self.reactor = reactor
        self.clientConnectedHandler = clientConnectedHandler
        self.clientDisconnectedHandler = clientDisconnectedHandler       

    def tick(self):
        self.tickcount += 1
        self.broadcast(json.dumps(self.getValues()))
        self.reactor.callLater(0.005, self.tick)

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)
            self.clientConnectedHandler(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)
            self.clientDisconnectedHandler(client)

    def broadcast(self, msg):
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))