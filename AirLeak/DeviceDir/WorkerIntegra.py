import time
import serial
from DeviceDir.DeviceBase import cDeviceBase
from GlobalDir import GlobalConf
from GlobalDir.GlobalGui import global_Gui
from ConfigureDir.Configure import cConfigure
from ConfigureDir import ConfigureKey
from TestDir.TestItem import cTestItem
from ConfigureDir import LimitKey
from ConfigureDir.Limit import cLimit

class cWorkerIntegra(cDeviceBase):
    def __init__(self, name):
        super(cWorkerIntegra, self).__init__(name)
        self.set_name(GlobalConf.WORKER_INTEGRA)
        self.limitConfig = cLimit()
        try:
            self.port = str
            self.baud = int
            self.ser = serial.Serial()
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    def Setup(self):
        try:
            confIns = cConfigure()
            confkeyIns = ConfigureKey

            self.port = confIns.ConfigureDic[confkeyIns.SEC_WORKER_INTEGRA][confkeyIns.KEY_PORT]
            self.baud = confIns.ConfigureDic[confkeyIns.SEC_WORKER_INTEGRA][confkeyIns.KEY_BAUD]

            self.ser = serial.Serial(self.port, self.baud)
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 10
            self.ser.writeTimeout = 10
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.locker.acquire()
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.release()
            return True
        except Exception as e:
            print(e)
            self.locker.release()
            global_Gui.tbvwLogEmit(str(e), 'red', False)
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
            global_Gui.tbvwLogEmit(str(e), 'red', False)
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

    def write(self, data=str):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            self.locker.acquire()
            result = self.ser.write(data.encode("utf-8"))
            print("写入数据长度为：", result)
            self.locker.release()
            return True
        except Exception as e:
            print(e)
            self.locker.release()
            return False

    def writeAndRead(self, timeout: int):
        try:
            tmpTestItem:cTestItem = cTestItem();
            if not self.ser.isOpen():
                if not self.Open():
                    return False, tmpTestItem
            triggureCmd = 'start testLeak\r\n'
            tmpStart = time.time()
            Interval = time.time() - tmpStart
            self.ser.write(triggureCmd.encode())
            self.ser.reset_output_buffer()
            while Interval < timeout:
                data = self.ser.read_all()#.decode('utf-8')
                #data = self.ser.read_until(b'\r\n')  # .decode('utf-8')
                if len(data) > 50:
                    endChar = data.find(b'\r\n')
                    global_Gui.tbvwLogEmit(str(data), GlobalConf.colorBlue)
                    if endChar <= 0:
                        #self.Close()
                        return False,tmpTestItem
                    tmpData = data[0:endChar].decode('utf-8')
                    if tmpData.count(',') >= 12 and not tmpData.endswith(','):
                        uplimit = self.str2float(str(self.limitConfig.ConfigureDic[LimitKey.SEC_LEAK][LimitKey.KEY_UPPER_LIMIT]))
                        lowlimit = self.str2float(str(self.limitConfig.ConfigureDic[LimitKey.SEC_LEAK][LimitKey.KEY_LOW_LIMIT]))
                        testResult = False
                        tmpList = tmpData.split(',')
                        value = self.str2float(tmpList[1])
                        if tmpList[8].upper() == 'ACCEPT':
                            if value == 0.0:
                                testResult = True
                            else:
                                testResult = (value > lowlimit and value < uplimit)
                            tmpTestItem.TestValue = tmpList[1]
                        else:
                            testResult = False
                            # fail情况下的0改为9999
                            tmpTestItem.TestValue = tmpList[1] == '0' and '9999' or tmpList[1]
                        tmpTestItem.TestName = 'Pressure decay test'
                        tmpTestItem.TestResult = testResult
                        tmpTestItem.TestUnit = tmpList[9]
                        tmpTestItem.TestUpLimit = str(uplimit)
                        tmpTestItem.TestLowLimit = str(lowlimit)

                        #self.Close()
                        return True, tmpTestItem

                time.sleep(0.8)
                Interval = time.time() - tmpStart
            #self.Close()
            return False, tmpTestItem
        except Exception as e:
            #self.Close()
            print(e)
            return False, tmpTestItem

    def str2float(self, data:str):
        try:
            data = data.replace(' ', '')
            return float(data)
        except Exception as e:
            return 0.0

if __name__ == '__main__':
    uplimit = 0
    lowlimit = -0.1
    value = -0.0012
    result = (value>lowlimit and value<uplimit)
    print(result)