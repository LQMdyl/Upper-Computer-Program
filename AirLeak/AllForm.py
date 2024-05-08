import json
import sys
import time
from datetime import datetime
import threading

import requests
from PyQt5.QtWidgets import QMessageBox, QWidget, QLineEdit, QInputDialog, QFileDialog, QApplication
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem
from PyQt5.QtGui import QRegExpValidator,QImage, QPixmap
from Login import  Ui_Login
from LogDir.AllLog import cAllLog
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import QRegExp, Qt
from SetConf import Ui_ConfigureForm
from unlock import Ui_UnlockForm
from UploadTestForm import Ui_UploadTestForm
from DevicesConfigForm import Ui_DevicesConfigForm
from ConfigureDir.Configure import cConfigure
from ConfigureDir.Configure import cUseCount
from ConfigureDir import ConfigureKey
from ConfigureDir.Limit import cLimit
from ConfigureDir import LimitKey
from GlobalDir.GlobalGui import global_Gui
from GlobalDir import GlobalConf
from TestDir.TestEngine import cTestEngine
from TestDir.TestItem import cTestItem, cReturnMessage
from DeviceDir.WorkerIntegra import cWorkerIntegra
from DeviceDir.CCD import Camera
from DeviceDir.Modbusclient import cModbusclient
from DeviceDir.Scan import cScan
from PLCtestForm import Ui_PlcTestForm
from ScanTestForm import Ui_scanTestForm
from OperatorChange import  Ui_OperatorChangeForm
from Mes.CheckRole import cCheckRole
import cv2

class cLogin(QWidget, Ui_Login):
    def __init__(self, parent = None):
        super(cLogin, self).__init__()
        self.setupUi(self)
        self.pbLogin.clicked.connect(self.pbLogin_clicked)
        self.pbExit.clicked.connect(self.pbExit_clicked)
        self.login = False
        #self.comblist = self.findChildren(QComboBox)
        self.logname = datetime.now().strftime('%Y-%m-%d') + '_log'
        self.log = cAllLog(self.logname)
        self.content = []

        self.conf = cConfigure()
        self.openResult = self.formOpen()
        if not self.openResult:
            self.pbLogin.setEnabled(False)

    def pbExit_clicked(self):
        self.log.writelog( '退出程序')
        self.close()

    def pbLogin_clicked(self):
        if not self.lineEdit_1.text() == '':
            if not self.lineEdit_1.text() == 'GTS' and not self.lineEdit_2.text() == 'GTS':
                check = cCheckRole(self.comboBox_1.currentIndex(), self.lineEdit_1.text(), self.lineEdit_2.text())
                result, txt = check.login()
                if not result:
                    QMessageBox.information(self, '提示', '登录失败!' + txt, QMessageBox.Ok)
                    return

            self.log.writelog(self.lineEdit_1.text() + '登录成功')
            self.loginSuccess()
            self.mainWindow = cMainWindow()
            self.mainWindow.lb_ProgramName.setText(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_PROGRAM])
            if self.comboBox_1.currentIndex() > 0:
                self.mainWindow.setMenuEnable(True)
            else:
                self.mainWindow.setMenuEnable(False)
            print('role:',self.comboBox_1.currentIndex())
            self.mainWindow.testEngine.OpID = self.lineEdit_1.text()
            self.mainWindow.lbRole.setText(self.comboBox_1.currentText())
            self.mainWindow.lbProject.setText(self.comboBox_5.currentText())
            self.mainWindow.lbWorkArea.setText(self.comboBox_6.currentText())
            self.mainWindow.lbOperator.setText(self.lineEdit_1.text())
            self.mainWindow.lbFixtureid.setText(self.comboBox_2.currentText())
            self.mainWindow.lbTestType.setText(self.comboBox_3.currentText())
            self.mainWindow.lbPartnumber.setText(self.comboBox_4.currentText())
            self.mainWindow.StarttestEgineThread()
            self.mainWindow.startWaitThread()
            self.mainWindow.show()
            self.close()
            return
        else:
            QMessageBox.information(self, '提示', '登录失败!操作员ID不能为空', QMessageBox.Ok)
            return
    def formOpen(self):
        try:
            # 软件名+供应商+月+IP 地址+设备编号
            self.log.writelog('打开程序')
            if len(self.conf.ConfigureDic) <= 0:
                QMessageBox.information(self, '提示', '读取登录信息失败，请检查配置文件', QMessageBox.Ok)
                self.log.writelog('读取登录信息失败， 请检查配置文件')
                return False
            self.comboBox_2.addItem(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_FIXTURE_ID])
            #self.comboBox_3.addItem(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_LINE_ID])
            if self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_TEST_TYPE] == 'LEAK-OQC':
                self.comboBox_3.setCurrentIndex(0)
            else :
                self.comboBox_3.setCurrentIndex(1)
            self.comboBox_4.addItem(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_PART_NUMBER])
            self.comboBox_5.addItem(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_PROJECT_NAME])
            self.comboBox_6.addItem(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_WORK_AREA])
            self.lineEdit_1.setText(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_OPERATOR])
            return True
        except Exception as e:
            QMessageBox.information(self, '提示', '打开程序失败, 请检查配置文件', QMessageBox.Ok)
            self.log.writelog('打开程序失败!' + str(e))
            return False
    # def formOpen(self):
    #     # 软件名+供应商+月+IP 地址+设备编号
    #     openLog = cAllLog(self.logname)
    #     #openLog.clearlog()
    #     openLog.writelog('打开程序')
    #     if os.path.exists(self.loginpath):
    #         with open(self.loginpath, 'r', encoding='utf-8') as fr:
    #             self.logininf = fr.readlines()
    #     if len(self.logininf )< 8:
    #         QMessageBox.information(self, '提示', '读取登录信息失败!', QMessageBox.Ok)
    #         return
    #
    #     for num,inf in enumerate(self.logininf):
    #         equalpo = inf.find('=')
    #         lipo = inf.find('\n')
    #         if num == 0:
    #             self.comboBox_1.setCurrentIndex(int(inf[equalpo + 1:lipo:]))
    #         elif num == 7:
    #             #self.lineEdit_1.setText(inf[equalpo + 1:lipo:])
    #             self.lineEdit_1.setText('GTS')
    #         else:
    #             self.comblist[num].addItem(inf[equalpo + 1:lipo:])
    #         self.content.append(inf[:equalpo + 1:])

    def loginSuccess(self):
        try:
            if not self.login:
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_FIXTURE_ID, self.comboBox_2.currentText())
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_TEST_TYPE, self.comboBox_3.currentText())
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_PART_NUMBER, self.comboBox_4.currentText())
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_PROJECT_NAME, self.comboBox_5.currentText())
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_WORK_AREA, self.comboBox_6.currentText())
                self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_OPERATOR, self.lineEdit_1.text())
                self.login = True
        except Exception as e:
            self.log.writelog('打开程序失败!' + str(e))
            print(e)

class cMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(cMainWindow, self).__init__()
        self.setupUi(self)
        self.testEngine = cTestEngine()
        self.testItem = cTestItem()
        self.conf = cConfigure()
        self.conf.loadConfigure()
        self.OperatorForm = cOperatorChange()
        self.le_barcode.returnPressed.connect(self.barcodeInput)
        self.actionChangeOperator.triggered.connect(self.channgeOperator)
        self.actionCheck.triggered.connect(self.setCheck)
        self.actionSample.triggered.connect(self.setSample)
        self.actionSettleConfig.triggered.connect(self.configShow)
        self.actionDevicesConfig.triggered.connect(self.devicesShow)
        self.actionUploadTest.triggered.connect(self.uploadShow)
        self.actionScanTest.triggered.connect(self.showScanTestForm)
        self.actionClearYield.triggered.connect(self.clearYield)
        self.actionUploadTest.setVisible(False)
        self.menubar.addAction(self.actionUploadTest)
        self.isLocking = False
        self.waitTime = datetime.now()
        self.waitTimeConfig = float(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_WAIT_TIME])
        self.timeCountThread: threading.Thread = None
        self.closeSignal = False
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.updateTestTime)
        # self.timer.start(1000)

        self.logname = datetime.now().strftime('%Y-%m-%d') + '_log'
        self.log = cAllLog(self.logname)
        global_Gui.tbvwLogSignal.connect(self.logshow)
        global_Gui.testStatus.connect(self.updateTestStatus)
        global_Gui.lblDeviceStatus.connect(self.updateDeviceStatus)
        global_Gui.lbCheckTime.connect(self.updateCheckTime)
        global_Gui.lbTestTime.connect(self.updateTestTime)
        global_Gui.leBarcode.connect(self.updateBarcode)
        global_Gui.lbMesUpload.connect(self.updateMesUpload)
        global_Gui.tbvwTestData.connect(self.updateTestData)
        global_Gui.msgForBox.connect(self.msgBox)
        global_Gui.lockEngineSignal.connect(self.lockEngine)
        global_Gui.unLockEngineSignal.connect(self.lockConfirm)
        global_Gui.clearTestSignal.connect(self.clearTestData)
        global_Gui.barcodeScanSignal.connect(self.barcodeRead)
        global_Gui.lbTotalSignal.connect(self.updateTotal)
        global_Gui.lbPassSignal.connect(self.updatePass)
        global_Gui.lbFailSignal.connect(self.updateFail)
        global_Gui.lbYieldSignal.connect(self.updateYield)
        global_Gui.menubarSignal.connect(self.setMenuEnable)
        global_Gui.roleSignal.connect(self.setRole)
        global_Gui.waitTimeSignal.connect(self.updateWaitTime)
        global_Gui.waitTimeConfigSignal.connect(self.updateConfig)

    def setMenuEnable(self, enable:bool):
        try:
            self.menuConfig.setEnabled(enable)
            self.menuTest.setEnabled(enable)
        except Exception as e:
            print(e)

    def channgeOperator(self):
        self.OperatorForm.exec()

    def setRole(self, role, userName):
        self.lbRole.setText(role)
        self.lbOperator.setText(userName)
    def setCheck(self):
        pass

    def setSample(self):
        self.testEngine.isSample = not self.testEngine.isSample
        color = self.testEngine.isSample and GlobalConf.passColor or GlobalConf.errorColor
        msg = self.testEngine.isSample and '进入样本测试' or '退出样本测试'
        self.log.writeAllLog(msg, True, GlobalConf.colorGreen, False, True)
        self.lbSample.setStyleSheet(color)

    def configShow(self):
        global_Gui.waitTimeEmit()
        self.confWindow = cSetConfigure()
        if self.confWindow.openresult:
            self.confWindow.exec()

    def devicesShow(self):
        global_Gui.waitTimeEmit()
        self.devicesWindow = cDevicesConfigForm()
        self.devicesWindow.exec()

    def uploadShow(self):
        global_Gui.waitTimeEmit()
        self.uploadWindow = cUploadTestForm()
        self.uploadWindow.exec()

    def updateDataTable(self, barcode, failItem, result):
        self.tbvwData.scrollToBottom()

    def updateBarcode(self, text):
        self.le_barcode.setText(text)

    def updateTestTime(self, text):
        self.lb_testtime.setText(text)

    def updateCheckTime(self, text):
        self.lb_check.setText(text)

    def updateWaitTime(self):
        self.waitTime = datetime.now()

    def updateConfig(self):
        self.waitTimeConfig = float(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_WAIT_TIME])

    def logshow(self, content: str, color: str = GlobalConf.colorGreen,clear: bool = False):
        writecontent ='<font color = ' + color +'> [' + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f') +'] ' +content
        if clear:
            self.txtLog.clear()
        self.txtLog.append(writecontent)
        self.log.writelog(content)
        self.txtLog.moveCursor(self.txtLog.textCursor().End)


    def barcodeRead(self, barcode:str = ''):
        self.le_barcode.setText(barcode)
        # <测试用代码>
        # self.Lock = False
        # self.thr = threading.Thread(target=self.thre1, name='test1')
        # self.thr.start()
        # return
        # global_Gui.tbvwLogEmit(self.le_barcode.text(), GlobalConf.colorGreen)
        # if len(self.le_barcode.text()) <=4:
        #     self.updateTestStatus(len(self.le_barcode.text()))
        # if len(self.le_barcode.text()) == 5:
        #     self.testlogin()
        # #self.updateDataTable(self.le_barcode.text(), self.testLine % 3 == 0 and '' or f'{self.testLine}_{self.le_barcode.text()}', self.testLine % 3 == 0 and 'pass' or 'fail')
        # #self.updateTestData(self.testLine, self.le_barcode.text(), self.testLine % 3 == 0 and 'pass' or 'fail', self.testLine % 3 == 0 and '' or f'{self.testLine}_{self.le_barcode.text()}')
        # if self.le_barcode.text().lower() == 'change mode':
        #     self.testEngine.TestModel = self.testEngine.TestModel == 'DOE' and 'OP' or 'DOE'
        #     self.logshow(f'MODEL:{self.testEngine.TestModel}', GlobalConf.colorGreen)
        # </测试用代码>
    def barcodeInput(self):
        #if self.le_barcode.text() == 'clear':
          #  self.clearTestData()
         #   return
        #self.updateTestData('barcode', 'result', 'upperlimt', 'lowerlimt','units','value')
        global_Gui.waitTimeEmit()
        if str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_SCAN_TYPE]) == 'A':
            return
        self.testEngine.barcode = self.le_barcode.text()
        # self.tempThread = threading.Thread(target=self.testEngine.TestFunction, name='InputTest')
        # self.tempThread.start()

    #<测试用代码>
    # def thre1(self):
    #     self.thr1 = threading.Thread(target=self.threte, name='test2')
    #     self.thr1.start()
    #     print('thre1 wait 2s')
    #     time.sleep(2)
    #     print('thre1 wait finish')
    # def threte(self):
    #     self.testEngine.showZeroAlarm(self.le_barcode.text())
    #     self.isclose = True
    #     print('thre2 wait 2s')
    #     time.sleep(2)
    #     print('thre2 wait finish')
    #</测试用代码>

    def updateTestStatus(self, status: int):
        if status == GlobalConf.statusIdel:
            lbtxt = GlobalConf.txtIdel
            color = GlobalConf.idelColor
        if status == GlobalConf.statusTest:
            lbtxt = GlobalConf.txtTest
            color = GlobalConf.testColor
        if status == GlobalConf.statusPass:
            lbtxt = GlobalConf.txtPass
            color = GlobalConf.passColor
        if status == GlobalConf.statusFail:
            lbtxt = GlobalConf.txtFail
            color = GlobalConf.failColor
        if status == GlobalConf.statusError:
            lbtxt = GlobalConf.txtError
            color = GlobalConf.errorColor
        self.lb_Status.setText(lbtxt)
        self.lb_Status.setStyleSheet(color)

    def updateDeviceStatus(self, device: str, status: bool):
        color = status and GlobalConf.passColor or GlobalConf.errorColor
        if device == GlobalConf.SCAN:
            if status:
                lbtxt = '扫码枪已连接'
            else:
                lbtxt = '扫码枪未连接'
            self.lb_scan1.setText(lbtxt)
            self.lb_scan1.setStyleSheet(color)
        if device == GlobalConf.WORKER_INTEGRA:
            if status:
                lbtxt = 'WorkerIntegra已连接'
            else:
                lbtxt = 'WorkerIntegra未连接'
            self.lb_workerIntegra.setText(lbtxt)
            self.lb_workerIntegra.setStyleSheet(color)
        if device == GlobalConf.PLC:
            if status:
                lbtxt = 'PLC已连接'
            else:
                lbtxt = 'PLC未连接'
            self.lb_plc.setText(lbtxt)
            self.lb_plc.setStyleSheet(color)


    def updateMesUpload(self, enable: bool):
        color = enable and GlobalConf.passColor or GlobalConf.errorColor
        self.lbMesUpload.setStyleSheet(color)

    def StarttestEgineThread(self):
        testThread = threading.Thread( target=self.testEngine.Initialize(), name='TestEngine')
        testThread.setDaemon(True)
        testThread.start()
        #self.debugFormLoad()

    def startWaitThread(self):
        self.timeCountThread = threading.Thread(target=self.testTimeCount, name='WaitTime')
        self.timeCountThread.start()

    def testTimeCount(self):
        while True:
            time.sleep(0.5)
            Interval = datetime.now() - self.waitTime
            #print(Interval.total_seconds())

            if round(Interval.total_seconds(), 2) > self.waitTimeConfig or self.closeSignal:
                break
        self.close()
        

    def closeEvent(self, event) -> None:
        self.closeSignal = True
        event.accept()

    def updateTestData(self, barcode:str, result:str, upperLimit:str, lowerLimit:str, units:str, value:str):
        row = self.tbvwTest.rowCount()
        self.tbvwTest.insertRow(self.tbvwTest.rowCount())
        self.tbvwTest.setItem(row, 0, QTableWidgetItem(barcode))
        self.tbvwTest.setItem(row, 1, QTableWidgetItem(result))
        self.tbvwTest.setItem(row, 2, QTableWidgetItem(upperLimit))
        self.tbvwTest.setItem(row, 3, QTableWidgetItem(lowerLimit))
        self.tbvwTest.setItem(row, 4, QTableWidgetItem(units))
        self.tbvwTest.setItem(row, 5, QTableWidgetItem(value))
        self.tbvwTest.scrollToBottom()

    def clearTestData(self):
        # 清除列表数据 ，使用clear会导致标题也被清除，因此用clearContents
        self.tbvwTest.clearContents()
        # 表格行数置为0，不置0不会从头开始写
        self.tbvwTest.setRowCount(0)

    def clearYield(self):
        if not self.testEngine.ClearCounter():
            global_Gui.tbvwLogEmit('良率清除失败', GlobalConf.colorRed)
            return
        global_Gui.tbvwLogEmit('良率清除成功', GlobalConf.colorGreen)

    def msgBox(self, title: str = '', text: str = '', lvl: int = 0):
        try:
            if lvl == 0:
                QMessageBox.information(self, title, text, QMessageBox.Ok)
            elif lvl == 1:
                QMessageBox.warning(self, title, text, QMessageBox.Ok)
        except Exception as e:
            print(e)

    def lockEngine(self):
        try:
            self.unlockForm = cUnlock()
            self.unlockForm.setWindowFlag(Qt.WindowCloseButtonHint, False)
            self.unlockForm.exec()
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    def lockConfirm(self):
        try:
            self.isLocking = False
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    # def resetPlc(self):
    #     try:
    #         result1 = self.testEngine.plc.Write_coil(7, 1)
    #         time.sleep(0.5)
    #         result2 = self.testEngine.plc.Write_coil(7, 0)
    #         print(f'result:{result1&result2}')
    #     except Exception as e:
    #         print(e)
    #         global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    def showScanTestForm(self):
        try:
            global_Gui.waitTimeEmit()
            self.scanTest = cScanTestForm()
            self.scanTest.exec()
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    def updateTotal(self, txt: str):
        self.lbTotal.setText(txt)

    def updatePass(self, txt: str):
        self.lbPass.setText(txt)

    def updateFail(self, txt: str):
        self.lbFail.setText(txt)

    def updateYield(self, txt: str):
        self.lbYield.setText(txt + '%')

