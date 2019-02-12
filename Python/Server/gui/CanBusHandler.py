from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from string import Template


class CanBusHandler(QObject):
    def __init__(self, adapter, reactor, callback):
        super().__init__()
        self._adapter = adapter
        self._bus = "vcan0"
        self._reactor = reactor
        self._callback = callback
        self._closed = False

    def update(self, message):
        self._callback(message)
        self.processedChanged.emit()

    def canBusStateChanged(self, state):
        self.finished = state
        self.stateChanged.emit()

    @pyqtSlot(str)
    def handleBusSelected(self, bus):
        self._bus = bus
        print(Template('Bus set to $bus').substitute(bus=self._bus))

    @pyqtSlot()
    def handleOpenBusClicked(self):
        if self._bus:
            print(Template('Opening bus $bus').substitute(bus=self._bus))
            self._adapter.openBus(self._bus, self._reactor, self.update)
            self.stateChanged.emit()
        else:
            print('No bus selected')

    @pyqtSlot()
    def handleCloseBusClicked(self):
        if self._bus and not self._closed:
            print(Template('Closing bus $bus').substitute(bus=self._bus))
            self._adapter.stopBus()
            self.stateChanged.emit()
        else:
            print('No bus selected')

    stateChanged = pyqtSignal()
    state = pyqtProperty(bool, lambda self: self._closed, notify=stateChanged)
    processedChanged = pyqtSignal()
    processed = pyqtProperty(int, lambda self: self._adapter.messagesProcessed(), notify=processedChanged)
    busChanged = pyqtSignal()
    bus = pyqtProperty(str, lambda self: self._bus, notify=processedChanged, fset=handleBusSelected)
