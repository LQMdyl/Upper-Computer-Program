import csv
import os.path
import time
import threading
from GlobalDir import GlobalConf
from ConfigureDir import ConfigureKey
from ConfigureDir.Counter import cCounter
from ConfigureDir import CounterKey
from ConfigureDir.Configure import cConfigure
from ConfigureDir.Configure import cUseCount
from DeviceDir.DeviceManager import cDeviceManager
from GlobalDir.GlobalGui import global_Gui
from LogDir.AllLog import cFileLog
from DeviceDir.CCD import Camera
from DeviceDir.Modbusclient import cModbusclient
from DeviceDir.WorkerIntegra import cWorkerIntegra
from DeviceDir.Scan import cScan
from datetime import datetime
from datetime import timedelta
from Mes.Mes import cMes
from TestDir.TestItem import cTestItem
import cv2
import guid


class cTestEngine():
    # <editor-fold desc="PLC定义">
    PLC_Emergency_Alarm = False  # 紧急停止
    PLC_SafeRaster_Alarm = False  # 安全光幕
    PLC_ThreeNG_Alarm = False #3次NG
    PLC_Negative_Alarm1 = False # 负压表1
    PLC_Negative_Alarm2 = False  # 负压表2
    PLC_Test_SafeRaster_Alarm = False #自动测试中安全光幕
    # </editor-fold>
    def __init__(self):
        self.isAbort = False
        self.barcode = ''
        self.Configure = cConfigure()
        self.useCount = cUseCount()
        self.counterIns = cCounter()
        self.counterKey = CounterKey
        self.devIns = cDeviceManager()
        self.Configurekey = ConfigureKey
        self.DetectThread: threading.Thread = None
        self.Mstart = False
        self.StartFlageEnable = False
        self.SafeDoorEnable = False
        self.TestModel = "OP"
        self.OpID = ''
        self.mes = cMes()
        self.barcodeM = ''
        self.localIP = ''
        self.isSample = False
        self.plc = cModbusclient(GlobalConf.PLC)
        self.camera = Camera()
        self.scan = cScan(GlobalConf.SCAN)
        self.findCamera = None
        self.workerIntegra = cWorkerIntegra(GlobalConf.WORKER_INTEGRA)
        self.testResultAlarm = []
        #self.runlog = cTxtLog('testlog')
        self.machine = ''
        self.zeroCount = 0
        self.checkStartTimeD = datetime.now()
        self.checkEndTimeD = datetime.now()
        self.DayOrNight= 'D'

    testAllItem = []
    def Initialize(self):
        try:
            #self.loadGoldentestData("/vault/Configure/点检数据.csv")
            isConnect = True
            #num=self.GoldenTestData
            #self.LimitDIC = self.Limit.ConfigureDic
            self.CollectPLC()
            time.sleep(1)  # 1s
            global_Gui.tbvwLogEmit('清除界面', 'black', True)
            global_Gui.tbvwLogEmit('开始初始化......', 'black', False)
            global_Gui.tbvwLogEmit('Start initialization......', 'black', False)
            global_Gui.tbvwLogEmit('登录工号为：'+self.OpID, 'blue', False)

            self.CheckCnt = self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_CHECK_CNT]

            self.checkStartTimeD = datetime.strptime(
                datetime.now().date().strftime('%Y%m%d ') +
                self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_CHECK_START_TIME],
                '%Y%m%d %H:%M:%S')
            self.checkEndTimeD = self.checkStartTimeD + timedelta(hours=12)

            checkDate = str(
                self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_CHECKED]).split('_')
            if len(checkDate) < 2:
                self.isSample = False
            else:
                datepa = datetime.strptime(checkDate[0], '%Y%m%d')
                if self.checkStartTimeD <= datetime.now() < self.checkEndTimeD:
                    self.DayOrNight = 'D'
                    self.isSample = False
                    if datepa.date() == datetime.now().date():
                        self.isSample = True
                else:
                    self.DayOrNight = 'N'
                    self.isSample = False
                    if datepa.date() == datetime.now().date():
                        if checkDate[1] == 'N':
                            self.isSample = True
                    elif (datepa + timedelta(days=1)).date() == datetime.now().date():
                        if checkDate[1] == 'N' and datetime.now() < self.checkStartTimeD:
                            self.isSample = True
            #self.updateCheckTime()
            global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, False)
            global_Gui.lblDeviceStatusEmit(GlobalConf.WORKER_INTEGRA, False)
            global_Gui.lblDeviceStatusEmit(GlobalConf.PLC, False)

            if not self.CheckAppConfigures():
                global_Gui.tbvwLogEmit( '配置文件有缺失，请手动配置缺少项目', 'red', False )
                return

            if not self.InitializeCounter():
                global_Gui.tbvwLogEmit('读取 Counter 文件失败', 'red', False)
                return

            self.useCount.loadConfigure()

            self.localIP = self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_HOST_IP]
            global_Gui.tbvwLogEmit('当前机器的IP地址：' + self.localIP, 'black', False)
            version=self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_VERSION]
            global_Gui.tbvwLogEmit('当前软件版本：'+version, 'black',False)

            time.sleep(0.3)
            global_Gui.testStatusEmit(GlobalConf.statusIdel)
            if str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_SCAN_TYPE] != 'A'):
                global_Gui.tbvwLogEmit('当前已开启手动扫码，无需连接扫码枪' , 'black', False)
                isConnect = True
            global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, isConnect)
            isConnect &= self.devIns.InitializeDevice()
            if not isConnect:
                global_Gui.tbvwLogEmit('连接失败，请检查后重新连接!', 'red', False)
                global_Gui.tbvwLogEmit('The connection failed. Please connect again!', 'red',False)
                return

            self.isAbort = False
            self.isTesting = False
            self.StartTime = datetime.now()
            self.StartDetectTask()
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), 'red', False)

    def TestFunction(self):
        try:
            global_Gui.testStatusEmit(GlobalConf.statusTest)
            global_Gui.waitTimeEmit()
            self.testAllItem.clear()
            self.isTesting = True
            self.TestResult = False
            self.isAlarm = False
            self.StartTime = datetime.now()
            self.nozzleCount = int(self.useCount.UseCountDic[ConfigureKey.SEC_USE_COUNT][ConfigureKey.KEY_NOZZLE])
            self.alarmCount = int(self.Configure.ConfigureDic[ConfigureKey.SEC_ALARM][ConfigureKey.KEY_ALARM_COUNT])
            self.workerIntegra: cWorkerIntegra = self.devIns.Devices(GlobalConf.WORKER_INTEGRA)
            self.scan: cScan = self.devIns.Devices(GlobalConf.SCAN)
            global_Gui.clearTestData()
            global_Gui.tbvwLogEmit('清除界面', 'black', True)
            global_Gui.tbvwLogEmit('开始测试', 'black', False)
            #global_Gui.tbvwLogEmit('当前测试模式：' + self.TestModel, 'blue', False)

            checkBarcode = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_CHECK_BARCODE]) == 'Y'
            barcodeLenth = int(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_BARCODE_CNT])
            debug = True
            if self.nozzleCount >= self.alarmCount:
                global_Gui.showMsgBox('警告', '吸嘴使用次数已达上限，请联系技术员或工程师进行更换')
                global_Gui.lockEngine()
                self.isAlarm = True
            else:
                self.nozzleCount += 1
                self.useCount.saveConfigure(ConfigureKey.SEC_USE_COUNT, ConfigureKey.KEY_NOZZLE, str(self.nozzleCount))
            if self.isAlarm:
                global_Gui.testStatusEmit(GlobalConf.statusError)
                self.writeTestFinish()
                return

            #<扫码>
            autoscan = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_SCAN_TYPE]) == 'A'
            if autoscan:
                ret, barcode = self.scan.GetBarcode(5)
                if not ret:
                    global_Gui.tbvwLogEmit('获取扫码结果失败', GlobalConf.colorRed)
                    self.isAlarm = True
                if self.isAlarm:
                    global_Gui.testStatusEmit(GlobalConf.statusError)
                    self.writeTestFinish()
                    return
                barcode = str(barcode).replace('\r', '')
                self.barcode = barcode
                if self.barcode == '' or self.barcode.__contains__('No Barcode'):
                    global_Gui.tbvwLogEmit('扫码失败', GlobalConf.colorRed)
                    self.isAlarm = True
            else:
                #手动扫码
                pass
            if checkBarcode:
                if len(self.barcode) != barcodeLenth:
                    global_Gui.tbvwLogEmit(f'条码不符合规定的长度{str(barcodeLenth)}', GlobalConf.colorRed)
                    self.isTesting = False
                    self.isAlarm = True

            global_Gui.barcodeScan(self.barcode)

            if self.isAlarm:
                global_Gui.testStatusEmit(GlobalConf.statusFail)
                self.writeTestFinish()
                return
            #</扫码>
            # if self.TestModel == 'DOE':
            #     self.isTesting = False

            #<判断是否需要点检>
            # goldenTest = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_GOLDEN_TEST]) != 'Y'
            # if goldenTest:
            #     self.IsCheckTimeEnable = False
            #     self.isSample = True
            # </判断是否需要点检>

            self.machine = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_MACHINE])
            if self.machine == 'MFLEX':
                ProcessControl = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROCESS_CONTROL]) == "Y"
                self.mes.ApiAddress = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_ADDRESS])
                self.mes.ApiPath = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_PRE_PATH])
                self.mes.Barcode = self.barcode
                self.mes.OperatorID = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_OPERATOR])
                self.mes.ToolNumber = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TOOL_NUMBER])
                self.mes.TestType = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TEST_TYPE])
                self.mes.PreviousTestType = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PREVIOUS_TEST_TYPE])
                self.mes.ProductName = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PRODUCT_NAME])
                self.mes.WorkArea = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_WORK_AREA])
                self.mes.Site = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_SITE])
                self.mes.Program = str(
                    self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROGRAM])
                self.mes.Lot = str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_SITE])
                self.mes.IpAddress = self.localIP
                self.mes.StationTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if ProcessControl and self.isTesting:
                    responbody = self.mes.SnCheck(self.barcode)
                    if responbody is None or not responbody.isOk:
                        global_Gui.tbvwLogEmit('SN检查失败' + responbody.erroMessage, 'red', False)
                        self.TestResult = False
                        self.isAlarm = True
                    else:
                        #dirName = r'\\OT-MFCISILON02.mflex.com.cn\OneFS\ETLocalbackup2021\MES_check''\\'
                        dirName = str(self.Configure.ConfigureDic[self.Configurekey.SEC_MES][self.Configurekey.KEY_PROCESS_URL])
                        if len(dirName) > 3 and (not dirName.endswith('\\') or dirName.endswith('/')):
                            dirName += '\\'
                        dirName += self.mes.ProductName
                        log = cFileLog(dirName)
                        endTime = datetime.now()
                        testTime = self.StartTime - endTime
                        log.mesCsvLog(self.barcode, testTime.microseconds / 1000, self.mes.Result.isSuccess,
                                      self.mes.Result.extensionCode, self.mes.Result.message,
                                      self.mes.ProductName, self.mes.ToolNumber, self.localIP,
                                      self.mes.TestType, self.mes.Program, self.StartTime, endTime)
                        global_Gui.tbvwLogEmit(
                            '卡站结果:{0}'.format(self.mes.Result.isSuccess == True and 'PASS' or 'FAIL'),
                            self.mes.Result.isSuccess and GlobalConf.colorGreen or GlobalConf.colorRed, False)
                    if self.mes.Result.extensionMessages.barcodeFamily != '1' and not self.isSample:
                        global_Gui.tbvwLogEmit('当前班次未进行点检，此次测试不被允许', GlobalConf.colorRed, False)
                        global_Gui.testStatusEmit(GlobalConf.statusFail)
                        self.isAlarm = True

            if self.isAlarm:
                global_Gui.testStatusEmit(GlobalConf.statusFail)
                self.writeTestFinish()
                return

            global_Gui.tbvwLogEmit('开始测试', GlobalConf.colorGreen,  False)
            testDelay = int(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_DELAY])
            tmpResult, tmpTestItem = self.workerIntegra.writeAndRead(testDelay)
            if not tmpResult:
                global_Gui.tbvwLogEmit('测试失败，无法获取测试信息', GlobalConf.colorRed,  False)
                global_Gui.testStatusEmit(GlobalConf.statusFail)
                self.isAlarm = True
            if self.isAlarm:
                global_Gui.testStatusEmit(GlobalConf.statusFail)
                self.writeTestFinish()
                return
            self.TestResult = tmpTestItem.TestResult
            if self.str2float(tmpTestItem.TestValue) == 0.0:
                self.zeroCount += 1
            else:
                self.zeroCount = 0
            if self.zeroCount >= 5:
                global_Gui.showMsgBox('警告', '连续5次出现测试值为0，请检查设备气孔是否被堵住')
                global_Gui.tbvwLogEmit('连续5次出现测试值为0，请检查设备气孔是否被堵住', GlobalConf.colorRed)
                self.zeroCount = 0
            self.testAllItem.append(tmpTestItem)
            self.showTestItem(tmpTestItem)
            endTime = datetime.now()

            if self.isTesting:
                if self.mes.Result.extensionMessages.barcodeFamily != '1':
                    uploadResult = self.mes.uploadMes(self.barcode, self.testAllItem, self.StartTime, endTime,
                                                      self.TestResult)
                    global_Gui.testStatusEmit(
                        (self.TestResult and uploadResult.isOk) and GlobalConf.statusPass or GlobalConf.statusFail)
                    if uploadResult.isOk:
                        global_Gui.tbvwLogEmit('上传成功', GlobalConf.colorGreen)
                    else:
                        global_Gui.tbvwLogEmit('上传失败:' + uploadResult.erroMessage, GlobalConf.colorRed)
                else:
                    failItem = self.TestResult and '' or 'MIC_TEST'
                    self.mes.SampleCompare(self.barcode, failItem, self.TestResult, endTime)
                    shift = self.checkStartTimeD <= endTime < self.checkEndTimeD and 'D' or 'N'
                    self.Configure.saveConfigure(self.Configurekey.SEC_APP, self.Configurekey.KEY_CHECKED,
                                                 endTime.strftime('%Y%m%d_') + shift)
                    self.isSample = True
                    global_Gui.testStatusEmit(self.TestResult and GlobalConf.statusPass or GlobalConf.statusFail)
            # 计数
            total = 1
            Pass = self.TestResult and 1 or 0
            Fail = not self.TestResult and 1 or 0
            self.RecordtestCount(total, Pass, Fail)

            if not self.isTesting:
                global_Gui.testStatusEmit(GlobalConf.statusError)
            self.writeTestFinish()
        except Exception as e:
            global_Gui.testStatusEmit(GlobalConf.statusError)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            self.writeTestFinish()
            self.isAlarm = True

    # def aaa(self, text, color,writeLvl: int, clear = False):
    #     try:
    #         global_Gui.tbvwLogEmit(text, color, clear)
    #         if writeLvl == 0:
    #             self.runlog.writeInfo(text)
    #         elif writeLvl == 1:
    #             self.runlog.writeDebug(text)
    #         elif writeLvl == 2:
    #             self.runlog.writeWarning(text)
    #         elif writeLvl == 3:
    #             self.runlog.writeError(text)
    #
    #     except Exception as e:
    #         global_Gui.tbvwLogEmit(str(e), 'red')


    def Abort(self):
        self.isAbort = True
        if self.DetectThread != None:
            self.DetectThread.join()

        for device in self.devIns.ALLDevices().values():
            if device is not None:
                device.Close()
            print("关闭")

    def StartDetectTask(self):
        try:
            if self.DetectThread != None and not self.DetectThread.is_alive():
                global_Gui.tbvwLogEmit('检测线程已运行，不能重复开启!', 'red', False)
                global_Gui.tbvwLogEmit('The detection thread is already running and cannot be opened repeatedly!',
                                       'red', False)
                return
            self.DetectThread = threading.Thread(target=self.DetectFunction, name='DetectFunction')
            self.DetectThread.start()
        except Exception as e:
            print(e)

    def DetectFunction(self):
        plc: cModbusclient = self.devIns.Devices(GlobalConf.PLC)
        if plc == None:
            global_Gui.tbvwLogEmit('获取PLC失败，请检查后重启软件', 'red', False)
            global_Gui.tbvwLogEmit('Failed to obtain PLC, please check and restart the software', 'red',
                                   False)

        Startflag = False
        while not self.isAbort:
            time.sleep(0.03)
            self.updateCheckTime()

            Startflag = self.readStartFlag()  # self.start1 is 0x01 and self.start2 is 0x01

            if Startflag and self.Mstart and not self.isTesting and self.Alarm != 0x01:
                global_Gui.tbvwLogEmit('获取开始测试信号成功', 'black', False)
                self.startTest()
                self.isAlarm = False
                self.Mstart = False
                self.TestThread = threading.Thread(target=self.TestFunction, name="Test")
                self.TestThread.start()

            if self.isTesting:
                Interval = datetime.now() - self.StartTime
                global_Gui.lbTestTimeEmit(str(round(Interval.total_seconds(), 2)))

    def readStartFlag(self):
        time.sleep(0.5)
        if not self.ReadPLCIo():
            global_Gui.tbvwLogEmit('获取PLC输入输出失败，请检查后重启软件', 'red')
            return False
        return True

    GoldenTestData = {}

    def loadGoldentestData(self, filepath):
        if not os.path.exists(filepath):
            global_Gui.tbvwLogEmit('不存在点检文件', 'red')
            return
        file = open(filepath, 'r')
        data = file.readlines()
        file.close()
        BT = data[0].split(",")
        Limit = data[1].split(',')

        for i in range(len(data)):
            if i <= 2: continue
            testdata = dict()
            tmpdata = data[i].split(',')
            Key = tmpdata[0]
            for j in range(len(tmpdata)):
                if j == 0:
                    continue
                tmplimit = Limit[j]
                if tmplimit == "NA":
                    continue
                testdata[BT[j].replace("\n", "")] = tmpdata[j].replace("\n", "")

            self.GoldenTestData[Key] = testdata

    def updateCheckTime(self):
        totalSeconds = 0.0
        if str(self.Configure.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_GOLDEN_TEST]) != 'Y':
            global_Gui.lbCheckTimeEmit("无需点检")
            #self.IsCheckTimeEnable = False
            self.isSample = True
            return
        if datetime.now().day != self.checkStartTimeD.day:
            self.checkStartTimeD += timedelta(days=1)
            self.checkEndTimeD += timedelta(days=1)

        if self.checkStartTimeD <= datetime.now() < self.checkEndTimeD:
            if self.DayOrNight != 'D':
                self.DayOrNight = 'D'
                self.isSample = False
            totalSeconds = (self.checkEndTimeD - datetime.now()).total_seconds()
        elif self.checkStartTimeD > datetime.now():
            totalSeconds = (self.checkStartTimeD - datetime.now()).total_seconds()
        elif self.checkEndTimeD <= datetime.now():
            if self.DayOrNight != 'N':
                self.DayOrNight = 'N'
                self.isSample = False
            totalSeconds = ((self.checkStartTimeD + timedelta(days=1)) - datetime.now()).total_seconds()

        if self.isSample:
            global_Gui.lbCheckTimeEmit("已点检")
            return
        hours = int(round(totalSeconds // 3600, 0))
        minutes = int(round(totalSeconds % 3600 // 60, 0))
        seconds = int(round(totalSeconds % 3600 % 60, 0))
        global_Gui.lbCheckTimeEmit("{0}:{1}:{2}".format(str(hours), str(minutes), str(seconds)))

    def CheckTestData(self,barcode):
        #if not self.IsCheckTimeEnable: return True

        if barcode not in self.GoldenTestData.keys():
            global_Gui.tbvwLogEmit( "点检时间到 无此条码点检数据！请检查点检csv是否配置", 'red', False )
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
                    global_Gui.tbvwLogEmit( "{0} 当前测试值：{1}  标准值{2}".format(tmpitem.TestName,tmpitem.TestValue,Checkdata[tmpitem.TestName]), 'red', False )
        if checkResult:
            global_Gui.tbvwLogEmit( "点检时间到 点检完成！", 'blue', False )
            self.Configure.saveConfigure(self.Configurekey.SEC_APP,self.Configurekey.KEY_CHECK_TIME,datetime.now().strftime( "%Y-%m-%d %H:%M" ))
            #self.CheckTime=datetime.now().strftime( "%Y-%m-%d %H:%M" )
            self.CheckCnt = 0
            self.Configure.saveConfigure(self.Configurekey.SEC_APP, self.Configurekey.KEY_CHECK_CNT, "0")
        else:
            self.CheckCnt += 1
            self.Configure.saveConfigure(self.Configurekey.SEC_APP, self.Configurekey.KEY_CHECK_CNT, str(self.CheckCnt))
            global_Gui.tbvwLogEmit( "点检时间到 点检失败！", 'red', False )

        return checkResult

    # def ReadMCUIo(self, mcu: cMcu):
    #     # sendData = [self.Cylinder, self.LedY, self.LedR, self.LedG, self.FMQ, self.XZK, self.FS, self.YL, self.Relay1,
    #     #             self.Relay2]
    #     try:
    #         sendData = [self.Cylinder, self.LedY, self.LedR, self.LedG, self.FMQ, self.XZK, self.FS, self.YL,
    #                     self.Relay1, self.Relay2, self.Y10, self.Y11, self.Y12, self.Y13, self.Y14, self.Y15, self.Y16,
    #                     self.Y17]
    #         result, Recive = mcu.WriteAndReadXY(sendData)#mcu.WriteAndReadIO(sendData)
    #         if not result: return False
    #         self.start1 = Recive[0]
    #         self.start2 = Recive[1]
    #         self.Alarm = Recive[2]
    #         self.begin = Recive[3]
    #         self.end = Recive[4]
    #         self.air = Recive[5]
    #         self.door = Recive[6]
    #         self.YLint = Recive[7]
    #         self.relay1 = Recive[8]
    #         self.relay2 = Recive[9]
    #         # if len(Recive) <= 10:
    #         #     return True
    #         self.X11 = Recive[10]
    #         self.X12 = Recive[11]
    #         self.X13 = Recive[12]
    #         self.X14 = Recive[13]
    #         self.X15 = Recive[14]
    #         self.X16 = Recive[15]
    #         self.X17 = Recive[16]
    #         self.X18 = Recive[17]
    #         return True
    #     except Exception as e:
    #         global_Gui.tbvwLogEmit('读取IO信息失败' + str(e), 'red', 0)
    #         return False
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
            global_Gui.tbvwLogEmit( "Open Camera ERROR-" + str( e ), GlobalConf.colorRed, False )
            return False

    PLC_AlarmDic = {}
    def CollectPLC(self):
        self.PLC_AlarmDic["PLC_Emergency_Alarm"] = self.PLC_Emergency_Alarm
        self.PLC_AlarmDic["PLC_SafeRaster_Alarm"] = self.PLC_SafeRaster_Alarm
        self.PLC_AlarmDic["PLC_ThreeNG_Alarm"] = self.PLC_ThreeNG_Alarm
        self.PLC_AlarmDic["PLC_Negative_Alarm1"] = self.PLC_Negative_Alarm1
        self.PLC_AlarmDic["PLC_Negative_Alarm2"] = self.PLC_Negative_Alarm2
        self.PLC_AlarmDic["PLC_Test_SafeRaster_Alarm"] = self.PLC_Test_SafeRaster_Alarm
    def ReadPLCIo(self):
        self.plc = self.devIns.Devices(GlobalConf.PLC)
        try:
            result, Recive = self.plc.Read_coils_msg()
            result1,startAble = self.plc.Read_Start()
            if not result or not result1: return False
            self.PLC_Emergency_Alarm = str(Recive[1]).upper() == 'TRUE'
            self.PLC_SafeRaster_Alarm = str(Recive[2]).upper() == 'TRUE'
            self.PLC_Test_SafeRaster_Alarm = str(Recive[3]).upper() == 'TRUE'
            self.PLC_Negative_Alarm1 = str(Recive[4]).upper() == 'TRUE'
            self.PLC_Negative_Alarm2 = str(Recive[5]).upper() == 'TRUE'

            alarm1 = False
            alarm2 = False
            alarm3 = False
            self.Alarm = 0x00

            if self.PLC_Emergency_Alarm:
                alarm1 = True
                global_Gui.tbvwLogEmit('紧急停止被按下', 'red')
                # self.showPLC_ALARM('紧急停止被按下')
            else:
                alarm1 = False

            if self.PLC_SafeRaster_Alarm:
                # self.isAlarm = True
                if self.isTesting:
                    global_Gui.tbvwLogEmit('安全光幕被遮挡', 'red')

            if self.PLC_Negative_Alarm1:
                alarm2 = True
                global_Gui.tbvwLogEmit('负压表1异常', 'red')
                # self.showPLC_ALARM('负压表1异常')
            else:
                alarm2 = False

            if self.PLC_Negative_Alarm2:
                alarm3 = True
                global_Gui.tbvwLogEmit('负压表2异常', 'red')
                # self.showPLC_ALARM('负压表2异常')
            else:
                alarm3 = False

            if self.PLC_Test_SafeRaster_Alarm:
                # self.isAlarm = True
                if self.isTesting:
                    global_Gui.tbvwLogEmit('安全光幕被遮挡', 'red')

            self.isAlarm = alarm1 | alarm2 | alarm3
            self.Alarm = self.isAlarm and 0x01 or 0x00

                # if self.PLC_ThreeNG_Alarm:
                #     self.Alarm = 0x01
                #     self.isAlarm = True
                #     global_Gui.tbvwLogEmit('产品已达到3次测试NG，请更换产品', 'red')
                # else:
                #     self.Alarm = 0x00

            if str(Recive[0]).upper() == 'TRUE' and startAble == 1:
                self.Mstart = True
            self.CollectPLC()
            return True
        except Exception as e:
            global_Gui.tbvwLogEmit('读取PLC信息失败' + str(e), 'red',False)
            return False

    def startTest(self):
        try:
            self.plc = self.devIns.Devices(GlobalConf.PLC)
            result = self.plc.Write_Hold_register(100,0)
            if result:
                global_Gui.tbvwLogEmit('写入PLC信息成功', 'green', False)
            else:
                global_Gui.tbvwLogEmit('写入PLC信息失败' , 'red', False)
        except Exception as e:
            global_Gui.tbvwLogEmit('写入PLC信息失败' + str(e), 'red', False)
    def writeTestFinish(self):
        plc: cModbusclient = self.devIns.Devices(GlobalConf.PLC)
        try:
            plc.Write_Hold_register(102, 1)
            self.isTesting = False
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red', False)
    def CheckAppConfigures(self):
        result = True
        for num in self.Configurekey.TotalAppKey:
            if num not in self.Configure.ConfigureDic[self.Configurekey.SEC_APP]:
                global_Gui.tbvwLogEmit( "配置文件缺少- " + num, 'red',False )
                result = False
        return result

    def InitializeCounter(self):
        try:
            tmpTotal = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total)
            tmpPass = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass)
            tmpFail = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail)
            tmpYield = self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Yield)
            global_Gui.updateTotal(tmpTotal)
            global_Gui.updatePass(tmpPass)
            global_Gui.updateFail(tmpFail)
            global_Gui.updateYield(tmpYield)
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), 'red',False)
            global_Gui.tbvwLogEmit('读取 Counter 计数文件失败', 'red', False)
            return False

    def ClearCounter(self):
        try:
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Total, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Fail, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Pass, str( 0 ) )
            self.counterIns.WriteValue( self.counterKey.SEC_CNT, self.counterKey.KEY_Yield, str( 100 ) )

            global_Gui.updateTotal('0')
            global_Gui.updatePass('0')
            global_Gui.updateFail('0')
            global_Gui.updateYield('100')
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), 'red', False)
            global_Gui.tbvwLogEmit('读取 Counter 计数文件失败', 'red',False)
            return False

    def RecordtestCount(self, total, Pass, Fail):
        tmpTotal = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total))
        tmpPass = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass))
        tmpFail = int(self.counterIns.ReadValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail))

        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Total, str(tmpTotal + total))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Fail, str(tmpFail + Fail))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Pass, str(tmpPass + Pass))
        self.counterIns.WriteValue(self.counterKey.SEC_CNT, self.counterKey.KEY_Yield,
                                   str(round((tmpPass + Pass) * 100 / (tmpTotal + total), 3)))

        global_Gui.updateTotal(str(tmpTotal + total))
        global_Gui.updatePass(str(tmpPass + Pass))
        global_Gui.updateFail(str(tmpFail + Fail))
        global_Gui.updateYield(str(round((tmpPass + Pass) * 100 / (tmpTotal + total), 3)))

    McuIntDic = {}
    McuOutDic = {}

    # def CollectMCU(self):
    #     self.McuOutDic["Cylinder"] = self.Cylinder
    #     self.McuOutDic["LedY"] = self.LedY
    #     self.McuOutDic["LedR"] = self.LedR
    #     self.McuOutDic["LedG"] = self.LedG
    #     self.McuOutDic["FMQ"] = self.FMQ
    #     self.McuOutDic["XZK"] = self.XZK
    #     self.McuOutDic["YL"] = self.YL
    #     self.McuOutDic["FS"] = self.FS
    #
    #     self.McuIntDic.clear()
    #     self.McuIntDic["start1"] = self.start1
    #     self.McuIntDic["start2"] = self.start2
    #     self.McuIntDic["Alarm"] = self.Alarm
    #     self.McuIntDic["begin"] = self.begin
    #     self.McuIntDic["air"] = self.air
    #     self.McuIntDic["door"] = self.door
    #     # self.McuIntDic["YLint"] = self.YLint
    #     self.McuIntDic["X11"] = self.X11
    #     self.McuIntDic["X12"] = self.X12
    #     self.McuIntDic["X13"] = self.X13
    #     self.McuIntDic["X14"] = self.X14
    #     self.McuIntDic["X15"] = self.X15
    #     self.McuIntDic["X16"] = self.X16

    def showTestItem(self, testItems: cTestItem):
        try:
            global_Gui.tbvwTestDataEmit(self.barcode, self.TestResult and 'PASS' or 'FAIL', testItems.TestUpLimit, testItems.TestLowLimit,
                                        testItems.TestUnit, testItems.TestValue)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red')

    def Matched(self, barcode):
        tmplist=[[],[],[]]
        if barcode == '':
            return False, tmplist
        self.Configure.loadBarcodeConfigure()
        equalResult, tmplist = self.Configure.Equal(barcode)
        if not equalResult:
            tmplist[0].append('--')
            tmplist[2].append(f'Barcode: {barcode}无匹配规则。')
        return equalResult, tmplist

    def showNozzleAlarm(self):
        global_Gui.lockEngine()
        return True

    def str2float(self, data:str):
        try:
            data = data.replace(' ', '')
            return float(data)
        except Exception as e:
            return 0.0

