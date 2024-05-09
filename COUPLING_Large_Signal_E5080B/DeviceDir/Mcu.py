import serial

import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase


class cMcu(cDeviceBase):
    def __init__(self, name):
        super(cMcu, self).__init__(name)
        self.set_name(Macro.MCU)
        try:
            self.port = str
            self.baud = int
            self.ser = serial.Serial()

            print("mcu:%s", self.get_name())
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)

    def Setup(self):
        try:
            confIns = cConfigure()
            confkeyIns = ConfigureKey

            self.port = confIns.ReadValue(confkeyIns.SEC_MCU, confkeyIns.KEY_PORT)
            self.baud = confIns.ReadValue(confkeyIns.SEC_MCU, confkeyIns.KEY_BAUD)
            # self.port = "/dev/cu.usbserial-FTBI73VQ"
            # self.baud=9600
            self.ser = serial.Serial(self.port, self.baud)
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 10
            self.ser.writeTimeout = 10
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.locker.acquire()
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.release()
            #if __name__ == '__main__':
            return self.Match()
        except Exception as e:
            print(e)
            self.locker.release()
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Close(self):
        try:
            self.locker.acquire()
            if self.ser.isOpen():
                self.ser.close()
            self.locker.release()
            return True
        except Exception as e:
            self.locker.release()
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Read(self, bytenum):
        try:
            if not self.ser.isOpen():
                self.Open()
            self.locker.acquire()
            buytes = self.ser.read(bytenum).decode("gbk")
            if buytes != None:
                self.locker.release()
                return buytes
            self.locker.release()
            return None
        except Exception as e:
            print(e)
            self.locker.release()
            return None

    def write(self, data = str):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.acquire()
            result = self.ser.write(data.encode("gbk"))
            print("写入数据长度为：", result)
            self.locker.release()
            return True
        except Exception as e:
            print(e)
            self.locker.release()
            return False

    def readHex(self):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.acquire()
            data = self.ser.read(self.ser.in_waiting).hex()
            self.locker.release()
            return True, data
            pass
        except Exception as e:
            print(e)
            self.locker.release()
            return False, None

    def writeHex(self, data):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.acquire()
            self.ser.write(data)
            self.locker.release()
            return True
            pass
        except Exception as e:
            print(e)
            self.locker.release()
            return False

    def Match(self):
        try:
            # 写：  0x68:  0x00:  0x10:  0x01:fun   0x01:数据个数   0x00:数据   0x24:结束
            # 返回: 0x68:  0x10:  0x01:  0x01:fun   0x01:数据个数   0x00:数据   0x24:结束
            # 匹配  0x68   0x00   0x10   0x01  0x01  0x00  0x24
            tmpCmd = [0x68, 0x00, 0x10, 0x01, 0x01, 0x00, 0x24]
            self.locker.acquire()
            if not self.ser.isOpen():
                self.ser.open()
            if not self.ser.write(tmpCmd):
                self.locker.release()
                return False
            #data:[] = self.ser.read(self.ser.in_waiting).hex()
            data:[]=self.ser.read(7)
            if len(data) >= 7:
                if data[0] == tmpCmd[0] and data[1] == 0x10 and data[2] == 0x01 and data[3] == 0x01 and data[6] == 0x24:
                    self.locker.release()
                    return True
            self.locker.release()
            return False
            pass
        except Exception as e:
            print(e)
            self.locker.release()
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def WriteAndReadXY(self, cmd=[]):
        try:
            # 写：  0x68:  0x01:  0x10:  0x02:fun   0xXX:数据长度  0xXX:数据帧   0x24:结束
            # 返回: 0x68:  0x10:  0x01:  0x02:fun   0xXX:数据长度  0xXX:数据帧   0x24:结束

            # 写入数据帧
            # cmd[0]:气缸  cmd[1]:黄灯  cmd[2]:红灯  cmd[3]:绿灯  cmd[4]:喇叭  cmd[5]:吸真空  cmd[6]:风扇  cmd[7]:预留
            # cmd[8]:realy  cmd[9]:realy9_10
            # cmd[11]:y9  cmd[12]:y10  cmd[13]:y11  cmd[14]:y12  cmd[15]:y13  cmd[16]:y14  cmd[17]:y15  cmd[18]:y16

            # 读取数据帧
            # data[0]:左按键  data[1]:右按键  data[2]:急停键  data[3]:夹紧始位感应器  data[4]:夹紧末位感应器
            # data[5]:总气压  data[6]:门开关  data[7]:预留   data[8]:realy         data[9]:realy9_10
            #10-17 YL-X
            if len(cmd) != 18: return False
            tmpCmd = [0x68, 0x00, 0x10, 0x02, 0x24]
            tmpCmd[4] = len(cmd)
            tmpCmd += cmd
            #tmpCmd[23] = 0x24
            tmpCmd.append(0x24)

            self.locker.acquire()
            if not self.ser.isOpen():
                self.ser.open()
            if not self.ser.write(tmpCmd):
                self.locker.release()
                return False, None
            #data1 = self.ser.read(self.ser.in_waiting).hex()
            data: [] = self.ser.read(24)
            if len(data) >= 24:
                if data[0] == tmpCmd[0] and data[1] == 0x10 and data[2] == 0x01 and data[3] == 0x02 and data[-1] == 0x24:
                    self.locker.release()
                    return True, data[5:]
            self.locker.release()
            return False, None
            pass
        except Exception as e:
            print(e)
            self.locker.release()
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None

    def WriteAndReadIO(self, cmd=[]):
        try:
            # 写：  0x68:  0x01:  0x10:  0x02:fun   0xXX:数据长度  0xXX:数据帧   0x24:结束
            # 返回: 0x68:  0x10:  0x01:  0x02:fun   0xXX:数据长度  0xXX:数据帧   0x24:结束

            # 写入数据帧
            # cmd[0]:气缸  cmd[1]:黄灯  cmd[2]:红灯  cmd[3]:绿灯  cmd[4]:喇叭  cmd[5]:吸真空  cmd[6]:风扇  cmd[7]:预留
            # cmd[8]:realy  cmd[9]:realy9_10
            # cmd[11]:y9  cmd[12]:y10  cmd[13]:y11  cmd[14]:y12  cmd[15]:y13  cmd[16]:y14  cmd[17]:y15  cmd[18]:y16

            # 读取数据帧
            # data[0]:左按键  data[1]:右按键  data[2]:急停键  data[3]:夹紧始位感应器  data[4]:夹紧末位感应器
            # data[5]:总气压  data[6]:门开关  data[7]:预留   data[8]:realy         data[9]:realy9_10
            if len(cmd) != 10: return False
            tmpCmd = [0x68, 0x00, 0x10, 0x02, 0x24]
            tmpCmd[4] = len(cmd)
            tmpCmd += cmd
            tmpCmd.append(0x24)
            #tmpCmd[23] = 0x24

            self.locker.acquire()
            if not self.ser.isOpen():
                self.ser.open()
            if not self.ser.write(tmpCmd):
                self.locker.release()
                return False, None
            #data = self.ser.read(self.ser.in_waiting).hex()
            data: [] = self.ser.read(16)
            if len(data) >= 16:
                #and data[4] == 0x10
                if data[0] == tmpCmd[0] and data[1] == 0x10 and data[2] == 0x01 and data[3] == 0x02  and data[-1] == 0x24:
                    self.locker.release()
                    return True, data[5:]
            self.locker.release()
            return False, None
            pass
        except Exception as e:
            print(e)
            self.locker.release()
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None