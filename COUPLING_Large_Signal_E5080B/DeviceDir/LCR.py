import socket

import time
import numpy
import pyvisa
from pyvisa.resources import TCPIPInstrument

import GlobalGui
from ConfigureDir import ConfigureKey, LimitKey
from ConfigureDir.Configure import cConfigure
from ConfigureDir.Limit import cLimit
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase
from TestDir.TestItem import cTestItem


class cLcr(cDeviceBase):
    def __init__(self, name):
        super(cLcr, self).__init__(name)
        self.set_name(Macro.LCR)
        try:
            self.IP = '169.254.94.36'
            self.port = 9999
            self.rem = pyvisa.ResourceManager()
            self.device: TCPIPInstrument = None
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            print("lcr:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            self.IP = self.confIns.ReadValue(self.confkeyIns.SEC_LCR, self.confkeyIns.KEY_IP)
            self.port = self.confIns.ReadValue(self.confkeyIns.SEC_LCR, self.confkeyIns.KEY_PORT)

            reIP = f"TCPIP::{self.IP}::INSTR"

            self.device: TCPIPInstrument = self.rem.open_resource(reIP)
            self.device.timeout = 500

            limitIns = cLimit()
            limitKey = LimitKey
            self.tmpAvge = 3#limitIns.ReadValue(limitKey.SEC_LIMIT, limitKey.KEY_Avge_Cnt)
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.device.open()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Close(self):
        try:
            self.device.close()
            self.rem.close()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Connect(self):
        try:
            self.device.write('*RST\n')
            self.device.write('*IDN?')
            strIDN = self.device.read()
            print(strIDN)
            if 'E4982A' in strIDN:
                print('ok')
                return True
            return False
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Init(self):
        try:
            self.device.write(':FUNCtion:DCResistance:RANGe:AUTO 1\n')
            self.device.write(':FREQuency 1000\n')
            self.device.write(':VOLTage 1\n')
            self.device.write(':BIAS:VOLTage 0\n')
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def SetFreq(self,FreQ):
        try:
            self.device.write(':FREQuency {0}\n'.format(FreQ))
            self.device.write(':VOLTage 1\n')
            self.device.write(':BIAS:VOLTage 0\n')
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Read_LSRS(self):
        try:
            self.device.write(':FUNCtion:IMPedance LSRS\n')
            tmpRS:float=0
            for i in range(int(self.tmpAvge)):
                tmpD = self.device.query(':FETCh?')
                if "+9.90000E+37" in tmpD:
                    continue
                tmpData = tmpD.split(",", 3)
                tmpRS += float(tmpData[1])
            tmpRS = tmpRS / int(self.tmpAvge) * 1000
            return True, tmpRS
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None

    def Read_LSQ(self):
        try:
            self.device.write(':FUNCtion:IMPedance LSQ\n')
            tmpLS: float = 0
            tmpQ: float = 0
            for i in range(int(self.tmpAvge)):
                tmpD = self.device.query(':FETCh?')
                if "+9.90000E+37" in tmpD:
                    continue
                tmpData = tmpD.split(",", 3)
                tmpLS += float(tmpData[0]) * 1000000
                tmpQ += float(tmpData[1])

            tmpLS = tmpLS / int(self.tmpAvge)
            tmpQ = tmpQ / int(self.tmpAvge)
            return True, tmpLS, tmpQ
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None, None

    def Model(self,model):
        try:
            self.device.write(':FUNCtion:IMPedance {0}\n'.format(model))
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Read_LSRD(self):
        try:
            self.device.write(':FUNCtion:IMPedance LSRD\n')

            tmpRX:float=0
            for i in range(int(self.tmpAvge)):
                tmpD = self.device.query(':FETCh?')
                if "+9.90000E+37" in tmpD:
                    continue
                tmpData = tmpD.split(",", 3)
                tmpRX += float(tmpData[1])
            tmpRX = tmpRX / int(self.tmpAvge) * 1000
            return True, tmpRX
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None

    def GetLs(self):
        try:
            result, LS, Q = self.Read_LSQ()
            if not result:
                return False, 0
            print(str(LS))
            GlobalGui.global_Gui.TextBrowserSignal.emit("LCR DATA:"+str(LS), 'black', False)
            return True, LS
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, -1

    def GetRDC(self):
        try:
            testItemList = []
            result, Rdc= self.Read_LSRD()
            if not result:
                return False, None
            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName = "Rdc"
            tmpTestitem.TestValue = Rdc
            testItemList.append(tmpTestitem.Clone())
            return True, testItemList
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None
    
    def GetLSRSQ(self):
        try:
            testItemList=[]
            result, LS, Q = self.Read_LSQ()
            if not result:
                return False, None
            result, RS = self.Read_LSRS()
            if not result:
                return False, None

            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName = "Ls"
            tmpTestitem.TestValue =LS
            testItemList.append(tmpTestitem.Clone())

            tmpTestitem.TestName = "Q"
            tmpTestitem.TestValue = Q
            testItemList.append(tmpTestitem.Clone())

            tmpTestitem.TestName = "Rs"
            tmpTestitem.TestValue = RS
            testItemList.append(tmpTestitem.Clone())
            return True,testItemList
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None

    def Read_debug(self):
        try:
            self.device.write(':FUNCtion:IMPedance LSQ\n')
            tmpLS: float = 0
            tmpQ: float = 0
            for i in range(100):
                tmpD = self.device.query(':FETCh?')
                print(tmpD)
            return True, tmpLS, tmpQ
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None, None
