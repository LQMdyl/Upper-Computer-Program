using NModbus.Utility;
using NModbus;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;
using Modbus.Device;

namespace MFLEX_Compass.Devices
{
    public class PLC_SerialPort
    {
        object locker;
        private SerialPort serialPort;
        public Modbus.Device.IModbusMaster master;
        public bool Connected = false;
        private int MStartAddress = 0;

        //下压气缸原位异常报警 (1,0)  M201
        //下压气缸到位异常报警 (1,0)  M202
        //转盘A工位上料超时报警 (1,0)  M203
        //安全光幕异常报警 (1,0)  M204
        //紧急停止异常报警 (1,0)  M205
        //转盘A工位气缸异常报警 (1,0)  M206
        //转盘B工位气缸异常报警 (1,0)  M207
        //转盘A工位1穴吸真空异常报警 (1,0)  M208
        //转盘A工位2穴吸真空异常报警 (1,0)  M209
        //转盘A工位1穴光纤异常报警 (1,0)  M210
        //转盘A工位2穴光纤异常报警 (1,0)  M211
        //转盘A工位1穴光纤检测有料报警 (1,0)  M212
        //转盘A工位2穴光纤检测有料报警 (1,0)  M213
        //转盘B工位1穴光纤检测有料报警 (1,0)  M214
        //转盘B工位2穴光纤检测有料报警 (1,0)  M215
        //转盘B工位1穴吸真空异常报警 (1,0)  M216
        //转盘B工位2穴吸真空异常报警 (1,0)  M217
        //转盘B工位1穴光纤异常报警 (1,0)  M218
        //转盘B工位2穴光纤异常报警 (1,0)  M219
        //转盘B工位上料超时报警 (1,0)  M220
        //转盘上模1穴光纤检测有料报警 (1,0)  M221
        //转盘上模2穴光纤检测有料报警 (1,0)  M222

        public PLC_SerialPort()
        {
            //初始化modbusmaster
            locker = new object();
        }

        public bool InitPLC(string port, int baud, out string errorInfo)
        {
            errorInfo = "";
            try
            {
                serialPort = new SerialPort(port);
                serialPort.BaudRate = baud;
                serialPort.Parity = Parity.None;
                serialPort.DataBits = 8;
                serialPort.StopBits = StopBits.One;
                serialPort.Open();
                master = ModbusSerialMaster.CreateRtu(serialPort);
                Connected = true;
                return true;
            }
            catch (Exception e)
            {
                Connected = false;
                errorInfo = string.Format("连接PLC异常:{0}", e.Message);
                return false;
            }
        }
        public void Close()
        {
            try
            {
                if (Connected)
                {
                    serialPort.Close();
                }
                Connected = false;
            }
            catch (Exception err)
            {
                throw new Exception(err.Message);
            }
        }
        public bool IsOpen
        {
            get { return Connected; }
        }

        public ushort[] ReadShort(int address, int length, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    ushort[] res = master.ReadHoldingRegisters(slaveAddress, (ushort)address, (ushort)length);
                    return res;
                }
                catch (Exception e)
                {
                    return null;
                }
            }
        }
        public bool WriteShort(int address, ushort[] data, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    master.WriteMultipleRegistersAsync(slaveAddress, (ushort)address, data);
                    return true;
                }
                catch (Exception e)
                {
                    return false;
                }
            }
        }
        public bool WriteInt32(int address, int value, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    ushort lowOrderValue = BitConverter.ToUInt16(BitConverter.GetBytes(value), 0);
                    ushort highOrderValue = BitConverter.ToUInt16(BitConverter.GetBytes(value), 2);
                    master.WriteMultipleRegistersAsync(slaveAddress, (ushort)address, new ushort[] { lowOrderValue, highOrderValue });
                    return true;
                }
                catch (Exception e)
                {
                    return false;
                }
            }
        }
        public int ReadInt32(int address, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    ushort[] registers = master.ReadHoldingRegisters(slaveAddress, (ushort)address, 2);
                    uint value = ModbusUtility.GetUInt32(registers[1], registers[0]);
                    return value < 2147483647 ? Convert.ToInt32(value) : Convert.ToInt32(value - 4294967296);
                }
                catch (Exception e)
                {
                    return ushort.MaxValue + 1;
                }
            }
        }
        public bool[] ReadMRegister(int address, int length, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    bool[] registers = master.ReadCoils(slaveAddress, (ushort)(address + MStartAddress), (ushort)length);
                    return registers;
                }
                catch (Exception e)
                {
                    return null;
                }
            }
        }
        public bool WriteMRegister(int address, bool data, byte slaveAddress = 0)
        {
            lock (locker)
            {
                try
                {
                    master.WriteMultipleCoils(slaveAddress, (ushort)(address + MStartAddress), new bool[] { data });
                    return true;
                }
                catch (Exception e)
                {
                    return false;
                }
            }
        }

        public bool FixtureKeepConnect()
        {
            lock (locker)
            {
                try
                {
                    WriteInt32(40101, 1);
                    return true;
                }
                catch (Exception ex)
                {
                    Connected = false;
                    return false;
                }
            }
        }

        public bool GetStart(int address)
        {
            lock (locker)
            {
                try
                {
                    int value = ReadInt32(address);
                    if (value < 1) return false;
                    if (value == 1) return WriteInt32(address, 0);
                    return false;
                }
                catch (Exception ex)
                {
                    return false;
                }
            }
        }
        public bool OpenOutOK(int address)
        {
            lock (locker)
            {
                try
                {
                    int value = ReadInt32(address);
                    if (value < 1) return false;
                    if (value == 2) return WriteInt32(address, 0);
                    return false;
                }
                catch (Exception ex)
                {
                    return false;
                }
            }
        }
        public bool ReadSN(int index, int count, out string SN)
        {
            List<ushort> stateList = new List<ushort>(count) { 0 };
            SN = "";
            try
            {
                lock (locker)
                {
                    var datas = ReadShort(index, count);
                    if (datas == null || datas.Length != count) return false;

                    stateList = datas.ToList();
                    foreach (var num in stateList) { SN += Chr(num); }
                    if (SN.Contains("\0"))
                    {
                        SN = "";
                    }
                    return true;
                }

            }
            catch (Exception ex)
            {
                Connected = false;
                return false;
            }
        }
        public string Chr(int asciiCode)
        {
            if (asciiCode >= 0 && asciiCode <= 255)
            {
                System.Text.ASCIIEncoding asciiEncoding = new System.Text.ASCIIEncoding();
                byte[] byteArray = new byte[] { (byte)asciiCode };
                string strCharacter = asciiEncoding.GetString(byteArray);
                return (strCharacter);
            }
            else
            {
                throw new Exception("ASCII Code is not valid.");
            }
        }
    }
}
