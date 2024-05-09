import pyvisa as visa
from pyvisa.resources import TCPIPInstrument
import time
import os
import numpy as np
import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir.DeviceBase import cDeviceBase
from TestDir.TestItem import cTestItem

class cOscillograph(cDeviceBase):
    def __init__(self, name):
        super(cOscillograph, self).__init__(name)
        try:
            self.ip = str
            self.rm = visa.ResourceManager()
            self.scope = visa.Resource
            #self.scope = MSO4B
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            self.confIns.LoadConfiogure()
            self.connected:bool = False
            self.cycle: int
            self.vLenth:float
        except Exception as e:
            print(str(e))
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)

    def Setup(self):
        try:
            self.ip = str(self.confIns.ReadValue(self.confkeyIns.SEC_OSC, self.confkeyIns.KEY_IP))
            #self.cycle = int(self.confIns.ReadValue(self.confkeyIns.SEC_OSC, self.confkeyIns.KEY_CYCLE))
            #self.vLenth = ((float(self.confIns.ReadValue(self.confkeyIns.SEC_OSC, self.confkeyIns.KEY_V_LENTH)) * 1000) % 40 + 1) * 0.040
            resource_address = f'TCPIP0::{self.ip}::inst0::INSTR'
            self.scope = self.rm.open_resource(resource_address)
            self.scope.timeout = 4000
            self.connected = True
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False

    def Open(self):
        try:
            self.scope.open()
            self.connected = True
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False

    def isOpen(self):
        try:
            if not self.connected:
                return self.Open()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False

    def Close(self):
        try:
            self.scope.close()
            self.rm.close()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False

    def init(self):
        try:
            # with DeviceManager(verbose=True):
            #     # self.scope.write("*IDN?")
            #     # self.scope.write("HEADer OFF")
            #     # 示波器复位
            #     self.scope.commands.rst.write()
            #     # 示波器自动设置，autoset
            #     self.scope.commands.autoset.write('EXECute')
            #     # 等待并确保上一步执行完成，以下相同
            #     self.scope.commands.opc.query()
            return True
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False

    # def test(self):
    #     try:
    #         ############################################################################
    #         # channels        = ['CH1' ,'CH2', 'CH3', 'CH4', 'CH5', 'CH6']
    #         channels = ['CH1', 'CH2', 'CH3', 'CH4']
    #         channels_len = len(channels)
    #         ############################################################################
    #
    #         ############################################################################
    #         sampleRate = 625e6
    #         recordLen = 125e3
    #         vScales = [0.5, 0.2, 0.3, 0.4]
    #         vOffsets = [0.1, 0.2, -0.1, -0.2]
    #         vPositions = [0.1, 0.2, -0.1, -0.2]
    #         vExtAttens = [1, 2, 3, 4]
    #         self.set_horizontal(self.scope, sampleRate, recordLen)
    #         self.set_channel_status(self.scope, channels, [1, 1, 1, 1])
    #         self.set_vertical(self.scope, channels, vScales, vOffsets, vPositions, vExtAttens)
    #         self.set_vertical_unit(self.scope, ['CH1', 'CH3'], ['mW', 'dBm'], [1000, 2])
    #         self.set_trigger_edge(self.scope, 'CH1', 'DC', 0.1, 'RISE')
    #         self.acquire_single(self.scope, 2, True)
    #
    #         record_len = int(self.scope.query('HORizontal:RECOrdlength?').rstrip('\n'))
    #         dataStart = 1
    #         dataStop = record_len
    #
    #         start = time.time()
    #         time_data, volt_data = self.transfer_wfm(self.scope, channels, dataStart, dataStop)
    #         end = time.time()
    #         print('the total time is ', end - start, 's')
    #
    #         self.transfer_screenshot(self.scope, "C:\\temp", "11.png")
    #
    #         plt.plot(time_data, volt_data[0])
    #         plt.plot(time_data, volt_data[1])
    #         plt.plot(time_data, volt_data[2])
    #         plt.plot(time_data, volt_data[3])
    #         # plt.plot(time_data, volt_data[4])
    #         # plt.plot(time_data, volt_data[5])
    #         plt.grid()
    #         plt.show()
    #         ############################################################################
    #         return True
    #     except Exception as e:
    #         GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
    #         return False
    #
    # def test(self):
    #     testList = []
    #     tempItem =  cTestItem()
    #     tempItem.TestValue = '9999'
    #     tempItem.TestName = 'OSC'
    #     try:
    #
    #         with DeviceManager(verbose=True) as device_manager:
    #
    #             # 这里输入仪器的IP
    #             # scope: MSO4B = device_manager.add_scope("192.168.3.25")
    #             scope: MSO4B = device_manager.add_scope(self.ip)
    #             # scope: MSO4B = device_manager.add_scope("TCPIP0::10.10.10.10::inst0::INSTR")
    #
    #             # 读取仪器信息
    #             print(scope.commands.idn.query())
    #             # 示波器复位
    #             scope.commands.rst.write()
    #             # 示波器自动设置，autoset
    #             scope.commands.autoset.write('EXECute')
    #             # 等待并确保上一步执行完成，以下相同
    #             scope.commands.opc.query()
    #             # 设置示波器单次触发
    #             scope.commands.acquire.stopafter.write('SEQuence')
    #             scope.commands.acquire.state.write('1')
    #             # 添加测量项，测量类型为频率
    #             # scope.commands.measurement.addmeas.write('FREQuency')
    #             # 添加测量项，测量类型为RMS
    #             scope.commands.measurement.addmeas.write('RMS')
    #             scope.commands.opc.query()
    #
    #             #设置刻度为40ns
    #             scope.commands.horizontal.scale.write('4.0e-08')
    #             # 设置AB光标位置,2.0e-6表示2us
    #             # 一个周期是74ns，此处计算5个周期，总共370ns
    #             scope.commands.display.waveview1.cursor.cursor1.vbars.aposition.write('-1.85e-07')
    #             scope.commands.display.waveview1.cursor.cursor1.vbars.bposition.write('1.85e-07')
    #             scope.commands.opc.query()
    #
    #             # 设置测量项选通类型为光标
    #             scope.commands.measurement.gating.write('CURSor')
    #             scope.commands.opc.query()
    #             print(scope.commands.measurement.gating.query())
    #
    #             # 回读测量项1的数值
    #             Meas1_Val = float(scope.commands.measurement.meas[1].results.allacqs.mean.query())
    #             scope.commands.opc.query()
    #             # print(Meas1_Val)
    #             print(f'value:{Meas1_Val}')
    #             tempItem.TestValue = f'{round(Meas1_Val * 1000, 4)}'
    #             testList.append(tempItem)
    #         return True, testList
    #     except Exception as e:
    #         GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
    #         print(str(e))
    #         return False, testList

    def test(self):
        #testList = []
        tempItem =  cTestItem()
        tempItem.TestValue = '9999'
        #tempItem.TestName = 'OSC'
        tempItem.TestUnit = 'mA'
        try:
            self.scope.write(':MEASUrement:MEAS1:TYPE RMS')
            self.scope.write(':MEASUrement:MEAS1:SOURCE CH1')
            self.scope.write('DISplay:WAVEView1:CURSor:CURSOR1:STATE 1')
            self.scope.write(':HORizontal:SCAle 4.0E-8')
            #self.scope.write(':CH1:SCAle 2.0E-02;')

            self.scope.write('DISPLAY:WAVEVIEW1:CURSOR:CURSOR1:VBARS:APOSITION -1.85E-07')
            self.scope.write('DISPLAY:WAVEVIEW1:CURSOR:CURSOR1:VBARS:BPOSITION 1.85E-07')
            self.scope.write('MEASUrement:GATing CURSOR')
            time.sleep(2)
            value0 = float(self.scope.query('MEASUrement:MEAS1:RESUlts:ALLAcqs:MEAN?'))
            tempItem.TestValue = f'{round(value0 * 1000, 4)}'
            #testList.append(tempItem)
            return True, tempItem
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(str(e))
            return False, tempItem
    def set_sample_rate(self, scope, sampleRate):
        cmdStr = ':HORizontal:MODE MANual;' + \
                 ':HORizontal:MODE:SAMPLERate %s' % sampleRate
        scope.write(cmdStr)

    def set_record_len(self, scope, recordLen):
        cmdStr = ':HORizontal:MODE MANual;' + \
                 ':HORizontal:MODE:RECOrdlength %s' % recordLen
        scope.write(cmdStr)

    def set_time_scale(self, scope, timeScale):
        cmdStr = ':HORizontal:MODE MANual;' + \
                 ':HORizontal:SCAle %s' % timeScale
        scope.write(cmdStr)

    def set_horizontal(self, scope, sampleRate, recordLen):
        cmdStr = ':HORizontal:MODE MANual;' + \
                 ':HORizontal:MODE:SAMPLERate %s;' % sampleRate + \
                 ':HORizontal:MODE:RECOrdlength %s' % recordLen
        scope.write(cmdStr)

    def set_channel_status(self, scope, channels, channelStatuses):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':DISplay:GLObal:%s:STATE %s;' % (channel, channelStatuses[i])
        scope.write(cmdStr)

    def set_vertical_scale(self, scope, channels, scales):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:SCAle %s;' % (channel, scales[i])
        scope.write(cmdStr)

    def set_vertical_offset(self, scope, channels, offsets):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:OFFSet %s;' % (channel, offsets[i])
        scope.write(cmdStr)

    def set_vertical_position(self, scope, channels, positions):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:POSition %s;' % (channel, positions[i])
        scope.write(cmdStr)

    def set_vertical_external_attenuation(self, scope, channels, extAttens):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:PROBEFunc:EXTAtten %s;' % (channel, extAttens[i])
        scope.write(cmdStr)

    def set_vertical_unit(self, scope, channels, units, scaleRatios):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:PROBEFunc:EXTUnits:STATE ON;' % channel
            cmdStr += ':%s:PROBEFunc:EXTUnits "%s";' % (channel, units[i])
            cmdStr += ':%s:SCALERATio %s;' % (channel, scaleRatios[i])
        scope.write(cmdStr)

    def set_vertical(self, scope, channels, scales, offsets=None, positions=None, extAttens=None):
        cmdStr = ''
        for i, channel in enumerate(channels):
            cmdStr += ':%s:SCAle %s;' % (channel, scales[i])
            if offsets != None:
                cmdStr += ':%s:OFFSet %s;' % (channel, offsets[i])

            if positions != None:
                cmdStr += ':%s:POSition %s;' % (channel, positions[i])

            if extAttens != None:
                cmdStr += ':%s:PROBEFunc:EXTAtten %s;' % (channel, extAttens[i])
        scope.write(cmdStr)

    def set_trigger_edge(self, scope, source='CH1', coupling='DC', triggerLevel=0, slope='RISE'):
        cmdStr = ':TRIGger:A:TYPe EDGE;' + \
                 ':TRIGger:A:EDGE:SOUrce %s;' % source + \
                 ':TRIGger:A:EDGE:COUPling %s;' % coupling + \
                 ':TRIGger:A:LEVel:%s %s;' % (source, triggerLevel) + \
                 ':TRIGger:A:EDGE:SLOpe %s' % slope
        scope.write(cmdStr)

    def acquire_single(self, scope, timeout, forceTrigger):
        ############################################################################
        ## waiting the scope to trigger and acq the waveform
        cmdStr = ':ACQuire:STATE STOP;' + \
                 ':ACQuire:STOPAfter SEQuence;' + \
                 ':ACQuire:SEQuence:NUMSEQuence 1;' + \
                 ':ACQuire:STATE RUN;'
        scope.write(cmdStr)

        start = time.time()
        while '0' not in scope.query('ACQuire:STATE?'):
            end = time.time()
            if 'READY' in scope.query('TRIGger:STATE?') and end - start > timeout and forceTrigger == False:
                break
            elif 'READY' in scope.query('TRIGger:STATE?') and end - start > timeout and forceTrigger == True:
                scope.write('TRIGger FORCe')
        ############################################################################

    def transfer_wfm(self, scope, channels, dataStart, dataStop):
        ############################################################################
        ## specify channel sources of the transferred waveforms
        channels_str = ''
        channels_len = len(channels)

        data_len = dataStop - dataStart + 1

        for channel in channels:
            channels_str = channels_str + channel + ', '
        channels_str = channels_str[0:-2]
        scope.write('DATa:SOUrce %s' % channels_str)
        # scope.query('DATa:SOUrce?')
        ############################################################################

        ############################################################################
        scope.write('DATa:ENCdg RIBinary')
        # scope.query('DATa:ENCdg?')

        scope.write('WFMOutpre:BYT_Nr 2')
        # scope.query('WFMOutpre:BYT_Nr?')

        scope.write('DATa:STARt %s' % dataStart)
        scope.write('DATa:STOP %s' % dataStop)
        # scope.query('DATa:STARt?')
        # scope.query('DATa:STOP?')
        ############################################################################

        ############################################################################
        ## get the waveform infos(WFMOutpre?)
        digitScales = [0] * channels_len
        digitZeros = [0] * channels_len
        digitOffsets = [0] * channels_len
        for idx, channel in enumerate(channels):
            scope.write('DATa:SOUrce %s' % channel)
            scope.write('WFMOutpre?')
            WFMOut_bytes = scope.read_raw()
            WFMOut_bytes_list = WFMOut_bytes.split(b';')
            print(WFMOut_bytes)
            if idx == 0:
                data_format = WFMOut_bytes_list[3].decode('ascii')
                nbytes_per_point = int(WFMOut_bytes_list[0].decode('ascii'))

                horiz_xincr = float(WFMOut_bytes_list[11].decode('ascii'))
                horiz_xzero = float(WFMOut_bytes_list[12].decode('ascii'))
                horiz_pt_offset = int(WFMOut_bytes_list[13].decode('ascii'))

            digitScales[idx] = float(WFMOut_bytes_list[15].decode('ascii'))
            digitOffsets[idx] = float(WFMOut_bytes_list[16].decode('ascii'))
            digitZeros[idx] = float(WFMOut_bytes_list[17].decode('ascii'))
            ############################################################################

        ############################################################################
        ## get the waveform data
        chunk_size = nbytes_per_point * data_len * channels_len
        # scope.write('DATa:SOUrce %s' % channels_str)
        # scope.write('CURVE?')
        # <add>

        all_data = []
        # </add>
        for ii in range(1):
            scope.write('DATa:SOUrce %s' % channels_str)
            scope.write('CURVE?')
            time.sleep(0.10)
            raw_data = scope.read_raw(chunk_size)
            ############################################################################

            ############################################################################
            raw_data_channel_len = int(len(raw_data) / channels_len)
            raw_data_list = [bytearray()] * channels_len
            for idx in range(0, channels_len):
                raw_data_list[idx] = raw_data[idx * raw_data_channel_len: (idx + 1) * raw_data_channel_len]

            ## calculate the time axis
            time_data = horiz_xzero + (np.arange(data_len) - horiz_pt_offset) * horiz_xincr

            ## calculate the voltage axis
            if 'RI' in data_format:
                if nbytes_per_point == 1:
                    unpack_fmt = '>b'
                elif nbytes_per_point == 2:
                    unpack_fmt = '>h'
                elif nbytes_per_point == 4:
                    unpack_fmt = '>l'

                volt_data = np.zeros((channels_len, data_len))
                for idx, raw_data_channel in enumerate(raw_data_list):
                    offset, _ = visa.util.parse_ieee_block_header(raw_data_list[idx])
                    digit = np.frombuffer(raw_data_channel, unpack_fmt, data_len, offset)
                    volt_data[idx] = digitZeros[idx] + digitScales[idx] * (np.array(digit) - digitOffsets[idx])
            ############################################################################
            all_data.append(volt_data)
            time.sleep(0.05)

        # return time_data, volt_data
        return time_data, all_data
        # scope.write('DATa:SOUrce %s' % channels_str)
        # scope.write('CURVE?')
        # raw_data = scope.read_raw(chunk_size)
        # ############################################################################
        #
        # ############################################################################
        # raw_data_channel_len = int(len(raw_data) / channels_len)
        # raw_data_list = [bytearray()] * channels_len
        # for idx in range(0, channels_len):
        #     raw_data_list[idx] = raw_data[idx * raw_data_channel_len: (idx + 1) * raw_data_channel_len]
        #
        # ## calculate the time axis
        # time_data = horiz_xzero + (np.arange(data_len) - horiz_pt_offset) * horiz_xincr
        #
        # ## calculate the voltage axis
        # if 'RI' in data_format:
        #     if nbytes_per_point == 1:
        #         unpack_fmt = '>b'
        #     elif nbytes_per_point == 2:
        #         unpack_fmt = '>h'
        #     elif nbytes_per_point == 4:
        #         unpack_fmt = '>l'
        #
        #     volt_data = np.zeros((channels_len, data_len))
        #     for idx, raw_data_channel in enumerate(raw_data_list):
        #         offset, _ = visa.util.parse_ieee_block_header(raw_data_list[idx])
        #         digit = np.frombuffer(raw_data_channel, unpack_fmt, data_len, offset)
        #         volt_data[idx] = digitZeros[idx] + digitScales[idx] * (np.array(digit) - digitOffsets[idx])
        # ############################################################################
        #
        # return time_data, volt_data

    def transfer_screenshot(self, scope, fileDir, fileName):
        ############################################################################
        ## check the file format
        fileExt = os.path.splitext(fileName)[1]
        if fileExt == '':
            fileExt = '.jpg'
            fileName = fileName + fileExt
        elif fileExt != '.bmp' or fileExt != '.BMP' or fileExt != '.jpg' or fileExt != '.JPG' or fileExt != '.png' or fileExt != '.PNG':
            pass
        ############################################################################

        ############################################################################
        scopeDir = "C:\\temp"
        scope.write('FILESystem:CWD "C:\\"')
        scope.write('FILESystem:MKDir "temp"')

        scope.write('SAVe:IMAGe "%s"' % (scopeDir + '\\' + fileName))
        scope.query('*OPC?')
        scope.write('FILESystem:READFile "%s"' % (scopeDir + '\\' + fileName))
        img_data = scope.read_raw()
        ############################################################################

        ############################################################################
        filePath = fileDir + '\\' + fileName
        if os.path.isdir(fileDir):
            pass
        else:
            os.makedirs(fileDir)

        fid = open(filePath, 'wb')
        fid.write(img_data)
        fid.close()
        ############################################################################


