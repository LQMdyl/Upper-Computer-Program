using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using MFLEX_Compass.GlobalDir;
using MFLEX_Compass.UI;

namespace MFLEX_Compass.Devices
{
    public class MCU
    {
        public SerialPort sp = new SerialPort();
        object obj = new object();
        public showLog updateMessage;
        public bool init(string portName, out string errorInfo)
        {
            errorInfo = "";
            sp = new SerialPort(portName, 9600, Parity.None, 8, StopBits.One);
            sp.ReadTimeout = 1000; //读超时 1000ms
            sp.WriteTimeout = 1000;//写超时 1000ms                                
            sp.ReadBufferSize = 1024;//输入缓冲区的大小            
            sp.WriteBufferSize = 1024;//输出缓冲区的大小  
            if (!sp.IsOpen)
            {
                sp.ReadTimeout = 1000;
                sp.WriteTimeout = 1000;
                try
                {
                    sp.Close();
                    sp.Open();
                }
                catch (Exception err)
                {
                    errorInfo = err.Message;
                    return false;
                }
            }
            else
            {
                sp.Close();
                sp.Open();
            }
            return sp.IsOpen;
        }
        public void Close()
        {
            try
            {
                sp.Close();
            }
            catch (Exception err)
            {
                throw new Exception(err.Message + err.StackTrace);
            }
        }
        public void Open()
        {
            try
            {
                sp.Open();
            }
            catch (Exception err)
            {
                throw new Exception(err.Message + err.StackTrace);
            }
        }
        public bool IsOpen
        {
            get { return sp.IsOpen; }
        }
        public void DiscardBuffer()
        {
            try
            {
                sp.DiscardInBuffer();
                sp.DiscardOutBuffer();
            }
            catch (Exception err)
            {
                throw new Exception("清除缓冲区数据错误！" + err.Message + err.StackTrace);
            }
        }
        public bool Write(string command)
        {
            lock (obj)
            {
                try
                {
                    if (string.IsNullOrEmpty(command)) return false;
                    sp.Write(command);
                    return true;
                }
                catch (Exception err)
                {
                    if (err is OperationCanceledException)
                    {
                        throw new Exception("清除缓冲区数据错误！" + err.Message + err.StackTrace);
                    }
                    return false;
                }
            }
        }

        public bool ReadExisting(out string data)
        {
            data = "";

            try
            {
                if (!sp.IsOpen) return false;

                data = sp.ReadExisting();

                return true;
            }
            catch (Exception ex)
            {
                if (ex is OperationCanceledException)
                {
                    throw new OperationCanceledException(ex.Message);
                }

                return false;
            }
        }
        public bool ReadTo(out string data, string delimiter = "\r\n", int timeout = 3000)
        {
            data = "";

            try
            {
                if (!sp.IsOpen) return false;

                sp.ReadTimeout = timeout;
                data = sp.ReadTo(delimiter);

                return true;
            }
            catch (Exception ex)
            {
                if (ex is OperationCanceledException)
                {
                    throw new OperationCanceledException(ex.Message);
                }

                return false;
            }
        }
        public string ReadyForTest()
        {
            if (!Write("\r")) return "";
            Thread.Sleep(200);

            string data = "";
            if (!ReadExisting(out data))
            {
                updateMessage(string.Format("读取缓冲区已存在的数据错误。\n"), GlobalKey.colorRed);
                return "";
            }

            return data;
        }

        public string WriteAndRead(string command, string delimiter, int timeout)
        {
            if (string.IsNullOrEmpty(command)) return "";

            if (!Write(command))
            {
                updateMessage(string.Format("发送命令{0}失败.\n", command.Trim('\r')), GlobalKey.colorRed);
                return "";
            }

            Thread.Sleep(1000);
            string readBuffer = "";
            if (string.IsNullOrEmpty(delimiter))
            {
                Thread.Sleep(3000);
                if (!ReadExisting(out readBuffer))
                {
                    updateMessage(string.Format("读取缓冲区已存在的数据错误。\n"), GlobalKey.colorRed);
                }
            }
            else
            {
                updateMessage("[MCU]"+readBuffer);
                if (!ReadTo(out readBuffer, delimiter, timeout))
                {
                    updateMessage(string.Format("读取数据到{0}错误。\n",delimiter), GlobalKey.colorRed);
                }
            }

            return readBuffer ?? "";
        }
        public string Test(string command)
        {
            try
            {
                if (string.IsNullOrEmpty(command))
                {
                    updateMessage(string.Format("测试命令为空。\n"), GlobalKey.colorRed);
                }

                lock (obj)
                {
                    ReadyForTest();
                }

                Thread.Sleep(50);

                lock (obj)
                {
                    string data = WriteAndRead(command, "end", 20000);
                    if (!string.IsNullOrEmpty(data)) return data;
                    return data = "";
                }
            }
            catch (Exception ex)
            {
                if (ex is OperationCanceledException)
                {
                    throw new Exception(ex.Message);
                }

                return "";
            }
        }
    }
}
