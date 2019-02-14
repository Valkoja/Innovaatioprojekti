from PyQt5.QtCore import QObject, pyqtSlot


class ModelBridge(QObject):
    def __init__(self, stateObject):
        super().__init__()
        self.stateObject = stateObject

    @pyqtSlot(result=float)
    def getBoomAngle(self):
		if 'main_boom' in self.stateObject.getState()['angles']:
			return self.stateObject.getState()['angles']['main_boom'] / 10
		else
			return 60

    @pyqtSlot(result=float)
    def getDiggingArmAngle(self):
		if 'digging_arm' in self.stateObject.getState()['angles']:
			return self.stateObject.getState()['angles']['digging_arm'] / 10
		else
			return 40

    @pyqtSlot(result=float)
    def getBucketAngle(self):
		if 'bucket' in self.stateObject.getState()['angles']:
			return self.stateObject.getState()['angles']['bucket'] / 10
		else
			return 20