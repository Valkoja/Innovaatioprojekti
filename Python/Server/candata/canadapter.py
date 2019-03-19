import logging
from sys import platform
import can
from candata.conversions import PDODecoder
from threading import Thread


class Bus:
    def __init__(self, interface, channel):
        self.interface = interface
        self.channel = channel
    interface = ''
    channel = ''

    def __str__(self):
        return self.interface + '/' + self.channel


class CanAdapter():
    def __init__(self):
        self._messagesProcessed = 0
        self._stopped = False
        self._thread = None

    def messagesProcessed(self):
        return self._messagesProcessed

    def stopBus(self):
        self._stopped = True
        #self._thread.join()

    @staticmethod
    def scan(cb):
        print("Scanning")
        available = []
        if platform == 'linux':
            # scan for socketcan
            available.append(Bus('socketcan', 'vcan0'))
            # scan for kvaser
            available.append(Bus('kvaser', '0'))
        elif platform == 'win32':
            # scan for kvaser
            available.append(Bus('kvaser', '0'))
        elif platform == 'darwin':
            available.append(Bus('nobus', '0'))
        cb(available)

    def openBus(self, bus, reactor, callback):
        def cbAndTrack(message):
            # print(message)
            self._messagesProcessed += 1
            callback(message)

        canbus = None

        if bus.interface == 'socketcan':
            canbus = can.Bus(bustype=bus.interface, channel=bus.channel)
        elif bus.interface == 'kvaser':
            from can.interfaces.kvaser.canlib import KvaserBus
            try:
                canbus = can.interface.Bus(bustype='kvaser', channel=0, bitrate=250000)
            except Exception as e:
                print("Problem setting bus")
                raise e
            print("Bus type set")
        else:
            return
        
        # NMT
        canopen_nmt_start = can.Message(arbitration_id=0x00, data=[0x01, 0x00], is_extended_id=False)
        print("Sending NMT-open")
        print(canopen_nmt_start.__str__())
        try:
            canbus.send(canopen_nmt_start)
        except Exception as e:
            print("Problem sending NMT-open")
            raise e

        decoder = PDODecoder()

        def getMessages():
            while True:
                if self._stopped:
                    print('Stopped')
                    canbus.shutdown()
                    return
                msg = canbus.recv(timeout=5)
                if msg:
                    message = decoder.decode_pdo(msg.arbitration_id, msg.data)
                    if message:
                        cbAndTrack(message)

        self._thread = Thread(target=getMessages)
        self._thread.setDaemon(True)
        self._thread.start()