if __name__ == '__main__':
    osc = cOscillograph('OSC')
    #osc.Setup()
    #osc.init()
    #resu,value = osc.test()
    # rem = visa.ResourceManager()
    # print(rem.list_resources())
    # device = rem.open_resource(f"TCPIP0::169.254.6.209::inst0::INSTR")
    # #TCPIP0::10.10.10.10::inst0::INSTR
    # device.timeout = 3000
    # device.write(':MEASUrement:MEAS1:TYPE RMS')
    # device.write(':MEASUrement:MEAS1:SOURCE CH1')
    # device.write('DISplay:WAVEView1:CURSor:CURSOR1:STATE 1')
    # device.write(':HORizontal:SCAle 4.0E-8')
    #
    # device.write('DISPLAY:WAVEVIEW1:CURSOR:CURSOR1:VBARS:APOSITION -1.85E-07')
    # device.write('DISPLAY:WAVEVIEW1:CURSOR:CURSOR1:VBARS:BPOSITION 1.85E-07')
    # device.write('MEASUrement:GATing CURSOR')
    # time.sleep(0.5)
    # value0 = device.query('MEASUrement:MEAS1:RESUlts:ALLAcqs:MEAN?')
    # value1 = round(float(value0) * 1000, 4)
    #result = format(3141.5926, '0.1E')
    value0 = '3141.5926'
    value1 = 3.1415926535
    #result = f'{value0:0.1E}'
    print(0.1 + 0.2)
    pass