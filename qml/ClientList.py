from PyQt5.QtCore import QTimer, QObject, QUrl, QAbstractListModel, QModelIndex, pyqtSlot, pyqtSignal, pyqtProperty

class ThingWrapper(QObject):
    def __init__(self, thing):
        super().__init__()
        self._thing = thing

    def _peer(self):
        return str(self._thing.peer) 

    changed = pyqtSignal()
    peer = pyqtProperty(str, _peer, notify=changed)

class ThingListModel(QAbstractListModel):
    COLUMNS = (b'thing',)

    def __init__(self, things):
        super().__init__()
        self._things = things

    def addThing(self, thing):
        row = len(self._things)
        self.beginInsertRows(QModelIndex(), row, row)
        self._things.append(thing)
        self.endInsertRows()
        return True
        #self.dataChanged.emit()

    def roleNames(self):
        return dict(enumerate(ThingListModel.COLUMNS))

    def rowCount(self, parent=QModelIndex()):
        return len(self._things)

    def data(self, index, role):
        if index.isValid() and role == ThingListModel.COLUMNS.index(b'thing'):
            #print(self._things[index.row()])
            return self._things[index.row()]
        else:
            return None

class Controller(QObject):
    @pyqtSlot(QObject)
    def thingSelected(self, wrapper):
        print("User clicked on: %s" %(wrapper._thing.peer))

class Client(object):
    def __init__(self, peer):
        self.peer = peer

    def str(self):
        return str("Peer {self.peer}")

class ListManager():
    def __init__(self, clients):
        self.clients = clients
        self.model = ThingListModel([ThingWrapper(thing) for thing in self.clients])

    def getModel(self):
        return self.model