class cSetConfigure(QDialog, Ui_ConfigureForm):
    def __init__(self, parent=None):
        super(cSetConfigure, self).__init__()
        self.setupUi(self)
        self.conf = cConfigure()
        self.limitConf = cLimit()
        self.pbSave.clicked.connect(self.ptbSave_click)
        self.pbLogPath.clicked.connect(self.pbLogPath_click)
        self.pbDataPath.clicked.connect(self.pbDataPath_click)
        self.logPathDlg = QFileDialog()
        self.dataPathDlg = QFileDialog()
        self.filelog = cAllLog(datetime.now().strftime('%Y-%m-%d') + '_log')
        regExpHead = QRegExp('^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])$') # 1 ~ 255
        self.leip1.setValidator(QRegExpValidator(regExpHead))
        regExpBody = QRegExp('^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$') # 0 ~ 255
        self.leip2.setValidator(QRegExpValidator(regExpBody))
        self.leip3.setValidator(QRegExpValidator(regExpBody))
        self.leip4.setValidator(QRegExpValidator(regExpBody))
        self.openresult = self.confShow()
        print(self.conf.ConfigureDic)

    def ptbSave_click(self):
        try:
            result, hours = self.str2float(self.leCheck.text())
            if not result:
                QMessageBox.information(self, '提示', '无法识别点检时间', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, delay = self.str2float(self.leDelay.text())
            if not result:
                QMessageBox.information(self, '提示', '无法识别超时时长', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, waitTime = self.str2float(self.leWaitTime.text())
            if not result:
                QMessageBox.information(self, '提示', '无法识别程序自动关闭时长', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, hostport = self.str2int(self.leHostPort.text())
            if not  result:
                QMessageBox.information(self, '提示', '无法识别端口', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, upperlimit = self.str2float(self.leUpperLimit.text())
            if not result:
                QMessageBox.information(self, '提示', '测试上限无法识别', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, lowlimit = self.str2float(self.leLowerLimit.text())
            if not result:
                QMessageBox.information(self, '提示', '测试下限无法识别', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, barcodeCnt = self.str2int(self.leBarcodeLenth.text())
            if not result:
                QMessageBox.information(self, '提示', '条码长度无法识别', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return

            result, useCount = self.str2int(self.leNozzle.text())
            if not result:
                QMessageBox.information(self, '提示', '吸嘴使用报警次数无法识别', QMessageBox.Ok)
                global_Gui.tbvwLogEmit('系统配置保存失败', GlobalConf.colorRed)
                return
            hostIp = '{0}.{1}.{2}.{3}'.format(self.leip1.text(), self.leip2.text(), self.leip3.text(), self.leip4.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_LOG, self.leLogPath.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_DATA_PATH, self.leDataPath.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_CHECK_TIME, self.dteCheckTime.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_CHECK_HOURS, self.leCheck.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_HOST_IP, hostIp)
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_HOST_PORT, self.leHostPort.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_FIXTURE_ID, self.leFixtureId.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_LINE_ID, self.leLineId.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_PART_NUMBER, self.lePartNumber.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_WORK_AREA, self.leWorkArea.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_PROJECT_NAME, self.leProjectName.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_DELAY, self.leDelay.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_WAIT_TIME, self.leWaitTime.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_MES_UPLOAD, self.cbUpload.isChecked() and 'Y' or 'N')
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_PROCESS_CONTROL, self.cbUpload.isChecked() and 'Y' or 'N')
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_BARCODE_CNT, self.leBarcodeLenth.text())
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_CHECK_BARCODE,
                                    self.cbCheckSn.isChecked() and 'Y' or 'N')
            self.conf.saveConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_SCAN_TYPE,
                                    self.cbAutoScan.isChecked() and 'A' or 'M')
            self.conf.saveConfigure(ConfigureKey.SEC_ALARM, ConfigureKey.KEY_ALARM_COUNT, self.leNozzle.text())
            self.limitConf.SaveConfigure(LimitKey.SEC_LEAK, LimitKey.KEY_UPPER_LIMIT, str(upperlimit))
            self.limitConf.SaveConfigure(LimitKey.SEC_LEAK, LimitKey.KEY_LOW_LIMIT, str(lowlimit))
            #global_Gui.lbMesUploadEmit(self.cbUpload.isChecked())
            global_Gui.waitTimeLoad()
            self.filelog.writeAllLog('系统配置保存成功', True, 'green', False, True)
            QMessageBox.information(self, '提示', '系统配置保存成功', QMessageBox.Ok)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed, False)

    def pbLogPath_click(self):
        tmpPath = self.logPathDlg.getExistingDirectory()
        if not tmpPath == '':
            self.leLogPath.setText(tmpPath)

    def pbDataPath_click(self):
        tmpPath = self.dataPathDlg.getExistingDirectory()
        if not tmpPath == '':
            self.leDataPath.setText(tmpPath)

    def confShow(self):
        try:
            self.conf.loadConfigure()
            self.limitConf.LoadConfiogure()
            #hostIp = self.conf.getLocalIP().split('.')
            hostIp = str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_HOST_IP]).split('.')
            if len(hostIp) != 4:
                QMessageBox.information(self, '提示', '系统配置加载失败，存在无法解析的IP地址', QMessageBox.Ok)
                return False
            for num in hostIp:
                result, data = self.str2int(num)
                if not result:
                    QMessageBox.information(self, '提示', '系统配置加载失败，存在无法解析的IP地址', QMessageBox.Ok)
                    return False

            self.leLogPath.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_LOG]))
            self.leDataPath.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_DATA_PATH]))
            self.leCheck.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_CHECK_HOURS]))
            self.leDelay.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_DELAY]))
            self.leWaitTime.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_WAIT_TIME]))
            self.leip1.setText(hostIp[0])
            self.leip2.setText(hostIp[1])
            self.leip3.setText(hostIp[2])
            self.leip4.setText(hostIp[3])
            self.leHostPort.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_HOST_PORT]))
            self.leFixtureId.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_FIXTURE_ID]))
            self.leLineId.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_LINE_ID]))
            self.lePartNumber.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_PART_NUMBER]))
            self.leWorkArea.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_WORK_AREA]))
            self.leProjectName.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_PROJECT_NAME]))
            self.cbUpload.setChecked(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_MES_UPLOAD]).upper() == 'Y')
            self.leBarcodeLenth.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_BARCODE_CNT]))
            self.cbCheckSn.setChecked(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_CHECK_BARCODE]).upper() == 'Y')
            self.cbAutoScan.setChecked(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_SCAN_TYPE]).upper() == 'A')
            self.leUpperLimit.setText(str(self.limitConf.ConfigureDic[LimitKey.SEC_LEAK][LimitKey.KEY_UPPER_LIMIT]))
            self.leLowerLimit.setText(str(self.limitConf.ConfigureDic[LimitKey.SEC_LEAK][LimitKey.KEY_LOW_LIMIT]))
            checktime = datetime.strptime(str(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_CHECK_TIME]),"%Y-%m-%d %H:%M:%S")
            self.dteCheckTime.setDateTime(checktime)
            self.leNozzle.setText(str(self.conf.ConfigureDic[ConfigureKey.SEC_ALARM][ConfigureKey.KEY_ALARM_COUNT]))
            return True
        except Exception as e:
            global_Gui.tbvwLogEmit('加载配置文件失败:' + str(e), GlobalConf.colorRed, False)

    def str2float(self, data = str):
        try:
            tmpstr:float = 0.0
            tmpstr = float(data)
            return True, tmpstr
        except:
            return False, tmpstr

    def str2int(self, data = str):
        try:
            tmpstr:int = 0
            tmpstr = int(data)
            return True, tmpstr
        except:
            return False, tmpstr

