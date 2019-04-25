import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from twisted.logger import Logger, globalLogBeginner, FilteringLogObserver, LogLevelFilterPredicate, LogLevel, textFileLogObserver

from network import XSiteBroadcastServerFactory, XSiteServerProtocol
from autobahn.twisted.websocket import listenWS

from candata import CanAdapter, MachineState

from gui import AppLogHandler, CanBusHandler, CanBusWrapper, ClientListModel, ClientController, LogPlayerHandler, \
    ModelWrapper, Networking, SVGElement


if __name__ == '__main__':
    # Force material theme
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']

    # Init PyQt5
    app = QGuiApplication(sys.argv)
    qmlRegisterType(SVGElement, 'SVGElement', 1, 0, 'SVGElement')
    qmlRegisterType(CanBusWrapper, 'CanBusWrapper', 1, 0, 'CanBusWrapper')
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    engine = QQmlApplicationEngine()

    # Init networking
    networking = Networking()
    engine.rootContext().setContextProperty('networking', networking)
    
    # Init logs, state object
    state = MachineState()

    # Init gui handler for logs
    logPlayerHandler = LogPlayerHandler(reactor, state.consumeMessage)
    engine.rootContext().setContextProperty('logPlayerHandler', logPlayerHandler)

    # Init can adapter
    adapter = CanAdapter()
    # Connect consumer to adapter
    state.setCommandConsumer(adapter.sendMessage)

    # Init gui handler for logs
    canBusHandler = CanBusHandler(adapter, state.consumeMessage)
    engine.rootContext().setContextProperty('canBusHandler', canBusHandler)

    # Init binding for visualization - no need to have a timer to run to use this, unfinished
    modelWrapper = ModelWrapper(state)
    engine.rootContext().setContextProperty('modelWrapper', modelWrapper)

    # Init client model and handlers
    controller = ClientController()
    engine.rootContext().setContextProperty('controller', controller)
    clientListModel = ClientListModel([])
    engine.rootContext().setContextProperty('clientListModel', clientListModel)

    # Init Twisted logging
    appLogHandler = AppLogHandler()
    # observers = [appLogHandler.appendEvent]
    # Comment out the line above and uncomment the one below to output log to stdout
    observers = [textFileLogObserver(sys.stdout), appLogHandler.appendEvent]
    # log = Logger()
    #infoPredicate = LogLevelFilterPredicate(LogLevel.info)
    #logfilter = FilteringLogObserver(textFileLogObserver(sys.stdout), predicates=[infoPredicate])
    #observers = [textFileLogObserver(sys.stdout), appLogHandler.appendEvent]
    globalLogBeginner.beginLoggingTo(observers)
    #globalLogBeginner.beginLoggingTo([logfilter])
    engine.rootContext().setContextProperty('appLogHandler', appLogHandler)
    
    # Disable server until we rework the protocol
    ServerFactory = XSiteBroadcastServerFactory
    factory = ServerFactory(u"ws://127.0.0.1:9000",
                            reactor,
                            state,
                            lambda client: clientListModel.addClient(client),
                            lambda client: clientListModel.removeClient(client))
    factory.protocol = XSiteServerProtocol
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
