from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty
from zope.interface import provider
from twisted.logger import ILogObserver, eventAsText


class AppLogHandler(QObject):
    def __init__(self):
        super().__init__()
        self._history = []

    @provider(ILogObserver)
    def appendEvent(self, event):
        self._history.insert(0, eventAsText(event))
        self.historyChanged.emit()

    historyChanged = pyqtSignal()
    history = pyqtProperty(list, lambda self: self._history, notify=historyChanged)