class cDevicesConfigForm(QDialog, Ui_DevicesConfigForm):
    def __init__(self):
        try:
            super(cDevicesConfigForm, self).__init__()
            self.setupUi(self)
            self.conf = cConfigure()
            self.pbtSave.clicked.connect(self.pbtSave_Click)
            self.workerIntegra = cWorkerIntegra(GlobalConf.WORKER_INTEGRA)
            #self.camera = Camera()
            self.scan = cScan(GlobalConf.SCAN)
            self.findCamera = None
            self.plc = cModbusclient(GlobalConf.PLC)
            self.pbtScan.clicked.connect(self.scanBarcode)
            self.pbtWPRead.clicked.connect(self.workerIntegraRead)
            self.ptbReadStart.clicked.connect(self.PLCReadStart)
            self.pbtTestFinish.clicked.connect(self.PLCTestFinish)
            self.pbtAlia.clicked.connect(self.PLCReadLt)
            self.pbtWpw.clicked.connect(self.PLCReadWpw)
            self.showConfigure()
        except Exception as e:
            print(e)

    def pbtSave_Click(self):
        try:
            self.conf.saveConfigure(ConfigureKey.SEC_PLC, ConfigureKey.KEY_PLC_IP, self.lePlcIp.text())
            self.conf.saveConfigure(ConfigureKey.SEC_PLC, ConfigureKey.KEY_PORT, self.le_PlcPort.text())
            self.conf.saveConfigure(ConfigureKey.SEC_WORKER_INTEGRA, ConfigureKey.KEY_PORT, self.le_WorkerIntegraPort.text())
            self.conf.saveConfigure(ConfigureKey.SEC_WORKER_INTEGRA, ConfigureKey.KEY_BAUD, self.le_WorkerIntegraBaud.text())
            self.conf.saveConfigure(ConfigureKey.SEC_SCAN, ConfigureKey.KEY_PORT, self.le_ScanPort.text())
            self.conf.saveConfigure(ConfigureKey.SEC_SCAN, ConfigureKey.KEY_BAUD, self.le_ScanBaud.text())
            self.logshow('保存成功', GlobalConf.colorGreen)
            global_Gui.waitTimeEmit()
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def showConfigure(self):
        try:
            self.le_PlcPort.setText(self.conf.ConfigureDic[ConfigureKey.SEC_PLC][ConfigureKey.KEY_PORT])
            self.lePlcIp.setText(self.conf.ConfigureDic[ConfigureKey.SEC_PLC][ConfigureKey.KEY_PLC_IP])
            self.le_WorkerIntegraPort.setText(
                self.conf.ConfigureDic[ConfigureKey.SEC_WORKER_INTEGRA][ConfigureKey.KEY_PORT])
            self.le_WorkerIntegraBaud.setText(
                self.conf.ConfigureDic[ConfigureKey.SEC_WORKER_INTEGRA][ConfigureKey.KEY_BAUD])
            self.le_ScanPort.setText(self.conf.ConfigureDic[ConfigureKey.SEC_SCAN][ConfigureKey.KEY_PORT])
            self.le_ScanBaud.setText(self.conf.ConfigureDic[ConfigureKey.SEC_SCAN][ConfigureKey.KEY_BAUD])
            if not self.plc.clientconnected:
                if not self.plc.Setup() or not self.plc.Open():
                    self.logshow('PLC连接失败', GlobalConf.colorRed)
            if not self.scan.clientconnected:
                if not self.scan.Setup() or not self.scan.Open():
                    self.logshow('扫码枪连接失败', GlobalConf.colorRed)
        except Exception as e:
            print(e)

    def workerIntegraRead(self):
        try:
            if not self.workerIntegra.Setup() or not self.workerIntegra.Open():
                self.logshow('WorkerIntegra 打开失败！', GlobalConf.colorRed)
            testDelay = int(self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_DELAY])
            getResult, testItem = self.workerIntegra.writeAndRead(testDelay)
            if not getResult:
                self.logshow('failed to get result', GlobalConf.colorRed)
                return
            self.logshow(
                f'result:{testItem.TestResult}, value:{testItem.TestValue}, upperLimit:{testItem.TestUpLimit}, lowerLimit:{testItem.TestLowLimit}, unit:{testItem.TestUnit}',
                GlobalConf.colorBlue)

        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)


    def PLCReadStart(self):
        try:
            self.logshow('开始读取开始状态', GlobalConf.colorGreen)
            result, value = self.plc.Read_Start()
            if not result:
                self.logshow('读取失败', GlobalConf.colorRed)
            else:
                if int(value) == 1:
                    self.logshow('已开始', GlobalConf.colorGreen)
                else:
                    self.logshow('未开始', GlobalConf.colorGreen)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def PLCTestFinish(self):
        try:
            self.logshow('写入测试完成状态', GlobalConf.colorGreen)
            result = self.plc.Write_Hold_register(102, 1)
            if result:
                self.logshow('写入成功', GlobalConf.colorGreen)
            else:
                self.logshow('写入失败', GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def PLCReadLt(self):
        try:
            self.logshow('开始读取光幕状态', GlobalConf.colorGreen)
            result, value = self.plc.Read_coils2(12, 1)
            self.logshow(f'{value}', GlobalConf.colorGreen)
            if result:
                if str(value[0]).upper() == 'TRUE':
                    self.logshow('光幕报警', GlobalConf.colorRed)
                else:
                    self.logshow('光幕正常', GlobalConf.colorGreen)
            else:
                self.logshow('未读取到状态', GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def PLCReadWpw(self):
        try:
            self.logshow('开始读取负压表状态', GlobalConf.colorGreen)
            result1, value1 = self.plc.Read_coils2(26, 1)
            result2, value2 = self.plc.Read_coils2(27, 1)
            if result1:
                if str(value1[0]).upper() != 'TRUE':
                    self.logshow('负压表1正常', GlobalConf.colorGreen)
                else:
                    self.logshow('负压表1报警', GlobalConf.colorGreen)
            else:
                self.logshow('未读取到负压表1状态', GlobalConf.colorRed)
            if result2:
                if str(value2[0]).upper() != 'TRUE':
                    self.logshow('负压表2正常', GlobalConf.colorGreen)
                else:
                    self.logshow('负压表2报警', GlobalConf.colorGreen)
            else:
                self.logshow('未读取到负压表2状态', GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def scanBarcode(self):
        try:
            result, barcode = self.scan.GetBarcode(5)
            if result:
                self.logshow(barcode, GlobalConf.colorBlue)
            else:
                self.logshow("扫码失败", GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)
    # def scanBarcode(self):
    #     try:
    #         self.findCamera = self.camera.find_camera(1)
    #         if not self.ConnectCamera():
    #             self.logshow('camera 打开失败！', GlobalConf.colorRed)
    #             print('camera 打开失败！')
    #             return
    #
    #         result, picture = self.camera.read_camera(self.findCamera)
    #         if not result:
    #             self.logshow('camera 读取失败！', GlobalConf.colorRed)
    #             print('camera 读取失败！')
    #             return
    #         barcode = self.camera.find_qrcode(picture)
    #         self.le_ScanBarcode.setText(barcode)
    #     except Exception as e:
    #         print(e)
    #         self.logshow(str(e), GlobalConf.colorRed)

    def ConnectCamera(self):
        try:
            index=0
            #self.Camera=self.CameraClass.find_camera(index)
            while True:
                self.findCamera = self.camera.find_camera(index)
                ret,picture=self.camera.read_camera(self.findCamera)
                if not ret:
                    index+=1

                if index>=5000:
                    self.camera.Isconnect=False
                    print("index-{0} CCD Open Fail".format(str(index)))
                    break

                if ret:
                    self.camera.Isconnect=True
                    print("index-{0} CCD Open Sucess".format(str(index)))
                    break

            #self.size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            return self.camera.Isconnect
        except Exception as e:
            self.logshow( "Open Camera ERROR-" + str( e ), GlobalConf.colorRed )
            return False


    def logshow(self, content: str, color: str = GlobalConf.colorGreen):
        writecontent ='<font color = ' + color +'> [' + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f') +'] ' +content
        self.tbLog.append(writecontent)
        self.tbLog.moveCursor(self.tbLog.textCursor().End)

class cUploadTestForm(QDialog, Ui_UploadTestForm):
    def __init__(self):
        super(cUploadTestForm, self).__init__()
        self.setupUi(self)
        self.pbtUpload.clicked.connect(self.uploadDataClick)
        self.pbtGetData.clicked.connect(self.getDataClick)
        self.pbtCheckData.clicked.connect(self.checkDataClick)
        self.pbtClearWindow.clicked.connect(self.clearWindow)

    def uploadDataClick(self):
        try:
            if len(self.leUploadUrl.text()) <= 0:
                self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] 上传地址不允许为空')
                return
            result, tmpjson = self.HttpPost(self.leUploadUrl.text(), self.tePostData.toPlainText())
            if result:
                self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(tmpjson))
        except Exception as e:
            self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(e))

    def getDataClick(self):
        try:
            if len(self.leUploadUrl.text()) <= 0:
                self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] 查询地址不允许为空')
                return
            tmpjson = self.HttpGet(self.leUploadUrl.text())
            if tmpjson != None:
                self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(json.loads(tmpjson)))
        except Exception as e:
            self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(e))
    def checkDataClick(self):
        try:
            #tmp = dict(json.dumps(self.tePostData.toPlainText())) #暂不校验
            checkData = self.tePostData.toPlainText()
            tmp = ''
            # 需满足utf-8格式，数据内容不包含中文，否则可能出现gbk无法转换错误
            if checkData[0:4] == 'file':
                with open(checkData[8:], 'r+') as fr:
                    tmp = json.loads(fr.read())
            else:
                tmp = json.loads(checkData)
            self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] BEGIN\n' + str(tmp) + '\n[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] END')
        except Exception as e:
            self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(e))

    def clearWindow(self):
        try:
            self.tbGetData.clear()
            self.tePostData.clear()
        except Exception as e:
            self.tbGetData.setText('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + str(e))

    def HttpGet(self, url, timeout = 10):
        try:
            response = requests.get(url,timeout)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            global_Gui.tbvwLogEmit( 'HTTP GET ERROR' + str(e), GlobalConf.colorRed)
            return None

    def HttpPost(self, url, data, timeout = 10):
        try:
            response = requests.post(url, data,timeout = timeout)
            return response.status_code==200,response.text
        except Exception as e:
            global_Gui.tbvwLogEmit('HTTP POST ERROR' + str(e), GlobalConf.colorRed)
            return False,e

class cUnlock(QDialog, Ui_UnlockForm):
    def __init__(self):
        super(cUnlock, self).__init__()
        self.setupUi(self)
        self.pbtExit.clicked.connect(self.exitClick)
        self.pbtLogin.clicked.connect(self.loginClick)
        self.useCount = cUseCount()
        print(self.useCount.UseCountDic)

    def loginClick(self):
        try:
            if self.leOperatorId.text() == 'GTS' and self.lePassword.text() == 'GTS123':
                self.close()
                global_Gui.showMsgBox('提示', '登录成功')
                return
            check = cCheckRole(self.cbRole.currentIndex() + 1, self.leOperatorId.text(), self.lePassword.text())
            result, txt = check.login()
            if result:
                self.useCount.saveConfigure(ConfigureKey.SEC_USE_COUNT, ConfigureKey.KEY_NOZZLE, '0')
                self.close()
            else:
                global_Gui.showMsgBox('提示', txt)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red')


    def exitClick(self):
        self.close()

    def clearUseCount(self):
        pass
class cPlcTestForm(QDialog, Ui_PlcTestForm):
    def __init__(self):
        try:
            super(cPlcTestForm, self).__init__()
            self.setupUi(self)
            self.pbtCoilRead.clicked.connect(self.readColi)
            self.pbtColiWrite.clicked.connect(self.writeColi)
            self.pbtHoldRead.clicked.connect(self.readHold)
            self.pbtHoldWrite.clicked.connect(self.writeHold)
            self.plc = cModbusclient(GlobalConf.PLC)
            if not self.plc.Setup() or not self.plc.Open():
                self.logshow('连接PLC失败', GlobalConf.colorRed)
        except Exception as e:
            print(e)

    def readColi(self):
        try:
            result, value = self.plc.Read_coils2(int(self.lePlcColi.text()), 1)
            if result:
                self.logshow(str(value[0]))
            else:
                self.logshow('读取失败', GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)
    def writeColi(self):
        try:
            self.plc.Write_coil(int(self.lePlcColi.text()), bool(self.leWrite.text()))
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)
    def readHold(self):
        try:
            result, value = self.plc.Read_holding_registers(int(self.lePlcHold.text()), 1)
            if result:
                self.logshow(value[0])
            else:
                self.logshow('读取失败', GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)
    def writeHold(self):
        try:
            self.plc.Write_Hold_register(int(self.lePlcHold.text()), self.leWrite.text())
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    def logshow(self, content: str, color: str = GlobalConf.colorGreen):
        writecontent = '<font color = ' + color + '> [' + datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S,%f') + '] ' + content
        self.textBrowser.append(writecontent)
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

