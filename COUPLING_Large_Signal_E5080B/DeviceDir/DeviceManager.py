import sys
import os
import time

from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.CCD import CCD
from DeviceDir.DeviceBase import cDeviceBase
from DeviceDir.E5071C_Large_Signal import cE5071C_Large_Signal
from DeviceDir.Hawk import cHawk
from DeviceDir.LCR import cLcr
from DeviceDir.Mcu import cMcu
from DeviceDir.Robot import cRobot
from DeviceDir.Scan import cScan
from DeviceDir.ModbusSerial import cModbusSerial
import GlobalGui
from DeviceDir.Vna import cVna
from  DeviceDir.Oscillograph import cOscillograph


class cDeviceManager():
    def __init__(self):
        self._Devices = {str : cDeviceBase}

    def ALLDevices(self):
        return self._Devices

    def Devices(self, key=' '):
        if not key == None:
            if key in self._Devices.keys():
                return self._Devices[key]

    def InitializeDevice(self):
        self._Devices.clear()
        self.confIns = cConfigure()
        if len(self.confIns.ConfigureDic) is 0:
            self.confIns.LoadConfiogure()
        self.confKey = ConfigureKey
        self.IsAutoScan = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_SCAN_mode] == "A"
        testMode = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_Test_mode]

        if self.IsAutoScan:
            # HAWK
            tmpkey = Macro.HWAK
            hawk = cHawk( tmpkey )
            if hawk == None or not hawk.Setup() or not hawk.Open():
                print( "HAWK扫码枪连接失败" )
                GlobalGui.global_Gui.TextBrowserSignal.emit( 'HAWK扫码枪连接失败', 'red', False )
                GlobalGui.global_Gui.TextBrowserSignal.emit( 'Connection failure of HAWK', 'red', False )
                GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )
                return False
            dicHawk = {tmpkey: hawk}
            self._Devices.update( dicHawk )
            GlobalGui.global_Gui.TextBrowserSignal.emit( 'HAWK扫码枪连接成功', 'green', False )
            GlobalGui.global_Gui.TextBrowserSignal.emit( 'HAWK connection succeeded', 'green', False )
            GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )

        # MCU
        tmpkey = Macro.MCU
        mcu = cMcu(tmpkey)
        if mcu== None or not mcu.Setup() or not mcu.Open():
            print("单片机连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('单片机连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of MCU', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey,False)
            return False
        dicMcu = {tmpkey: mcu}
        self._Devices.update(dicMcu)
        GlobalGui.global_Gui.TextBrowserSignal.emit('单片机连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('MCU connection succeeded', 'green', False)
        GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, True)
        #data=mcu.WriteAndReadXY([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01])


        # # SCAN
        # tmpkey = Macro.SCAN
        # scan = cScan(tmpkey)
        # if scan==None or not scan.Setup() or not scan.Open():
        #     print("扫码枪连接失败")
        #     GlobalGui.global_Gui.TextBrowserSignal.emit('扫码枪连接失败', 'red', False)
        #     GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of SCAN', 'red', False)
        #     GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )
        #     return False
        # dicScan = {tmpkey: scan}
        # self._Devices.update(dicScan)
        # GlobalGui.global_Gui.TextBrowserSignal.emit('扫码枪连接成功', 'green', False)
        # GlobalGui.global_Gui.TextBrowserSignal.emit('SCAN connection succeeded', 'green', False)
        #GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )

        # CCD
        tmpkey = Macro.CAMREA
        ccd = CCD(tmpkey)
        if ccd==None or not ccd.Setup() or not ccd.Open():
            print("CCD连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('CCD连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of CCD', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False)
            return False
        dicCCD = {tmpkey: ccd}
        self._Devices.update(dicCCD)
        GlobalGui.global_Gui.TextBrowserSignal.emit('CCD连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('CCD connection succeeded', 'green', False)
        GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )

        # LCR
        # tmpkey = Macro.LCR
        # LCR = cLcr(tmpkey)
        # if LCR == None or not LCR.Setup() or not LCR.Open() or not LCR.Init():
        #     print("LCR连接失败")
        #     GlobalGui.global_Gui.TextBrowserSignal.emit('LCR连接失败', 'red', False)
        #     GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of LCR', 'red', False)
        #     GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )
        #     return False
        # dicLCR = {tmpkey: LCR}
        # self._Devices.update(dicLCR)
        # GlobalGui.global_Gui.TextBrowserSignal.emit('LCR连接成功', 'green', False)
        # GlobalGui.global_Gui.TextBrowserSignal.emit('LCR connection succeeded', 'green', False)
        # GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )

        # 温度模块
        tempflag = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_TEMP_ENABLE] == "Y"
        if tempflag:
            tmpkey = Macro.TEMP
            temp = cModbusSerial(tmpkey)
            temp.port = self.confIns.ReadValue(self.confKey.SEC_TEMP, self.confKey.KEY_PORT)
            temp.baud = int(self.confIns.ReadValue(self.confKey.SEC_TEMP, self.confKey.KEY_BAUD))
            if temp == None or not temp.Setup() or not temp.Open():
                print("测试产品温度模块连接失败")
                GlobalGui.global_Gui.TextBrowserSignal.emit('测试温度模块连接失败', 'red', False)
                GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of 测试温度模块', 'red', False)
                GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, False)
                return False
            dicTEMP = {tmpkey: temp}
            self._Devices.update(dicTEMP)
            GlobalGui.global_Gui.TextBrowserSignal.emit('测试温度模块连接成功', 'green', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('测试温度模块 connection succeeded', 'green', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, True)

        # 环境温度模块.
        tempflag = self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.SEC_SUR_TEMP_ENABLE] == "Y"
        if tempflag:
            tmpkey = Macro.SUR_TEMP
            temp1 = cModbusSerial(tmpkey)
            temp1.port = self.confIns.ReadValue(self.confKey.SEC_SUR_TEMP, self.confKey.KEY_PORT)
            temp1.baud = int(self.confIns.ReadValue(self.confKey.SEC_SUR_TEMP, self.confKey.KEY_BAUD))
            if temp1 == None or not temp1.Setup() or not temp1.Open():
                print("环境温度模块连接失败")
                GlobalGui.global_Gui.TextBrowserSignal.emit('环境温度模块连接失败', 'red', False)
                GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of 环境温度模块', 'red', False)
                GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, False)
                return False
            dicTEMP1 = {tmpkey: temp1}
            self._Devices.update(dicTEMP1)
            GlobalGui.global_Gui.TextBrowserSignal.emit('环境温度模块连接成功', 'green', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('环境温度模块 connection succeeded', 'green', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, True)

        #OSC
        tmpkey = Macro.OSC
        Osc = cOscillograph(tmpkey)
        if Osc == None or not Osc.Setup():
            GlobalGui.global_Gui.TextBrowserSignal.emit('OSC连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of OSC', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, False)
            return False
        dicOsc = {tmpkey: Osc}
        self._Devices.update(dicOsc)
        GlobalGui.global_Gui.TextBrowserSignal.emit('OSC连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('OSC connection succeeded', 'green', False)
        GlobalGui.global_Gui.lblDeviceStatueEmit(tmpkey, True)

        # VNA
        tmpkey = Macro.VNA
        VNA = cE5071C_Large_Signal(tmpkey)
        if VNA == None or not VNA.Setup() or not VNA.Open() or not VNA.Init():
            print("VNA连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('VNA连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of VNA', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )
            return False
        dicVNA = {tmpkey: VNA}
        self._Devices.update(dicVNA)
        GlobalGui.global_Gui.TextBrowserSignal.emit('VNA连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('VNA connection succeeded', 'green', False)
        GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )


        # ROBOT
        tmpkey = Macro.ROBOT_2002
        robot_2002 = cRobot(tmpkey, 2002)
        if robot_2002 == None or not robot_2002.Setup() or not robot_2002.Open():
            print("机械手-2002连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2002连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of ROBOT-2002', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )

            return False
        dicRobot_2002 = {tmpkey: robot_2002}
        self._Devices.update(dicRobot_2002)
        GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2002连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('ROBOT-2002 connection succeeded', 'green', False)
        time.sleep(0.5)
        robot_2002.Write(robot_2002.Login0)
        time.sleep(0.5)
        robot_2002.Write(robot_2002.Reset)
        time.sleep(0.5)
        robot_2002.Write(robot_2002.Start)
        time.sleep(4)

        # ROBOT 2001
        tmpkey = Macro.ROBOT_2001
        robot_2001 = cRobot(tmpkey, 2001)
        if robot_2001 == None or not robot_2001.Setup() or not robot_2001.Open():
            print("机械手-2001连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2001连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of ROBOT-2001', 'red', False)
            GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, False )

            return False
        dicRobot_2001 = {tmpkey: robot_2001}
        self._Devices.update(dicRobot_2001)
        GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2001连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('ROBOT-2001 connection succeeded', 'green', False)
        time.sleep(1)
        if robot_2001.Init(2):
            # time.sleep(4)
            robot_2001.Move(-120, 0, 0, 0, 0, 0)

        GlobalGui.global_Gui.lblDeviceStatueEmit( tmpkey, True )
        return True

    def Reconnect2001(self):
        # ROBOT
        tmpkey = Macro.ROBOT_2001
        if tmpkey in self._Devices.keys():
            self._Devices[tmpkey]:cRobot.Close()
        time.sleep(2)
        robot_2001 = cRobot(tmpkey, 2001)
        if robot_2001 == None or not robot_2001.Setup() or not robot_2001.Open():
            print("机械手-2001连接失败")
            GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2001连接失败', 'red', False)
            GlobalGui.global_Gui.TextBrowserSignal.emit('Connection failure of ROBOT-2001', 'red', False)
            return False
        dicRobot_2001 = {tmpkey: robot_2001}

        if tmpkey in self._Devices.keys():
            self._Devices[tmpkey]=robot_2001
        else:
            self._Devices.update(dicRobot_2001)
        GlobalGui.global_Gui.TextBrowserSignal.emit('机械手-2001连接成功', 'green', False)
        GlobalGui.global_Gui.TextBrowserSignal.emit('ROBOT-2001 connection succeeded', 'green', False)
        time.sleep(1)
        if robot_2001.Init(2):
            # time.sleep(4)
            robot_2001.Move(-120, 0, 0, 0, 0, 0)
            return True
        else:
            return False




