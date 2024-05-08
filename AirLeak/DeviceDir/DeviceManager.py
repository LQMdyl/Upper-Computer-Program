
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir.DeviceBase import cDeviceBase
from DeviceDir.Modbusclient import cModbusclient
from DeviceDir.Scan import cScan
from DeviceDir.WorkerIntegra import cWorkerIntegra
from GlobalDir.GlobalGui import global_Gui
from GlobalDir import GlobalConf


class cDeviceManager():
    def __init__(self):
        self._Devices = {str : cDeviceBase}
        self.isConnect = False

    def ALLDevices(self):
        return self._Devices

    def Devices(self, key=' '):
        if not key == None:
            if key in self._Devices.keys():
                return self._Devices[key]

    def InitializeDevice(self):
        self._Devices.clear()
        self.confIns = cConfigure()
        if len(self.confIns.ConfigureDic) == 0:
            self.confIns.loadConfigure()
        self.confKey = ConfigureKey

        # PLC
        tmpkey = GlobalConf.PLC
        plc = cModbusclient(tmpkey)
        if plc is None or not plc.Setup() or not plc.Open():
            global_Gui.tbvwLogEmit('PLC连接失败', 'red', False)
            #global_Gui.tbvwLogEmit('Connection failure of PLC', 'red', False)
            self.isConnect = False
            global_Gui.lblDeviceStatusEmit(GlobalConf.PLC, False)
        else:
            dicPlc = {tmpkey: plc}
            self._Devices.update(dicPlc)
            global_Gui.tbvwLogEmit('PLC连接成功', 'green', False)
            #global_Gui.tbvwLogEmit('PLC connection succeeded', 'green', False)
            global_Gui.lblDeviceStatusEmit(GlobalConf.PLC, True)
            self.isConnect = True

        # SCAN
        if self.confIns.ConfigureDic[self.confKey.SEC_APP][self.confKey.KEY_SCAN_TYPE] == 'A':
            tmpkey = GlobalConf.SCAN
            scan = cScan(tmpkey)
            if scan is None or not scan.Setup() or not scan.Open():
                global_Gui.tbvwLogEmit('扫码枪连接失败', 'red', False)
                global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, False)
                self.isConnect &= False
            else:
                dicScan = {tmpkey:scan}
                self._Devices.update(dicScan)
                global_Gui.tbvwLogEmit('扫码枪连接成功', 'green', False)
                global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, True)
                self.isConnect &= True
        # #SCAN
        # if self.confIns.ConfigureDic[self.confKey.SEC_SCAN][self.confKey.KEY_AUTO_SCAN] == 'Y':
        #     camera_index = GlobalConf.CAMERA_INDEX
        #     tmpCamera = Camera()
        #     camera = tmpCamera.find_camera(camera_index)
        #     if camera is None:
        #         global_Gui.tbvwLogEmit('扫码枪连接失败', 'red', False)
        #         global_Gui.tbvwLogEmit('Connection failure of SCAN', 'red', False)
        #         global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, False)
        #         return False
        #     dicScan = {GlobalConf.SCAN: camera}
        #     self._Devices.update(dicScan)
        #     global_Gui.tbvwLogEmit('扫码枪连接成功', 'green', False)
        #     global_Gui.tbvwLogEmit('SCAN connection succeeded', 'green', False)
        #     global_Gui.lblDeviceStatusEmit(GlobalConf.SCAN, True)
        # workerIntegra
        tmpkey = GlobalConf.WORKER_INTEGRA
        workerIntegra = cWorkerIntegra(tmpkey)
        if workerIntegra is None or not workerIntegra.Setup() or not workerIntegra.Open():
            global_Gui.tbvwLogEmit('workerIntegra连接失败', 'red', False)
            global_Gui.tbvwLogEmit('Connection failure of workerIntegra', 'red', False)
            global_Gui.lblDeviceStatusEmit(GlobalConf.WORKER_INTEGRA, False)
            self.isConnect &= False
        else:
            dicWorkerIntegra = {tmpkey: workerIntegra}
            self._Devices.update(dicWorkerIntegra)
            global_Gui.tbvwLogEmit('workerIntegra连接成功', 'green', False)
            global_Gui.tbvwLogEmit('workerIntegra connection succeeded', 'green', False)
            global_Gui.lblDeviceStatusEmit(GlobalConf.WORKER_INTEGRA, True)
            self.isConnect &= True
        return self.isConnect






