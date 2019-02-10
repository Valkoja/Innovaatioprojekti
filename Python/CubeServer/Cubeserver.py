import sys

from PyQt5.QtCore import QTimer, QObject, QUrl, QAbstractListModel, QModelIndex, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QNetworkInterface

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from TickServer import BroadcastServerProtocol, BroadcastServerFactory, CubeOrientation
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

from ClientList import Controller, ListManager, Client, ThingWrapper

class ClickHandler(QObject):
    def __init__(self, ws):
        super().__init__()
        self.ws = ws
    @pyqtSlot()
    def handleButtonClicked(self):
        print("Hello from QML")
        self.ws()

x = 0.5
y = 0.5
z = 0.5

class SliderHandler(QObject):
    @pyqtSlot(str, float)
    def handleSliderMoved(self, slider, value):
        global x
        global y
        global z
        print("Slider {slider} set to {value} from QML".format(slider=slider, value=value))
        # Set value
        if slider == "x":
            x = value
        elif slider == "y":
            y = value
        elif slider == "z":
            z = value


class Networking(QObject):
    @pyqtSlot(result=str)
    def getIP(self):
        info = QNetworkInterface().allAddresses()
        print(info[3].toString())
        if info:
            return info[3].toString()

people = [
]

if __name__ == '__main__':
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']

    app = QGuiApplication(sys.argv)
    import qt5reactor
    qt5reactor.install()

    engine = QQmlApplicationEngine()
    #handler = ClickHandler(start_ws)
    sliderHandler = SliderHandler()
    networking = Networking()

    controller = Controller()
    peopleManager = ListManager(people)
    listModel = ListManager(people).getModel()

    log.startLogging(sys.stdout)

    from twisted.internet import reactor
    ServerFactory = BroadcastServerFactory
    factory = ServerFactory(u"ws://127.0.0.1:9000", reactor, lambda: CubeOrientation(x, y, z), lambda client: listModel.addThing(ThingWrapper(Client(client.peer))))
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    engine.rootContext().setContextProperty('controller', controller)
    engine.rootContext().setContextProperty('pythonListModel', listModel)
    engine.rootContext().setContextProperty('sliderHandler', sliderHandler)
    #engine.rootContext().setContextProperty("handler", handler)
    engine.rootContext().setContextProperty("networking", networking)

    engine.load(QUrl.fromLocalFile('App.qml'))
    #loop.run_forever()
    if not engine.rootObjects():
        sys.exit(-1)
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        app.quit()