from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty


class ModelWrapper(QObject):
    def __init__(self, stateObject):
        super().__init__()
        self.stateObject = stateObject
        self.stateObject.setUpdateCallback(self.update)

    def _main_boom(self):
        if 'main_boom' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['main_boom'] / 10
        else:
            return 60

    def _digging_arm(self):
        if 'digging_arm' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['digging_arm'] / 10
        else:
            return 40

    def _bucket(self):
        if 'bucket' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['bucket'] / 10
        else:
            return 20

    def update(self):
        self.changed.emit()

    changed = pyqtSignal()
    mainBoomAngle = pyqtProperty(float, _main_boom, notify=changed)
    diggingArmAngle = pyqtProperty(float, _digging_arm, notify=changed)
    bucketAngle = pyqtProperty(float, _bucket, notify=changed)