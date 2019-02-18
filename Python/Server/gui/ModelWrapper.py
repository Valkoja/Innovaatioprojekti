from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QQuaternion

class ModelWrapper(QObject):
    def __init__(self, stateObject, useQuarternions=True):
        super().__init__()
        self.stateObject = stateObject
        self.stateObject.setUpdateCallback(self.update)
        self.useQuarternions = useQuarternions

    def _main_boom(self):
        if self.useQuarternions and 'main_boom_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['main_boom_orientation']
            quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return quart.x()
        elif not self.useQuarternions and 'main_boom' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['main_boom'] / 10
        else:
            return 60

    def _digging_arm(self):
        if self.useQuarternions and 'digging_arm_orientatation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['digging_arm_orientation']
            quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return quart.x()
        elif not self.useQuarternions 'digging_arm' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['digging_arm'] / 10
        else:
            return 40

    def _bucket(self):
        if self.useQuarternions and 'bucket_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['bucket_orientation']
            quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return quart.x()
        elif not self.useQuarternions 'bucket' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['bucket'] / 10
        else:
            return 20

    def update(self):
        self.changed.emit()

    changed = pyqtSignal()
    mainBoomAngle = pyqtProperty(float, _main_boom, notify=changed)
    diggingArmAngle = pyqtProperty(float, _digging_arm, notify=changed)
    bucketAngle = pyqtProperty(float, _bucket, notify=changed)
