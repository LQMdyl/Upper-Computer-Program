using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MFLEX_Compass.GlobalDir
{
    public class GlobalValue
    {
        #region value
        public static string ATurnTable = "A-";
        public static string BTurnTable = "B-";
        public static string testCommand = "test\r";
        #endregion value

        #region counter.ini
        public static string secTotal = "TOTAL";
        public static string secAStation1 = "A1";
        public static string secAStation2 = "A2";
        public static string secBStation1 = "B1";
        public static string secBStation2 = "B2";
        public static string keyTotal = "total";
        public static string keyPass = "pass";
        public static string keyFail = "fail";
        public static string keyYield = "yield";
        #endregion counter.ini

        #region config.ini
        public static string secApp = "APP";
        public static string secMcu1 = "MCU1";
        public static string secMcu2 = "MCU2";
        public static string secScan1 = "SCAN1";
        public static string secScan2 = "SCAN2";
        public static string secPlc1 = "FIXTURE_PLC";
        public static string secPlc2 = "LOAD_PLC";
        public static string secMes = "MES";
        public static string keyPort = "port";
        public static string keyBaudrate = "baud";
        public static string keyPlcIp = "plcip";
        public static string keyClearTime = "cleartime";
        public static string keyClearDate = "cleardate";
        public static string keyCheckStartTime = "checkstarttime";
        public static string keyCheckEndTime = "checkendtime";
        public static string keyCheckDate = "checkdate";
        public static string keyNgCount = "ngcount";
        public static string keyProbeCount = "probecount";
        public static string keyUseCount = "usecount";
        public static string keyDelay = "delay";
        public static string keyOperator = "operator";
        public static string keyFixtureId = "fixtureid";
        public static string keyLineId = "lineid";
        public static string keyWorkArea = "workarea";
        public static string keySerialNumber = "serialnumber";
        public static string keyProgram = "program";
        public static string keyProcess = "process";
        public static string keyUpload = "upload";
        public static string keyCheckBarcode = "checkbarcode";
        public static string keyBarcodeLenth = "barcodelenth";
        public static string keyLocalIp = "localip";
        public static string keyScanMode = "scanmode";
        public static string keyApiAddress = "apiaddress";
        public static string keyApiProcessPath = "apiprevalidationpath";
        public static string keyApiUploadPath = "apiuploadpath";
        public static string keyApiSamplePath = "apisamplepath";
        public static string keyTestType = "testtype";
        public static string keyPreTestType = "previoustesttype";
        public static string keyProductName = "productname";
        public static string keySite = "site";
        public static string keyLot = "lot";
        public static string keyProjectName = "projectname";
        public static string keyConnectAble = "connectable";
        public static string keyResourceName = "resourcename";
        public static string keyVersion = "version";
        public static string keyMesUrl = "mesurl";
        public static string keyProcessUrl = "processurl";
        public static string keySampleUrl = "sampleurl";
        #endregion config.ini

        #region get error message
        public readonly static Dictionary<int, string> ERR_MSG = new Dictionary<int, string>{ {201, "下压气缸原位异常"},
            {202, "下压气缸到位异常" },{203,"转盘A工位上料超时"},{204,"安全光幕异常"},
            {205,"紧急停止触发"},{206,"转盘A工位气缸异常"},{207,"转盘B工位气缸异常"},
            {208,"转盘A工位1穴吸真空异常"},{209,"转盘A工位2穴吸真空异常"},
            {210,"转盘A工位1穴光纤异常"},{211,"转盘A工位2穴光纤异常"},{212,"转盘A工位1穴光纤检测有料"},
            {213,"转盘A工位2穴光纤检测有料"},{214,"转盘B工位1穴光纤检测有料"},{215,"转盘B工位2穴光纤检测有料"},
            {216," 转盘B工位1穴吸真空异常"},{217 ,"转盘B工位2穴吸真空异常"},{218,"转盘B工位1穴光纤异常"},
            {219 ,"转盘B工位2穴光纤异常"},{220,"转盘B工位上料超时报警"},{221,"转盘上模1穴光纤检测有料"},{222,"转盘上模2穴光纤检测有料"}};
        public static void getErrMsg(int iErrCode, out string strMsg)
        {
            strMsg = "找不到错误信息";
            if (ERR_MSG.Keys.Contains(iErrCode))
            {
                strMsg = ERR_MSG[iErrCode];
            }
        }
        #endregion get error message
    }


    public enum Station
    {
        stationNone,
        stationA1,
        stationB1,
        stationA2,
        stationB2
    }

    public enum DevicesNum
    {
        MCU1 = 1,
        MCU2,
        Scan1,
        Scan2,
        FIXTURE_PLC,
        LOAD_PLC
    }

    public enum PLCCmdMode
    {
        readCoil = 1,
        writeCoil,
        readHold,
        writeHold
    }

    public enum TestMode
    {
        oAndO = 1,
        reTest,
        sample
    }
}
