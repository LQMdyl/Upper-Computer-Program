import math
import time

import numpy
import pyvisa
from pyvisa.resources import TCPIPInstrument
import GlobalGui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from DeviceDir import Macro
from DeviceDir.DeviceBase import cDeviceBase
from TestDir.TestItem import cTestItem
from DeviceDir.Oscillograph import cOscillograph

CAL_FILE = "D:\\STATE08.STA"
DEFAULT_STR = "13560"
DEBUG_MODE = False
class cVna(cDeviceBase):
    def __init__(self, name):
        super(cVna, self).__init__(name)
        try:
            self.IP = str
            self.port = str
            self.rem = pyvisa.ResourceManager()
            self.device: TCPIPInstrument = None
            self.frequencies:float =[300000]
            self.confIns = cConfigure()
            self.confkeyIns = ConfigureKey
            print("vna:%s", self.get_name())
            self.Knom_POWER_GAIN = ""
            self.Freeair_POWER_GAIN = ""
            self.ls_offset = "-0.04"
            self.rs_offset = "-118"
            self.TxRoffset=float
            self.RxRoffeset=float

            self.TxXoffset = float
            self.RxXoffeset = float

        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)

    def Setup(self):
        try:
            self.IP = self.confIns.ReadValue(self.confkeyIns.SEC_VNA, self.confkeyIns.KEY_IP)
            self.port = self.confIns.ReadValue(self.confkeyIns.SEC_VNA, self.confkeyIns.KEY_PORT)
            self.TxRoffset=float(self.confIns.ReadValue(self.confkeyIns.SEC_APP, self.confkeyIns.SEC_TxRoffset))
            self.RxRoffeset=float(self.confIns.ReadValue(self.confkeyIns.SEC_APP, self.confkeyIns.SEC_RxRoffset))

            self.TxXoffset = float( self.confIns.ReadValue( self.confkeyIns.SEC_APP, self.confkeyIns.SEC_TxXoffset ) )
            self.RxXoffeset = float( self.confIns.ReadValue( self.confkeyIns.SEC_APP, self.confkeyIns.SEC_RxXoffset ) )

            reIP = f"TCPIP::{self.IP}::INSTR"

            self.device: TCPIPInstrument = self.rem.open_resource(reIP)

            self.device.timeout = 3000  # ms
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Open(self):
        try:
            self.device.open()
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Close(self):
        try:
            self.device.close()
            self.rem.close()
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def Init(self):
        try:
            self.device.write('*CLS')
            self.device.write('*RST')
            self.device.write('*IDN?')
            strIDN = self.device.read()
            print(strIDN)
            # if 'E5071C' in strIDN:
            #     print('ok')
            # elif 'CNA' in strIDN:
            #     print('OK')
            # else:
            #     return False

            # load cal file
            if CAL_FILE:
                self.device.write(f'MMEM:LOAD:STAT "{CAL_FILE}"')
                print(f"Loaded calibration from '{CAL_FILE}'")

            # setup sweep 设置扫描
            sweep:float = []
            for f in self.frequencies:
                closest_freq, _ = self.get_closest_freq(f)
                sweep.append(closest_freq)
            self.set_sweep_segments(sweep)
            print("sweep is setup")

            # setup trigger
            self.device.write(":TRIG:SEQ:SOUR BUS")
            self.device.write(":INIT:CONT ON")
            print("trigger is setup")
            return True
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            print(e)
            return False

    def get_closest_freq(self, frequency):
        resp = self.device.query('SENS:FREQ:DATA?')
        freq_list = [float(x) for x in resp.split(',')]
        freq_index = min(range(len(freq_list)), key=lambda i: abs(frequency - freq_list[i]))
        closest_freq = freq_list[freq_index]
        return closest_freq, freq_index

    def set_sweep_segments(self, f_list):
        """
        Sets up a segment sweep of all frequencies in f_list.  If the number
        of points is odd, the final point is repeated.
        """

        # make the length of f_list even before continuing
        if len(f_list) % 2 != 0:
            f_list = f_list + [f_list[-1]]

        # set up the preamble
        buf = 5
        stim = 0
        ifbw = 0
        pow_ = 0
        del_ = 0
        dur = 0
        segm = len(f_list) / 2

        query_str = [str(x) for x in [buf, stim, ifbw, pow_, del_, dur, segm]]

        # write each segment of the table

        for star, stop in zip(f_list[0::2], f_list[1::2]):
            nop = 2
            query_str += ['%0.6g' % star, '%0.6g' % stop, str(nop)]

        # write segment data to the VNA
        query_str = ','.join(query_str)
        query_str = 'SENS:SEGM:DATA ' + query_str

        self.device.write(query_str)

        # enable segment-based sweep
        self.device.write("SENS1:SWE:TYPE SEGM")
        # self.update_freq_list() ???

    def set_power(self, dBm):
        self.device.write(":SOUR1:POW {}".format(dBm))

    def run_sweep(self):
        # Trigger once
        # Mac = self.confIns.ReadValue( self.confkeyIns.SEC_VNA, self.confkeyIns.SEC_MAC )
        # if Mac is not "mac":
        #     time.sleep(0.3)
        self.device.write(":TRIG:SEQ:SING")
        self.device.query("*OPC?")  # Wait for operation to complete

    def get_z(self, frequency):
        if DEBUG_MODE:
            import random
            return numpy.array([[1.7 + 20j, 1 + 10j], [1 + 10j, 0.6 + random.random() + 30j]]), frequency

        # Trigger once and get s params
        s, closest_freq = self.get_s_params(frequency)

        # Convert to Z
        z0 = float(self.device.query("SENS:CORR:IMP:INP:MAGN?"))
        sqrt_z = numpy.diag([math.sqrt(z0)] * 2)
        eye = numpy.identity(2)
        z = sqrt_z * (eye + s) * numpy.linalg.inv(eye - s) * sqrt_z
        return z, closest_freq

    # noinspection PyDeprecation
    def get_s_params(self, frequency):
        # Determine the frequency index
        closest_freq, freq_index = self.get_closest_freq(frequency)

        # Parse the response into an S matrix.  The returned string looks like
        # as below.  Note that the order of S11, S12, ..., Snn is the same as
        # the query_str sequence contructed above.
        #
        # S11[f1].real, S11[f1].imag, S11[f2].real, S11[f2].imag, ...
        # S12[f1].real, S12[f1].imag, S12[f2].real, S12[f2].imag, ...
        # ...
        # Snn[f1].real, Snn[f1].imag, Snn[f2].real, Snn[f2].imag, ...

        # generate a flat list of complex numbers from the query response
        raw_string = self.device.query('SENS:CORR:DATA:CDAT? "S11,S12,S21,S22"')
        s_params = [float(x) for x in raw_string.split(',')]
        s_params = numpy.matrix([s_params])
        s_params = s_params[0, 0::2] + 1j*s_params[0, 1::2]

        # filter the s_params list to only those parameters measured at the given frequency index
        num_freqs = numpy.size(s_params, 1) // 4
        s_params = s_params[0, freq_index::num_freqs]

        # reshape the s_params list into a matrix with dimensions num_ports x num_ports
        s_params_mat = numpy.reshape(s_params, (2, 2))

        return s_params_mat, closest_freq

    @staticmethod
    def z_to_q(z,offset=float,Roffset=float):
        if z.real != 0:
            return (z.imag-offset) / (z.real-Roffset)
        else:
            return 0.0

    @staticmethod
    def z_to_kl(z,txoffset=float,rxoffset=float):
        x01_x10_average = (z[0, 1].imag + z[1, 0].imag) / 2.0
        x00_x11_product = (z[0, 0].imag-txoffset) * (z[1, 1].imag-rxoffset)
        print("x01_x10_average={0}  x00_x11_product={1}".format(str(x01_x10_average),str(x00_x11_product)))

        if x00_x11_product > 0:
            return x01_x10_average / math.sqrt(x00_x11_product)
        else:
            return 0.0

    @staticmethod
    def z_to_kr(z,offeset=float,rxoffset=float):
        r01_r10_average = (z[0, 1].real + z[1, 0].real) / 2.0
        r00_r11_product = (z[0, 0].real - offeset) * (z[1, 1].real-rxoffset)
        print( "r01_r10_average={0}  r00_r11_product={1}".format( str( r01_r10_average ), str( r00_r11_product ) ) )
        if r00_r11_product > 0:
            return r01_r10_average / math.sqrt(r00_r11_product)
        else:
            return 0.0


    @staticmethod
    def get_ac_efficiency(z):
        """
        Calculate the optimum load and optimum efficiency for a 2x2 impedance matrix.
        Returns a tuple of the optimum load and optimum efficiency.
        http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6839568&tag=1
        """
        r11, r22 = z[0, 0].real, z[1, 1].real

        # average z12 and z21 to reduce noise, in a passive system they should ideally be the same
        r21 = (z[0, 1].real + z[1, 0].real) / 2
        x21 = (z[0, 1].imag + z[1, 0].imag) / 2

        z21_sq = r21 ** 2 + x21 ** 2
        r = r11 * r22 - r21 ** 2

        rl_sqrt_term = (r11 * r22 + x21 ** 2) * (r11 * r22 - r21 ** 2)
        if rl_sqrt_term >= 0 and r11 != 0:
            pass
        else:
            return 0.0

        eff_sqrt_term = (r + z21_sq) * r
        if eff_sqrt_term >= 0 and z21_sq != 0:
            return 1 + 2 / z21_sq * (r - math.sqrt(eff_sqrt_term))
        else:
            return 0.0

    def get_lqk(self, z, frequency):
        w = 2 * math.pi * frequency

        ltx = (z[0, 0].imag-self.TxXoffset) / w
        qtx = self.z_to_q(z[0, 0],self.TxXoffset,self.TxRoffset)
        part1 = f"Ltx={ltx * 1e6:6.3f},Qtx={qtx:6.3f}"

        lrx = (z[1, 1].imag-self.RxXoffeset) / w
        qrx = self.z_to_q(z[1, 1],self.RxXoffeset,self.RxRoffeset)
        part2 = f"Lrx={lrx * 1e6:6.3f},Qrx={qrx:6.3f}"

        k = math.fabs(self.z_to_kl(z,self.TxXoffset,self.RxXoffeset))
        kr = math.fabs(self.z_to_kr(z,self.TxRoffset,self.RxRoffeset))
        eff = self.get_ac_efficiency(z)
        part3 = f"k={k :5.4f},kr={kr :5.4f},Eff={eff * 100:5.4f}"
        print(f"get_Lqk f={frequency / 1000:6.1f}kHz,{part1},{part2},{part3}")
        return f"f={frequency / 1000:6.1f}kHz,{part1},{part2},{part3}"

    CSV_HEADER = "Label,Freq,Ltx,Qtx,Lrx,Qrx,k,kr,AC_Eff\n"

    def get_lqk_2(self, power, z, frequency):
        w = 2 * math.pi * frequency
        ltx = z[0, 0].imag / w
        qtx = self.z_to_q(z[0, 0])
        rtx = ltx * w / qtx
        ls1 = round(ltx * 1e6, 3) + float(self.ls_offset)
        rs1 = round(rtx * 1e3, 3) + float(self.rs_offset)
        part1 = f"Ltx={ls1}uH, Qtx={qtx:6.3f}, Rtx={rs1}mΩ"

        return f"Power = {power} | f={frequency / 1000:6.1f}kHz | {part1}", rs1

    def get_lqk_csv_line(self, z, frequency):
        w = 2 * math.pi * frequency

        ltx = (z[0, 0].imag-self.TxXoffset)/ w
        qtx = self.z_to_q(z[0, 0],self.TxXoffset,self.TxRoffset)
        part1 = f"{ltx * 1e6:.3f},{qtx:.3f}"

        lrx = (z[1, 1].imag-self.RxXoffeset) / w
        qrx = self.z_to_q(z[1, 1],self.RxXoffeset,self.RxRoffeset)
        part2 = f"{lrx * 1e6:.3f},{qrx:.3f}"

        k = math.fabs(self.z_to_kl(z,self.TxXoffset,self.RxXoffeset))
        kr = math.fabs(self.z_to_kr(z,self.TxRoffset,self.RxRoffeset))
        eff = self.get_ac_efficiency(z)
        part3 = f"{k:.4f},{kr:.4f},{eff:.4f}"

        return f"{frequency / 1000:.1f},{part1},{part2},{part3}\n"

    def test(self):
        try:
            items = self.frequencies
            target_freqs = [x * 1000 for x in items]
            for f in target_freqs:
                print(f"targeting f ={f / 1000:.1f}kHz")

            nice_lines =[]
            self.run_sweep()
            for target_freq in target_freqs:
                z, freq = self.get_z(target_freq)
                nice_lines.append(self.get_lqk(z, freq))
            return True, nice_lines
            pass
        except Exception as e:
            print(e)
            return False, None

    def test(self, even, POWER_GAIN, osc: cOscillograph):
        try:
            result = True
            message = ""
            testOscList = []
            self.frequencies = DEFAULT_STR
            items = self.frequencies.split(",")
            target_freqs = [float(x.strip()) * 1000 for x in items]
            for f in target_freqs:
                print(f"Targeting f = {f / 1000:.1f}kHz")

            items = POWER_GAIN.split(",")
            items.remove('')
            target_power = [float(x.strip()) for x in items]
            for f in target_power:
                print(f"Targeting VNA Power = {f:.1f}dBm")

            nice_lines = []
            start = time.time()
            for power in target_power:
                self.set_power(power)
                time.sleep(1)

                # data collecting
                self.run_sweep()
                for target_freq in target_freqs:
                    result, tempTestItem = osc.test()
                    tempTestItem.TestName = f'_{power:.1f}_{target_freq / 1000:.1f}'
                    testOscList.append(tempTestItem.Clone())
                    z, freq = self.get_z(target_freq)
                    tmpdata, Rtx = self.get_lqk_2(power, z, freq)
                    nice_lines.append(tmpdata)
                    if -30.0 == power:
                        if float(Rtx) < 0.8:
                            result = False
                            message = "Rtx 值小于0.8"

                for line in nice_lines:
                    print(line)
                time.sleep(0.5)

            # lower down power to -30dBm
            self.set_power(-30)

            return result, nice_lines, message, testOscList
            pass
        except Exception as e:
            print(e)
            return False, None, str(e), None

    def get_Knom_Value(self, event, osc: cOscillograph):
        import re
        try:
            power = ""
            testItemList = []
            Result, data, message, testOscList = self.test(event, self.Knom_POWER_GAIN, osc)
            if not Result: return False, None, None
            # data = ['Power = -30.0 | f=13560.0kHz | Ltx= 0.399uH, Qtx=35.779, Rtx=949.322mΩ',
            #         'Power = -20.9 | f=13560.0kHz | Ltx= 0.399uH, Qtx=35.760, Rtx=950.239mΩ',
            #         'Power = -4.8 | f=13560.0kHz | Ltx= 0.408uH, Qtx=20.708, Rtx=1678.635mΩ',
            #         'Power = -4.25 | f=13560.0kHz | Ltx= 0.410uH, Qtx=19.602, Rtx=1780.448mΩ'
            #         ]
            GlobalGui.global_Gui.TextBrowserSignal.emit("Knom-Value:" + str(data), "black", False)
            print("GetKnom" + str(data))
            for dlist in data:
                Tmpdata = re.split(",|\|", dlist)
                for num in Tmpdata:
                    if "f=" in num:
                        continue
                    if 'Power' in num:
                        power = "Knom" + num.split("=")[1].replace(" ", "")
                        continue
                    tmpTestitem: cTestItem = cTestItem()
                    tmpTestitem.TestName = power + "_" + num.split("=")[0].replace(" ", "")
                    tmpTestitem.TestValue = num.split("=")[1].replace(" ", "")

                    if "uH" in tmpTestitem.TestValue:
                        tmpTestitem.TestValue = tmpTestitem.TestValue.replace("uH", "")
                        tmpTestitem.TestUnit = "uH"

                    if "mΩ" in tmpTestitem.TestValue:
                        tmpTestitem.TestValue = str(float(tmpTestitem.TestValue.replace("mΩ", "")) / 1000)
                        tmpTestitem.TestUnit = "Ohm"

                    testItemList.append(tmpTestitem.Clone())
            return True, testItemList, testOscList
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None, None

    def get_Freeair_Value(self, event, osc: cOscillograph):
        import re
        try:
            power = ""
            testItemList = []
            Result, data, message, testOscList = self.test(event, self.Freeair_POWER_GAIN, osc)
            if not Result: return False, None, message, None
            GlobalGui.global_Gui.TextBrowserSignal.emit("Freeair-Value:" + str(data), "black", False)
            print("GetFreeair" + str(data))
            for dlist in data:
                Tmpdata = re.split(",|\|", dlist)
                for num in Tmpdata:
                    if "Qtx=" in num:
                        continue
                    if "f=" in num:
                        continue
                    if 'Power' in num:
                        power = "Freeair" + num.split("=")[1].replace(" ", "")
                        continue
                    tmpTestitem: cTestItem = cTestItem()
                    tmpTestitem.TestName = power + "_" + num.split("=")[0].replace(" ", "")
                    tmpTestitem.TestValue = num.split("=")[1].replace(" ", "")
                    if "uH" in tmpTestitem.TestValue:
                        tmpTestitem.TestValue = tmpTestitem.TestValue.replace("uH", "")
                        tmpTestitem.TestUnit = "uH"

                    if "mΩ" in tmpTestitem.TestValue:
                        tmpTestitem.TestValue = str(float(tmpTestitem.TestValue.replace("mΩ", "")) / 1000)
                        tmpTestitem.TestUnit = "Ohm"

                    testItemList.append(tmpTestitem.Clone())
            return True, testItemList, "", testOscList
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None, str(e), None

    def GetRS(self):
        testItemList = []
        TxRS = 0.0
        RxRS = 0.0
        LS = 0.0
        Q = 0.0
        try:
            items = self.frequencies
            target_freqs = [x * 1000 for x in items]
            for f in target_freqs:
                print(f"targeting f ={f / 1000:.1f}kHz")

            self.run_sweep()
            for target_freq in target_freqs:
                z, freq = self.get_z(target_freq)
                w = 2 * math.pi * freq
                TxRS=z[0,0].real
                RxRS=z[1,1].real
                LS = ((z[0,0].imag-self.TxXoffset) / w)* 1e6
                Q = self.z_to_q(z[0, 0],self.TxXoffset,self.TxRoffset)

            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName ="RAC"
            tmpTestitem.TestValue =TxRS-self.TxRoffset
            testItemList.append(tmpTestitem.Clone())

            tmpTestitem.TestName = "L"
            tmpTestitem.TestValue = LS
            testItemList.append(tmpTestitem.Clone())

            tmpTestitem.TestName = "Q"
            tmpTestitem.TestValue = Q
            testItemList.append(tmpTestitem.Clone())

            return True, testItemList
            pass
        except Exception as e:
            print(e)
            return False, None

    def GetTXRXRS(self):
        testItemList = []
        TxRS = 0.0
        RxRS = 0.0
        try:
            items = self.frequencies
            target_freqs = [x * 1000 for x in items]
            for f in target_freqs:
                print(f"targeting f ={f / 1000:.1f}kHz")

            self.run_sweep()
            for target_freq in target_freqs:
                z, freq = self.get_z(target_freq)
                w = 2 * math.pi * freq
                TxRS=z[0,0].real
                RxRS=z[1,1].real


            tmpTestitem: cTestItem = cTestItem()
            tmpTestitem.TestName ="RTX"
            tmpTestitem.TestValue =TxRS-self.TxRoffset
            testItemList.append(tmpTestitem.Clone())

            tmpTestitem.TestName = "RRX"
            tmpTestitem.TestValue = RxRS-self.RxRoffeset
            testItemList.append(tmpTestitem.Clone())

            return True, testItemList
            pass
        except Exception as e:
            print(e)
            return False, None

    def GetLs(self):
        try:
            LSValue = 0.0
            Result, data = self.test()
            print(data)
            Tmpdata = str(data[0]).split(",")
            LSValue = float(Tmpdata[5].split("=")[1].replace(" ", ""))
            print("GetLS:"+str(LSValue))
            GlobalGui.global_Gui.TextBrowserSignal.emit('VNA 读取LStx数据:' + str(LSValue), 'black', False)
            if not Result:
                return False, -1
            return True, LSValue

        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, -1

    def GetK(self):
        try:
            testItemList=[]
            Result, data = self.test()
            if not Result: return False, None
            GlobalGui.global_Gui.TextBrowserSignal.emit( "K-Value:"+str(data), "black", False )
            print("GetK"+str(data))
            Tmpdata = str(data[0]).split(",")
            for num in Tmpdata:
                if "f=" in num:
                    continue
                tmpTestitem:cTestItem=cTestItem()
                tmpTestitem.TestName=num.split("=")[0].replace(" ", "")
                tmpTestitem.TestValue = num.split("=")[1].replace(" ", "")
                testItemList.append(tmpTestitem.Clone())
            return True, testItemList
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit(str(e), 'red', False)
            return False, None

    def GetAll(self):
        Result, data = self.test()
        if not Result:
            return False, None
        return True, data

    def FormatSmit(self):
        Result= self.device.write('CALC:FORM SMIT')
        raw_string = self.device.query('SENS:CORR:DATA:CDAT? "S11,S22"')
        print("hi")


