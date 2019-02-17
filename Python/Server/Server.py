import sys

from PyQt5.QtCore import QObject, QUrl, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.python import log
from network.TickServer import BroadcastServerProtocol, BroadcastServerFactory
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

from candata.logplayer import LogPlayer
from candata.MachineState import MachineState
from candata.conversions import PDODecoder
from candata.canadapter import CanAdapter

#from gui.PiirtoQML import PiirtoQML
from gui.LogPlayerHandler import LogPlayerHandler
from gui.ModelWrapper import ModelWrapper
from gui.Networking import Networking
from gui.ClientList import Controller, ListManager, Client, ThingWrapper
from gui.CanBusHandler import CanBusHandler
from gui.SVGView import SVGView

if __name__ == '__main__':
    # Force material theme
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']

    # Init PyQt5
    app = QGuiApplication(sys.argv)
    qmlRegisterType(SVGView, 'SVGView', 1, 0, 'SVGView')
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    engine = QQmlApplicationEngine()

    # Init networking
    networking = Networking()
    engine.rootContext().setContextProperty('networking', networking)
    
    # Init logs, state object
    player = LogPlayer()
    state = MachineState()

    # Init gui handler for logs
    logPlayerHandler = LogPlayerHandler(player, reactor, state.consumeMessage)
    engine.rootContext().setContextProperty('logPlayerHandler', logPlayerHandler)

    # Init can adapter
    adapter = CanAdapter()

    # Init gui handler for logs
    canBusHandler = CanBusHandler(adapter, reactor, state.consumeMessage)
    engine.rootContext().setContextProperty('canBusHandler', canBusHandler)

    # Init binding for visualization - no need to have a timer to run to use this, unfinished
    modelWrapper = ModelWrapper(state)
    engine.rootContext().setContextProperty('modelWrapper', modelWrapper)

    # Init client model and handlers
    clients = [
    ]
    controller = Controller()
    engine.rootContext().setContextProperty('controller', controller)
    #peopleManager = ListManager(clients)
    listModel = ListManager(clients).getModel()
    engine.rootContext().setContextProperty('pythonListModel', listModel)

    # Init Twisted logging
    log.startLogging(sys.stdout)
    
    # Disable server until we rework the protocol
    ServerFactory = BroadcastServerFactory
    factory = ServerFactory(u"ws://127.0.0.1:9000", reactor, lambda: state.getState(), lambda client: listModel.addThing(ThingWrapper(Client(client.peer))))
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    # Load main QML file
    engine.load(QUrl.fromLocalFile('ServerMain.qml'))

    # Exit if we fail to load
    if not engine.rootObjects():
        sys.exit(-1)
    
    # Run until QML kills the program
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        app.quit()