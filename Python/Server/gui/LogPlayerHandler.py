from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from string import Template
from urllib.parse import urlparse
from candata.logplayer import LogPlayer
from enum import Enum

PlayerState = Enum('state', 'notready ready playing stopped')

class LogPlayerHandler(QObject):
    def __init__(self, reactor, callback):
        super().__init__()
        self._file = None
        self._reactor = reactor
        self._callback = callback
        self.finished = False
        self._loopLog = False
        self._player = LogPlayer(reactor, self.update, self.playerStateChanged)

    def _finished(self):
        return self.finished

    def _processed(self):
        return self._player.messagesProcessed()

    def _hasFile(self):
        if self._file:
            return True
        else:
            return False

    def update(self, message):
        self._callback(message)
        self.processedChanged.emit()

    def playerStateChanged(self):
        if not self._loopLog:
            self.finished = True
            self.stateChanged.emit()
        else:
            print(Template('Replaying log $file').substitute(file=self._file))
            self._player.processFile(self._file)


    @pyqtSlot(str)
    def handleLogFileSelected(self, file):
        self._file = urlparse(file).path
        print(Template('Log set to $file').substitute(file=self._file))
        self.hasFileChanged.emit()

    @pyqtSlot()
    def handlePlayLogClicked(self):
        if self._file:
            print(Template('Playing log $file').substitute(file=self._file))
            self._player.processFile(self._file)
            self.finished = False
            self.stateChanged.emit()
        else:
            print('No log selected')

    @pyqtSlot()
    def handleStopLogClicked(self):
        if not self.finished:
            self._player.stop()
            print(Template('Stopped log $file').substitute(file=self._file))

    @pyqtSlot(bool)
    def handleLoopLogClicked(self, state):
        self._loopLog = state

    stateChanged = pyqtSignal()
    state = pyqtProperty(bool, _finished, notify=stateChanged)
    processedChanged = pyqtSignal()
    processed = pyqtProperty(int, _processed, notify=processedChanged)
    hasFileChanged = pyqtSignal()
    hasFile = pyqtProperty(bool, _hasFile, notify=hasFileChanged)