import time
import serial
from DeviceDir.DeviceBase import cDeviceBase
from GlobalDir import GlobalConf
from GlobalDir.GlobalGui import global_Gui
from ConfigureDir.Configure import cConfigure
from ConfigureDir import ConfigureKey

class cScan(cDeviceBase):
    def __init__(self, name):
        super(cScan, self).__init__(name)
        self.set_name(GlobalConf.SCAN)
        try:
            self.port = str
            self.baud = int
            self.ser = serial.Serial()
            self.clientconnected = False
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)

    def Setup(self):
        try:
            confIns = cConfigure()
            confkeyIns = ConfigureKey

            self.port = confIns.ConfigureDic[confkeyIns.SEC_SCAN][confkeyIns.KEY_PORT]
            self.baud = confIns.ConfigureDic[confkeyIns.SEC_SCAN][confkeyIns.KEY_BAUD]

            self.ser = serial.Serial(self.port, self.baud)
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 10
            self.ser.writeTimeout = 10
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
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
                self.clientconnected = True
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

    def GetBarcode(self, timeout=int):
        try:
            if not self.ser.isOpen():
                self.Open()

            # delay = self.confIns.ReadValue(self.confkeyIns.SEC_SCAN, self.confkeyIns.KEY_SCAN_DELAY)
            triCMD = [0x16, 0x54, 0x0d]
            closeCMD = [0x16, 0x55, 0x0d]
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            tmpStart = time.time()
            while (time.time() - tmpStart) < timeout:
                # 'S'.encode('utf-8')
                wrele = self.ser.write(triCMD)
                print(wrele)
                time.sleep(1.2)
                barcode = self.ser.read_all().decode('utf-8')
                if barcode != None:
                    if '\r' in barcode:
                        self.ser.write(closeCMD)
                        return True, barcode
            self.ser.write(closeCMD)
            return False, None
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False, None