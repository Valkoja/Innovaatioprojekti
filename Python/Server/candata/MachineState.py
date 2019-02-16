from string import Template
import re

class MachineState():
    def __init__(self):
        self._properties = dict()
        self._properties['limitWarnings'] = dict()
        self._properties['zeroLevel'] = dict()
        self._properties['angles'] = dict()
        self._properties['quarternions'] = dict()
        self._modelUpdated = None

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
        elif messagetype.endswith('quarternion'):
            kind = re.sub(r'\_quarternion$', '', messagetype)
            self._properties['quarternions'][re.sub(r'\_quarternion$', '', kind)] = dict()
            for name, value in message._asdict().items():
                self._properties['quarternions'][kind][re.sub(r'\_orientation$', '', name)] = value
                
        else:
            print('Unknown message')
            
        # If we have a cb, call it now
        if self._modelUpdated:
            print(self.getState())
            self._modelUpdated()

    def setUpdateCallback(self, cb):
        self._modelUpdated = cb
    
    def getState(self):
        return self._properties