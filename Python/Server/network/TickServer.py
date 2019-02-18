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
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, reactor, getValues, newClientHandler):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0
        self.getValues = getValues
        self.tick()
        self.reactor = reactor
        self.newClientHandler = newClientHandler

    def tick(self):
        self.tickcount += 1
        #self.broadcast("tick %d from server" % self.tickcount)
        self.broadcast(json.dumps(self.getValues()))
        #print(self.getValues())
        self.reactor.callLater(0.005, self.tick)

    def register(self, client):
        if client not in self.clients:
            #print("registered client {}".format(client.peer))
            self.clients.append(client)
            self.newClientHandler(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        #print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            #print("message sent to {}".format(c.peer))