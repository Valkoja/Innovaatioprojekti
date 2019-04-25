from enum import Enum

from autobahn.twisted.websocket import WebSocketServerProtocol
import json
import datetime
import dateutil.parser
from twisted.logger import Logger
from network.XSiteMessage import StateMessage, MessageType


class ClientState(Enum):
    connected = 1
    listening = 2
    disconnected = 3


class XSiteServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._state = ClientState.connected
        self._clientLibrary = None
        self._clientPlatform = None
        self._clientVersion = None
        self._tickInterval = 0.005
        self._latencies = []
        self._id = 0
        self._trackingId = None
        self._trackingOk = True
        self._onUpdate = None
        self.log = Logger()
        self.log.namespace = type(self).__name__

    def clientLibrary(self):
        return self._clientLibrary

    def clientPlatform(self):
        return self._clientPlatform

    def clientVersion(self):
        return self._clientVersion

    def setOnUpdate(self, cb):
        self._onUpdate = cb

    def latency(self):
        from statistics import mean
        if len(self._latencies) > 0:
            return mean(self._latencies)
        else:
            return 0

    def tickRate(self):
        return 1 / self._tickInterval

    def setTickRate(self, tickRate):
        self._tickInterval = 1 / tickRate

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = json.loads(payload.decode('utf8'))
            if msg['type'] == MessageType.hello.value:
                self._clientLibrary = msg['library']
                self._clientPlatform = msg['platform']
                self._clientVersion = msg['version']
                self._state = ClientState.listening
                self.log.info('Hello from ' + self._clientLibrary+ ' on ' + self._clientPlatform)
                self.sendState()
            elif msg['type'] == MessageType.confirm.value:
                if self._trackingId == msg['id']:
                    delta = datetime.datetime.now() - dateutil.parser.parse(msg['timestamp'])
                    self._latencies.append(delta.microseconds / 2 / 1000)
                    if self._latencies.__len__() > 20:
                        self._latencies.pop(0)
                    self._trackingOk = True
            elif msg['type'] == MessageType.command.value:
                command = msg['command']
                self.log.info('Command ' + command + ' from ' + self.peer)
                if msg['argument']:
                    argument = msg['argument']
                    self.factory.stateObject.consumeCommand(command, argument)
                else:
                    self.factory.stateObject.consumeCommand(command)
            else:
                print(msg)
                self.log.critical('Unknown type of message')

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.log.info('Client ' + self.peer + "@" + self.clientLibrary() + ' on ' + self.clientPlatform() + " disconnected")
        self.factory.unregister(self)
        self._state = ClientState.disconnected

    def disconnectClient(self):
        self.sendClose(1000, 'please leave')

    def sendState(self):
        if self._state == ClientState.listening:
            state = self.factory.stateObject.getState()
            msg = StateMessage(self._id, state, self.latency(), self.tickRate()).asJson()
            self._id = self._id + 1
            if self._id % 50 == 0 and self._trackingOk:
                self._trackingId = self._id
                self._trackingOk = False
            self.sendMessage(msg.encode('utf8'))
            if self._onUpdate:
                self._onUpdate()

        if self._state != ClientState.disconnected:
            self.factory.reactor.callLater(self._tickInterval, self.sendState)