class cScanTestForm(QDialog, Ui_scanTestForm):
    def __init__(self):
        super(cScanTestForm, self).__init__()
        self.setupUi(self)
        #self.camera = Camera()
        self.scan = cScan(GlobalConf.SCAN)
        self.findCamera = None
        self.isConnect = False
        self.pbtGetBarcode.clicked.connect(self.getBarcode)


    def getBarcode(self):
        try:
            if not self.isConnect:
                if not self.scan.Setup() or not self.scan.Open():
                    self.logshow("扫码枪连接失败", GlobalConf.colorRed)
                    return
                self.isConnect = True
            result, barcode = self.scan.GetBarcode(5)
            if result:
                barcode = str(barcode).replace('\r', '')
                self.logshow(barcode, GlobalConf.colorBlue)
            else:
                self.logshow("扫码失败", GlobalConf.colorRed)
        except Exception as e:
            self.logshow(str(e), GlobalConf.colorRed)

    # def getBarcode(self):
    #     try:
    #         if not self.isConnect:
    #             if not self.ConnectCamera():
    #                 self.logshow("Open Camera failed-", GlobalConf.colorRed)
    #                 return
    #             self.isConnect = True
    #
    #         result, picture = self.camera.read_camera(self.findCamera)
    #         if result:
    #             self.showPicture(picture)
    #             barcode = self.camera.find_qrcode(picture)
    #             self.logshow(barcode, GlobalConf.colorBlue)
    #     except Exception as e:
    #         print(e)
    #         self.logshow(str(e), GlobalConf.colorRed)
    #
    # def showPicture(self, picture):
    #     if not self.isConnect:
    #         if not self.ConnectCamera():
    #             self.logshow("Open Camera failed-", GlobalConf.colorRed)
    #             return
    #         self.isConnect = True
    #
    #     show = cv2.cvtColor(cv2.resize(picture, (512,512)), cv2.COLOR_BGR2RGB)
    #     showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
    #     self.lbPicture.setPixmap(QPixmap.fromImage(showImage))
    #
    # def ConnectCamera(self):
    #     try:
    #         index=1
    #         #self.Camera=self.CameraClass.find_camera(index)
    #         while True:
    #             self.findCamera = self.camera.find_camera(index)
    #             ret,picture=self.camera.read_camera(self.findCamera)
    #             if not ret:
    #                 index+=1
    #
    #             if index>=5000:
    #                 self.camera.Isconnect=False
    #                 print("index-{0} CCD Open Fail".format(str(index)))
    #                 break
    #
    #             if ret:
    #                 self.camera.Isconnect=True
    #                 print("index-{0} CCD Open Sucess".format(str(index)))
    #                 break
    #
    #         #self.size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    #         return self.camera.Isconnect
    #     except Exception as e:
    #         self.logshow( "Open Camera ERROR-" + str( e ), GlobalConf.colorRed )
    #         return False
    def logshow(self, content: str, color: str = GlobalConf.colorGreen):
        writecontent ='<font color = ' + color +'> [' + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f') +'] ' +content
        self.tbResult.append(writecontent)
        self.tbResult.moveCursor(self.tbResult.textCursor().End)

