from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtNetwork import QNetworkInterface


class Networking(QObject):
    @pyqtSlot(result=str)
    def getIP(self):
        info = QNetworkInterface().allAddresses()
        print(info[3].toString())
        if info:
            return info[3].toString()