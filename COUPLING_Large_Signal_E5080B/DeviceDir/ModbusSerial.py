from pymodbus.client import ModbusSerialClient
from pymodbus.pdu import ModbusResponse
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir.DeviceBase import cDeviceBase
from DeviceDir import Macro
import GlobalGui
from TestDir.TestItem import cTestItem

class cModbusSerial(cDeviceBase):
    def __init__(self, name):
        super(cModbusSerial, self).__init__(name)
        self.set_name(name)
        try:
            self.port = str
            self.baud = int
            self.client = None #ModbusSerialClient(method='rtu')
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            self.temp_offset = 0.0
            print("modbusSerial:%s", self.get_name())
        except Exception as e:
            print(e)

    def Setup(self):
        try:
            self.temp_offset = float(self.confIns.ReadValue(self.confkeyIns.SEC_APP, self.confkeyIns.SEC_TEMP_OFFSET))

            # self.port = self.confIns.ReadValue(self.confkeyIns.SEC_TEMP, self.confkeyIns.KEY_PORT)
            # self.baud = int(self.confIns.ReadValue(self.confkeyIns.SEC_TEMP, self.confkeyIns.KEY_BAUD))

            self.client = ModbusSerialClient(method='rtu',port = self.port, baudrate = self.baud)
            print("modbusSerial-STUEP")
            return True
        except Exception as e:
            print(e)
            return False

    def Open(self):
        try:
            #if not self.client.connected:
            self.client.connect()
            print("modbusSerial-Open")
            return True
        except Exception as e:
            print(e)
            return False

    def Close(self):
        try:
            #if self.client.connected:
            self.client.close()
            return True
        except Exception as e:
            print(e)
            return False

    def Write_register(self, address: int = 1, slave: int = 1, value = int): #写入寄存器
        try:
            #if self.client.connected:
            #if self.client.connected:
            result = self.client.write_register(address=address, value=value, slave=slave)
                # self.client.write_register(address=0, value=data)
            if result != None and not result.isError():
                return True, result
            return False, ModbusResponse()
        except Exception as e:
            print(e)
            return False, ModbusResponse()

    def Read_holding_registers(self, address: int = 1, count: int = 1, slave: int = 1): #读取寄存器
        try:
            #if self.client.connected:
            result = self.client.read_holding_registers(address=address, count=count, slave=slave)
            if result != None and not result.isError():
                return True, result
            return False, ModbusResponse()
        except Exception as e:
            print(e)
            print('dump to')
            return False, ModbusResponse()

    def ReadTemperature(self):
        testItemList = []
        try:

            temperature:float = 0.0
            result, data = self.Read_holding_registers(0,1,1)
            if not result:
                print('block1')
                return False, testItemList
            print('calum', data.registers[0])
            decimalPoint = int(data.registers[0]) // 10000
            tmpV = data.registers[0] % 10000
            #tmpV = tmpV > 1210 and tmpV - 4 or tmpV
            if decimalPoint <= 0:
                temperature = (tmpV - 1000) / 0.75 * 0.1
            else:
                temperature = (tmpV - 1000) / 0.75 * 0.1

            temperature =temperature + float(self.temp_offset)
            #GlobalGui.global_Gui.TextBrowserSignal.emit(str(temperature), 'red', False)
            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName = 'temperature'
            tmpTestitem.TestUnit = 'Celsius'
            tmpTestitem.TestValue = str(temperature)
            testItemList.append(tmpTestitem.Clone())
            return True, testItemList
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            print('dump in this block')
            return False, testItemList

    def ReadSurroundsTemperature(self):
        testItemList = []
        try:

            temperature: float = 0.0
            result, data = self.Read_holding_registers(0x2000, 1, 1)
            if not result:
                print('ReadSurroundsTemperature block')
                return False, testItemList
            temperature = float(data.registers[0])

            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName = 'SurroundsTemperature'
            tmpTestitem.TestUnit = 'Celsius'
            tmpTestitem.TestValue = str(temperature)
            testItemList.append(tmpTestitem.Clone())
            return True, testItemList
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            print('dump in ReadSurroundsTemperature block')
            return False, testItemList






