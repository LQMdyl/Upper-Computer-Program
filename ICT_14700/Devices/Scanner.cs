using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace MFLEX_Compass.Devices
{
    public class Scanner
    {
        public SerialPort sp = new SerialPort();
        object obj = new object();

        public bool init(string portName, out string errorInfo)
        {
            errorInfo = "";
            sp = new SerialPort(portName, 9600, Parity.None, 8, StopBits.One);
            sp.ReadTimeout = 1000; //读超时 1000ms
            sp.WriteTimeout = 1000;//写超时 1000ms                                
            sp.ReadBufferSize = 1024;//输入缓冲区的大小            
            sp.WriteBufferSize = 1024;//输出缓冲区的大小  
            sp.ReceivedBytesThreshold = 1;

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

        public bool IsOpen
        {
            get { return sp.IsOpen; }
        }

        public bool ScanBarcode(out string barcode, out string message)
        {
            barcode = "";
            message = "";
            byte[] triggerCommand = { 0x16, 0x54, 0x0d };
            byte[] closeCommand = { 0x16, 0x55, 0x0d };
            try
            {
                lock (obj)
                {
                    if (!sp.IsOpen)
                    {
                        sp.Open();
                    }
                    sp.DiscardInBuffer();
                    sp.DiscardOutBuffer();
                    sp.Write(triggerCommand, 0, triggerCommand.Length);
                    barcode = sp.ReadExisting();
                    DateTime now = DateTime.Now;
                    while (true)
                    {
                        barcode += sp.ReadExisting();
                        if (barcode.Contains("\r\n"))
                        {
                            break;
                        }
                        if (DateTime.Now.Subtract(now).TotalSeconds > 5)
                        {
                            message = "扫码超时";
                            return false;
                        }
                        Thread.Sleep(200);
                    }
                    sp.Write(closeCommand, 0, closeCommand.Length);
                    sp.Close();
                    barcode = barcode.Replace("\r\n", "");
                    return true;
                }
            }
            catch (Exception ex)
            {
                message = ex.Message;
                sp.Write(closeCommand, 0, closeCommand.Length);
                sp.Close();
                return false;
            }
        }
    }
}
