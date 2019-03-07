from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from string import Template
from urllib.parse import urlparse
from candata.logplayer import LogPlayer
from enum import Enum

LogPlayerState = Enum('state', 'nofile ready playing')


class LogPlayerHandler(QObject):
    def __init__(self, reactor, callback):
        super().__init__()
        self._file = None
        self._reactor = reactor
        self._callback = callback
        self._player = LogPlayer(reactor, self.update, self.playerStateChanged)
        self._state = LogPlayerState.nofile

    def state(self):
        return self._state.name

    def processed(self):
        return self._player.messagesProcessed()

    def update(self, message):
        self._callback(message)
        self.processedChanged.emit()

    def playerStateChanged(self):
        if not self._loopLog:
            self._state = LogPlayerState.ready
            self.stateChanged.emit()
        else:
            print(Template('Replaying log $file').substitute(file=self._file))
            self._player.processFile(self._file)

    @pyqtSlot(str)
    def handleLogFileSelected(self, file):
        self._file = urlparse(file).path
        print(Template('Log set to $file').substitute(file=self._file))
        self._state = LogPlayerState.ready
        self.stateChanged.emit()

    @pyqtSlot()
    def handlePlayLogClicked(self):
        if self._file:
            print(Template('Playing log $file').substitute(file=self._file))
            self._player.processFile(self._file)
            self._state = LogPlayerState.playing
            self.stateChanged.emit()
        else:
            print('No log selected')

    @pyqtSlot()
    def handleStopLogClicked(self):
        if not self._state == 'playing':
            self._player.stop()
            self._state = LogPlayerState.ready
            self.stateChanged.emit()
            print(Template('Stopped log $file').substitute(file=self._file))

    @pyqtSlot(bool)
    def handleLoopLogClicked(self, state):
        self._loopLog = state

    stateChanged = pyqtSignal()
    state = pyqtProperty(str, state, notify=stateChanged)
    processedChanged = pyqtSignal()
    processed = pyqtProperty(int, processed, notify=processedChanged)