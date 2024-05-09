import socket
import time
import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase


class cRobot(cDeviceBase):
    def __init__(self, name, port = int):
        super(cRobot, self).__init__(name)
        self.set_name("ROBOT")
        try:
            self.Login0 = '$Login,0'
            self.Reset = '$Reset'
            self.Start = '$Start,0'
            self.Stop = '$Stop'
            self.Logout = '$Logout'

            self.IP = str
            self.port = port
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("robot:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            self.IP = self.confIns.ReadValue(self.confkeyIns.SEC_ROBOT, self.confkeyIns.KEY_IP)
            #self.port = self.confIns.ReadValue(self.confkeyIns.SEC_ROBOT, self.confkeyIns.KEY_PORT)


            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
            #self.client.setblocking(True)
            # self.client.ioctl(socket.SIO_KEEPALIVE_VALS,
            #                   (1,         # 开启保活机制
            #                    60*1000,   # 1分钟后无反应，检测是否存在连接
            #                    30*1000)   # 30s检测一次，默认探测10次，失败则断开
            #                   )
            return True
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False

    def Open(self):
        try:
            self.client.connect((self.IP, self.port))
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

    def Write(self, msg):
        try:
            tmpMsg = msg +'\r\n'
            n = self.client.send(tmpMsg.encode('utf-8'))
            print('发送的字节数:' + str(n))
            return True
        except Exception as e:
            print(e+"Robot write error"+msg)
            return False

    def Read(self, lenght=int):
        try:
            bytes = self.client.recv(lenght)
            return bytes
        except Exception as e:
            print(e)
            return None

    def Init(self, timeout=int):   #  运动到初始位置
        try:
            sendCMD = 'init'
            n = self.client.send((sendCMD+'\r\n').encode('utf-8'))
            print('发送的字节数:' + str(n))
            time.sleep(0.5)
            self.client.settimeout(timeout)
            data = self.client.recv(1024)
            #data += str(data.decode('utf-8'))
            print('接受的数据为:' +str(data))
            GlobalGui.global_Gui.TextBrowserSignal.emit('init 接受的数据为:' + str(data), 'black', False)
            if 'init OK' in str(data):
                return True
            return False
            pass
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e)+"Init P2", 'red', False)
            return False

    def Move(self, x_Loc, y_Loc, z_Loc, u_Loc, v_Loc, w_Loc, timeout=2):
        try:
            tmpLoc = 'A {0} {1} {2} {3} {4} {5}'.format(x_Loc, y_Loc, z_Loc, u_Loc, v_Loc, w_Loc)
            n = self.client.send((tmpLoc + '\r\n').encode('utf-8'))
            print('发送的字节数:' + str(n))
            self.client.settimeout(timeout)
            data = self.client.recv(1024)
            data = str(data.decode('utf-8'))
            print('接受的数据为:' + data)
            GlobalGui.global_Gui.TextBrowserSignal.emit('move 接受的数据为:' + data.split("/R")[0], 'black', False)
            if '{0} OK'.format(tmpLoc) in data:
                time.sleep(0.2)
                return True
            return False
        except Exception as e:
            print(e)
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e)+"Move Error", 'red', False)
            return False



    def GetPoint(self, timeout=int):
        try:
            sendCMD = 'here'
            n = self.client.send((sendCMD + '\r\n').encode('utf-8'))
            print('发送的字节数:' + str(n))
            self.client.settimeout(timeout)
            data = self.client.recv(1024)
            data = str(data.decode('utf-8'))
            print('接受的数据为:' + data)
            if 'here OK' in data:
                loca = data.split(',')
                tmpPoit = loca[1].split(':')

                tmp_x = tmpPoit[1].split(':')
                tmp_y = tmpPoit[2].split(':')
                tmp_z = tmpPoit[3].split(':')
                tmp_u = tmpPoit[4].split(':')
                tmp_v = tmpPoit[5].split(':')
                tmp_w = tmpPoit[6].split(':')
                return True, tmp_x, tmp_y, tmp_z, tmp_u, tmp_v, tmp_w
            return False, None
            pass
        except Exception as e:
            print(e)
            return False, None


