from PyQt5.QtCore import QTimer, QObject, QUrl, QAbstractListModel, QModelIndex, pyqtSlot, pyqtSignal, pyqtProperty

class ClientWrapper(QObject):
    def __init__(self, client):
        super().__init__()
        self._client = client

    def _peer(self):
        return self._client.peer

    changed = pyqtSignal()
    peer = pyqtProperty(str, _peer, notify=changed)

class ClientListModel(QAbstractListModel):
    COLUMNS = (b'client',)

    def __init__(self, clients):
        super().__init__()
        self._clients = clients

    def addClient(self, client):
        row = len(self._clients)
        self.beginInsertRows(QModelIndex(), row, row)
        self._clients.append(ClientWrapper(client))
        self.endInsertRows()

    def removeClient(self, client):
        # Qt deals in indexes and our objects have different wrappers, so we need to find the index to remove an item
        row = [i for i in range(len(self._clients)) if self._clients[i].peer == client.peer][0]
        print(row)
        self.beginRemoveRows(QModelIndex(), row, row)
        self._clients.pop(row)
        self.endRemoveRows()
        return True

    def roleNames(self):
        return dict(enumerate(ClientListModel.COLUMNS))

    def rowCount(self, parent=QModelIndex()):
        return len(self._clients)

    def data(self, index, role):
        if index.isValid() and role == ClientListModel.COLUMNS.index(b'client'):
            #print(self._things[index.row()])
            return self._clients[index.row()]
        else:
            return None

class ClientController(QObject):
    @pyqtSlot(QObject)
    def clientKicked(self, wrapper):
        print("User clicked on: %s" %(wrapper._client.peer))
        wrapper._client.disconnectClient()

class MockClient(object):
    def __init__(self, peer):
        self.peer = peer

    def str(self):
        return str("Peer {self.peer}")