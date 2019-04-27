from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QQuaternion
import math


class ModelWrapper(QObject):
    def __init__(self, stateObject):
        super().__init__()
        self.stateObject = stateObject
        self.stateObject.setUpdateCallback(self.update)
        self.zeroTimestamp = -1
        self.slopeTimestamp = -1
        self.cache = {
            'main_boom_angle_from_quaternion': 40,
            'digging_arm_angle_from_quaternion': -60,
            'bucket_angle_from_quaternion': -150}

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
            if components['w'] and components['x'] and components['y'] and components['z']:
                angle = self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
                self.cache['main_boom_angle_from_quaternion'] = angle
                return angle

        return self.cache['main_boom_angle_from_quaternion']

    def _digging_armQuaternion(self):
        if 'digging_arm_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['digging_arm_orientation']
            if components['w'] and components['x'] and components['y'] and components['z']:
                angle = self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
                self.cache['digging_arm_angle_from_quaternion'] = angle
                return angle

        return self.cache['digging_arm_angle_from_quaternion']

    def _bucketQuaternion(self):
        if 'bucket_orientation' in self.stateObject.getState()['quaternions']:
            components = self.stateObject.getState()['quaternions']['bucket_orientation']
            if components['w'] and components['x'] and components['y'] and components['z']:
                angle = self.toEulerXAngle(components['w'], components['x'], components['y'], components['z'])
                self.cache['bucket_angle_from_quaternion'] = angle
                return angle

        return self.cache['bucket_angle_from_quaternion']

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

    def _slope(self):
        return self.stateObject.getState()['slope']

    def update(self):
        self.changed.emit()

        if self.zeroTimestamp < self.stateObject.getState()['zero_with_bucket_tip']:
            self.zeroTimestamp = self.stateObject.getState()['zero_with_bucket_tip']
            self.zeroChanged.emit()

        if self.slopeTimestamp < self.stateObject.getState()['set_slope']:
            self.slopeTimestamp = self.stateObject.getState()['set_slope']
            self.getSlope()

    changed = pyqtSignal()
    zeroChanged = pyqtSignal()

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
    slope = pyqtProperty(float, _slope, notify=changed)

    @pyqtSlot(float)
    def setSlope(self, slope):
        self.stateObject.consumeCommand('set_slope', slope)

    @pyqtSlot()
    def getSlope(self):
        self.stateObject.consumeCommand('get_slope')

    @pyqtSlot()
    def setZero(self):
        self.stateObject.consumeCommand('zero_with_bucket_tip')

    @pyqtSlot()
    def emitZero(self):
        self.zeroChanged.emit()

    @staticmethod
    def toEulerXAngle(w, x, y, z):
        # roll (x-axis rotation)
        sinr_cosp = +2.0 * (w * x + y * z)
        cosr_cosp = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        return math.degrees(roll)
