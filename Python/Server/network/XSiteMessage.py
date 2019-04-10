from enum import Enum
import datetime
import json


class StateMessage:
    def __init__(self, msgid, data, latency, tickrate):
        self.id = msgid
        self.state = data
        self.timestamp = datetime.datetime.now().isoformat()
        self.latency = latency
        self.tickRate = tickrate

    def asJson(self):
        return json.dumps(self.__dict__)


class MessageType(Enum):
    hello = 'HELLO'
    confirm = 'CONFIRM'
    command = 'COMMAND'
