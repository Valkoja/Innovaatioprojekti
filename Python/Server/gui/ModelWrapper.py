from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QQuaternion
import math


class ModelWrapper(QObject):
    def __init__(self, stateObject):
        super().__init__()
        self.stateObject = stateObject
        self.stateObject.setUpdateCallback(self.update)

    def _main_boom(self):
        if 'main_boom' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['main_boom'] / 10
        else:
            return 40

    def _digging_arm(self):
        if 'digging_arm' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['digging_arm'] / 10
        else:
            return -100

    def _bucket(self):
        if 'bucket' in self.stateObject.getState()['angles']:
            return self.stateObject.getState()['angles']['bucket'] / 10
        else:
            return -90

    def _main_boomQuaternion(self):
        if 'main_boom_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['main_boom_orientation']
            # quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
        else:
            return 40

    def _digging_armQuaternion(self):
        if 'digging_arm_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['digging_arm_orientation']
            # quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
        else:
            return -60

    def _bucketQuaternion(self):
        if 'bucket_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['bucket_orientation']
            # quart = QQuaternion(components['w'], components['x'], components['y'], components['z']).toEulerAngles()
            return self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
        else:
            return -150

    def _limitLeft(self):
        if 'left' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['left']
        else:
            return False

    def _limitRight(self):
        if 'right' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['right']
        else:
            return False

    def _limitUpper(self):
        if 'upper' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['upper']
        else:
            return False

    def _limitLower(self):
        if 'lower' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['lower']
        else:
            return False

    def _limitForward(self):
        if 'forward' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['forward']
        else:
            return False

    def _limitProperty(self):
        if 'property' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['property']
        else:
            return False

    def _limitOverload(self):
        if 'overload' in self.stateObject.getState()['limitWarnings']:
            return self.stateObject.getState()['limitWarnings']['overload']
        else:
            return False

    def _heightFromZero(self):
        if 'height_from_zero' in self.stateObject.getState()['zeroLevel']:
            return self.stateObject.getState()['zeroLevel']['height_from_zero']
        else:
            return 0

    def _distanceToZero(self):
        if 'distance_to_zero' in self.stateObject.getState()['zeroLevel']:
            return self.stateObject.getState()['zeroLevel']['distance_to_zero']
        else:
            return 0

    def _heightToSlopeFromZero(self):
        if 'height_to_slope_from_zero' in self.stateObject.getState()['zeroLevel']:
            return self.stateObject.getState()['zeroLevel']['height_to_slope_from_zero']
        else:
            return 0

    def update(self):
        self.changed.emit()

    changed = pyqtSignal()
    mainBoomAngle = pyqtProperty(float, _main_boom, notify=changed)
    diggingArmAngle = pyqtProperty(float, _digging_arm, notify=changed)
    bucketAngle = pyqtProperty(float, _bucket, notify=changed)
    mainBoomAngleQuaternion = pyqtProperty(float, _main_boomQuaternion, notify=changed)
    diggingArmAngleQuaternion = pyqtProperty(float, _digging_armQuaternion, notify=changed)
    bucketAngleQuaternion = pyqtProperty(float, _bucketQuaternion, notify=changed)
    limitWarningLeft = pyqtProperty(bool, _limitLeft, notify=changed)
    limitWarningRight = pyqtProperty(bool, _limitRight, notify=changed)
    limitWarningUpper = pyqtProperty(bool, _limitUpper, notify=changed)
    limitWarningLower = pyqtProperty(bool, _limitLower, notify=changed)
    limitWarningForward = pyqtProperty(bool, _limitForward, notify=changed)
    limitWarningProperty = pyqtProperty(bool, _limitProperty, notify=changed)
    limitWarningOverload = pyqtProperty(bool, _limitOverload, notify=changed)
    heightFromZero = pyqtProperty(float, _heightFromZero, notify=changed)
    distanceToZero = pyqtProperty(float, _distanceToZero, notify=changed)
    heightToSlopeFromZero = pyqtProperty(float, _heightToSlopeFromZero, notify=changed)

    def toEulerXAngle(self, w, x, y, z):
        # roll (x-axis rotation)
        sinr_cosp = +2.0 * w * x + y * z
        cosr_cosp = +1.0 - 2.0 * x * x + y * y
        roll = math.atan2(sinr_cosp, cosr_cosp)
        return math.degrees(roll)