from string import Template

class MachineState():
    def __init__(self):
        self._properties = dict()
        self._properties['limitWarnings'] = dict()
        self._properties['zeroLevel'] = dict()
        self._properties['angles'] = dict()

    def consumeMessage(self, message):
        if type(message).__name__ == 'limit_warnings':
            for name, value in message._asdict().items():
                self._properties['limitWarnings'][name] = value
        elif type(message).__name__.startswith('zero_level'):
            for name, value in message._asdict().items():
                self._properties['zeroLevel'][name] = value
        elif type(message).__name__.startswith('angles'):
            for name, value in message._asdict().items():
                self._properties['angles'][name] = value
        else:
            print('Unknown message')
    
    def getState(self):
        return self._properties