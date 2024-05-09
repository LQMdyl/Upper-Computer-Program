import pyvisa
from pyvisa.resources import TCPIPInstrument, PXIInstrument

import GlobalGui

class cP9382B():
    def __init__(self):
        try:
            self.IP = str
            self.port = str
            self.rem = pyvisa.ResourceManager()
            oo = self.rem.list_resources()
            print(oo)
            self.device: PXIInstrument = None
            self.frequencies = "326.5, 1780"
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            #self.IP = self.confIns.ReadValue(self.confkeyIns.SEC_VNA, self.confkeyIns.KEY_IP)
            #self.port = self.confIns.ReadValue(self.confkeyIns.SEC_VNA, self.confkeyIns.KEY_PORT)

            reIP = f"USB0::0x2A8D::0x3E01::f329d1447025cb17::RAW"
            #reIP = f"PXI10::CHASSIS::SLOT1::FUNC0::INSTR"
            self.device: PXIInstrument = self.rem.open_resource(reIP)

            self.device.timeout = 300  # ms
            self.device.write('*CLS')
            self.device.write('*RST')
            self.device.write('*IDN?')
            strIDN = self.device.read()
            print(strIDN)
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False


if __name__== '__main__':
    p9382B = cP9382B()
    p9382B.Setup()
    pass