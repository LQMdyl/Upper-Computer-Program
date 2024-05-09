import time

import serial

import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase


class cScan(cDeviceBase):
    def __init__(self, name):
        super(cScan, self).__init__(name)
        self.set_name(Macro.SCAN)
        try:
            self.port = str
            self.baud = int
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            self.ser = serial.Serial()
            print("scan:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            self.port = self.confIns.ReadValue(self.confkeyIns.SEC_SCAN, self.confkeyIns.KEY_PORT)
            self.baud = self.confIns.ReadValue(self.confkeyIns.SEC_SCAN, self.confkeyIns.KEY_BAUD)

            self.ser = serial.Serial(self.port, self.baud)
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 3000
            self.ser.writeTimeout = 3000
            self.ser.set_buffer_size(4096, 4096)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Open(self):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Close(self):
        try:
            if self.ser.isOpen():
                self.ser.close()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def clearSocketBuffer(self):
        try:
           pass
        except Exception as e:
            print( '' )
            return


    def GetBarcde(self, lenght = int, timeout = int ):
        try:
            if not self.ser.isOpen():
                self.Open()

            delay = self.confIns.ReadValue(self.confkeyIns.SEC_SCAN, self.confkeyIns.KEY_SCAN_DELAY)
            triCMD = {0x16, 0x54, 0x0d}
            closeCMD = {0x16, 0x55, 0x0d}

            tmpStart = time.time()
            Interval = time.time() - tmpStart
            while Interval < timeout:
                self.ser.write(triCMD)
                time.sleep(delay)
                barcode = self.ser.read_all().decode('utf-8')
                if  barcode != None:
                    if barcode.len >= lenght:
                        self.ser.write(closeCMD)
                        return True , barcode
            self.ser.write(closeCMD)
            return False , None
        except Exception as e:
            print('')
            return False , None
