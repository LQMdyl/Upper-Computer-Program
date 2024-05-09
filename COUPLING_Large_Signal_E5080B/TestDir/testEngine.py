import json
import math
import os
import threading
import time
from datetime import datetime, timedelta

import numpy

import GlobalGui
from ConfigureDir import CounterKey, ConfigureKey, LimitKey
from ConfigureDir.Configure import cConfigure
from ConfigureDir.Counter import cCounter
from ConfigureDir.Limit import cLimit
from ConfigureDir.TestDB import cTestDB
from ConfigureDir.TestItemName import cTestItemName
from DeviceDir import Macro
from DeviceDir.DeviceManager import cDeviceManager
from DeviceDir.E5071C_Large_Signal import cE5071C_Large_Signal
from DeviceDir.Hawk import cHawk
from DeviceDir.LCR import cLcr
from DeviceDir.Mcu import cMcu
from DeviceDir.CCD import CCD
from DeviceDir.Robot import cRobot
from LogDir.Csv import cCsv
from LogDir.TxtLog import cTxtLog
from TestDir.TestItem import cTestItem
from Trace.Trace import cTrace, Responsebody
from DeviceDir.ModbusSerial import cModbusSerial
from DeviceDir.Oscillograph import cOscillograph
# from ConfigureDir.OscLimit import cOscLimit
# from ConfigureDir import OscLimitKey


