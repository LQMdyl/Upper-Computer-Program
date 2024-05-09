import time
import socket

import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase


class CCD(cDeviceBase):
    def __init__(self, name):
        super(CCD, self).__init__(name)
        self.set_name(Macro.CAMREA)
        try:
            self.IP = str
            self.port = str
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("hawk:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            confIns = cConfigure()
            confkeyIns = ConfigureKey
            self.IP = confIns.ReadValue(confkeyIns.SEC_CAMERA, confkeyIns.KEY_IP)
            self.port = confIns.ReadValue(confkeyIns.SEC_CAMERA, confkeyIns.KEY_PORT)

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.client.connect((self.IP, int(self.port)))
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Close(self):
        try:
            self.client.close()
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def GetData(self,count=int):
        try:
            Distance=0.0
            Angle=0.0
            for i in range(count):
                command = "trigger\r\n"
                self.client.send( command.encode())
                self.client.settimeout(2)
                data = self.client.recv( 1024 )
                Tmp = data.decode( "UTF-8" ).split( "," )
                if len( Tmp ) != 2:
                    return False, 0.0, 0.0
                Angle +=float(Tmp[0])
                Distance +=float(Tmp[1].replace( "\r", "" ).replace( "\n", "" ))
                time.sleep(0.2)

            return True,round(Distance/count,4),round(Angle/count,4)
            pass
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, 0.0,0.0





