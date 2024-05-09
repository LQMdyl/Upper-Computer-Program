using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MFLEX_Compass.GlobalDir
{
    public class GlobalKey
    {
        public static string idelTxt = "IDEL";
        public static string testTxt = "TEST";
        public static string passTxt = "PASS";
        public static string failTxt = "FAIL";
        public static string errorTxt = "ERROR";
        public static Color colorRed = Color.Red;
        public static Color colorGreen = Color.Green;
        public static Color colorBlue = Color.Blue;
        public static Color colorBlack = Color.Black;
        public static Color colorGray = Color.Gray;
        public static Color colorYellow = Color.Yellow;
    }

    public enum Status
    {
        statusIdel = 1,
        statusTest,
        statusPass,
        statusFail,
        statusError
    }

    public enum DevicesStatus
    {
        connected,
        disconnect
    }

    
}
