from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from string import Template
from enum import Enum
from twisted.logger import Logger


CanAdapterState = Enum('state', 'idle scanning ready open error')


class CanBusWrapper(QObject):
    def __init__(self, bus):
        super().__init__()
        self._bus = bus

    def bus(self):
        return self._bus

    interface = pyqtProperty(str, lambda self: self._bus.interface, constant=True)
    channel = pyqtProperty(str, lambda self: self._bus.channel, constant=True)
    toString = pyqtProperty(str, lambda self: self._bus.__str__(), constant=True)


class CanBusHandler(QObject):
    log = Logger()

    def __init__(self, adapter, reactor, callback):
        super().__init__()
        self._adapter = adapter
        self._available = []
        self._bus = ''
        self._reactor = reactor
        self._callback = callback
        self._state = CanAdapterState.idle
        self._errorMessage = ''

    def update(self, message):
        self._callback(message)
        self.processedChanged.emit()

    def scanCompleted(self, available):
        self._state = CanAdapterState.idle
        self._available.clear()
        for bus in available:
            self.available.append(CanBusWrapper(bus))
        print('Scan done')
        # self._bus = self._available[0]
        self._state = CanAdapterState.ready
        self.busChanged.emit()
        self.stateChanged.emit()
        self.availableChanged.emit()

    def canBusStateChanged(self):
        self._state = CanAdapterState.idle
        self.stateChanged.emit()

    @pyqtSlot()
    def handleErrorAcknowledgedClicked(self):
        self._state = CanAdapterState.ready
        self.stateChanged.emit()

    @pyqtSlot()
    def handleScanClicked(self):
        self._state = CanAdapterState.scanning
        self.stateChanged.emit()
        print('Scanning...')
        self._adapter.scan(self.scanCompleted)

    @pyqtSlot(int)
    def handleBusSelected(self, index):
        try:
            if index < len(self._available):
                self._bus = self._available[index].bus()
                print(Template('Bus set to $bus').substitute(bus=self._bus))
        except:
            self.log.info("fail")

    @pyqtSlot()
    def handleOpenBusClicked(self):
        if self._bus:
            self._state = CanAdapterState.open
            self.stateChanged.emit()
            print(Template('Opening bus $bus').substitute(bus=self._bus))
            try:
                self._adapter.openBus(self._bus, self._reactor, self.update)
            except Exception as e:
                print("Error opening can")
                self._state = CanAdapterState.error
                self.stateChanged.emit()
                self._errorMessage = str(e)
                self.errorMessageChanged.emit()
        else:
            print('No bus selected')

    @pyqtSlot()
    def handleCloseBusClicked(self):
        if self._state == CanAdapterState.open:
            print(Template('Closing bus $bus').substitute(bus=self._bus))
            self._adapter.stopBus()
            self._state = CanAdapterState.ready
            self.stateChanged.emit()
        else:
            print('No bus selected')

    stateChanged = pyqtSignal()
    state = pyqtProperty(str, lambda self: self._state.name, notify=stateChanged)
    processedChanged = pyqtSignal()
    processed = pyqtProperty(int, lambda self: self._adapter.messagesProcessed(), notify=processedChanged)
    busChanged = pyqtSignal()
    bus = pyqtProperty(CanBusWrapper, lambda self: self._bus, notify=busChanged, fset=handleBusSelected)
    availableChanged = pyqtSignal()
    available = pyqtProperty(list, lambda self: self._available, notify=availableChanged)
    errorMessageChanged = pyqtSignal()
    errorMessage = pyqtProperty(str, lambda self: self._errorMessage, notify=errorMessageChanged)
