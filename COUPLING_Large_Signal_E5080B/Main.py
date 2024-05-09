import csv
import datetime
import sys
import threading
import time
from threading import Timer

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit, QHBoxLayout, QTableView, \
    QTableWidgetItem, QPushButton
from PyQt5 import QtWidgets

from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from ConfigureDir.Limit import cLimit
from ConfigureDir.TestDB import cTestDB
from ConfigureDir.TestItemName import cTestItemName
from GlobalGui import cGlobalGui, global_Gui
from TestDir.testEngine import cTestEngine
#from CMainForm import Ui_MainWindow
from MainForm import Ui_MainWindow
from DeviceDir import Macro


class ui_window( QtWidgets.QMainWindow ):
    def __init__(self):
        QtWidgets.QMainWindow.__init__( self )
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        self.testEngine = cTestEngine()

        # <editor-fold desc="表格控件初始设置">
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        self.ui.tableWidget.setEditTriggers( QTableView.NoEditTriggers )  # 表格内容不可修改
        self.ui.tableWidget.setRowCount( 20 )
        self.ui.tableWidget.setColumnCount( 6 )
        self.ui.tableWidget.setHorizontalHeaderLabels( ['Item', 'Limit L', 'Limit H', 'Value', 'Result', 'Unit'] )
        self.ui.tableWidget.setColumnWidth( 0, 300 )
        self.ui.tableWidget.setColumnWidth( 1, 140 )
        self.ui.tableWidget.setColumnWidth( 2, 140 )
        self.ui.tableWidget.setColumnWidth( 3, 220 )
        self.ui.tableWidget.setColumnWidth( 4, 105 )
        self.ui.tableWidget.setColumnWidth( 5, 80 )
        # self.layout = QHBoxLayout()
        # self.layout.addWidget(self.ui.tableWidget)
        # </editor-fold>

        # 配置界面设置
        self.ui.lblVan.setText("Vna")
        self.ui.actionMotion.setText("ClearCount")
        self.ui.label_10.setText("IP")
        self.ui.label_11.setText("PORT")

        self.ui.pbtnSteupSave.setStyleSheet("background-color: gray")
        self.ui.tabwConfig.setColumnWidth(0, 150)
        self.ui.tabwConfig.setColumnWidth(1, 260)
        self.ui.tabwConfig.setAlternatingRowColors(True)

        self.ui.tabFreeLimit.setColumnWidth(0, 100)
        self.ui.tabFreeLimit.setColumnWidth(1, 130)
        self.ui.tabFreeLimit.setAlternatingRowColors(True)

        self.ui.tabKnomLimit.setColumnWidth(0, 100)
        self.ui.tabKnomLimit.setColumnWidth(1, 130)
        self.ui.tabKnomLimit.setAlternatingRowColors(True)

        self.ui.tabTestItem.setColumnWidth(0, 130)
        self.ui.tabTestItem.setColumnWidth(1, 270)
        self.ui.tabTestItem.setAlternatingRowColors(True)

        self.ui.cmbAdress.addItems(["CD_MCEG", "CD_JP", "YC_LIKAI"])
        self.ui.cmbProduct.addItems(["J4XX", "J5XX", "J6XX", "J7XX"])
        self.Factory = ''
        self.Product = ''


        # 机械手单步调试设置
        self.ui.txbPassword_4.setText("0.1")
        self.total_X = 0.0
        self.total_Y = 0.0
        self.total_Z = 0.0
        self.total_U = 0.0
        self.total_V = 0.0
        self.total_W = 0.0

        # 初始化界面
        self.vMain = 0
        self.vSteup = 1
        self.vDebug = 2
        self.vMotion = 3
        self.ui.lblAppName.setText("       GTS-TEST-Coupling大信号           VNA-STATE03.STA" )
        self.ui.menuWindow.setEnabled( False )
        self.ui.leTotal.setReadOnly( True )
        self.ui.lePass.setReadOnly( True )
        self.ui.leFail.setReadOnly( True )
        self.ui.leYield.setReadOnly( True )
        self.ui.tabWidget.setCurrentIndex( int( self.vMain ) )

        #  信号绑定
        self.ui.actionDOE.triggered.connect(self.actionQC_triggered)
        self.ui.actionOP.triggered.connect(self.actionOP_triggered)

        self.ui.actionLogin.triggered.connect( self.actionLogin_triggered )
        self.ui.actionLogout.triggered.connect( self.actionLogout_triggered )
        self.ui.actionMain.triggered.connect( self.actionMain_triggered )
        self.ui.actionSteup.triggered.connect( self.actionSteup_triggered )
        self.ui.actionDebug.triggered.connect( self.actionDebug_triggered )
        self.ui.actionMotion_2.triggered.connect(self.actionMotion_triggered)
        self.ui.actionMotion.triggered.connect( self.actionClearCounter_triggered )
        self.ui.actionreset.triggered.connect(self.ResetRobot)
        self.ui.leBarcode.returnPressed.connect( self.lbBarcodeChange )
        self.ui.pbtnSteupSave.clicked.connect( self.pbtnSteupSave_clicked )
        self.ui.pbtnJson.clicked.connect(self.pbtnJson_clicked)

        self.ui.robotX1.clicked.connect( self.MoveRobot )
        self.ui.robotX2.clicked.connect( self.MoveRobot )

        self.ui.robotY1.clicked.connect( self.MoveRobot )
        self.ui.robotY2.clicked.connect( self.MoveRobot )

        self.ui.robotZ1.clicked.connect( self.MoveRobot )
        self.ui.robotZ2.clicked.connect( self.MoveRobot )

        self.ui.robotU1.clicked.connect( self.MoveRobot )
        self.ui.robotU2.clicked.connect( self.MoveRobot )

        self.ui.robotV1.clicked.connect( self.MoveRobot )
        self.ui.robotV2.clicked.connect( self.MoveRobot )

        self.ui.robotW1.clicked.connect( self.MoveRobot )
        self.ui.robotW2.clicked.connect( self.MoveRobot )

        self.ui.MCUWrite.clicked.connect( self.MCUOutCOntrol )
        self.ui.MCURead.clicked.connect( self.MCUIntCOntrol )

        global_Gui.TextBrowserSignal.connect( self.TextBrowser_SetText )
        global_Gui.leBarcodeSignal.connect( self.leBarcode_SetText )
        global_Gui.lblTestTimeSignal.connect( self.lblTestTime_SetText )
        global_Gui.leTotalSignal.connect( self.leTotal_SetText )
        global_Gui.lePassSignal.connect( self.lePass_SetText )
        global_Gui.leFailSignal.connect( self.leFail_SetText )
        global_Gui.leYieldSignal.connect( self.leYield_SetText )
        global_Gui.tableWidgetSignal.connect( self.updateTableWidget )
        global_Gui.lbStatueSignal.connect( self.lbStatue )
        global_Gui.lbDeviceStatueSignal.connect( self.lbDeviceStatue )
        global_Gui.lbTestResultSignal.connect( self.lbTestResultStatue )
        global_Gui.lbRobotLocationSignal.connect( self.lbRobotLocation )
        global_Gui.lbAngelorDistanceSignal.connect( self.lbCCDData )
        global_Gui.lbCheckTime.connect(self.lbCheckTime)
        try:
            # 配置加载
            self.confIns = cConfigure()
            self.confIns.LoadConfiogure()
            self.confKey = ConfigureKey
            self.IsAutoScan = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_SCAN_mode] == "A"
            if not self.IsAutoScan:
                self.ui.leBarcode.setFocus()
            self.isLcr = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_Test_mode] == "LCR"
            self.Limit = cLimit(self.isLcr)
            self.Limit.LoadConfiogure()

            self.testDB = cTestDB()
            self.testDB.LoadConfiogure()

            self.testItemName = cTestItemName()
            self.testItemName.LoadConfiogure()

            self.configRead()
            # <editor-fold desc="登录界面">
            input_dialog = QtWidgets.QInputDialog(self)
            input_dialog.setInputMode(QInputDialog.TextInput)
            input_dialog.setWindowTitle('Login')
            input_dialog.setLabelText('请输入当前作业员工号            \n'
                                      '        ______ ______ _____ \n'
                                      '       / ____//_  __// ___/ \n'
                                      '      / / __   / /   \__ \  \n'
                                      '     / /_/ /  / /   ___/ /  \n'
                                      '     \____/  /_/   /____/   \n'
                                      '\n默认工号--GTS')
            input_dialog.setTextValue("GTS")
            input_dialog.setFixedSize(300, 300)
            input_dialog.show()
            if input_dialog.exec_() == input_dialog.Accepted:
                text = input_dialog.textValue()
                self.testEngine.OpID = text
            else:
                self.testEngine.OpID = 'GTS'
            # </editor-fold>

            tmpFactory = ''

            if self.Factory == Macro.ADDRESS_CD_MCEG:
                tmpFactory = '成都MCEG'
            elif self.Factory == Macro.ADDRESS_CD_JP:
                tmpFactory = '成都JP'
            elif self.Factory == Macro.ADDRESS_YC_LIKAI:
                tmpFactory = '盐城LIKAI'

            self.ui.lblAppName.setText(tmpFactory + '-' + self.Product +"       GTS-TEST-Coupling大信号-1.0.1           VNA-STATE03.STA")
            # 连接设配
            # self.StarttestEgineThread()
        except Exception as e:
            QMessageBox.about(self, 'error', 'config write error:' + str(e))

    def StarttestEgineThread(self):
        testThread = threading.Thread( target=self.testEngine.Initialize(), name='TestEngine')
        testThread.setDaemon(True)
        testThread.start()
        self.debugFormLoad()

    def debugFormLoad(self):
        intDic = cTestEngine.McuIntDic
        outDic = cTestEngine.McuOutDic
        for num in intDic.keys():
            self.ui.cmbInt.addItem(num)
        for num in outDic.keys():
            self.ui.cmbOut.addItem(num)
        pass

    def UpdateRobotDebugLoaction(self):
        self.ui.label_21.setText(
            "坐标 {0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f}".format( self.total_X, self.total_Y, self.total_Z, self.total_U, self.total_V,
                                                 self.total_W ) )

    def lbBarcodeChange(self):
        if self.IsAutoScan: return
        text = self.ui.leBarcode.text()
        print( str( text ) )
        if "\r" in text:
            self.testEngine.BarcodeM = text.replace( "\r", "" )
            #self.testEngine.Mstart=True
        else:
            self.testEngine.BarcodeM = text
            #self.testEngine.Mstart = True

    def MoveRobot(self):
        try:
            button: QPushButton = self.sender()
            step = round( float( self.ui.txbPassword_4.text() ), 3 )
            print( button.text() + str( step ) )
            tmp = button.text()
            if tmp in "X+":
                self.total_X += step
                if abs( self.total_X ) >= 3:
                    self.total_X -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( step, 0, 0, 0, 0, 0 )

            if tmp in "X-":
                self.total_X += step * -1
                if abs( self.total_X ) >= 3:
                    self.total_X -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( step * -1, 0, 0, 0, 0, 0 )

            if tmp in "Y+":
                self.total_Y += step
                if abs( self.total_Y ) >= 3:
                    self.total_Y -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, step, 0, 0, 0, 0 )

            if tmp in "Y-":
                self.total_Y += step * -1
                if abs( self.total_Y ) >= 3:
                    self.total_Y -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, step * -1, 0, 0, 0, 0 )

            if tmp in "Z+":
                self.total_Z += step
                if abs( self.total_Z ) >= 3:
                    self.total_Z -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, step, 0, 0, 0 )

            if tmp in "Z-":
                self.total_Z += step * -1
                if abs( self.total_Z ) >= 3:
                    self.total_Z -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, step * -1, 0, 0, 0 )

            if tmp in "U+":
                self.total_U += step
                if abs( self.total_U ) >= 3:
                    self.total_U -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, step, 0, 0 )

            if tmp in "U-":
                self.total_U += step * -1
                if abs( self.total_U ) >= 3:
                    self.total_U -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, step * -1, 0, 0 )

            if tmp in "V+":
                self.total_V += step
                if abs( self.total_V ) >= 3:
                    self.total_V -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, 0, step, 0 )

            if tmp in "V-":
                self.total_V += step * -1
                if abs( self.total_V ) >= 3:
                    self.total_V -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, 0, step * -1, 0 )

            if tmp in "W+":
                self.total_W += step
                if abs( self.total_W ) >= 3:
                    self.total_W -= step
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, 0, 0, step )

            if tmp in "W-":
                self.total_W += step * -1
                if abs( self.total_W ) >= 3:
                    self.total_W -= step * -1
                    QMessageBox.about( self, 'error', '机械手移动超出范围' )
                    return
                self.testEngine.munaRobot( 0, 0, 0, 0, 0, step * -1 )
            pass
        except Exception as e:
            QMessageBox.about( self, 'error', '机械手移动错误' + str( e ) )
        finally:
            self.UpdateRobotDebugLoaction()

    def MCUOutCOntrol(self):
        try:
            Key = self.ui.cmbOut.currentText()
            value = self.ui.cmbOutValue.currentText() == "1" and 0x01 or 0x00
            self.testEngine.McuControl( Key, value )
            print( Key + "--" + str( value ) )
            pass
        except Exception as e:
            QMessageBox.about( self, 'error', 'MCU debug error' + str( e ) )

    def MCUIntCOntrol(self):
        try:
            Key = self.ui.cmbInt.currentText()
            Tmpvalue = self.testEngine.McuRead( Key )
            self.ui.txbint.setText( str( Tmpvalue ) )
            print( Key + "--" + str( Tmpvalue ) )
            pass
        except Exception as e:
            QMessageBox.about( self, 'error', 'MCU debug error' + str( e ) )

    # <editor-fold desc="菜单操作">
    def actionQC_triggered(self):
        print("DOE 模式切换")
        text, ok = QInputDialog.getText(self, 'LoginForm', 'PassWord', echo=QLineEdit.Password)
        if ok and text:
            if text == 'GTS123456':
                self.testEngine.TestModel = "DOE"
                self.ui.menuOP.setTitle("DOE")
                print(self.testEngine.TestModel)
            else:
                QMessageBox.about(self, 'error', 'password error')

    def actionOP_triggered(self):
        print("OP 模式切换")
        self.testEngine.TestModel = "OP"
        self.ui.menuOP.setTitle("OP")
        print(self.testEngine.TestModel)

    def actionMain_triggered(self):
        print( '主界面按键被按下' )
        self.ui.tabWidget.setCurrentIndex( int( self.vMain ) )

    def actionDebug_triggered(self):
        print( '调试按键被按下' )
        self.confIns.SaveConfigure(self.confKey.SEC_APP, self.confKey.SEC_DeBugTime,
                                   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.ui.tabWidget.setCurrentIndex( int( self.vDebug ) )

    def actionSteup_triggered(self):
        print( '设置按键被按下' )
        self.ui.tabWidget.setCurrentIndex( int( self.vSteup ) )

    def actionMotion_triggered(self):
        print( 'IO监控按键被按下' )
        #self.testEngine.ClearCounter()
        self.ui.tabWidget.setCurrentIndex( int( self.vMotion ) )

    def actionClearCounter_triggered(self):
        print( 'ClearCounter按键被按下' )
        self.testEngine.ClearCounter()
        #self.ui.tabWidget.setCurrentIndex( int( self.vMotion ) )

    def actionLogin_triggered(self):
        print( '登入按键被按下' )
        text, ok = QInputDialog.getText( self, 'LoginForm', 'PassWord', echo=QLineEdit.Password )
        if ok and text:
            if text == '1234':
                print( 'ok' )
                self.total_X = 0.0
                self.total_Y = 0.0
                self.total_Z = 0.0
                self.total_U = 0.0
                self.total_V = 0.0
                self.total_W = 0.0
                self.UpdateRobotDebugLoaction()
                self.ui.menuWindow.setEnabled( True )
            else:
                QMessageBox.about( self, 'error', 'password error' )

    def actionLogout_triggered(self):
        print( '登出按键被按下' )
        self.ui.menuWindow.setEnabled( False )

    # </editor-fold>

    # <editor-fold desc="计数良率">
    def leTotal_SetText(self, cnt=str):
        self.ui.leTotal.setText( cnt )

    def lePass_SetText(self, cnt=str):
        self.ui.lePass.setText( cnt )

    def leFail_SetText(self, cnt=str):
        self.ui.leFail.setText( cnt )
    #CR1052604VFPFYN5E
    def leYield_SetText(self, cnt=str):
        self.ui.leYield.setText( cnt + '%' )

    # </editor-fold>

    def leBarcode_SetText(self, msg):
        self.ui.leBarcode.setText( msg )
        if msg is "":
            self.ui.tableWidget.setRowCount( 0 )
            self.recordCount = 0

    def lblTestTime_SetText(self, msg):
        self.ui.lblTestTime.setText( msg )

    def lbCCDData(self, Angle, Distance):
        self.ui.lbAngle.setText( Distance )
        self.ui.lbDistance.setText( Angle )

    def lbCheckTime(self,time):
        self.ui.lblCheckTime.setText(time)

    # 1气压 2启动 3急停
    def lbStatue(self, key: int, statue: bool):
        if key == 1:
            self.ui.lbAir.setStyleSheet( statue and "color:green" or "color:red" )
        if key == 2:
            self.ui.lbStart.setStyleSheet( statue and "color:green" or "color:red" )
        if key == 3:
            self.ui.lbStop.setStyleSheet( statue and "color:green" or "color:red" )

    def lbDeviceStatue(self, key: str, statue: bool):
        if key == Macro.MCU:
            self.ui.lblMcu.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.HWAK or key == Macro.SCAN:
            self.ui.lblScan.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.CAMREA:
            self.ui.lblCamera.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.VNA:
            self.ui.lblVan.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.LCR:
            self.ui.lblLcr.setSty0leSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.ROBOT_2001 or key == Macro.ROBOT_2002:
            self.ui.lblRobot.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.TEMP:
            self.ui.lbTemp.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.SUR_TEMP:
            self.ui.lbSurTemp.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}" )
        if key == Macro.OSC:
            self.ui.lbOsc.setStyleSheet(
                statue and "QLabel{background-color:green;}" or "QLabel{background-color:red;}")

    def lbTestResultStatue(self, key: str):
        if key == Macro.PASS:
            self.ui.lblTestState.setText( key )
            self.ui.lblTestState.setStyleSheet( "QLabel{background-color:green;}" )

        if key == Macro.IDEL:
            self.ui.lblTestState.setText( key )
            self.ui.lblTestState.setStyleSheet( "QLabel{background-color:grey;}" )

        if key == Macro.FAIL:
            self.ui.lblTestState.setText( key )
            self.ui.lblTestState.setStyleSheet( "QLabel{background-color:red;}" )

        if key == Macro.TEST:
            self.ui.lblTestState.setText( key )
            self.ui.lblTestState.setStyleSheet( "QLabel{background-color:yellow;}" )

        self.ui.leBarcode.setFocus()
        self.ui.leBarcode.selectAll()
        pass
    def ResetRobot(self):
        self.testEngine.RestRobot()
    def lbRobotLocation(self, x, y, z, u, v, w):
        self.ui.lbLocation.setText( "{0}  {1}  {2}  {3}  {4}  {5}".format( x, y, z, u, v, w ) )

    def TextBrowser_SetText(self, msg, fontColor=str, clear=False):
        if clear:
            self.ui.tbMessage.clear()
            return
        dt = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S:%f' )
        tmpMsg = "<font color = " + fontColor + ">" + dt + ' --> ' + msg
        self.ui.tbMessage.append( tmpMsg )

    recordCount = 0

    def updateTableWidget(self, Name=str, High=str, Low=str, Value=str, Result=bool, Unit=str):

        self.ui.tableWidget.setRowCount( self.recordCount + 1 )
        self.ui.tableWidget.setItem( self.recordCount, 0, QTableWidgetItem( Name ) )
        self.ui.tableWidget.setItem( self.recordCount, 1, QTableWidgetItem( High ) )
        self.ui.tableWidget.setItem( self.recordCount, 2, QTableWidgetItem( Low ) )
        self.ui.tableWidget.setItem( self.recordCount, 3, QTableWidgetItem( Value ) )
        resultItem = None
        if Result:
            resultItem = QTableWidgetItem( "PASS" )
            resultItem.setBackground( QBrush( Qt.green ) )
        else:
            resultItem = QTableWidgetItem( "FAIL" )
            resultItem.setBackground( QBrush( Qt.red ) )
        self.ui.tableWidget.setItem( self.recordCount, 4, resultItem )
        self.ui.tableWidget.setItem( self.recordCount, 5, QTableWidgetItem( Unit ) )
        self.ui.tableWidget.scrollToBottom()
        self.recordCount += 1

    # <editor-fold desc="robot 手动">
    def pbtnManuRobot_X_P_clicked(self):
        pass

    # </editor-fold>

    def pbtnSteupSave_clicked(self):
        try:
            if self.SaveAppConfigure() and self.SaveLimitConfigure():
                QMessageBox.about( self, "提示", "保存数据成功！" )
        except Exception as e:
            QMessageBox.about( self, 'error', 'config write error:' + str( e ) )
            print( e )

    # <editor-fold desc="config 读写">

    def setBoxText(self,box:QLineEdit,data:str):
        box.setText(data)
        pass

    def pbtnJson_clicked(self):
        try:
            if self.SaveDB() and self.SaveItemName():
                QMessageBox.about(self, "提示", "保存数据成功！")
        except Exception as e:
            QMessageBox.about(self, 'error', 'config write error:' + str(e))
            print(e)

    def configRead(self):
        try:

            tmpPort = self.confIns.ReadValue( self.confKey.SEC_MCU, self.confKey.KEY_PORT )
            tmpBaud = self.confIns.ReadValue( self.confKey.SEC_MCU, self.confKey.KEY_BAUD )
            self.ui.ldMcuPort.setText( tmpPort )
            self.ui.ldMcuBaud.setText( tmpBaud )

            tmpPort = self.confIns.ReadValue( self.confKey.SEC_HAWK, self.confKey.KEY_IP )
            tmpBaud = self.confIns.ReadValue( self.confKey.SEC_HAWK, self.confKey.KEY_PORT )
            self.ui.ldScanPort.setText( tmpPort )
            self.ui.ldScanBaud.setText( tmpBaud )

            tmpIP = self.confIns.ReadValue( self.confKey.SEC_CAMERA, self.confKey.KEY_IP )
            tmpPort = self.confIns.ReadValue( self.confKey.SEC_CAMERA, self.confKey.KEY_PORT )
            self.ui.ldCameraIP.setText( tmpIP )
            self.ui.ldCaneraPort.setText( tmpPort )

            tmpIP = self.confIns.ReadValue( self.confKey.SEC_ROBOT, self.confKey.KEY_IP )
            tmpPort = self.confIns.ReadValue( self.confKey.SEC_ROBOT, self.confKey.KEY_PORT )
            self.ui.ldRobotIP.setText( tmpIP )
            self.ui.ldRobotPort.setText( tmpPort )

            tmpIP = self.confIns.ReadValue( self.confKey.SEC_LCR, self.confKey.KEY_IP )
            tmpPort = self.confIns.ReadValue( self.confKey.SEC_LCR, self.confKey.KEY_PORT )
            self.ui.ldLcrIP.setText( tmpIP )
            self.ui.ldLcrPort.setText( tmpPort )

            tmpIP = self.confIns.ReadValue( self.confKey.SEC_VNA, self.confKey.KEY_IP )
            tmpPort = self.confIns.ReadValue( self.confKey.SEC_VNA, self.confKey.KEY_PORT )

            self.Factory = self.confIns.ReadValue(self.confKey.SEC_MACHINE, self.confKey.KEY_ADDRESS)
            self.Product = self.confIns.ReadValue(self.confKey.SEC_MACHINE, self.confKey.KEY_TYPR)


            self.ui.ldVnaIP.setText( tmpIP )
            self.ui.ldVnaPort.setText( tmpPort )

            Dic = self.confIns.ConfigureDic[self.confKey.SEC_APP]
            self.UpdateAppConfigure( Dic )

            self.UpdateAppLimit(self.Limit.ConfigureDic["FREE"], self.Limit.ConfigureDic["KNOM"])

            self.Updatetestdb(self.testDB.ConfigureDic["DB"])

            self.UpdatetestItemName(self.testItemName.ConfigureDic["NAME"])

        except Exception as e:
            QMessageBox.about( self, 'error', 'config read error:' + str( e ) )
            print( e )

    def UpdateAppConfigure(self, Dic=dict):
        if len( Dic ) <= 0: return "Error：配置文件错误！请检查是否正确"
        self.ui.tabwConfig.setRowCount( len( Dic ) )
        index = 0
        for num in Dic.keys():
            print( str( num ) + "--" + str( Dic[num] ) )

            item = QtWidgets.QTableWidgetItem( str( num ) )
            item.setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable )
            self.ui.tabwConfig.setItem( index, 0, item )

            item2 = QtWidgets.QTableWidgetItem( str( Dic[num]))
            self.ui.tabwConfig.setItem( index, 1, item2)
            index += 1
        return "OK"

    def SaveAppConfigure(self):
        try:
            self.confIns.SaveConfigure( self.confKey.SEC_MCU, self.confKey.KEY_PORT, self.ui.ldMcuPort.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_MCU, self.confKey.KEY_BAUD, self.ui.ldMcuBaud.text() )

            self.confIns.SaveConfigure( self.confKey.SEC_HAWK, self.confKey.KEY_IP, self.ui.ldScanPort.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_HAWK, self.confKey.KEY_PORT, self.ui.ldScanBaud.text() )

            self.confIns.SaveConfigure( self.confKey.SEC_CAMERA, self.confKey.KEY_IP, self.ui.ldCameraIP.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_CAMERA, self.confKey.KEY_PORT, self.ui.ldCaneraPort.text() )

            self.confIns.SaveConfigure( self.confKey.SEC_ROBOT, self.confKey.KEY_IP, self.ui.ldRobotIP.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_ROBOT, self.confKey.KEY_PORT, self.ui.ldRobotPort.text() )

            self.confIns.SaveConfigure( self.confKey.SEC_LCR, self.confKey.KEY_IP, self.ui.ldLcrIP.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_LCR, self.confKey.KEY_PORT, self.ui.ldLcrPort.text() )

            self.confIns.SaveConfigure( self.confKey.SEC_VNA, self.confKey.KEY_IP, self.ui.ldVnaIP.text() )
            self.confIns.SaveConfigure( self.confKey.SEC_VNA, self.confKey.KEY_PORT, self.ui.ldVnaPort.text() )

            self.confIns.SaveConfigure(self.confKey.SEC_MACHINE, self.confKey.KEY_ADDRESS, self.ui.cmbAdress.currentText())
            self.confIns.SaveConfigure(self.confKey.SEC_MACHINE, self.confKey.KEY_TYPR, self.ui.cmbProduct.currentText())


            count = self.ui.tabwConfig.rowCount()
            if count == 0:
                QMessageBox.Warning( self, "警告", "无配置选项可以保存", QMessageBox.Yes )
                return False

            for i in range( count ):
                key = self.ui.tabwConfig.item( i, 0 ).text()
                value = self.ui.tabwConfig.item( i, 1 ).text()
                if key in self.confIns.ConfigureDic[self.confKey.SEC_APP]:
                    self.confIns.ConfigureDic[self.confKey.SEC_APP][key] = value
                    self.confIns.SaveConfigure( self.confKey.SEC_APP, key, value )
            return True
        except Exception as e:
            QMessageBox.Warning( self, "警告", "ERROR" + str( e ), QMessageBox.Yes )
            return False

    def UpdateAppLimit(self, freeDic=dict, knomDic=dict):
        try:
            if len(freeDic) <= 0 or len(knomDic) <= 0: return "Error：Limit配置文件错误！请检查上下限是否 数目正确"
            self.ui.tabFreeLimit.setRowCount(len(freeDic))
            self.ui.tabKnomLimit.setRowCount(len(knomDic))
            index = 0
            for num in freeDic.keys():
                item = QtWidgets.QTableWidgetItem(str(num))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tabFreeLimit.setItem(index, 0, item)
                item2 = QtWidgets.QTableWidgetItem(str(freeDic[num]))
                self.ui.tabFreeLimit.setItem(index, 1, item2)
                index += 1

            index = 0
            for num in knomDic.keys():
                item = QtWidgets.QTableWidgetItem(str(num))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tabKnomLimit.setItem(index, 0, item)
                item2 = QtWidgets.QTableWidgetItem(str(knomDic[num]))
                self.ui.tabKnomLimit.setItem(index, 1, item2)
                index += 1
            return "OK"

        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return "NG"

    def SaveLimitConfigure(self):
        try:

            count = self.ui.tabFreeLimit.rowCount()
            if count == 0:
                QMessageBox.Warning(self, "警告", "无freeLimit配置选项可以保存", QMessageBox.Yes)
                return False

            for i in range(count):
                key = self.ui.tabFreeLimit.item(i, 0).text()
                value = self.ui.tabFreeLimit.item(i, 1).text()
                if key in self.Limit.ConfigureDic["FREE"]:
                    self.Limit.ConfigureDic["FREE"][key] = value
                    self.Limit.SaveConfigure("FREE", key, value)

            count = self.ui.tabKnomLimit.rowCount()
            if count == 0:
                QMessageBox.Warning(self, "警告", "无knomLimit配置选项可以保存", QMessageBox.Yes)
                return False

            for i in range(count):
                key = self.ui.tabKnomLimit.item(i, 0).text()
                value = self.ui.tabKnomLimit.item(i, 1).text()
                if key in self.Limit.ConfigureDic["KNOM"]:
                    self.Limit.ConfigureDic["KNOM"][key] = value
                    self.Limit.SaveConfigure("KNOM", key, value)

            return True
        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return False

    def Updatetestdb(self, DBDic=dict):
        try:
            if len(DBDic) <= 0: return "Error：db配置文件错误！请检查上下限是否 数目正确"
            self.ui.tabwdb.setRowCount(len(DBDic))
            index = 0
            for num in DBDic.keys():
                item = QtWidgets.QTableWidgetItem(str(num))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tabwdb.setItem(index, 0, item)
                item2 = QtWidgets.QTableWidgetItem(str(DBDic[num]))
                self.ui.tabwdb.setItem(index, 1, item2)

                index += 1
            return "OK"

        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return "NG"

    def SaveDB(self):
        try:
            count = self.ui.tabwdb.rowCount()
            if count <= 0:
                QMessageBox.Warning(self, "警告", "无db配置选项可以保存", QMessageBox.Yes)
                return False
            for i in range(count):
                key = self.ui.tabwdb.item(i, 0).text()
                db = self.ui.tabwdb.item(i, 1).text()
                if key in self.testDB.ConfigureDic["DB"]:
                    self.testDB.ConfigureDic["DB"][key] = db
                    self.testDB.SaveConfigure("DB", key, db)
            return True
            pass
        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return False

    def UpdatetestItemName(self, ItemNameDic=dict):
        try:
            if len(ItemNameDic) <= 0: return "Error：db配置文件错误！请检查上下限是否 数目正确"
            self.ui.tabTestItem.setRowCount(len(ItemNameDic))
            index = 0
            for num in ItemNameDic.keys():
                item = QtWidgets.QTableWidgetItem(str(num))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.ui.tabTestItem.setItem(index, 0, item)
                item2 = QtWidgets.QTableWidgetItem(str(ItemNameDic[num]))
                self.ui.tabTestItem.setItem(index, 1, item2)

                index += 1
            return "OK"

        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return "NG"

    def SaveItemName(self):
        try:
            count = self.ui.tabTestItem.rowCount()
            if count <= 0:
                QMessageBox.Warning(self, "警告", "无项目名称配置选项可以保存", QMessageBox.Yes)
                return False
            for i in range(count):
                key = self.ui.tabTestItem.item(i, 0).text()
                name = self.ui.tabTestItem.item(i, 1).text()
                if key in self.testItemName.ConfigureDic["NAME"]:
                    self.testItemName.ConfigureDic["NAME"][key] = name
                    self.testItemName.SaveConfigure("NAME", key, name)
            return True
            pass
        except Exception as e:
            QMessageBox.Warning(self, "警告", "ERROR" + str(e), QMessageBox.Yes)
            return False

    # </editor-fold>


def Main():
    app = QApplication( [sys.argv] )
    window = ui_window()
    window.move( 200, 100 )  # 窗口处于电脑界面的位置
    window.StarttestEgineThread()
    window.show()
    app.aboutToQuit.connect(window.testEngine.Abort)
    sys.exit( app.exec_() )

def rrr(e):
    if e.isSet():
        print("123")
    else:
        print("456")


def wait_for_event(e, t):
    if e.isSet():
        print("123")
    else:
        print("456")
    #e.clear()
    rrr(e)

def eventM():
    event = threading.Event()
    t2 = threading.Thread(name="t2", target=wait_for_event, args = (event, 2))
    #event.set() # e.isSet() == True
    #event.clear() # e.isSet() == False
    t2.start()

if __name__ == '__main__':
    Main()
    #eventM()
