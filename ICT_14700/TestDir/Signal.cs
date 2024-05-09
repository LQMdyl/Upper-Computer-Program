using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MFLEX_Compass.TestDir
{
    public class Signal
    {
        public Signal() { }
        #region 主控
        public static int TestReboot = 40100;
        public static int AutoReboot = 40106;
        public static int ReleaseAlarm = 40107;
        public static int AutoAlarm = 40108;
        public static int TestException = 40110;
        public static int ActionException = 40111;
        public static int WaitUnload = 40117;
        public static int Slot1Result = 40118;
        public static int Slot2Result = 40119;
        public static int WaitLoad = 40122;
        public static int TestMode = 40203;
        public static int UnloadFinish = 40204;
        public static int LoadFinish = 40205;
        public static int Carrier = 40217;
        public static int Barcode1Lenth = 40220;
        public static int Barcode1Start = 40221;
        public static int Barcode1End = 40234;
        public static int Barcode2Lenth = 40235;
        public static int Barcode2Start = 40236;
        public static int Barcode2End = 40249;
        #endregion 主控

        #region PLC

        #endregion PLC
    }
}
