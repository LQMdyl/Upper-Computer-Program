import json
import socket

from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from GlobalDir import GlobalConf, GlobalGui
from DeviceDir.DeviceBase import cDeviceBase


class cTestApp(cDeviceBase):
    def __init__(self, name):
        super(cTestApp, self).__init__(name)
        self.set_name(GlobalConf.TestApp)
        try:
            self.IP = str
            self.port = str
            self.isConnect = False
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("cTestApp:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)



    def Setup(self):
        try:
            self.client=None
            confIns = cConfigure()
            confkeyIns = ConfigureKey
            self.IP = confIns.getConfigure(confkeyIns.SEC_APP, confkeyIns.KEY_IP_ADDRESS)
            self.port = confIns.getConfigure(confkeyIns.SEC_APP, confkeyIns.KEY_HOST_PORT)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.client.connect((self.IP, int(self.port)))
            cc=self.client.recv( 500 )
            self.isConnect = len(cc)>0
            print(cc)
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            self.isConnect = False
            return False

    def Close(self):
        try:
            self.client.close()
            self.isConnect=False
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            return False

    def send(self, cmd):
        try:
            cmd_ba = bytearray("%s\r\n" % cmd, "utf8")
            self.client.send(cmd_ba)
            data = self.client.recv(100000)
            js = json.loads((data).decode("utf8"))
            if js["cmdCompleted"]:
                return js
            else:
                raise Exception("SoundCheck command did not complete:  %s: %s: %s: %s" % (
                    js["errorDescription"], js["errorType"], js["originalCommand"], data))
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit("重新连接 SoundCheck-" + str(e), GlobalConf.colorBlue, False)
            self.Setup()
            self.Open()
            cmd_ba = bytearray("%s\r\n" % cmd, "utf8")
            self.client.send(cmd_ba)
            data = self.client.recv(100000)
            js = json.loads((data).decode("utf8"))
            if js["cmdCompleted"]:
                return js
            else:
                raise Exception("SoundCheck command did not complete:  %s: %s: %s: %s" % (
                    js["errorDescription"], js["errorType"], js["originalCommand"], data))

    def open(self, filename):
        self.send( "Sequence.Open('%s')" % filename )

    def setLotNumber(self, lotNumber):
        self.send( "SoundCheck.SetLotNumber('%s')" % lotNumber )

    def getLotNumber(self):
        js = self.send( "SoundCheck.GetLotNumber" )
        return js["returnData"]["Value"]

    def setLoginLevel(self, level="engr"):
        js = self.send( "SoundCheck.SetLoginLevel('%s')" % level )

    def getLoginLevel(self):
        js = self.send( "SoundCheck.GetLoginLevel" )
        return js["returnData"]["Value"]

    def memGetAllNames(self):
        js = self.send( "MemoryList.GetAllNames" )
        return js["returnData"]

    def run(self):
        js = self.send( "Sequence.Run('7200000')" )
        return js["returnData"]["Pass?"]

    def getCurveNames(self):
        return self.memGetAllNames()["Curves"]

    def getWaveformNames(self):
        return self.memGetAllNames()["Waveforms"]

    def getValueNames(self):
        return self.memGetAllNames()["Values"]

    def getResultNames(self):
        return self.memGetAllNames()["Results"]

    def get(self, gtype, name):
        js = self.send( "MemoryList.Get('%s', '%s')" % (gtype, name) )
        return js["returnData"]

    def getCurve(self, name):
        return self.get( 'Curve', name )

    def getWaveform(self, name):
        return self.get( 'Waveform', name )

    def getValue(self, name):
        return self.get( 'Value', name )

    def getResult(self, name):
        return self.get( 'Result', name )

    # <editor-fold desc="测试方法">

    # def TestApp_DOE_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["Command"]
    #         self.client.send( command.encode() )
    #         data.TestValue = "PASS"
    #         data.TestResult = True
    #         data.Reback = "Send Command:" + command + "success"
    #
    #         return data
    #     except Exception as e:
    #
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Send Command:" + command + "fail-" + str( e )
    #         return data
    #
    # def TestApp_Open_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["FilePath"]
    #         self.open( command )
    #         data.TestValue = "PASS"
    #         data.TestResult = True
    #         data.Reback = "Send Command:" + command + "success"
    #         return data
    #     except Exception as e:
    #
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Send Command:" + command + "fail-" + str( e )
    #         return data
    #
    # def TestApp_Run_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         data.TestResult=self.run()
    #         #self.test.DeleGate_ReTest(not data.TestResult)
    #         data.TestValue ="PASS"
    #         data.Reback = "Send Command:"  + "success"
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Send Command:"  + "fail-" + str( e )
    #         return data
    #
    # def TestApp_CheckWater_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["FilePath"]
    #         if not os.path.exists(command):
    #             data.TestValue = "PASS"
    #             data.TestResult = True
    #             self.test.DeleGate_ReTest(not data.TestResult)
    #             data.Reback = "File does not exist:{0} check Water Sucess".format(command)
    #             return data
    #
    #         data.TestResult=False
    #         data.TestValue ="PASS"
    #         data.Reback = "Check Water Fail"
    #         self.test.DeleGate_ReTest(not data.TestResult)
    #         os.remove(command)
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Send Command:"  + "fail-" + str( e )
    #         return data
    #
    # def TestApp_RunLooP_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         loopCount = int( paraDic["Loop"] )
    #         for i in range( loopCount ):
    #             GlobalGui.global_Gui.tbvwLogEmit( "SoundCheck -Index-{0} Test".format(  str(i) ),GlobalConf.colorBlack, False )
    #             data.TestResult = self.run()
    #             GlobalGui.global_Gui.tbvwLogEmit( "SoundCheck -Index-{0} Test Result-{1}".format(  str(i),data.TestResult and "PASS" or "FAIL" ),GlobalConf.colorBlack, False )
    #             data.TestValue = "PASS"
    #             data.Reback = "SoundCheck Test-" + "success"
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "SoundCheck Test-"  + "fail-" + str( e )
    #         return data
    #
    # def TestApp_SpeakerTest_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         loopCount = int( paraDic["FuctionLoop"] )
    #         for i in range( loopCount ):
    #             GlobalGui.global_Gui.tbvwLogEmit( "SoundCheck -Index-{0} Test".format( str( i ) ), GlobalConf.colorBlack, False )
    #             data.TestResult = self.run()
    #             GlobalGui.global_Gui.tbvwLogEmit(
    #                 "SoundCheck -Index-{0} Test Result-{1}".format( str( i ), data.TestResult and "PASS" or "FAIL" ),
    #                 GlobalConf.colorBlack, False )
    #             data.TestValue = "PASS"
    #             data.Reback = "SoundCheck Test-" + "success"
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "SoundCheck Test-" + "fail-" + str( e )
    #         return data
    #
    # def TestApp_DealData_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["FilePath"]
    #         filetag=paraDic["FileName"]
    #         sn= self.test.DeleGate_GetSn()
    #         Config=self.test.DeleGate_GetConfig()
    #         if not os.path.exists( command ):
    #             data.TestValue = "FAIL"
    #             data.TestResult = False
    #             data.Reback = "File does not exist:{0}".format( command )
    #             return data
    #
    #         #读取文件
    #         with open(command, 'r') as f:
    #             content = f.read()
    #
    #         #替换SN
    #         content=content.replace("SN_Replace",sn)
    #         content = content.replace("Lot_Replace", Config)
    #         tmp=content.replace("\r","").split("\n")
    #         if len(tmp)<7:
    #             data.TestValue = "FAIL"
    #             data.TestResult = False
    #             data.Reback = "File data error"
    #             return data
    #         self.test.DeleGate_SaveData(filetag,tmp)
    #
    #         # 删除文件
    #         if os.path.exists( command ):
    #             os.remove( command )
    #
    #         data.TestResult=True
    #         data.TestValue ="PASS"
    #         data.Reback = "Send Command:" + command + "success"
    #         return data
    #     except Exception as e:
    #
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "APP Run Send Command:"  + "fail-" + str( e )
    #         return data
    #
    # def TestApp_SaveAllDataFile_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["FileCount"]
    #         Dic= self.test.TestDataRecord
    #         if len(Dic) !=int(command):
    #             data.TestValue = "FAIL"
    #             data.TestResult = False
    #             data.Reback = "Save All Data :" + "fail- the Count of testData Saved is not Match setUp"
    #             return data
    #         index_1_Test = []
    #         index_2_BT = []
    #         index_3_display = []
    #         index_4_PDCA = []
    #         index_5_Up = []
    #         index_6_Lower = []
    #         index_7_unit = []
    #         index_8_data = []
    #         index=0
    #         for num in Dic:
    #             Tmplist:list=num
    #             testList = Tmplist[0].split(",")
    #             Bt = Tmplist[1].split(",")
    #             Display = Tmplist[2].split(",")
    #             PDCA = Tmplist[3].split(",")
    #             Up = Tmplist[4].split(",")
    #             Low = Tmplist[5].split(",")
    #             unit = Tmplist[6].split(",")
    #             Data = Tmplist[7].split(",")
    #             GlobalGui.global_Gui.tbvwLogEmit( "TestData -Index-{0} Count-{1}".format( str( index ),str(len(Bt))), GlobalConf.colorGreen, False )
    #             TtestList=[]
    #             TBt=[]
    #             TDisplay=[]
    #             TPDCA=[]
    #             TUp=[]
    #             TLow=[]
    #             Tunit=[]
    #             TData=[]
    #             if index==0:
    #                 TtestList = testList
    #                 TBt = Bt
    #                 TDisplay = Display
    #                 TPDCA = PDCA
    #                 TUp = Up
    #                 TLow = Low
    #                 Tunit = unit
    #                 TData = Data
    #             else:
    #                 TtestList = testList[15:]
    #                 TBt = Bt[15:]
    #                 TDisplay = Display[15:]
    #                 TPDCA = PDCA[15:]
    #                 TUp = Up[15:]
    #                 TLow = Low[15:]
    #                 Tunit = unit[15:]
    #                 TData = Data[15:]
    #
    #             for tl1 in TtestList:
    #                 index_1_Test.append(tl1.replace("\r","").replace("\n",""))
    #             for tl1 in TBt:
    #                 index_2_BT.append(tl1.replace("\r","").replace("\n",""))
    #             for tl1 in TDisplay:
    #                 index_3_display.append(tl1.replace("\r","").replace("\n",""))
    #             for tl1 in TPDCA:
    #                 index_4_PDCA.append(tl1.replace("\r","").replace("\n",""))
    #             for tl1 in TUp:
    #                 index_5_Up.append(tl1.replace("\r", "").replace("\n", ""))
    #             for tl1 in TLow:
    #                 index_6_Lower.append(tl1.replace("\r", "").replace("\n", ""))
    #             for tl1 in Tunit:
    #                 index_7_unit.append(tl1.replace("\r", "").replace("\n", ""))
    #             for tl1 in TData:
    #                 index_8_data.append(tl1.replace("\r", "").replace("\n", ""))
    #
    #             index+=1
    #
    #         alldatalist=[index_1_Test,index_2_BT,index_3_display,index_4_PDCA,index_5_Up,index_6_Lower,index_7_unit,index_8_data]
    #         Testdatalist=[index_8_data]
    #
    #         Filepath = "D:\\Log\\CSVLog\\{0}\\{1}".format(time.strftime( "%Y%m%d", time.localtime() ),self.test.PN)
    #         if not os.path.exists( Filepath ):
    #             os.makedirs( Filepath )
    #
    #         FileName="{0}\\{1}_{2}.csv".format(Filepath,time.strftime( "%Y%m%d", time.localtime() ),self.test.TestModel)#sn=="" and "NULL" or sn)
    #         if not os.path.exists( FileName ):
    #             with open( FileName, "a", newline='' ) as f:
    #                 writer = csv.writer( f )
    #                 for num in alldatalist:
    #                     writer.writerow( num )
    #         else:
    #             with open( FileName, "a", newline='') as f:
    #                 writer = csv.writer( f )
    #                 for num in Testdatalist:
    #                     writer.writerow(num)
    #
    #         data.TestResult = True
    #         data.TestValue = "PASS"
    #         data.Reback = "Remove:" + command + "-success"
    #         self.test.TestDataRecord.clear()
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Save All Data :" + "fail-" + str(e)
    #         return data
    #
    # def TestApp_RemoveFile_TestFlow(self, data: ScriptDataBase):
    #     try:
    #         paraDic = data.Param
    #         command = paraDic["FilePath"]
    #
    #         if not os.path.exists( command ):
    #             data.TestValue = "PASS"
    #             data.TestResult = True
    #             data.Reback= "File does not exist:{0}".format( command )
    #             return data
    #
    #         # 删除文件
    #         if os.path.exists( command ):
    #             os.remove( command )
    #
    #         data.TestResult = True
    #         data.TestValue = "PASS"
    #         data.Reback = "Remove:" + command + "-success"
    #         return data
    #     except Exception as e:
    #         data.TestValue = "FAIL"
    #         data.TestResult = False
    #         data.Reback = "Remove :" + "fail-" + str( e )
    #         return data

    # </editor-fold>