class cOperatorChange(QDialog, Ui_OperatorChangeForm):
    def __init__(self):
        super(cOperatorChange, self).__init__()
        self.setupUi(self)
        self.pbtExit.clicked.connect(self.exitClick)
        self.pbtLogin.clicked.connect(self.loginClick)

    def loginClick(self):
        if self.leOperatorId.text() == 'GTS' and self.lePassword.text() == 'GTS123':
            global_Gui.showMenu(True)
            self.close()
            global_Gui.showMsgBox('提示','登录成功')
            return
        check = cCheckRole(self.cbRole.currentIndex(), self.leOperatorId.text(), self.lePassword.text())
        result, txt = check.login()
        if result:
            self.close()
            if self.cbRole.currentIndex() > 0:
                global_Gui.showMenu(True)
            else:
                global_Gui.showMenu(False)
            global_Gui.showMsgBox('提示', '切换工号成功')
            global_Gui.changeRole(self.cbRole.currentText(), self.leOperatorId.text())
            global_Gui.tbvwLogEmit('切换工号成功', GlobalConf.colorGreen)
        else:
            global_Gui.showMsgBox('提示', '切换工号失败'+txt)
            global_Gui.tbvwLogEmit('切换工号成功', GlobalConf.colorRed)


    def exitClick(self):
        self.close()

if __name__ == '__main__':
    app = QApplication([sys.argv])
    window = cScanTestForm()
    window.move(200, 100)  # 窗口处于电脑界面的位置
    window.show()
    sys.exit(app.exec_())

