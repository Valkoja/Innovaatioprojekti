from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtNetwork import QNetworkInterface, QAbstractSocket, QHostAddress


class Networking(QObject):
    @pyqtSlot(result=str)
    def getIP(self):
        localhost = QHostAddress(QHostAddress.LocalHost)
        addresses = QNetworkInterface().allAddresses()
        if addresses:
            for address in addresses:
                if address.protocol() == QAbstractSocket.IPv4Protocol and address != localhost:
                    return address.toString()
