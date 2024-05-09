from PyQt5.QtCore import pyqtSignal, QObject

class cGuiSignals(QObject):
    TextBrowserSignal = pyqtSignal(str, str, bool)
    leBarcodeSignal = pyqtSignal(str)
    leTotalSignal = pyqtSignal(str)
    lePassSignal = pyqtSignal(str)
    leFailSignal = pyqtSignal(str)
    leYieldSignal = pyqtSignal(str)
    lblTestTimeSignal = pyqtSignal(str)
    tableWidgetSignal = pyqtSignal(str, str, str, str, bool, str)
    lbStatueSignal=pyqtSignal(int, bool)
    lbDeviceStatueSignal = pyqtSignal(str, bool)
    lbAngelorDistanceSignal = pyqtSignal( str, str )
    lbTestResultSignal = pyqtSignal(str)
    lbRobotLocationSignal = pyqtSignal(str,str,str,str,str,str)
    lbCheckTime = pyqtSignal(str)



    def TextBrowserEmit(self, text = str, fontColor = str, clear = bool):
        self.TextBrowserSignal.emit(text, fontColor, clear)

    def lbAngleorDistanceEmit(self, Angle=str, Distance=str):
        self.lbAngelorDistanceSignal.emit( Angle,Distance )

    def leBarcodeEmit(self, text = str):
        self.leBarcodeSignal.emit(text)

    def lbCheckTimeEmit(self, text = str):
        self.lbCheckTime.emit(text)

    def lbRobotLoactionEmit(self,x,y,z,u,v,w):
        self.lbRobotLocationSignal.emit(str(round(x,4)),str(round(y,4)),str(round(z,4)),str(round(u,4)),str(v),str(w))

    def leTotalEmit(self, text = str):
        self.leTotalSignal.emit(text)

    def lePassEmit(self, text = str):
        self.lePassSignal.emit(text)

    def leFailEmit(self, text = str):
        self.leFailSignal.emit(text)

    def leYieldEmit(self, text = str):
        self.leYieldSignal.emit(text)

    def lbtestResultEmit(self, text = str):
        self.lbTestResultSignal.emit(text)

    def lblTestTimeEmit(self, text = str):
        self.lblTestTimeSignal.emit(text)

    def lblStatueEmit(self, index=int, statue=bool):
        self.lbStatueSignal.emit(index,statue)

    def lblDeviceStatueEmit(self, index=str, statue=bool):
        self.lbDeviceStatueSignal.emit( index, statue )

    def tableWidgetEmit(self, Name, High, Low, Value, Result, Unit):
        self.tableWidgetSignal.emit(Name, High, Low, Value, Result, Unit)