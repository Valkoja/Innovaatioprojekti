from string import Template
import re

class MachineState():
    def __init__(self):
        self._properties = dict()
        self._properties['limitWarnings'] = dict()
        self._properties['zeroLevel'] = dict()
        self._properties['angles'] = dict()
        self._properties['quaternions'] = dict()
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
        elif messagetype.endswith('quaternion'):
            kind = re.sub(r'\_quaternion$', '', messagetype)
            self._properties['quaternions'][re.sub(r'\_quaternion$', '', kind)] = dict()
            for name, value in message._asdict().items():
                self._properties['quaternions'][kind][re.sub(r'\_orientation$', '', name)] = value
                
        else:
            print('Unknown message')
            
        # If we have a cb, call it now
        if self._modelUpdated:
            #print(self.getState())
            self._modelUpdated()

    def setUpdateCallback(self, cb):
        self._modelUpdated = cb
    
    def getState(self):
        return self._properties