if __name__ == '__main__':
    bdata = b'Leak,-0.0000,11,19-2023,02:03pm,MIC,4,,,ERROR,psi,4.5,-0.2993,0.00000\r\n\r\xff\r'
    bdata1 = b'Leak,-0.000,01-01-1970,04:59am,LED ALT,540,,,ACCEPT,psi,5.0,-2.0444,-0.00014\r\n\r\xff\r'
    bdata2= b'start testLeak\r\n\r\nStart Error -1 :invalid\r\nStart Error -1:invalid\r\n'
    time1 = datetime.strptime(
        datetime.now().date().strftime('%Y%m%d ')
        + '8:02:46',
        '%Y%m%d %H:%M:%S')
    check1 = datetime.strptime(datetime.now().date().strftime('%Y%m%d ') + '8:00:00', '%Y%m%d %H:%M:%S')
    check2 = datetime.strptime(
        datetime.now().date().strftime('%Y%m%d ')
        + '8:10:0',
        '%Y%m%d %H:%M:%S')
    check3 = datetime.strptime(datetime.now().date().strftime('%Y%m%d'), '%Y%m%d')
    print(check3.date().strftime('%Y-%m-%d'))
    print(check2.date().strftime('%Y-%m-%d'))
    print(check2.date() == check3.date())
    if check1 <= time1 <= check2:
        check4 = check2 + timedelta(days=1,hours=12)
        print(check4.strftime('%Y-%m-%d %H:%M:%S'))
        print('time in')
    else:
        print('time out')


