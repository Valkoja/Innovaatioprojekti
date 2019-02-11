from PyQt5.QtCore import QObject, pyqtSlot


class ModelBridge(QObject):
    def __init__(self, stateObject):
        super().__init__()
        self.stateObject = stateObject

    @pyqtSlot(result=float)
    def getBoomAngle(self):
        return self.stateObject.getState()['angles']['main_boom'] / 10

    @pyqtSlot(result=float)
    def getDiggingArmAngle(self):
        return self.stateObject.getState()['angles']['digging_arm'] / 10

    @pyqtSlot(result=float)
    def getBucketAngle(self):
        return self.stateObject.getState()['angles']['bucket'] / 10