from pymodbus.client import ModbusTcpClient
#macOS from pymodbus.client.sync import ModbusTcpClient
from GlobalDir import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from GlobalDir import GlobalConf
from DeviceDir.DeviceBase import cDeviceBase

class cModbusclient(cDeviceBase):
    def __init__(self, name):
        super(cModbusclient, self).__init__(name)
        self.set_name(GlobalConf.PLC)
        try:
            # M6-M7 （自动动）自动运行，复位  1触发，0无状态
            # M30 M35 (PC写) 运行，复位 1触发
            # M32 M37 (PC写) 停止 1触发
            # D100 plc通知测试 1触发
            # D102 (pc写)测试完成 1触发
            # (M10)紧急停止、(M12)光幕异常、(M19)自动中触发光幕报警、(M26)负压表1数值异常、(M27)负压表2数值异常1触发
            self.port = str
            self.baud = int
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            self.client = None
            self.clientconnected = False
            print("modbusTcp:%s", self.get_name())
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            self.ip = self.confIns.ConfigureDic[self.confkeyIns.SEC_PLC][self.confkeyIns.KEY_PLC_IP]
            self.port = self.confIns.ConfigureDic[self.confkeyIns.SEC_PLC][self.confkeyIns.KEY_PORT]
            self.client = ModbusTcpClient(host = self.ip, port = self.port)
            return True
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False

    def Open(self):
        try:
            if not self.clientconnected:
                self.client.connect()
                self.clientconnected = True
            return self.clientconnected
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False

    def Close(self):
        try:
            if self.clientconnected:
                self.client.close()
            return self.clientconnected
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False

    def Read_coils_msg(self):
        try:
            allValue = []
            if self.clientconnected:
                allValue.append(self.client.read_coils(slave = 1, address = 6, count = 1).bits[0])
                allValue.append(self.client.read_coils(slave = 1, address = 10, count = 1).bits[0])
                allValue.append(self.client.read_coils(slave = 1, address = 12, count = 1).bits[0])
                allValue.append(self.client.read_coils(slave = 1, address = 19, count = 1).bits[0])
                allValue.append(self.client.read_coils(slave = 1, address = 26, count = 1).bits[0])
                allValue.append(self.client.read_coils(slave=1, address=27, count=1).bits[0])
                return True, allValue
            return False, allValue
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False, allValue

    def Read_coils2(self, add = int, cnt = int):
        try:
            value =None
            if self.clientconnected:
                value = self.client.read_coils(slave = 1, address = add, count = cnt)
                return True, value.bits
            return False
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False, None

    def Write_coil(self, add =int, value1 = bool):
        try:
            if self.clientconnected:
                self.client.write_coil(slave = 1, address = add, value= value1)
                return True
            return False
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            return False

    def Read_holding_registers(self, add =int, cnt = int):
        try:
            value =None
            if self.clientconnected:
                value = self.client.read_holding_registers(slave = 1, address = add, count = cnt)
                return True, value.registers[0]
            return False, None
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False, None

    def Write_register(self, add =int, value1 = int):
        try:
            if self.clientconnected:
                self.client.write_register(slave=1, address=add, value= value1)
                return True
            return False
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False

    def Read_Start(self):
        try:
            if self.clientconnected:
                res, value = self.Read_holding_registers(100, 1)
                #GlobalGui.global_Gui.tbvwLogEmit('D100:'+str(value), 'black', False)
                if res:
                    return True,value
            return False,value
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False,value
    def Write_Hold_register(self, add, value):
        try:
            if self.clientconnected:
                self.client.write_register(slave = 1, address = add, value=value)
                return True
            return False
        except Exception as e:
            GlobalGui.global_Gui.tbvwLogEmit(str(e), 'red', False)
            print(e)
            return False
    def isOpen(self):
        return self.clientconnected


if __name__ == '__main__':
    tmpdic = {'abc':'13', 'cdf':'555', 'eds':'796'}
    print('13' in tmpdic.values())