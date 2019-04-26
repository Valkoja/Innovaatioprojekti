import logging
from sys import platform
import can
from candata.conversions import XSiteDecoder, SDOEncoder
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
        self._bus = None
        self._writeHandle = None

    def messagesProcessed(self):
        return self._messagesProcessed

    def stopBus(self):
        self._stopped = True

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

    def sendMessage(self, message, argument):
        encoder = SDOEncoder()
        msg = encoder.encode_sdo(message, argument)

        if self._bus.interface == 'socketcan':
            if not self._writeHandle:
                try:
                    self._writeHandle = can.Bus(bustype=self._bus.interface, channel=self._bus.channel)
                except Exception as e:
                    print("Problem setting bus")
                    raise e
        elif self._bus.interface == 'kvaser':
            if not self._writeHandle:
                try:
                    self._writeHandle = can.interface.Bus(bustype='kvaser', channel=0, bitrate=250000)
                except Exception as e:
                    print("Problem setting bus")
                    raise e
        else:
            print("Nobus, sending message " + msg.__str__())
            return
        try:
            self._writeHandle.send(can.Message(arbitration_id=msg.id, data=msg.data, extended_id=False))
        except Exception as e:
            print("Problem sending command")
            raise e

    def setBus(self, bus):
        self._bus = bus

    def openBus(self, callback):
        def cbAndTrack(message):
            # print(message)
            self._messagesProcessed += 1
            callback(message)

        canbus = None

        if self._bus.interface == 'socketcan':
            canbus = can.Bus(bustype=self._bus.interface, channel=self._bus.channel)
        elif self._bus.interface == 'kvaser':
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

        decoder = XSiteDecoder()

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
                    else:
                        message = decoder.decode_sdo(msg.arbitration_id, msg.data)
                        if message:
                            cbAndTrack(message)

        self._thread = Thread(target=getMessages)
        self._thread.setDaemon(True)
        self._thread.start()