class cTestEngine():
    # <editor-fold desc="单片机定义">
    # 输出
    Cylinder = 0x00
    LedY = 0x00
    LedR = 0x00
    LedG = 0x00
    FMQ = 0x00
    XZK = 0x00
    FS = 0x01
    YL = 0x00 #DownCylinder
    Relay1 = 0x00
    Relay2 = 0x00
    Y10 = 0x00
    Y11 = 0x00
    Y12 = 0x00
    Y13 = 0x00
    Y14 = 0x00
    Y15 = 0x00
    Y16 = 0x00
    Y17 = 0x00

    # 输入
    start1 = 0x00
    start2 = 0x00
    Alarm = 0x00
    begin = 0x00
    end = 0x00
    air = 0x00
    door = 0x00 #光幕 挡着为0 不挡为1
    YLint = 0x00
    relay1 = 0x00
    relay2 = 0x00
    X11 = 0x00 #下压气缸始位
    X12 = 0x00 #下压气缸末位
    X13 = 0x00
    X14 = 0x00
    X15 = 0x00
    X16 = 0x00
    X17 = 0x00
    X18 = 0x00

    # </editor-fold>
    def __init__(self):
        self.isAbort = False
        self.isAlarm = False
        self.isTesting = False
        self.StartTime = None
        self.TestResult = True
        self.BarcodeM = ""
        self.ConfigM = ""
        self.OpID =""
        self.TestModel = "OP"
        self.MACHINE_TYPE =""   # 4XX, 5XX, 6XX, 7XX
        self.MACHINE_ADDRESS = ""   #CDMCEG:成都MCEG, CDJP:成都JP, YCLIKAI:盐城立凯
        self.trace = cTrace()
        self.devIns = cDeviceManager()
        self.DetectThread: threading.Thread = None
        self.counterIns = cCounter()
        self.counterKey = CounterKey
        self.Configure = cConfigure()
        self.Configurekey = ConfigureKey
        self.Configure.LoadConfiogure()
        self.Limit = cLimit()
        self.Limitkey = LimitKey
        self.testDB = cTestDB()
        self.testItemName = cTestItemName()
        self.txtLog = cTxtLog('pcoss')
        self.txtLog.OverdueLog(7)
        self.Csv = cCsv()
        self.Ydetail = {}
        self.Zdetail = {}
        self.Mstart = False
        self.StartFlageEnable=False
        self.SafeDoorEnable=False
        self.Checktime=""
        self.CheckHours=8.0
        self.IsCheckTimeEnable=False
        self.DOEKeys = ""
        self.IsTempEnable = False  # 测温使能
        self.isSurTempEnable = False
        # self.OscLimit = cOscLimit()
        # self.OscLimitKey = OscLimitKey
        # self.OscLimitDic = {}



        print('testEngine')

    def InitializeCounter(self):
        try:
            tmpTotal = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total)
            tmpPass = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass)
            tmpFail = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail)
            tmpYield = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Yield)
            GlobalGui.global_Gui.leTotalSignal.emit(tmpTotal)
            GlobalGui.global_Gui.lePassSignal.emit(tmpPass)
            GlobalGui.global_Gui.leFailSignal.emit(tmpFail)
            GlobalGui.global_Gui.leYieldSignal.emit(tmpYield)
            return True
            pass
        except Exception as e:
            print(e)
            self.RecordLoadMessage(str(e), 'red', 0, False)
            self.RecordLoadMessage('读取 Counter 计数文件失败', 'red', 0, False)
            return False

    def ClearCounter(self):
        try:
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Total, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Fail, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Pass, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Yield, str( 100 ) )
            GlobalGui.global_Gui.leTotalSignal.emit( "0" )
            GlobalGui.global_Gui.lePassSignal.emit( "0" )
            GlobalGui.global_Gui.leFailSignal.emit( "0" )
            GlobalGui.global_Gui.leYieldSignal.emit( "100" )
            return True
            pass
        except Exception as e:
            print(e)
            self.RecordLoadMessage(str(e), 'red', Macro.INFO, False)
            self.RecordLoadMessage('读取 Counter 计数文件失败', 'red', 0, False)
            return False

    def Initialize(self):
        try:
            self.testDB.LoadConfiogure()
            self.testItemName.LoadConfiogure()
            self.loadGoldentestData("E:\Configure\点检数据.csv")
            num=self.GoldenTestData
            self.DOEKeys = self.loadDOEKey("E:\Configure\DoeKey.txt")


            self.Configure.LoadConfiogure()
            self.ConfigureDIC = self.Configure.ConfigureDic
            self.LimitDIC = self.Limit.ConfigureDic
            # self.OscLimit.LoadConfiogure()
            # self.OscLimitDic = self.OscLimit.OscConfigureDic
            self.CollectMCU()
            self.MACHINE_TYPE = self.Configure.ReadValue( self.Configurekey.SEC_MACHINE, self.Configurekey.KEY_TYPR )
            self.MACHINE_ADDRESS = self.Configure.ReadValue( self.Configurekey.SEC_MACHINE, self.Configurekey.KEY_ADDRESS )
            self.IsTempEnable = self.Configure.ConfigureDic[self.Configurekey.SEC_APP][
                                    self.Configurekey.SEC_TEMP_ENABLE] == "Y"

            time.sleep(1)  # 1s
            self.RecordLoadMessage('', 'black', 0, True)
            self.RecordLoadMessage('开始初始化......', 'black', 0, False)
            self.RecordLoadMessage('Start initialization......', 'black', 0, False)

            if not self.InitializeCounter():
                print('读取 Counter 文件失败')
                return
            self.SafeDoorEnable= self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_SafetydoorEnable] == "Y"

            TxRoffset = float( self.Configure.ReadValue( self.Configurekey.SEC_APP, self.Configurekey.SEC_TxRoffset ) )
            RxRoffset = float( self.Configure.ReadValue( self.Configurekey.SEC_APP, self.Configurekey.SEC_RxRoffset ) )

            TxXoffset = float( self.Configure.ReadValue( self.Configurekey.SEC_APP, self.Configurekey.SEC_TxXoffset ) )
            RxXoffset = float( self.Configure.ReadValue( self.Configurekey.SEC_APP, self.Configurekey.SEC_RxXoffset ) )

            self.Checktime=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CheckTime]
            self.CheckHours = float( self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_checkHours] )
            self.ShowCheckTime()

            self.ReadCoilMessage()

            # if not self.CheckAppConfigures():
            #     self.RecordLoadMessage('配置文件有缺失，请手动配置缺少项目', 'red', 0, False)
            #     return


            print(TxRoffset)
            print(self.SafeDoorEnable)

            version=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Version]
            self.RecordLoadMessage('当前软件版本：'+version, 'black', 0, False)

            print( "tx_R" + str( TxRoffset ) )
            print( "Rx_R" + str( RxRoffset ) )

            print( "tx_L" + str( TxXoffset ) )
            print( "Rx_L" + str( RxXoffset ) )



            # #<editor-fold desc="验证">
            # testlist =[]
            # d = cTestItem()
            # d.TestName = "Knom-30.0_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-30.0_Rtx"
            # d.TestValue = "0.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-30.0_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-20.9_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-20.9_Rtx"
            # d.TestValue = "0.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-20.9_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.85_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.85_Rtx"
            # d.TestValue = "0.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.85_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.2_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.2_Rtx"
            # d.TestValue = "0.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Knom-4.2_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            # self.CheckTestItemLargeSignal("knom", testlist)
            # d.Clear()
            # testlist.clear()
            # d.TestName = "Freeair-30.0_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-30.0_Rtx"
            # d.TestValue = "1.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-30.0_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-20.9_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-20.9_Rtx"
            # d.TestValue = "1.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-20.9_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-3.9_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-3.9_Rtx"
            # d.TestValue = "1.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-3.9_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-2.8_Ltx"
            # d.TestValue = "0.375"
            # d.TestUnit = "uH"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-2.8_Rtx"
            # d.TestValue = "1.768"
            # d.TestUnit = "Ohm"
            # testlist.append(d.Clone())
            #
            # d.TestName = "Freeair-2.8_Qtx"
            # d.TestValue = "65.909"
            # d.TestUnit = ""
            # testlist.append(d.Clone())
            # self.CheckTestItemLargeSignal("free", testlist)
            # return
            # #</editor-fold>

            time.sleep(0.2)
            self.RecordLoadMessage('连接单片机、扫码枪、机械手、相机、LCR或VNA、温度计，温度传感器, 示波器', 'black', 0, False)
            self.RecordLoadMessage('Connecting MCU、SACN、ROBOT、CAMERA、LCR or VNA、TEMP、SUR_TEMP、OSC', 'black', 0, False)

            GlobalGui.global_Gui.lblStatueEmit(1, False)
            GlobalGui.global_Gui.lblStatueEmit(2, False)
            GlobalGui.global_Gui.lblStatueEmit(3, False)

            GlobalGui.global_Gui.lbtestResultEmit(Macro.IDEL)

            # GlobalGui.global_Gui.tableWidgetEmit('DCR2', '100', '20', '50', True, 'ohm')
            if not self.devIns.InitializeDevice():
                print('连接失败，请检查后重新连接')
                self.RecordLoadMessage('连接失败，请检查后重新连接!', 'red', 0, False)
                self.RecordLoadMessage('The connection failed. Please connect again!', 'red', 0, False)
                return

            self.FS = 0x00
            self.isAbort = False
            self.isTesting = False
            self.StartTime = datetime.now()

            self.StartDetectTask()
        except Exception as e:
            print(e)
            self.RecordLoadMessage(str(e), 'red', 0, False)

    McuIntDic = {}
    McuOutDic = {}

    def CollectMCU(self):
        self.McuOutDic["Cylinder"] = self.Cylinder
        self.McuOutDic["LedY"] = self.LedY
        self.McuOutDic["LedR"] = self.LedR
        self.McuOutDic["LedG"] = self.LedG
        self.McuOutDic["FMQ"] = self.FMQ
        self.McuOutDic["XZK"] = self.XZK
        self.McuOutDic["YL"] = self.YL
        self.McuOutDic["FS"] = self.FS

        self.McuIntDic.clear()
        self.McuIntDic["start1"] = self.start1
        self.McuIntDic["start2"] = self.start2
        self.McuIntDic["Alarm"] = self.Alarm
        self.McuIntDic["begin"] = self.begin
        self.McuIntDic["air"] = self.air
        self.McuIntDic["door"] = self.door
        #self.McuIntDic["YLint"] = self.YLint
        self.McuIntDic["X11"] = self.X11
        self.McuIntDic["X12"] = self.X12
        self.McuIntDic["X13"] = self.X13
        self.McuIntDic["X14"] = self.X14
        self.McuIntDic["X15"] = self.X15
        self.McuIntDic["X16"] = self.X16


    def loadDOEKey(self,filepath):
        if not os.path.exists(filepath):
            self.RecordLoadMessage('不存在DOEKey.txt文件 ', 'red', 0, False )
            return ""
        file = open(filepath, 'r' )
        data = file.readlines()
        file.close()
        return data


    GoldenTestData={}
    def loadGoldentestData(self,filepath):
        if not os.path.exists(filepath):
            self.RecordLoadMessage('不存在点检文件', 'red', Macro.INFO, False )
            return
        file = open(filepath, 'r' )
        data = file.readlines()
        file.close()
        BT=data[0].split(",")
        Limit=data[1].split(',')

        for i in range(len(data)):
            if i<=2: continue
            testdata=dict()
            tmpdata = data[i].split( ',' )
            Key=tmpdata[0]
            for j in range(len(tmpdata)):
                if j is 0:
                    continue
                tmplimit=Limit[j]
                if tmplimit =="NA":
                    continue
                testdata[BT[j].replace("\n","")] = tmpdata[j].replace("\n","")

            self.GoldenTestData[Key]=testdata

    def CheckBarcode(self,barcode):
        time=float(self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_checkHours])*3600
        lastchecktime=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CheckTime]
        Time=datetime.strptime(lastchecktime,"%Y-%m-%d %H:%M")
        timespan = (datetime.now() - Time).total_seconds()
        if timespan>=time or barcode in self.GoldenTestData.keys():
            self.RecordLoadMessage( '点检开始', 'blue', Macro.INFO, False )
            self.IsCheckTimeEnable=True
            return barcode in self.GoldenTestData.keys()
        else:
            self.RecordLoadMessage( '正常测试开始', 'blue', Macro.INFO, False )
            self.IsCheckTimeEnable = False
        return True

    def ShowCheckTime(self):
        Time = datetime.strptime( self.Checktime, "%Y-%m-%d %H:%M" )
        timespan=datetime.now() - Time
        timeDiff=self.CheckHours*3600-timespan.total_seconds()
        TimeHours =round(timeDiff//3600,0)
        MM=round(timeDiff%3600//60,0)
        ss=round(timeDiff%3600%60,0)

        if timespan.total_seconds()>=self.CheckHours*3600:
            GlobalGui.global_Gui.lbCheckTimeEmit("点检时间到")
        else:
            GlobalGui.global_Gui.lbCheckTimeEmit("{0}:{1}:{2}".format(str(TimeHours),str(MM),str(ss)))

    def CheckTestData(self,barcode):
        if not self.IsCheckTimeEnable: return True

        if barcode not in self.GoldenTestData.keys():
            self.RecordLoadMessage( "点检时间到 无此条码 点检数据！请检查点检csv是否配置", 'red', Macro.INFO, False )
            return False
        Checkdata:dict=self.GoldenTestData[barcode]
        checkResult=True
        for num in self.testAllItem:
            tmpitem:cTestItem=num
            if tmpitem.TestName in Checkdata.keys():
                limit=float(tmpitem.TestValue)*0.2
                diff=abs(float(tmpitem.TestValue)-float(Checkdata[tmpitem.TestName]))
                checkResult&=diff<=limit
                if diff>limit:
                    self.RecordLoadMessage( "{0} 当前测试值：{1}  标准值{2}".format(tmpitem.TestName,tmpitem.TestValue,Checkdata[tmpitem.TestName]), 'red', Macro.INFO, False )
        if checkResult:
            self.RecordLoadMessage( "点检时间到 点检完成！", 'blue', Macro.INFO, False )
            self.Configure.SaveConfigure(self.Configurekey.SEC_APP,self.Configurekey.SEC_CheckTime,datetime.now().strftime( "%Y-%m-%d %H:%M" ))
            self.Checktime=datetime.now().strftime( "%Y-%m-%d %H:%M" )
        else:
            self.RecordLoadMessage( "点检时间到 点检失败！", 'red', Macro.INFO, False )

        return checkResult

    def StartDetectTask(self):
        try:
            if self.DetectThread != None and not self.DetectThread.is_alive():
                self.RecordLoadMessage('检测线程已运行，不能重复开启!', 'red', 0, False)
                self.RecordLoadMessage('The detection thread is already running and cannot be opened repeatedly!',
                                       'red', 0, False)
                return
            self.DetectThread = threading.Thread(target=self.DetectFunction, name='DetectFunction')
            self.DetectThread.start()
        except Exception as e:
            print(e)

    PreAlarm = 0x00
    PreAir = 0x00
    preStart = False
    SafeDoor=False

    def DetectFunction(self):
        mcu: cMcu = self.devIns.Devices(Macro.MCU)
        Robot2002: cRobot = self.devIns.Devices(Macro.ROBOT_2002)
        Robot2001: cRobot = self.devIns.Devices(Macro.ROBOT_2001)
        if mcu == None:
            self.RecordLoadMessage('获取单片机失败，请检查后重启软件', 'red', Macro.INFO, False)
            self.RecordLoadMessage('Failed to obtain MCU, please check and restart ''the software', 'red', 0, False)
            #GlobalGui.global_Gui.leBarcodeSignal.emit('FE12345678')

        while not self.isAbort:
            time.sleep(0.03)  # 20ms

            self.ShowCheckTime()

            if not self.ReadIo(mcu):
                self.RecordLoadMessage('获取单片机输入输出失败，请检查后重启软件', 'red', Macro.INFO, False)
                break

            if self.air is not self.PreAir:
                GlobalGui.global_Gui.lblStatueEmit(1, self.air == 0x01)
                self.PreAir = self.air
            SafetyEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_SafetyfenceEnable] == "Y"
            if SafetyEnable and self.door is 0x00 and self.isTesting:
                self.RecordLoadMessage('测试中，door', 'red', Macro.INFO, False)
                self.SafeDoor = True
                self.isAlarm = True

            if self.SafeDoorEnable and (self.X13 is 0x00 or self.X14 is 0x00 or self.X15 is 0x00) and self.isTesting:
                self.RecordLoadMessage('测试中，安全门未关上，请检查', 'red', Macro.INFO, False)
                self.SafeDoor=True
                self.isAlarm=True

            if self.SafeDoorEnable and self.door is 0x01:
                self.SafeDoor = False


            # 急停按下 松开复位机械手
            if self.Alarm is not self.PreAlarm:
                GlobalGui.global_Gui.lblStatueEmit(3, self.Alarm == 0x01)
                if self.Alarm is 0x01:
                    self.RecordLoadMessage('急停触发', 'red', Macro.INFO, False)
                    self.LedG = 0x00
                    self.LedY = 0x00
                    self.LedR = 0x01

                if self.Alarm is not 0x01:
                    self.RecordLoadMessage('急停复位', 'black', Macro.INFO, False)
                    self.LedG = 0x00
                    self.LedY = 0x01
                    self.LedR = 0x00

                self.isAlarm = self.Alarm == 0x01
                self.PreAlarm = self.Alarm
                if self.Alarm is 0x00:
                    Robot2002.Write('$Reset')
                    time.sleep(0.2)
                    Robot2002.Write('$Start,0')
                    time.sleep(0.2)
                    self.devIns.Reconnect2001()

            Startflag=self.readStartFlag(mcu)   #self.start1 is 0x01 and self.start2 is 0x01

            if Startflag is not self.preStart:
                GlobalGui.global_Gui.lblStatueEmit(2, self.start1 is 0x01 and self.start2 is 0x01)
                self.preStart = Startflag

            if (Startflag or self.Mstart) and not self.isTesting and self.Alarm != 0x01:
                self.RecordLoadMessage('获取开始测试信号成功', 'black', Macro.INFO, False)
                self.Mstart = False


                self.TestThread = threading.Thread(target=self.testFunc, name="TestThread")
                self.TestThread.start()

                pass

            if self.isTesting:
                Interval = datetime.now() - self.StartTime
                GlobalGui.global_Gui.lblTestTimeSignal.emit(str(round(Interval.total_seconds(), 2)))

    def readStartFlag(self,mcu):
        if self.start1 is 0x01 or self.start2 is 0x01:
            time.sleep(0.5)
            if not self.ReadIo(mcu):
                self.RecordLoadMessage('获取单片机输入输出失败，请检查后重启软件', 'red', Macro.INFO, False)
                return False

            if self.start1 is not 0x01 and self.start2 is 0x01:
                self.RecordLoadMessage('请保证双手启动测试 左启动未按下', 'red', Macro.INFO, False)
                self.StartFlageEnable=False
                return False

            if self.start2 is not 0x01 and self.start1 is 0x01:
                self.RecordLoadMessage('请保证双手启动测试 右启动未按下', 'red', Macro.INFO, False)
                self.StartFlageEnable = False
                return False

            if self.start2 is 0x01 and self.start1 is 0x01 and self.StartFlageEnable:
                return True
        else:
            self.StartFlageEnable=True

        return False


    def RestRobot(self):
        Robot2001: cRobot = self.devIns.Devices( Macro.ROBOT_2001 )
        if self.SafeDoor:
            self.Cylinder = 0x00
            self.YL = 0x00

            Robot2001.Init( 2 )
            time.sleep( 0.5 )
            Robot2001.Move( -120, 0, 0, 0, 0, 0 )
            self.SafeDoor=False
        else:
            self.RecordLoadMessage( '无需复位', 'blue', Macro.INFO, False )


    # <editor-fold desc="测试流程">
    testAllItem = []

    def testFunc(self):
        self.IsLCR = str(self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Test_mode]) == "LCR"
        Robot2001: cRobot = self.devIns.Devices(Macro.ROBOT_2001)
        ccd: CCD = self.devIns.Devices(Macro.CAMREA)
        hawk: cHawk = self.devIns.Devices(Macro.HWAK)
        vna = self.IsLCR and self.devIns.Devices(Macro.LCR) or self.devIns.Devices(Macro.VNA)
        temp: cModbusSerial = self.devIns.Devices(Macro.TEMP)
        surTemp: cModbusSerial = self.devIns.Devices(Macro.SUR_TEMP)
        Osc: cOscillograph = self.devIns.Devices(Macro.OSC)

        xLocation = 0.00
        yLocation = 0.00
        zLocation = 0.00
        uLocation = 0.00
        vLocation = 0.00
        WLocation = 0.00
        try:
            self.isAlarm = False
            self.isTesting = True
            GlobalGui.global_Gui.lbtestResultEmit(Macro.TEST)
            self.testAllItem.clear()
            self.TestResult = True
            self.BarcodeFail = False
            self.StartTime = datetime.now()
            self.RecordLoadMessage('清除界面', 'black', Macro.INFO, True)
            self.RecordLoadMessage('开始测试', 'black', Macro.INFO, False)
            self.RecordLoadMessage('当前测试模式：' + self.TestModel, 'blue', 0, False)

            debug = True
            self.LedG = 0x01
            self.LedY = 0x00
            self.LedR = 0x00

            if self.SafeDoor:
                self.RecordLoadMessage('安全连锁打开或光栅阻挡！请检查！无问题 复位后再启动', 'red', 0, False)
                return

            IsAutoScan = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_SCAN_mode] == "A"
            Barcodelength = int(self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Barcode_Cnt])
            IsCheckBarcode = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Barcode_Check] == "Y"
            IsMac=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_MAC] == "mac"
            Barcode = ""

            self.MACHINE_TYPE = self.Configure.ReadValue( self.Configurekey.SEC_MACHINE, self.Configurekey.KEY_TYPR )

            if not IsAutoScan:
                Barcode = self.BarcodeM
                if IsCheckBarcode and len(Barcode) != Barcodelength:
                    self.RecordLoadMessage('条码长度不符 测试结束', 'red', Macro.INFO, False)
                    self.TestResult = False
                    self.BarcodeFail = True
                    self.isAlarm = True
            GlobalGui.global_Gui.leBarcodeSignal.emit("")
            GlobalGui.global_Gui.leBarcodeSignal.emit(Barcode)
            if self.isAlarm: return

            self.RecordLoadMessage('吸真空打开', 'black', Macro.INFO, False)
            self.FS = 0x00
            self.Cylinder = 0x01

            for i in range(5):
                time.sleep(0.2)
                if self.isAlarm: return


            self.XZK = 0x01
            self.Relay1 = 0x00
            self.Relay2 = 0x00

            if self.isAlarm: return

            self.RecordLoadMessage('下压气缸', 'black', Macro.INFO, False)
            self.YL=0x01 #下压气缸

            # for i in range(15):
            #     time.sleep(0.2)
            #     if self.isAlarm: return
            for i in range(8):
                time.sleep(0.2)
                if self.isAlarm: return



            if self.X12!=0x01:
                self.isAlarm=True
                self.RecordLoadMessage('气缸下压超时', 'red', Macro.INFO, False)
            self.Cylinder = 0x00

            if self.isAlarm: return
            SafetyEnable= self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_SafetyfenceEnable] == "Y"
            if IsAutoScan:
                # if SafetyEnable and self.door is 0x00:
                #     self.RecordLoadMessage( '安全光幕被遮挡！请安全操作', 'red', 0, False )
                #     self.TestResult=False
                #     return

                self.RecordLoadMessage('开始扫码', 'black', Macro.INFO, False)
                result, Barcode = hawk.GetBarcde(Barcodelength, 3)
                self.RecordLoadMessage('扫码结果：' + str(result) + '，条码：' + str(Barcode), 'black', Macro.INFO, False)
                if result:
                    GlobalGui.global_Gui.leBarcodeSignal.emit(str(Barcode))
                else:
                    self.BarcodeFail = True
                    self.isAlarm = True

            if self.isAlarm: return
            self.RecordLoadMessage('点检检测,是否到点检时间', 'black', Macro.INFO, False)
            #判断点检物料
            if not self.CheckBarcode(Barcode):
                self.RecordLoadMessage( '点检时间到 此物料非点检物料', 'red', Macro.INFO, False )
                self.isAlarm = True

            if self.isAlarm: return

            # 3次不良
            Color = "NA"
            Model = "NA"
            CoilSN = "NA"
            if self.MACHINE_ADDRESS == Macro.ADDRESS_CD_JP and not self.IsCheckTimeEnable:
                ThreeCheckEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_ThreeCheckEnable] == "Y"
                API = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_API]
                ProcessID = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_ProcessID]
                PreStationProcessID = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_PreStationProcessID]

                if ThreeCheckEnable and not self.isAlarm:
                    self.RecordLoadMessage('三次NG卡控，开始检查', 'black', Macro.INFO, False)
                    result, Message, Color, Model, CoilSN, self.ConfigM = self.trace.CheckBarcodeThreeNG_JP(API,
                                                                                                            Barcode,
                                                                                                            ProcessID,
                                                                                                            PreStationProcessID,
                                                                                                            self.DOEKeys)
                    self.RecordLoadMessage('卡控结果：'+str(result) +'卡控信息：'+ Message+'Color：'+ Color+'Model：'+ Model
                                           +'CoilSN：'+ CoilSN+'Config：'+ self.ConfigM,
                                           'black',
                                           Macro.INFO,
                                           False)
                    # result, Message, Color, Model = self.trace.CheckBarcodeThreeNG_JP(API, Barcode, ProcessID,
                    #                                                                   PreStationProcessID)
                    if not result:
                        self.RecordLoadMessage('ERROR：' + Message, 'red', Macro.INFO, False)
                        self.TestResult = False
                        self.isAlarm = True
                        self.BarcodeFail = True

            if self.isAlarm:
                return

            ProcessControl = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_ProcessControl] == "Y"
            if ( ProcessControl and self.TestModel != "DOE" and self.MACHINE_ADDRESS == Macro.ADDRESS_CD_MCEG) and not self.IsCheckTimeEnable:
                uploadEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Upload_Enable] == "Y"
                if IsAutoScan and uploadEnable:
                    self.RecordLoadMessage('比对条码', 'black', Macro.INFO, False)
                    responsebody = Responsebody()
                    responsebody.isOk = False
                    responsebody.erroMessage = ""
                    responsebody = self.trace.SnCheck(Barcode)
                    self.RecordLoadMessage(
                        f'校验条码结果：' + str(responsebody.isOk) + '，比对信息：' + responsebody.erroMessage, 'black', Macro.INFO,
                        False)
                    if responsebody is None or not responsebody.isOk:
                        self.TestResult = False
                        self.BarcodeFail = True
                        self.isAlarm = True

            self.RecordLoadMessage('开始abb', 'black', Macro.INFO, False)
            self.RecordLoadMessage(f'TestModel：' + str( self.TestModel) + '，ADDRESS：' +str( self.MACHINE_ADDRESS)+
                                   ',MACHINE_TYPE:'+str(self.MACHINE_TYPE)+',CheckTime:'+str(self.IsCheckTimeEnable),
                                   'black',
                                   Macro.INFO,
                                   False)

            if self.TestModel != "DOE" and self.MACHINE_ADDRESS == Macro.ADDRESS_CD_MCEG and self.MACHINE_TYPE == Macro.TYPE_5XX and not self.IsCheckTimeEnable:
                ProcessID = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_ProcessID]
                ReworkProcessID = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Rework_ProcessID]
                result_r, Message_r = self.trace.CheckBarcodeRework_MCEG("", Barcode, ReworkProcessID)
                self.RecordLoadMessage(f'rework判定结果：' + str(result_r) + '，rework判定信息：' + Message_r, 'black', Macro.INFO, False)
                if result_r:
                    self.RecordLoadMessage(f'当前为rework不判定3次', 'black', Macro.INFO, False)
                else:
                    self.RecordLoadMessage(f'当前不为rework开始判定3次', 'black', Macro.INFO, False)
                    result, Message = self.trace.CheckBarcodeThreeNG_MCEG("", Barcode, ProcessID, 3)

                    self.RecordLoadMessage(f'判定结果：' + str(result) + '，判定信息：' + Message, 'black', Macro.INFO,
                                           False)
                    if not result:
                        self.RecordLoadMessage(f'判定结果：' + str(result), 'black', Macro.INFO, False)
                        self.TestResult = False
                        self.BarcodeFail = True
                        self.isAlarm = True

            self.RecordLoadMessage(f'TestResult：' + str(self.TestResult) + '，BarcodeFail：' + str(self.BarcodeFail)
                                   + '，isAlarm：' + str(self.isAlarm), 'black', Macro.INFO, False)
            if self.isAlarm:
                self.RecordLoadMessage('结束1', 'black', Macro.INFO, False)
                return


            if self.MACHINE_ADDRESS == Macro.ADDRESS_YC_LIKAI  and not self.IsCheckTimeEnable:
                uploadEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Upload_Enable] == "Y"
                if IsAutoScan and uploadEnable:
                    self.RecordLoadMessage('比对条码', 'black', Macro.INFO, False)
                    responsebody = Responsebody()
                    responsebody.isOk = False
                    responsebody.erroMessage = ""
                    responsebody = self.trace.SnCheck(Barcode)
                    self.RecordLoadMessage(
                        f'校验条码结果：' + str(responsebody.isOk) + '，比对信息：' + responsebody.erroMessage, 'black', Macro.INFO,
                        False)
                    if responsebody is None or not responsebody.isOk:
                        self.TestResult = False
                        self.BarcodeFail = True
                        self.isAlarm = True

                if self.isAlarm:
                    return

                CoilEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CoilConfigEnable] == "Y"
                if CoilEnable and self.TestModel != "DOE" and not self.isAlarm and not self.IsCheckTimeEnable:
                    Result, CoilSN, CoilVendor, CoilFerrite = self.trace.RTGetCoilConfig(Barcode)

                station_id = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Station_Rk_Csv]
                NgCheck = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_ThreeCheckEnable] == "Y"
                if NgCheck and self.TestModel != "DOE" and not self.isAlarm and not self.IsCheckTimeEnable:
                    self.RecordLoadMessage('三次NG卡控检测开始', 'black', Macro.INFO, False)
                    Result, Message = self.trace.RTSnCheck(Barcode, station_id)
                    if not Result:
                        self.isAlarm = True
                        self.RecordLoadMessage('三次NG卡控：' + Message, 'red', Macro.INFO, False)

            if self.isAlarm:
                self.RecordLoadMessage('结束2', 'black', Macro.INFO, False)
                return





            CoilVendor = "NA"
            CoilFerrite = "NA"
            if (self.MACHINE_ADDRESS == Macro.ADDRESS_CD_MCEG and self.TestModel !="DOE") and not self.IsCheckTimeEnable:
                self.RecordLoadMessage('Coil线圈信息读取开始', 'black', Macro.INFO, False)
                Result, CoilSN, CoilVendor, CoilFerrite = self.GetCoil(Barcode)
                if not Result:
                    self.isAlarm = True
                    self.RecordLoadMessage('获取线圈信息失败', 'red', Macro.INFO, False)

            if self.isAlarm:
                return

            if self.isAlarm: return

            # <editor-fold desc="LCR前四项测试">
            # if self.isAlarm: return
            # if self.IsLCR:
            #     vna.SetFreq("1000")
            #     self.Relay1 = 1 << 2 | 1 << 3
            #     time.sleep(0.2)
            #     if self.Relay1 is not self.relay1:
            #         self.RecordLoadMessage('继电器切换超时', 'red', 0, False)
            #         self.isAlarm = True
            #
            #     if self.isAlarm: return
            #     Result, DCR = vna.GetRDC()
            #     if not Result:
            #         self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            #         self.isAlarm = True
            #     self.CheckTestItem("TX", DCR)
            #     vna.SetFreq("300000")
            #     Result, LSRSQ = vna.GetLSRSQ()
            #     if not Result:
            #         self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            #         self.isAlarm = True
            #     self.CheckTestItem("TX", LSRSQ)
            # else:
            #     if self.isAlarm: return
            #     self.Relay1 = 0x01
            #     time.sleep(0.1)
            #     Result, RSLS = vna.GetRS()
            #     if not Result:
            #         self.RecordLoadMessage('读取VNA数据失败', 'red', 0, False)
            #         self.isAlarm = True
            #     self.CheckTestItem("TX", RSLS)
            #     pass
            # </editor-fold>

            rs_temp_Offset = '0'
            # <editor-fold desc="获取温度补偿系数放入测试项目">
            if self.IsTempEnable:
                rs_temp_Offset = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_RS_TEMP_OFFSET]
                # testItemList_HSG_cof = []
                # tmpdata_HSG_cof = cTestItem()
                # tmpdata_HSG_cof.TestName = 'HSG_cof'
                # tmpdata_HSG_cof.TestResult = True
                # tmpdata_HSG_cof.TestUnit = 'mOhm/Celsius'
                # tmpdata_HSG_cof.TestLowLimit = 'NA'
                # tmpdata_HSG_cof.TestUpLimit = 'NA'
                # tmpdata_HSG_cof.TestValue = str(rs_temp_Offset)
                # testItemList_HSG_cof.append(tmpdata_HSG_cof.Clone())
                #
                # self.CheckTestItemLargeSignal('HSG_cof', testItemList_HSG_cof)

            # </editor-fold">
            # <editor-fold desc="环境温度测试">
            self.isSurTempEnable = self.Configure.ConfigureDic[self.Configurekey.SEC_APP][
                                       self.Configurekey.SEC_SUR_TEMP_ENABLE] == "Y"
            temperature = 0.0
            if self.isSurTempEnable:
                self.RecordLoadMessage('开始读取环境温度', 'black', Macro.INFO, False)

                result, tmpTestitem = surTemp.ReadSurroundsTemperature()
                if not result:
                    self.RecordLoadMessage('读取环境温度失败', 'red', Macro.INFO, False)
                    self.TestResult = False
                    self.isAlarm = True
                if self.isAlarm: return

                for item in tmpTestitem:
                    tmpdata: cTestItem = item
                    temperature: float = float(tmpdata.TestValue)

                self.RecordLoadMessage('环境温度为：' + str(temperature), 'black', Macro.INFO, False)

                # self.Differ: float = float(float(temperature) - 25.0)
                # self.RecordLoadMessage('环境温度和25度差值为：' + str(self.Differ), 'black', Macro.INFO, False)

                self.CheckTestItemLargeSignal('SUR_TEMP', tmpTestitem)
            # </editor-fold">
            # <editor-fold desc="产品测试温度测试">
            self.Differ = 0.0
            if self.IsTempEnable:
                self.RecordLoadMessage('开始读取温度', 'black', Macro.INFO, False)
                temperature = 0.0
                result, tmpTestitem = temp.ReadTemperature()
                if not result:
                    self.RecordLoadMessage('读取温度失败', 'red', Macro.INFO, False)
                    self.TestResult = False
                    self.isAlarm = True
                if self.isAlarm: return

                for item in tmpTestitem:
                    tmpdata: cTestItem = item
                    temperature: float = float(tmpdata.TestValue)

                self.RecordLoadMessage('温度为：' + str(temperature), 'black', Macro.INFO, False)

                self.Differ: float = round((float(temperature) - 25), 1)
                self.RecordLoadMessage('温度和25度差值为：' + str(self.Differ), 'black', Macro.INFO, False)
                # if self.differ < 0:
                #     self.AIM_DCR_VALUE = str(float(self.AIM_DCR_VALUE) - abs(self.differ) * 0.117)
                # if self.differ > 0:
                #     self.AIM_DCR_VALUE = str(float(self.AIM_DCR_VALUE) + abs(self.differ) * 0.117)

                self.CheckTestItemLargeSignal('TEMP-test', tmpTestitem)

            # </editor-fold">
            # <editor-fold desc="获取测试db值">
            vna.Knom_POWER_GAIN = ""
            vna.Freeair_POWER_GAIN = ""
            DBDic = self.testDB.ConfigureDic["DB"]
            for key, value in DBDic.items():
                if "free" in key:
                    vna.Freeair_POWER_GAIN += value
                    vna.Freeair_POWER_GAIN += ","
                if "knom" in key:
                    vna.Knom_POWER_GAIN += value
                    vna.Knom_POWER_GAIN += ","
            # </editor-fold>
            if self.isAlarm: return
            vna.ls_offset = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.KEY_LS_OFFSET]
            vna.rs_offset = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.KEY_RS_OFFSET]

            if self.isAlarm: return
            self.RecordLoadMessage('开始测试 Freeair', 'black', Macro.INFO, False)
            # <editor-fold desc="Freeair测试">
            if self.isAlarm: return
            time.sleep(0.1)
            Result, Data, Msg, OscData = vna.get_Freeair_Value(1, osc=Osc)

            if not Result:
                self.RecordLoadMessage(str(Msg), 'red', Macro.INFO, False)
                self.RecordLoadMessage('读取VNA数据失败', 'red', Macro.INFO, False)
                self.isAlarm = True
            if OscData == None:
                self.RecordLoadMessage(str(Msg), 'red', Macro.INFO, False)
                self.RecordLoadMessage('读取OSC数据失败', 'red', Macro.INFO, False)
                self.isAlarm = True
            if self.isAlarm: return
            tmpOffset:float = 0.0
            tmpOffset = abs(float(self.Differ)) * float(rs_temp_Offset)
            if float(self.Differ) < 0:
                tmpOffset *= -1
            self.CheckTestItemLargeSignal("free", Data, tmpOffset)
            self.CheckTestItemLargeSignal("osc_free", OscData, 0)
            # </editor-fold>
            if self.isAlarm: return


            # <editor-fold desc="相机流程">
            DistanceLimit = float(self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_DistanceLimit])
            AngleLimit = float(self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_AngleLimit])

            if self.isAlarm: return

            self.RecordLoadMessage('机械手回原点开始', 'black', Macro.INFO, False)
            if not Robot2001.Init(2):
                self.RecordLoadMessage('机械手回原点失败，请检查机械手连接是否正常', 'red',Macro.INFO, False)
                return

            if self.isAlarm: return

            for i in range(15):
                time.sleep(0.2)
                if self.isAlarm: return

            if self.isAlarm: return
            Cnt = 0
            DistanceTotal: float = 0
            AngleTotal: float = 0
            Distance=0
            Angle=0
            if self.isAlarm: return
            while not self.isAlarm:
                if Cnt > 4:
                    self.RecordLoadMessage('相机调整超时', 'red', Macro.INFO, False)
                    self.isAlarm = True
                    break

                if DistanceLimit > 1 and AngleLimit > 1:
                    self.RecordLoadMessage('相机屏蔽', 'red', Macro.INFO, False)
                    xLocation = 0.0
                    uLocation = 0.0
                    break

                CCDResult, Distance, Angle = ccd.GetData(3)
                GlobalGui.global_Gui.lbAngleorDistanceEmit(str(Angle), str(Distance))
                if not CCDResult:
                    self.RecordLoadMessage('相机拍照失败，请检查相机是否正常', 'red', Macro.INFO, False)
                    self.isAlarm = True
                    break

                if self.isAlarm: return
                DistanceDiff = abs(Distance - 0.88)
                AngleDiff = abs(Angle)

                DistanceOffset: float = 0
                AngleOffset: float = 0
                if self.isAlarm: return
                if DistanceDiff <= DistanceLimit and AngleDiff <= AngleLimit:
                    self.RecordLoadMessage('相机调整完成', 'black', Macro.INFO, False)
                    xLocation = Distance
                    uLocation = Angle
                    break
                if self.isAlarm: return
                if DistanceDiff > DistanceLimit:
                    DistanceOffset = round(Distance - 0.88, 4)
                    DistanceTotal += DistanceOffset
                    pass
                if self.isAlarm: return
                if AngleDiff > AngleLimit:
                    AngleOffset = round(Angle, 4)
                    AngleTotal += AngleOffset
                    pass
                if self.isAlarm: return
                if abs(AngleTotal) > 1 or abs(DistanceTotal) > 0.7:
                    self.RecordLoadMessage('相机调整超过设定范围', 'red', Macro.INFO, False)
                    self.isAlarm = True
                    break
                if self.isAlarm: return
                MoveResult = Robot2001.Move(DistanceOffset, 0, 0, AngleOffset, 0, 0)
                if not MoveResult:
                    self.RecordLoadMessage('机械手移动失败', 'red', Macro.INFO, False)
                    self.isAlarm = True
                    break
                time.sleep(0.1)
                Cnt += 1
                if self.isAlarm: return

            # </editor-fold>
            if self.isAlarm: return
            # <editor-fold desc="Knom测试">
            time.sleep(0.1)
            self.RecordLoadMessage('开始测试 knom', 'black', Macro.INFO, False)
            Result, Data, OscData = vna.get_Knom_Value(1, osc=Osc)
            if not Result:
                self.RecordLoadMessage('读取VNA数据失败', 'red', Macro.INFO, False)
                self.isAlarm = True
            if OscData == None:
                self.RecordLoadMessage('读取OSC数据失败', 'red', Macro.INFO, False)
                self.isAlarm = True
            if self.isAlarm: return
            self.CheckTestItemLargeSignal("knom", Data)
            self.CheckTestItemLargeSignal("osc_knom", OscData)
            # </editor-fold>
            if self.isAlarm: return

            # # <editor-fold desc="OSC测试">
            # time.sleep(0.1)
            # Result, Data = Osc.test()
            # if not Result:
            #     self.RecordLoadMessage(str(Msg), 'red', Macro.INFO, False)
            #     self.RecordLoadMessage('读取OSC数据失败', 'red', Macro.INFO, False)
            #     self.isAlarm = True
            # if self.isAlarm: return
            # self.CheckTestItemLargeSignal("osc", Data)
            # # </editor-fold>
            time.sleep(2)


            version = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Version]
            self.RecordtestItem( "Version", version )

            if self.isAlarm: return
            # 强制pass
            #self.TestResult=True

            #计数
            total = 1
            Pass = self.TestResult and 1 or 0
            Fail = not self.TestResult and 1 or 0
            self.RecordtestCount(total, Pass, Fail)
            CheckResult= self.CheckTestData(Barcode)

            Interval = datetime.now() - self.StartTime  # 测试时间CT
            Project = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Project]
            if self.isAlarm: return

            #上传

            self.RecordLoadMessage('保存CSV数据', 'black', Macro.INFO, False)
            fileName =""
            if self.TestModel == "DOE" and not self.IsCheckTimeEnable:
                fileName = "{0}-{1}.csv".format(time.strftime("%Y-%m-%d", time.localtime()),"DOE" )
                self.Csv.SaveDOECSVLog(Project, fileName, self.testAllItem, Barcode, self.StartTime,
                                       self.MACHINE_ADDRESS, CoilSN, CoilVendor, CoilFerrite,
                                       str(Interval.total_seconds()))
            else:
                fileName = "{0}-{1}.csv".format(time.strftime("%Y-%m-%d", time.localtime()),
                                                self.IsCheckTimeEnable and "Check" or self.IsLCR and "LCR" or "VNA")
                self.Csv.SaveCSVLog( self.MACHINE_TYPE, fileName, Project, self.testAllItem, Barcode, self.StartTime,
                                 self.MACHINE_ADDRESS, CoilSN, CoilVendor, CoilFerrite, str(Interval.total_seconds()))
            if self.isAlarm: return
            uploadEnable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Upload_Enable] == "Y"


            self.RecordLoadMessage('上传数据', 'black', Macro.INFO, False)
            # trace2.0 书签
            Upload_OP = self.OpID
            Upload_fixture_id = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_FixtureID]
            Upload_goldenSN = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_GoldenSN]
            Upload_line_id = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_line_id]
            Upload_soft_name = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_soft_name]
            Upload_station_id = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_station_id]
            Upload_Version = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Version]
            Upload_checkTime = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CheckTime]
            if self.isAlarm: return
            if self.MACHINE_ADDRESS == Macro.ADDRESS_YC_LIKAI and not self.IsCheckTimeEnable:  # 盐城立凯
                if uploadEnable and not self.IsCheckTimeEnable:
                    if IsMac:
                        UploadfileName = "{0}_{1}.csv".format(Barcode,
                                                              time.strftime('%Y%m%d%H%M%S%f', time.localtime()))
                        self.Csv.SaveUploadCSVLog(UploadfileName, self.testAllItem, Barcode, self.StartTime)
                        if self.isAlarm: return
                    else:
                        Interval = datetime.now() - self.StartTime
                        shift = self.DorN()
                        startTimeStr = self.StartTime.strftime('%Y-%m-%d %H:%M:%S')
                        endTimeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        # self.McegJson( Barcode, datetime.now(), Interval.total_seconds(), self.TestResult, self.testAllItem )
                        responsebody = Responsebody()
                        responsebody.isOk = False
                        responsebody.erroMessage = ""
                        responsebody = self.trace.UploadJson_RK(self.TestResult and "pass" or "fail", Barcode,
                                                                startTimeStr, endTimeStr,
                                                                str(Interval.total_seconds()), Upload_OP, shift,
                                                                Upload_line_id,
                                                                Upload_station_id, Upload_soft_name, Upload_Version,
                                                                Upload_fixture_id,
                                                                Upload_goldenSN, Upload_checkTime,
                                                                self.IsCheckTimeEnable, self.testAllItem)
                        self.SaveRKCSV(Barcode, self.TestResult, self.StartTime)
                        self.RecordLoadMessage(f'上传结果：' + str(responsebody.isOk) + '，上传结果信息：'
                                               + responsebody.erroMessage,'black', Macro.INFO, False)
                        if self.isAlarm: return

            if (self.TestModel !="DOE" and self.MACHINE_ADDRESS == Macro.ADDRESS_CD_MCEG) and not self.IsCheckTimeEnable:  # 成都MCEG
                if uploadEnable and not self.IsCheckTimeEnable:
                    if IsMac:
                        UploadfileName = "{0}_{1}.csv".format(Barcode,
                                                              time.strftime('%Y%m%d%H%M%S%f', time.localtime()))
                        self.Csv.SaveUploadCSVLog(UploadfileName, self.testAllItem, Barcode, self.StartTime)
                        if self.isAlarm: return
                    else:
                        Interval = datetime.now() - self.StartTime
                        #shift = self.DorN()   # 白夜班
                        startTimeStr = self.StartTime.strftime('%Y-%m-%d %H:%M:%S')
                        endTimeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        #self.McegJson( Barcode, datetime.now(), Interval.total_seconds(), self.TestResult, self.testAllItem )
                        responsebody = Responsebody()
                        responsebody.isOk = False
                        responsebody.erroMessage = ""
                        responsebody = self.trace.UploadJson_MCEG(self.TestResult and "pass" or "fail", Barcode,
                                                                startTimeStr, endTimeStr,
                                                                str(Interval.total_seconds()), Upload_OP,
                                                                Upload_line_id,
                                                                Upload_station_id, "MahiCoupling", Upload_Version,
                                                                Upload_fixture_id,
                                                                Upload_goldenSN, Upload_checkTime,
                                                                self.IsCheckTimeEnable, self.testAllItem)
                        self.SaveRKCSV(Barcode, self.TestResult, self.StartTime)
                        self.RecordLoadMessage(f'上传结果：' + str(responsebody.isOk) + '，上传结果信息：'
                                               + responsebody.erroMessage, 'black', Macro.INFO, False)
                        if self.isAlarm: return

            if self.MACHINE_ADDRESS == Macro.ADDRESS_CD_JP and not self.IsCheckTimeEnable:  # 成都JP
                if uploadEnable and not self.IsCheckTimeEnable:
                    if IsMac:
                        UploadfileName = "{0}_{1}.csv".format(Barcode,
                                                              time.strftime('%Y%m%d%H%M%S%f', time.localtime()))
                        self.Csv.SaveUploadCSVLog(UploadfileName, self.testAllItem, Barcode, self.StartTime)
                        if self.isAlarm: return
                    else:
                        Interval = datetime.now() - self.StartTime
                        # self.McegJson( Barcode, datetime.now(), Interval.total_seconds(), self.TestResult, self.testAllItem )
                        self.JPJson_2(Barcode, self.StartTime,  Interval.total_seconds(), Color, Model, self.TestResult,
                                    self.testAllItem, CoilSN )
                        if self.isAlarm: return

            if self.isAlarm: return


        except Exception as e:
            self.RecordLoadMessage( 'Test-Error：'+str(e), 'red', Macro.INFO, False )
            print(e)

        finally:
            if self.MACHINE_ADDRESS == Macro.ADDRESS_CD_JP:
                self.BarcodeM = ""
                self.FS = 0x00
                self.XZK = 0x00
                self.LedG = 0x00
                self.LedY = 0x01
                self.LedR = 0x00
                self.Relay1 = 0x00
                self.Relay2 = 0x00

                if not self.SafeDoor:
                    self.Cylinder = 0x00
                    self.YL = 0x00

                if self.SafeDoor:
                    self.RecordLoadMessage('安全门 打开或光栅阻挡！停止测试 请复位。', 'red', Macro.INFO, False)



                if not self.BarcodeFail and not self.SafeDoor:
                    Robot2001.Init(2)
                    time.sleep(0.5)
                    Robot2001.Move(-120, 0, 0, 0, 0, 0)

                if self.isAlarm and self.SafeDoor:
                    GlobalGui.global_Gui.lbtestResultEmit(Macro.FAIL)
                else:
                    GlobalGui.global_Gui.lbtestResultEmit(self.TestResult and Macro.PASS or Macro.FAIL)
                self.RecordLoadMessage('测试结束', 'black', Macro.INFO, False)
                self.BarcodeFail = False
                self.isTesting = False
                self.isAlarm = False
            else:
                self.BarcodeM = ""
                self.FS = 0x00
                self.XZK = 0x00
                self.LedG = 0x00
                self.LedY = 0x01
                self.LedR = 0x00
                self.Relay1 = 0x00
                self.Relay2 = 0x00

                self.Cylinder = 0x00
                self.YL = 0x00

                if self.SafeDoor:
                    self.RecordLoadMessage('安全门 打开或光栅阻挡！ 停止测试', 'red', Macro.INFO, False)

                if not self.BarcodeFail and not self.SafeDoor:
                    Robot2001.Init(2)
                    time.sleep(0.5)
                    Robot2001.Move(-120, 0, 0, 0, 0, 0)

                if self.isAlarm and self.SafeDoor:
                    GlobalGui.global_Gui.lbtestResultEmit(Macro.FAIL)
                else:
                    GlobalGui.global_Gui.lbtestResultEmit(self.TestResult and Macro.PASS or Macro.FAIL)

                self.RecordLoadMessage('测试结束', 'black', Macro.INFO, False)
                self.BarcodeFail = False
                self.isTesting = False
                self.isAlarm = False

            pass

    # </editor-fold>
    # 判断当前是白天还是晚上
    def DorN(self):
        now = datetime.now()
        if now.hour >= 8 and now.hour < 20:
            return "D"
        else:
            return "N"

    def SaveRKCSV(self, Barcode,result,startTime):

        uploadPath = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_UploadPath]
        product=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Product_Rk_Csv]
        source=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Source_Rk_Csv]
        line=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Line_Rk_Csv]
        station=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Station_Rk_Csv]
        equipment=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Ip_Rk_Csv]
        process=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Process_Rk_Csv]

        filename="{0}.csv".format(Barcode)
        self.Csv.RKSaveCSVLog(uploadPath,filename,self.testAllItem,Barcode,startTime.strftime('%Y-%m-%d %H:%M:%S'),product,source,line,station,
                              self.DorN()=="D" and "B" or "Y",equipment,result and "OK" or "NG",process)

    def GetLcrK(self, LCR: cLcr):
        testItemList = []
        self.Relay1 = 1 << 2 | 1 << 3
        time.sleep(0.2)
        if self.Relay1 is not self.relay1:
            self.RecordLoadMessage('继电器切换超时', 'red', 0, False)
            self.isAlarm = True
            return False, None
        Result, Ltx = LCR.GetLs()
        Result, Rtx = LCR.Read_LSRS()
        if not Result:
            self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            self.isAlarm = True
            return False, None

        self.Relay1 = 1 << 0 | 1 << 1
        time.sleep(0.2)
        if self.Relay1 is not self.relay1:
            self.RecordLoadMessage('继电器切换超时', 'red', 0, False)
            self.isAlarm = True
            return False, None
        Result, Lrx = LCR.GetLs()
        Result, Rrx = LCR.Read_LSRS()
        if not Result:
            self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            self.isAlarm = True
            return False, None

        self.Relay1 = 1 << 2 | 1 << 7
        self.Relay2 = 1 << 0
        time.sleep(0.2)
        if self.Relay1 is not self.relay1 or self.Relay2 is not self.relay2:
            self.RecordLoadMessage('继电器切换超时', 'red', 0, False)
            self.isAlarm = True
            return False, None
        Result, L24 = LCR.GetLs()
        Result, R24 = LCR.Read_LSRS()
        if not Result:
            self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            self.isAlarm = True
            return False, None

        self.Relay1 = 1 << 0 | 1 << 2
        self.Relay2 = 1 << 1
        time.sleep(0.2)
        if self.Relay1 is not self.relay1 or self.Relay2 is not self.relay2:
            self.RecordLoadMessage('继电器切换超时', 'red', 0, False)
            self.isAlarm = True
            return False, None
        Result, L23 = LCR.GetLs()
        Result, R23 = LCR.Read_LSRS()
        if not Result:
            self.RecordLoadMessage('读取LCR数据失败', 'red', 0, False)
            self.isAlarm = True
            return False, None

        K = abs(L23 - L24) / (4 * math.sqrt(Ltx * Lrx))
        Kr = abs(R23 - R24) / (4 * math.sqrt(Rtx * Rrx))

        tmpTestitem: cTestItem = cTestItem()

        tmpTestitem.TestName = "k"
        tmpTestitem.TestValue = K
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "Ltx"
        tmpTestitem.TestValue = Ltx
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "Lrx"
        tmpTestitem.TestValue = Lrx
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "L24"
        tmpTestitem.TestValue = L24
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "L23"
        tmpTestitem.TestValue = L23
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "kr"
        tmpTestitem.TestValue = Kr
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "Rtx"
        tmpTestitem.TestValue = Rtx
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "Rrx"
        tmpTestitem.TestValue = Rrx
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "R24"
        tmpTestitem.TestValue = R24
        testItemList.append(tmpTestitem.Clone())

        tmpTestitem.TestName = "R23"
        tmpTestitem.TestValue = R23
        testItemList.append(tmpTestitem.Clone())

        print("K={0} Ltx={1} Lrx={2} L23={3} L24={4} Kr={5} Rtx={6} Rrx={7} R23={8} R24={9}".format
              (str(K), str(Ltx), str(Lrx), str(L23), str(L24), str(Kr), str(Rtx), str(Rrx), str(R23), str(R24)))
        return True, testItemList
        pass

    def CompleteLoaction(self, Axis, Value):
        try:
            if len(Axis) < 5 or len(Value) < 5:
                return False, 0.0

            p_array = numpy.polyfit(Axis, Value, 2)
            p1 = p_array[0]
            p2 = p_array[1]
            p3 = p_array[2]
            peak_location = round((-1 * p2) / (p1 * 2), 3)
            return True, peak_location

        except Exception as E:
            self.RecordLoadMessage('计算失败' + str(E), 'red', 0, False)
            return False, 0.0

    def RecordtestItem(self, Name, Value,testUp="-",testLow="-"):
        tmpTestitem: cTestItem = cTestItem()
        tmpTestitem.TestName = Name
        tmpTestitem.TestUpLimit = testUp
        tmpTestitem.TestLowLimit=testLow
        tmpTestitem.TestValue = Value
        tmpTestitem.TestResult = True
        self.testAllItem.append(tmpTestitem.Clone())

    def CheckTestItemLargeSignal(self, FreeOrKnom, TestItemList, rs_temp_offset:float = 0.0):
        # <editor-fold desc="测试LIMIT">
        FREE_UP = []
        FREE_LOW = []
        KNOM_UP = []
        KNOM_LOW = []

        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G1_L_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G1_L_Low]))
        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G1_R_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G1_R_Low]))

        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G2_L_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G2_L_Low]))
        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G2_R_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G2_R_Low]))

        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G3_L_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G3_L_Low]))
        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G3_R_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G3_R_Low]))

        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G4_L_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G4_L_Low]))
        FREE_UP.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G4_R_High]))
        FREE_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_FREE][self.Limitkey.KEY_G4_R_Low]))

        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G1_L_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G1_L_Low]))
        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G1_R_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G1_R_Low]))

        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G2_L_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G2_L_Low]))
        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G2_R_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G2_R_Low]))

        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G3_L_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G3_L_Low]))
        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G3_R_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G3_R_Low]))

        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G4_L_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G4_L_Low]))
        KNOM_UP.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G4_R_High]))
        KNOM_LOW.append(float(self.LimitDIC[self.Limitkey.SEC_KNOM][self.Limitkey.KEY_G4_R_Low]))

        #Osc_Up = float(self.OscLimitDic[self.OscLimitKey.SEC_OSC][self.OscLimitKey.KEY_UP])
        #Osc_Low = float(self.OscLimitDic[self.OscLimitKey.SEC_OSC][self.OscLimitKey.KEY_LOW])
        # </editor-fold>

        # <editor-fold desc="测试项目名称">
        FREE_L_ITEM_NAME = []
        FREE_Q_ITEM_NAME = []
        FREE_R_ITEM_NAME = []

        KNOM_L_ITEM_NAME = []
        KNOM_Q_ITEM_NAME = []
        KNOM_R_ITEM_NAME = []
        for key, value in self.testItemName.ConfigureDic["NAME"].items():
            if 'free' in key:
                if 'ltx' in key:
                    FREE_L_ITEM_NAME.append(value)
                if 'qtx' in key:
                    FREE_Q_ITEM_NAME.append(value)
                if 'rtx' in key:
                    FREE_R_ITEM_NAME.append(value)
            if 'knom' in key:
                if 'ltx' in key:
                    KNOM_L_ITEM_NAME.append(value)
                if 'qtx' in key:
                    KNOM_Q_ITEM_NAME.append(value)
                if 'rtx' in key:
                    KNOM_R_ITEM_NAME.append(value)

        # </editor-fold>
        index = 0
        index_l = 0
        index_q = 0
        index_r = 0
        for num in TestItemList:
            tmpdata: cTestItem = num
            # tmpdata.TestName = testName + "-" + tmpdata.TestName
            tmpdata.TestValue = round(float(tmpdata.TestValue), 4)

            if "ltx" in tmpdata.TestName.lower() or "rtx" in tmpdata.TestName.lower():
                if FreeOrKnom == "free":
                    tmpdata.TestResult = tmpdata.TestValue >= FREE_LOW[index] and tmpdata.TestValue <= FREE_UP[index]
                    if 'ltx' in tmpdata.TestName.lower():
                        tmpdata.TestName = FREE_L_ITEM_NAME[index_l]
                        index_l += 1
                    elif 'rtx' in tmpdata.TestName.lower():
                        tmpdata.TestName = FREE_R_ITEM_NAME[index_r]
                        index_r += 1
                        tmpdata.TestValue = float(tmpdata.TestValue) + rs_temp_offset
                        tmpdata.TestResult = tmpdata.TestValue >= FREE_LOW[index] and tmpdata.TestValue <= FREE_UP[index]
                    tmpdata.TestUpLimit = FREE_UP[index]
                    tmpdata.TestLowLimit = FREE_LOW[index]
                elif FreeOrKnom == "knom":
                    tmpdata.TestResult = tmpdata.TestValue >= KNOM_LOW[index] and tmpdata.TestValue <= KNOM_UP[index]
                    if 'ltx' in tmpdata.TestName.lower():
                        tmpdata.TestName = KNOM_L_ITEM_NAME[index_l]
                        index_l += 1
                    elif 'rtx' in tmpdata.TestName.lower():
                        tmpdata.TestName = KNOM_R_ITEM_NAME[index_r]
                        index_r += 1
                    tmpdata.TestUpLimit = KNOM_UP[index]
                    tmpdata.TestLowLimit = KNOM_LOW[index]
                index += 1
            else:
                tmpdata.TestResult = True
                tmpdata.TestUpLimit = "NA"
                tmpdata.TestLowLimit = "NA"
                if FreeOrKnom == "free":
                    tmpdata.TestName = FREE_Q_ITEM_NAME[index_q]
                    index_q += 1
                elif FreeOrKnom == "knom":
                    tmpdata.TestName = KNOM_Q_ITEM_NAME[index_q]
                    index_q += 1
                elif 'osc' in FreeOrKnom:
                    tmpdata.TestName = FreeOrKnom + tmpdata.TestName

            self.TestResult &= tmpdata.TestResult

            # tmpdata.TestUnit = ("-L" in tmpdata.TestName) and "uH" or ("-R" in tmpdata.TestName) and "mohm" or "NA"
            GlobalGui.global_Gui.tableWidgetEmit(tmpdata.TestName, str(tmpdata.TestLowLimit), str(tmpdata.TestUpLimit),
                                                 str(tmpdata.TestValue), tmpdata.TestResult, tmpdata.TestUnit)
            self.testAllItem.append(tmpdata.Clone())

    def CheckTestItem(self, testName, TestItemList):
        for num in TestItemList:
            tmpdata: cTestItem = num
            tmpdata.TestName = testName + "-" + tmpdata.TestName
            tmpdata.TestValue = round(float(tmpdata.TestValue), 4)

            if tmpdata.TestName.lower() in self.LimitDIC["UP"] and tmpdata.TestName.lower() in self.LimitDIC["LOW"]:
                UP = float(self.LimitDIC["UP"][tmpdata.TestName.lower()])
                LOW = float(self.LimitDIC["LOW"][tmpdata.TestName.lower()])
                tmpdata.TestResult = tmpdata.TestValue >= LOW and tmpdata.TestValue <= UP
                if "-kr" in tmpdata.TestName:
                    tmpdata.TestResult=True
                tmpdata.TestUpLimit = UP
                tmpdata.TestLowLimit = LOW
            else:
                tmpdata.TestResult = True
                tmpdata.TestUpLimit = "NA"
                tmpdata.TestLowLimit = "NA"
            self.TestResult &= tmpdata.TestResult

            tmpdata.TestUnit = ("-L" in tmpdata.TestName) and "uH" or ("-R" in tmpdata.TestName) and "mohm" or "NA"
            GlobalGui.global_Gui.tableWidgetEmit(tmpdata.TestName, str(tmpdata.TestLowLimit), str(tmpdata.TestUpLimit),
                                                 str(tmpdata.TestValue), tmpdata.TestResult, tmpdata.TestUnit)
            self.testAllItem.append(tmpdata.Clone())

    def ReadIo(self, mcu: cMcu):
        # sendData = [self.Cylinder, self.LedY, self.LedR, self.LedG, self.FMQ, self.XZK, self.FS, self.YL, self.Relay1,
        #             self.Relay2]
        try:
            sendData = [self.Cylinder, self.LedY, self.LedR, self.LedG, self.FMQ, self.XZK, self.FS, self.YL,
                        self.Relay1, self.Relay2, self.Y10, self.Y11, self.Y12, self.Y13, self.Y14, self.Y15, self.Y16,
                        self.Y17]
            result, Recive = mcu.WriteAndReadXY(sendData)#mcu.WriteAndReadIO(sendData)
            if not result: return False
            self.start1 = Recive[0]
            self.start2 = Recive[1]
            self.Alarm = Recive[2]
            self.begin = Recive[3]
            self.end = Recive[4]
            self.air = Recive[5]
            self.door = Recive[6]
            self.YLint = Recive[7]
            self.relay1 = Recive[8]
            self.relay2 = Recive[9]
            # if len(Recive) <= 10:
            #     return True
            self.X11 = Recive[10]
            self.X12 = Recive[11]
            self.X13 = Recive[12]
            self.X14 = Recive[13]
            self.X15 = Recive[14]
            self.X16 = Recive[15]
            self.X17 = Recive[16]
            self.X18 = Recive[17]
            return True
        except Exception as e:
            self.RecordLoadMessage('读取IO信息失败' + str(e), 'red', 0, False)
            return False

    def munaRobot(self, x, y, z, u, v, w):
        try:
            robot_2001: cRobot = self.devIns.Devices(Macro.ROBOT_2001)
            if robot_2001 is None:
                GlobalGui.global_Gui.TextBrowserSignal.emit('Robot-2001 获取失败，请检查后重启软件!', 'red', False)
                return False
            return robot_2001.Move(x, y, z, u, v, w)
        except Exception as e:
            print(e)
            return False

    def McuControl(self, key, value):
        try:
            MCU: cMcu = self.devIns.Devices(Macro.MCU)
            if MCU is None:
                GlobalGui.global_Gui.TextBrowserSignal.emit('MCU 获取失败，请检查后重启软件!', 'red', False)
                return False

            if key in "Cylinder":
                self.Cylinder = value
            if key in "LedY":
                self.LedY = value
            if key in "LedR":
                self.LedR = value
            if key in "LedG":
                self.LedG = value
            if key in "FMQ":
                self.FMQ = value
            if key in "XZK":
                self.XZK = value
            if key in "YL":
                self.YL = value
            if key in "FS":
                self.FS = value
            return True
        except Exception as e:
            print(e)
            return False

    def McuRead(self, key):
        try:
            MCU: cMcu = self.devIns.Devices(Macro.MCU)
            self.CollectMCU()
            if MCU is None:
                GlobalGui.global_Gui.TextBrowserSignal.emit('MCU 获取失败，请检查后重启软件!', 'red', False)
                return 0
            if key in self.McuIntDic.keys():
                return self.McuIntDic[key]
            return 0
        except Exception as e:
            print(e)
            return 0

    def RecordtestCount(self, total, Pass, Fail):
        tmpTotal = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total))
        tmpPass = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass))
        tmpFail = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail))

        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total, str(tmpTotal + total))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail, str(tmpFail + Fail))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass, str(tmpPass + Pass))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Yield,
                                   str(round((tmpPass + Pass) * 100 / (tmpTotal + total), 3)))

        GlobalGui.global_Gui.leTotalSignal.emit(str(tmpTotal + total))
        GlobalGui.global_Gui.lePassSignal.emit(str(tmpPass + Pass))
        GlobalGui.global_Gui.leFailSignal.emit(str(tmpFail + Fail))
        GlobalGui.global_Gui.leYieldSignal.emit(str(round((tmpPass + Pass) * 100 / (tmpTotal + total), 3)))
        pass

    def RecordLoadMessage(self, msg, color, writeType, clear):
        try:
            GlobalGui.global_Gui.TextBrowserSignal.emit(msg, color, clear)

            #  writeType != 1,2,3,4不写
            if writeType == Macro.INFO:  # info == 1
                self.txtLog.writeInfo(msg)
            elif writeType == Macro.DEBUG:  # debug == 2
                self.txtLog.writeDebug(msg)
            elif writeType == Macro.WARNING:  # warning == 3
                self.txtLog.writeWarning(msg)
            elif writeType == Macro.ERROR:  # error == 3
                self.txtLog.writeError(msg)
            pass
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit('写log错误 - ' + str(e), 'red', False)

    def GetCoil(self,sn):
        enable = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CoilConfigEnable]=="Y"

        if not enable:
            return True,"NA","NA","NA"
        self.MACHINE_TYPE = self.Configure.ReadValue(self.Configurekey.SEC_MACHINE, self.Configurekey.KEY_TYPR)

        if self.MACHINE_TYPE == Macro.TYPE_5XX:
            result, CoilSN = self.trace.McegGetCoilConfig_5xx(sn)
        else:
            result, CoilSN = self.trace.McegGetCoilConfig(sn)


        if not result or CoilSN =="":
            return False,"NA","NA","NA"

        coilVendor="NA"
        coilFerrite="NA"

        for num in self.CoilFerrite.keys():
            if num ==CoilSN[-1]:
                coilFerrite=self.CoilFerrite[num]
                break

        for num in self.CoilVendor.keys():
            if num ==CoilSN[-2]:
                coilVendor=self.CoilVendor[num]
                break

        return True,CoilSN,coilVendor,coilFerrite

    CoilFerrite = {}
    CoilVendor = {}

    def ReadCoilMessage(self):
        self.CoilFerrite.clear()
        self.CoilVendor.clear()

        CoilFerrite = self.readFile("E:\Configure\CoilFerrite.txt").split("\n")
        CoilVendor = self.readFile("E:\Configure\CoilVendor.txt").split("\n")

        for num in CoilFerrite:
            tmpdata = num.split("-")
            if len(tmpdata) < 2:
                continue
            self.CoilFerrite[tmpdata[0]] = tmpdata[1]

        for num in CoilVendor:
            tmpdata = num.split("-")
            if len(tmpdata) < 2:
                continue
            self.CoilVendor[tmpdata[0]] = tmpdata[1]

    def readFile(self, fileName):
        with open(fileName, 'r') as f:
            return f.read()

    def McegJson(self,barcode,Time,testTime,testresult:bool,TestResult):
        jsonDic:dict= dict()
        jsonDic["pid"]=barcode
        tmp = timedelta( days=0, hours=8, minutes=0, seconds=0)
        jsonDic["time"]=(Time-tmp).strftime( '%Y-%m-%dT%H:%M:%SZ')
        jsonDic["pass"]=testresult
        tmpTestitem:dict=dict()
        Tmp:dict=dict()
        Tmp["Project"]=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Project]
        Tmp["station_id"]=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_station_id]
        Tmp["Model"]=""
        Tmp["Color"]=""
        Tmp["TestMode"]=""
        Tmp["fixture_id"]="0"
        Tmp["Vehicle"]=""
        Tmp["line_id"]=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_line_id]
        Tmp["machineNo"]=""
        Tmp["Test time"]=str(round(testTime,2))
        Tmp["Config"]=""

        for num in TestResult:
            item:cTestItem=num
            if item.TestLowLimit is "-" : continue
            itemName=item.TestName
            value=round(float(item.TestValue),4)
            Tmp[itemName]=value

        tmpTestitem["results"]=Tmp
        jsonDic["data"] = tmpTestitem

        path=self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_UploadPath]
        if not os.path.exists( path ):
            os.makedirs( path )

        fileName=str.format("{0}\\{1}_{2}.json",path,Time.strftime('%Y-%m-%d-%H-%M-%S'),barcode)
        with open( fileName, 'w' ) as write_f:
            write_f.write( json.dumps( jsonDic, indent=4, ensure_ascii=False ) )
        pass

    def JPJson(self, barcode, Time, testTime, color, model, testresult: bool, TestResult):
        jsonDic: dict = dict()
        jsonDic["pid"] = barcode
        tmp = timedelta(days=0, hours=8, minutes=0, seconds=0)
        jsonDic["time"] = (Time - tmp).strftime('%Y-%m-%dT%H:%M:%SZ')
        jsonDic["pass"] = testresult
        tmpTestitem: dict = dict()
        Tmp: dict = dict()
        Tmp["project"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Project]
        Tmp["model"] = model
        Tmp["color"] = color
        Tmp["process"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_process]
        Tmp["machine"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_machine]
        Tmp["line"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_line_id]
        Tmp["test time"] = str(round(testTime, 2))

        defet = ""
        for num in TestResult:
            item: cTestItem = num
            if item.TestLowLimit is "-": continue
            itemName = item.TestName
            value = round(float(item.TestValue), 4)
            Tmp[itemName] = value
            if item.TestResult is False:
                defet = defet + item.TestName + ","

        Tmp["defect"] = defet
        tmpTestitem["results"] = Tmp
        jsonDic["data"] = tmpTestitem

        path = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_UploadPath]
        if not os.path.exists(path):
            os.makedirs(path)

        fileName = str.format("{0}\\{1}_{2}.json", path, Time.strftime('%Y-%m-%d-%H-%M-%S'), barcode)
        with open(fileName, 'w') as write_f:
            write_f.write(json.dumps(jsonDic, indent=4, ensure_ascii=False))
        pass

    def JPJson_2(self, barcode, Time, testTime, color, model, testresult: bool, TestResult, coilsn):
        jsonDic: dict = dict()
        jsonDic["pid"] = barcode
        tmp = timedelta(days=0, hours=8, minutes=0, seconds=0)
        jsonDic["time"] = (Time - tmp).strftime('%Y-%m-%dT%H:%M:%SZ')
        jsonDic["pass"] = testresult
        tmpTestitem: dict = dict()
        Tmp: dict = dict()
        Tmp["test_result"] = testresult and "pass" or "fail"
        Tmp["project"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Project]
        Tmp["model"] = model
        Tmp["color"] = color
        Tmp["process"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_process]
        Tmp["machine"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_machine]
        Tmp["line_id"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_line_id]
        Tmp["CT"] = str(round(testTime, 2))
        Tmp["AIM status"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_DeBugTime]
        Tmp["HSG Config"] = self.ConfigM
        Tmp["Coil sn"] = coilsn
        Tmp["station_id"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_station_id]
        Tmp["cavity_id"] = "1"
        Tmp["uut_start"] = Time.strftime('%Y-%m-%d %H:%M:%S')
        Tmp["uut_stop"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Tmp["software_name"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_soft_name]
        Tmp["software_version"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_Version]
        Tmp["calibration_hsg"] = "N"
        Tmp["last_calibration_time"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_CheckTime]
        Tmp["last_calibration_hsg_no"] = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_GoldenSN]
        Tmp["station_vendor"] = "GTS"

        defet = ""
        for num in TestResult:
            item: cTestItem = num
            if item.TestLowLimit is "-": continue
            itemName = item.TestName
            value = round(float(item.TestValue), 4)
            Tmp[itemName] = value
            if item.TestResult is False:
                defet = defet + item.TestName + ","
                diff = abs(float(item.TestUpLimit) - float(item.TestLowLimit))
                testDiff = value < float(item.TestLowLimit) and abs(value - float(item.TestLowLimit)) or abs(
                    value - float(item.TestUpLimit))
                if testDiff > diff * 2:
                    self.RecordLoadMessage("测试数据异常 超出两倍公差带 数据不上传 ", 'red', 0, False)
                    return

        Tmp["Defect"] = defet

        tmpTestitem["properties"] = {"Defect": defet}
        tmpTestitem["results"] = Tmp
        jsonDic["data"] = tmpTestitem

        path = self.ConfigureDIC[self.Configurekey.SEC_APP][self.Configurekey.SEC_UploadPath]
        if not os.path.exists(path):
            os.makedirs(path)

        fileName = str.format("{0}\\{1}_{2}.json", path, Time.strftime('%Y-%m-%d-%H-%M-%S'), barcode)
        with open(fileName, 'w') as write_f:
            write_f.write(json.dumps(jsonDic, indent=4, ensure_ascii=False))
        pass

    def Abort(self):
        self.isAbort = True
        if self.DetectThread != None:
            self.DetectThread.join()

        robot_2002: cRobot = self.devIns.Devices(Macro.ROBOT_2002)
        if robot_2002 != None:
            robot_2002.Write(robot_2002.Stop)
            time.sleep(0.5)
            robot_2002.Write(robot_2002.Logout)
            time.sleep(0.5)

        for device in self.devIns.ALLDevices().values():
            if device is not None:
                device.Close()
            print("关闭")

if __name__ == '__main__':
    tempitem = cTestItem()
    tempitem.TestValue = 5
    if tempitem.TestValue > 3:
        print(True)
    else:
        print(False)