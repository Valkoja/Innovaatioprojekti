from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty


class ModelWrapper(QObject):
    def __init__(self, state):
        super().__init__()
        self._state = state

    def _main_boom(self):
        return float(self._state.getState()['angles']['main_boom'] / 10)

    def _digging_arm(self):
        return float(self._state.getState()['angles']['digging_arm'] / 10)

    def _bucket(self):
        return float(self._state.getState()['angles']['bucket'] / 10)

    changed = pyqtSignal()
    mainBoom = pyqtProperty(float, _main_boom, notify=changed)
    diggingArm = pyqtProperty(float, _digging_arm, notify=changed)
    bucket = pyqtProperty(float, _bucket, notify=changed)