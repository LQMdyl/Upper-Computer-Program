import time
import socket

import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase


class cHawk(cDeviceBase):
    def __init__(self, name):
        super(cHawk, self).__init__(name)
        self.set_name(Macro.HWAK)
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
            self.IP = confIns.ReadValue(confkeyIns.SEC_HAWK, confkeyIns.KEY_IP)
            self.port = confIns.ReadValue(confkeyIns.SEC_HAWK, confkeyIns.KEY_PORT)

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

    def clearSocketBuffer(self):
        try:
            self.client.settimeout(0.5)
            data = self.client.recv( 1024 )
            pass
        except Exception as e:
            return

    def Close(self):
        try:
            self.client.close()
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def GetBarcde(self, lenght=int, timeout=int):
        try:
            self.clearSocketBuffer()
            triCMD = '<S>'
            n = self.client.send( triCMD.encode( 'utf-8' ) )
            print( '发送的字节数:' + str( n ) )
            self.client.settimeout( timeout )
            data = self.client.recv( 1024 )
            barcode = str( data.decode( 'utf-8' ) ).replace( '\r', '' ).replace( '\n', '' )
            print( '接受的数据为:' + barcode )
            if len( barcode ) >= lenght:
                return True, barcode
            return False, None
            pass
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None





