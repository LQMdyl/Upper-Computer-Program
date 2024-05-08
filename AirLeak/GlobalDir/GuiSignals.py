from PyQt5.QtCore import pyqtSignal, QObject

class cGuiSignals(QObject):
    tbvwLogSignal = pyqtSignal(str, str, bool)
    lblDeviceStatus = pyqtSignal(str, bool)
    testStatus = pyqtSignal(int)
    lbCheckTime = pyqtSignal(str)
    lbTestTime = pyqtSignal(str)
    leBarcode = pyqtSignal(str)
    lbMesUpload = pyqtSignal(bool)
    tbvwTestData = pyqtSignal(str, str, str, str, str, str)
    msgForBox = pyqtSignal(str, str, int)
    lockEngineSignal = pyqtSignal()
    unLockEngineSignal = pyqtSignal()
    clearTestSignal = pyqtSignal()
    barcodeScanSignal = pyqtSignal(str)
    lbTotalSignal = pyqtSignal(str)
    lbPassSignal = pyqtSignal(str)
    lbFailSignal = pyqtSignal(str)
    lbYieldSignal = pyqtSignal(str)
    menubarSignal = pyqtSignal(bool)
    roleSignal = pyqtSignal(str, str)
    waitTimeSignal = pyqtSignal()
    waitTimeConfigSignal = pyqtSignal()

    def tbvwLogEmit(self, text = str, color = str, writeMode: bool = False):
        self.tbvwLogSignal.emit(text, color, writeMode)

    def lblDeviceStatusEmit(self, device:str, status:bool):
        self.lblDeviceStatus.emit(device, status)

    def testStatusEmit(self, status = int):
        self.testStatus.emit(status)

    def lbCheckTimeEmit(self, text = str):
        self.lbCheckTime.emit(text)

    def lbTestTimeEmit(self, text = str):
        self.lbTestTime.emit(text)

    def leBarcodeEmit(self, text = str):
        self.leBarcode.emit(text)

    def lbMesUploadEmit(self, enable = bool):
        self.lbMesUpload.emit(enable)

    def tbvwTestDataEmit(self, barcode:str, result:str, upperLimit:str, lowerLimit:str, units:str, value:str):
        self.tbvwTestData.emit(barcode, result, upperLimit, lowerLimit, units, value)

    def showMsgBox(self, title: str = '', text: str = '', lvl:int = 0):
        self.msgForBox.emit(title, text, lvl)

    def lockEngine(self):
        self.lockEngineSignal.emit()

    def unlockEngine(self):
        self.unLockEngineSignal.emit()

    def clearTestData(self):
        self.clearTestSignal.emit()

    def barcodeScan(self, barcode: str):
        self.barcodeScanSignal.emit(barcode)

    def updateTotal(self, txt: str):
        self.lbTotalSignal.emit(txt)

    def updatePass(self, txt:str):
        self.lbPassSignal.emit(txt)

    def updateFail(self, txt:str):
        self.lbFailSignal.emit(txt)

    def updateYield(self, txt:str):
        self.lbYieldSignal.emit(txt)

    def showMenu(self, enable:bool):
        self.menubarSignal.emit(enable)

    def changeRole(self, role:str, userName:str):
        self.roleSignal.emit(role, userName)

    def waitTimeEmit(self):
        self.waitTimeSignal.emit()

    def waitTimeLoad(self):
        self.waitTimeConfigSignal.emit()
