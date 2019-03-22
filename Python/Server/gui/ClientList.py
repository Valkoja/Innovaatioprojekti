from PyQt5.QtCore import QTimer, QObject, QUrl, QAbstractListModel, QModelIndex, pyqtSlot, pyqtSignal, pyqtProperty


class ClientWrapper(QObject):
    def __init__(self, client):
        super().__init__()
        self._client = client
        self._client.setOnUpdate(self.changed.emit)

    def _peer(self):
        return self._client.peer.split(':')[1]

    changed = pyqtSignal()
    peer = pyqtProperty(str, _peer, notify=changed)
    library = pyqtProperty(str, lambda self: self._client.clientLibrary(), notify=changed)
    platform = pyqtProperty(str, lambda self: self._client.clientPlatform(), notify=changed)
    version = pyqtProperty(str, lambda self: self._client.clientVersion(), notify=changed)
    latency = pyqtProperty(str, lambda self: str(round(self._client.latency(), 0)) if self._client.latency() else "-", notify=changed)
    tickRate = pyqtProperty(float, lambda self: self._client.tickRate(), notify=changed)


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
        row = [i for i in range(len(self._clients)) if self._clients[i]._client.peer == client.peer][0]
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
            return self._clients[index.row()]
        else:
            return None


class ClientController(QObject):
    @pyqtSlot(QObject)
    def clientKicked(self, wrapper):
        wrapper._client.disconnectClient()


class MockClient(object):
    def __init__(self, peer):
        self.peer = peer

    def str(self):
        return str("Peer {self.peer}")
