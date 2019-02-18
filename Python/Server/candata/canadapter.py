import time
import datetime
from pathlib import Path
import sys

from sys import platform

import can as pycan
from candata.conversions import PDODecoder

# Play busmaster logs
class CanAdapter():
    def __init__(self):
        self._messagesProcessed = 0
        self._stopped = False

    def messagesProcessed(self):
        return self._messagesProcessed

    def stopBus(self):
        self._stopped = True

    def openBus(self, bus, reactor, callback):
        def cbAndTrack(message):
            # print(message)
            self._messagesProcessed += 1
            callback(message)
        #f platform == 'linux' and bus == 'vcan0':
        if False:
            canbus = pycan.Bus('vcan0', bustype='socketcan')
        else:
            canbus = pycan.Bus(0, bustype='kvaser', bitrate=250000)
        
        # NMT
        canopen_nmt_start = pycan.Message(arbitration_id=0x00, data=[0x01, 0x00])
        canbus.send(canopen_nmt_start)
        
        decoder = PDODecoder()
        def getMessages():
            #for msg in canbus:
            msg = canbus.recv()
            message = decoder.decode_pdo(msg.arbitration_id, msg.data)
            
            if message:
                cbAndTrack(message)

            if not self._stopped:
                reactor.callLater(0.001, getMessages)
            else:
                canbus.shutdown()
                return

        reactor.callLater(0.001, getMessages)
