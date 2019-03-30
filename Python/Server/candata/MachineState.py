import re


class MachineState():
    def __init__(self):
        self._properties = dict()
        self._properties['limitWarnings'] = dict()
        self._properties['zeroLevel'] = dict()
        self._properties['angles'] = dict()
        self._properties['quaternions'] = dict()
        self._properties['slope'] = 0
        self._modelUpdated = None
        self._commandConsumer = None

    def consumeMessage(self, message):
        messagetype = type(message).__name__ 
        if messagetype == 'limit_warnings':
            for name, value in message._asdict().items():
                self._properties['limitWarnings'][name] = value
        elif messagetype.startswith('zero_level'):
            for name, value in message._asdict().items():
                self._properties['zeroLevel'][name] = value
        elif messagetype.startswith('angles'):
            for name, value in message._asdict().items():
                self._properties['angles'][name] = value
        elif messagetype.endswith('quaternion'):
            kind = re.sub(r'\_quaternion$', '', messagetype)
            self._properties['quaternions'][re.sub(r'\_quaternion$', '', kind)] = dict()
            for name, value in message._asdict().items():
                self._properties['quaternions'][kind][re.sub(r'\_orientation$', '', name)] = value
        elif messagetype == 'slope':
            self._properties['slope'] = message.slope
        else:
            print('Unknown message')
            
        # If we have a cb, call it now
        if self._modelUpdated:
            self._modelUpdated()

    def setCommandConsumer(self, consumer):
        self._commandConsumer = consumer

    def consumeCommand(self, command, argument=None):
        if self._commandConsumer:
            self._commandConsumer(command, argument)

    def setUpdateCallback(self, cb):
        self._modelUpdated = cb
    
    def getState(self):
        return self._properties
