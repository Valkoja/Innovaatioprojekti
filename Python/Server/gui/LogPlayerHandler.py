from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from string import Template
from urllib.parse import urlparse


class LogPlayerHandler(QObject):
    def __init__(self, player, reactor, callback):
        super().__init__()
        self._player = player
        self._file = None
        self._reactor = reactor
        self._callback = callback
        self.finished = False

    def _finished(self):
        return self.finished

    def _processed(self):
        return self._player.messagesProcessed()

    def update(self, message):
        self._callback(message)
        self.processedChanged.emit()

    def playerStateChanged(self, state):
        self.finished = state
        self.stateChanged.emit()

    stateChanged = pyqtSignal()
    state = pyqtProperty(bool, _finished, notify=stateChanged)
    processedChanged = pyqtSignal()
    processed = pyqtProperty(int, _processed, notify=processedChanged)

    @pyqtSlot(str)
    def handleLogFileSelected(self, file):
        self._file = urlparse(file).path
        print(Template('Log set to $file').substitute(file=self._file))

    @pyqtSlot()
    def handlePlayLogClicked(self):
        if self._file:
            print(Template('Playing log $file').substitute(file=self._file))
            self._player.processFile(self._file, self._reactor, self.update, self.playerStateChanged)
            self.finished = False
            self.stateChanged.emit()
        else:
            print('No log selected')