using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MFLEX_Compass.UI;
using MFLEX_Compass.Devices;
using MFLEX_Compass.ConfigDir;
using MFLEX_Compass.LogDir;
using MFLEX_Compass.GlobalDir;
using System.Net;
using System.ComponentModel;
using CommonHelper;
using System.Drawing;
using System.IO;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Forms;
using MFLEX_Compass.MesDir;
using System.Security.Cryptography.X509Certificates;
using System.Reflection;
using System.Runtime.InteropServices;
//using static System.Collections.Specialized.BitVector32;

namespace MFLEX_Compass.TestDir
{

    public class TestEngine
    {
        #region value
        public TestMode m_TestMode;
        public int m_iNowTestMode;
        public int m_iPreTestMode;
        public int m_iTestTimes;
        public int m_iNgCount;  //NG报警次数
        public int m_iProbeCount;   //探针使用报警次数
        public int m_iUseCount; //探针使用次数
        public MCU m_mcu1;
        public MCU m_mcu2;
        public PLC m_fixturePlc;
        public PLC_Cont m_mainConPlc;
        private Configure configure;
        private Count counter;
        private Task detectTask;
        private Task initTask;
        private AllLog txtLog;
        //private AllLog csvLog;
        private string m_strLocalIp;
        private bool m_isInit;
        private bool m_isTesting;    // 是否测试中，测试开始时置为true，测试结束时置为false
        private bool m_isAbort;     // 是否停止正在运行的任务，初始化为false
        private bool m_isTerminate;     //程序是否终止，暂未使用，初始化未false
        public bool m_isAlarm;   // 是否异常，出现异常时置为true，解除异常置为false
        private bool m_isLoad;  // 是否允许上料，检测到允许上料信号时置为true，上料完成后置为false
        private bool m_isUnLoad;        // 是否允许下料，检测到允许下料信号时置为true，下料完成后置为false
        private bool m_isConnect;       // 是否连接主控上位机，读取配置文件，连接-true，不连接-false
        private bool m_isLoadAlive;     // 是否正在上料，开始上料时置为true，上料结束置为false
        private bool m_isUnloadAlive;       // 是否正在下料，开始下料时置为true，下料结束置为false
        public bool m_isAutoMode;       // 是否为自动模式
        public bool m_isProcess;        //是否开启卡控，初始化时读取配置文件
        public bool m_isUpload;         // 是否开启上传，初始化时读取配置文件
        public bool m_isSample;         //是否开启样本模式
        public bool m_isAUnloadAble;
        public bool m_isBUnloadAble;
        public int m_iTaskCount;    //当前线程数
        private int m_iDayStartTime;    //白班开始时间: H
        private ushort m_serialNum;     //流水号
        private DateTime m_dtStartTime;     //开始测试时间
        private CancellationTokenSource m_tokenSource;
        private readonly GTSManualResetEvent m_resetEvent;
        public Dictionary<Station, Result> DicBarcode;      //条码字典，用于确定物料放置的穴位
        public Dictionary<int, ushort> DicCommand;      //流水号字典，用于记录与主控上位机通讯产生的有效流水号
        private string m_strTurnTable;      //转盘编号：(A-, B-)
        private Station m_station1;     //1穴编号：（A1, B1）
        private Station m_station2;     //2穴编号：（A2, B2）
        private object m_lockObj;       //线程锁
        public bool m_bStartTest;       //是否接收到开始测试信号
        public bool m_bTestEnd;     //[预留] 是否接收到测试结束信号，暂未使用
        private bool m_isDayClear;  //白班良率已清除标志
        private bool m_isNightClear;    //夜班良率已清除标志
        private bool m_isCheckTime; //点检时间标志
        private bool m_isChecked;
        private bool m_isDay;
        private int[] m_intsNgCount;    //各穴位NG计数
        public bool m_isOperator;
        // <单元测试用代码>
        public int m_iType;
        public int m_iStart;
        public int m_iEnd;
        public int m_iTurnTable;
        public int m_iLoadAble;
        public int m_iUnloadAble;
        // </单元测试用代码>
        public bool m_ModuleDryRun_A; //模块A空转标记
        public bool m_ModuleDryRun_B; //模块B空转标记
        #endregion value

        #region method
        public showLog updateLog;
        public UpdateBarcode updateBarcode;
        public UpdateDevicesStatus updateDevicesStatus;
        public UpdateAllTestStatus updateAllTestStatus;
        public UpdateSampleListview updateSampleListview;
        public UpdateTestStatus updateTestStatus;
        public UpdateTestTime updateTestTime;
        public UpdateYield updateYield;
        public ShowTestDataList showTestDataList;
        public ShowTestDataSingle showTestDataSingle;
        public MainInit flushWindow;
        public ClearYield clearYield;
        public ClearSampleListView clearSampleListView;
        #endregion method

        #region new object
        public TestEngine()
        {
            m_TestMode = TestMode.oAndO;
            m_mcu1 = new MCU();
            m_mcu2 = new MCU();
            configure = new Configure();
            counter = new Count();
            m_fixturePlc = new PLC();
            m_mainConPlc = new PLC_Cont();
            txtLog = new AllLog();
            //csvLog = new AllLog();
            m_tokenSource = new CancellationTokenSource();
            m_resetEvent = new GTSManualResetEvent(true);
            m_isInit = false;
            m_isTesting = false;
            m_isAbort = false;
            m_isAlarm = false;
            m_isLoad = false;
            m_isUnLoad = false;
            m_isConnect = false;
            m_isLoadAlive = false;
            m_isUnloadAlive = false;
            m_isAutoMode = true;
            m_serialNum = 0x100;
            DicBarcode = new Dictionary<Station, Result>();
            DicCommand = new Dictionary<int, ushort>();
            m_station1 = new Station();
            m_station2 = new Station();
            m_lockObj = new object();
            m_bStartTest = false;
            m_bTestEnd = false;
            m_isProcess = configure.configData[GlobalValue.secApp][GlobalValue.keyProcess] == "Y";
            m_isUpload = configure.configData[GlobalValue.secApp][GlobalValue.keyUpload] == "Y";
            m_isSample = false;
            m_iPreTestMode = 1;
            m_iNowTestMode = 1;
            m_iTestTimes = 1;
            m_isAUnloadAble = true;
            m_isBUnloadAble = true;
            m_iTaskCount = 0;
            m_ModuleDryRun_A = false;
            m_ModuleDryRun_B = false;
            m_isTerminate = false;
            m_isDayClear = false;
            m_isNightClear = false;
            m_iDayStartTime = 7;
            m_isCheckTime = false;
            m_iNgCount = int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyNgCount]);
            m_iProbeCount = int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyProbeCount]);
            m_iUseCount = int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyUseCount]);
            m_intsNgCount = new int[] { 0, 0, 0, 0 };
            m_isOperator = false;
            m_isChecked = false;
            m_isDay = false;
            // <单元测试用代码>
            m_iType = 0;
            m_iStart = 0;
            m_iTurnTable = 0;
            m_iLoadAble = 0;
            m_iUnloadAble = 0;
            // </单元测试用代码>
        }
        #endregion new object

        #region initialize
        /*
        * @function：InitializeEngine()
        * @pararm：
        * @return：void
        * @action：程序初始化
        */
        public void InitializeEngine()
        {
            bool bIniSuccess = true;
            getLocalIp();
            getClearDate();
            bIniSuccess &= initializeLogFile();
            bIniSuccess &= ConnectDevices();
            bIniSuccess &= IniFunction();
            if (!bIniSuccess)
            {
                updateLog("程序初始化失败，请检查设备并重启程序");
                return;
            }
            if (getCheckDate()) { GetETShiftSamples(); }
            StartDetectTask();
        }

        /*
         * @function：initializeLogFile()
         * @pararm：
         * @return：true/false
         * @action：初始化日志文件
         */
        public bool initializeLogFile()
        {
            try
            {
                string tmpDir = @"D:/Log/TestLog";
                txtLog.path = string.Format("{0:yyyy_MM_dd}.txt", DateTime.Now);
                txtLog.DirPath = tmpDir;
                txtLog.FileName = string.Format("{0:yyyy_MM_dd}.txt", DateTime.Now);
                //txtLog.DeleteOverdueLog(tmpDir, TimeHelper.TimeFormat.DAYLEVEL, 3);
                return true;
            }
            catch (Exception ex)
            {
                if (updateLog != null) { updateLog("生成Log文件错误 - " + ex.Message, GlobalKey.colorRed); }

                return false;
            }
        }

        /*
         * @function：ConnectDevices()
         * @pararm：
         * @return：true/false
         * @action：连接设备
         */
        public bool ConnectDevices()
        {
            try
            {
                string strErrMsg = "";
                string strFixturePlcIp = configure.configData[GlobalValue.secPlc1][GlobalValue.keyPlcIp];
                int iFixturePlcport = int.Parse(configure.configData[GlobalValue.secPlc1][GlobalValue.keyPort]);
                string strUploadPlcIp = configure.configData[GlobalValue.secPlc2][GlobalValue.keyPlcIp];
                int iUploadPlcport = int.Parse(configure.configData[GlobalValue.secPlc2][GlobalValue.keyPort]);
                string strMcu1Name = configure.configData[GlobalValue.secMcu1][GlobalValue.keyPort];
                string strMcu2Name = configure.configData[GlobalValue.secMcu2][GlobalValue.keyPort];
                m_isConnect = configure.configData[GlobalValue.secApp][GlobalValue.keyConnectAble].ToUpper() == "Y";

                WriteRunLog("开始连接治具PLC");
                if (!m_fixturePlc.InitPLC(strFixturePlcIp, iFixturePlcport, out strErrMsg))
                {
                    WriteRunLog("治具PLC连接失败 - " + strErrMsg, GlobalKey.colorRed);
                    return false;
                }
                WriteRunLog("治具PLC连接成功");
                updateDevicesStatus(DevicesNum.FIXTURE_PLC, DevicesStatus.connected);
                if (!m_fixturePlc.WriteMRegister(6, true)) { return false; }

                if (m_isConnect)
                {
                    WriteRunLog("开始连接上料PLC");
                    if (!m_mainConPlc.InitPLC(strUploadPlcIp, iUploadPlcport, out strErrMsg))
                    {
                        WriteRunLog("上料PLC连接失败 - " + strErrMsg, GlobalKey.colorRed);
                        return false;
                    }
                    WriteRunLog("上料PLC连接成功");
                    updateDevicesStatus(DevicesNum.LOAD_PLC, DevicesStatus.connected);
                }
                else
                {
                    bool bWrite = m_fixturePlc.WriteMRegister(15, true);
                    Thread.Sleep(1000);
                    bWrite &= m_fixturePlc.WriteMRegister(15, false);
                }

                bool[] bMode = m_fixturePlc.ReadMRegister(17, 1);
                if (bMode == null)
                {
                    WriteRunLog("无法确定操作模式", Color.Red);
                    return false;
                }
                m_isAutoMode = !bMode[0];
                WriteRunLog(string.Format("当前为{0}模式", m_isAutoMode ? "自动" : "手动"));

                WriteRunLog("开始连接治具单片机1");
                if (!m_mcu1.init(strMcu1Name, out strErrMsg))
                {
                    WriteRunLog("单片机1连接失败 - " + strErrMsg, GlobalKey.colorRed);
                    return false;
                }
                WriteRunLog("单片机1连接成功");
                updateDevicesStatus(DevicesNum.MCU1, DevicesStatus.connected);

                WriteRunLog("开始连接治具单片机2");
                if (!m_mcu2.init(strMcu2Name, out strErrMsg))
                {
                    WriteRunLog("单片机2连接失败 - " + strErrMsg, GlobalKey.colorRed);
                    return false;
                }
                WriteRunLog("单片机2连接成功");
                updateDevicesStatus(DevicesNum.MCU2, DevicesStatus.connected);
                WriteRunLog("设备连接成功，等待后续指令");
                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }
        }


        /*
         * @function：IniFunction()
         * @pararm：
         * @return：true/false
         * @action：设备初始化
         */
        private bool IniFunction()
        {
            try
            {
                DateTime startTime1 = DateTime.Now;
                int totalAlarmMin = 0;

                while (m_isAbort)
                {
                    Thread.Sleep(2000);
                    if (m_iTaskCount == 0)
                    {

                        lock (m_lockObj)
                        {
                            m_isAbort = false;
                        }
                        if (m_isConnect)
                        {
                            if (!m_mainConPlc.WriteShort(40106, 0))
                            {
                                throw new Exception("通知主控上位机治具已开始初始化[40106-0]失败");
                            }
                        }
                        flushWindow();
                        m_isAUnloadAble = true;
                        m_isBUnloadAble = true;
                        WriteRunLog("发送治具初始化指令", Color.Black, true);
                        break;
                    }
                }

                if (!m_fixturePlc.WriteMRegister(6, true)) { return false; }
                Thread.Sleep(1000);
                if (!m_fixturePlc.WriteMRegister(6, false)) { return false; }
                if (m_isConnect)
                {

                    if (!m_mainConPlc.WriteShort(40106, 0)) { throw new Exception("通知主控上位机治具已开始初始化[40106-0]失败"); }
                    WriteRunLog("通知主控上位机[40106-0]，治具已开始初始化", Color.Black, true);
                    Thread.Sleep(1000);

                    lock (m_lockObj)
                    {
                        m_iTaskCount++;
                    }
                    while (!m_isAbort)
                    {
                        Thread.Sleep(1000);
                        if (DateTime.Now.Subtract(startTime1).TotalMinutes >= 2)
                        {
                            totalAlarmMin += 1;
                            WriteRunLog(string.Format("等待治具初始化完成:{0}超时{1}分钟", 40100, totalAlarmMin * 2), Color.Red, true);
                            startTime1 = DateTime.Now;
                        }
                        if (m_fixturePlc.ReadShort(150) == 1) //初始化完成
                        {
                            WriteRunLog("治具初始化完成,向主控上位机[40100-1]发送完成信号", Color.Black, true);
                            if (!m_mainConPlc.WriteShort(40100, 1))
                            {
                                throw new Exception("向主控上位机[40100-1]发送完成信号失败");
                            }
                            break;
                        }
                    }
                    Thread.Sleep(2000);
                    startTime1 = DateTime.Now;
                    while (!m_isAbort)
                    {
                        Thread.Sleep(1000);
                        if (DateTime.Now.Subtract(startTime1).TotalMinutes >= 2)
                        {
                            totalAlarmMin += 1;
                            WriteRunLog(string.Format("等待主控上位机初始化完成:{0}超时{1}分钟", 40100, totalAlarmMin * 2), Color.Red, true);
                            startTime1 = DateTime.Now;
                        }
                        if (m_mainConPlc.ReadShort(40100) == 0)
                        {
                            WriteRunLog("主控上位机初始化[40100-0]完成信号", Color.Black, true);
                            break;
                        }

                    }
                    lock (m_lockObj)
                    {
                        m_iTaskCount--;
                        m_isInit = true;
                    }

                    //由于此流水号不通过测试上位机产生，因此提前初始化一个无效的流水号，确保后续使用时，key存在
                    if (!DicCommand.Keys.Contains(3))
                    {
                        DicCommand.Add(3, 1);
                    }
                }

                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed, true);
                if (!m_isAbort && m_isConnect)
                {
                    lock (m_lockObj)
                    {
                        m_iTaskCount--;
                    }
                }
                return false;
            }
        }

        /*
         * @function：IniYield()
         * @pararm：
         * @return：void
         * @action：自动清除良率
         */
        private void IniYield()
        {
            try
            {
                int iHour = DateTime.Now.Hour;
                if (iHour >= m_iDayStartTime && iHour < (m_iDayStartTime + 12))
                {
                    if (m_isDayClear) { return; }
                    m_isDayClear = true;
                    m_isNightClear = false;
                }
                else if (iHour < m_iDayStartTime || iHour >= (m_iDayStartTime + 12))
                {
                    if (m_isNightClear) { return; }
                    m_isNightClear = true;
                    m_isDayClear = false;
                }
                string strClearDate = string.Format("{0:yyyyMMdd}_{1}", DateTime.Now, m_isDayClear ? "D" : "N");
                configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyClearDate, strClearDate);
                clearYield();
                WriteRunLog(string.Format("自动清除良率{0}", strClearDate));
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
            }
        }
        #endregion initialize

        #region startEngine
        /*
        * @function：StartDetectTask()
        * @pararm：
        * @return：void
        * @action：检测线程，用于检测程序是否重复开启线程
        */
        private void StartDetectTask()
        {
            //flushWindow();
            if (detectTask != null && !detectTask.IsCompleted)
            {
                WriteRunLog("检测线程正在执行中，不可重复启动。");
                return;
            }

            (detectTask = new Task(DetectFunction)).Start();
            WriteRunLog("PLC信号检测线程已开启。");
            //if (m_isConnect)
            //{
            //    Thread thdKeepCon = new Thread(ConnectIngUpload);
            //    thdKeepCon.Start();
            //}
        }

        /*
       * @function：DetectFunction()
       * @pararm：
       * @return：void
       * @action：触发线程，根据信号开启对应的线程
       */
        private void DetectFunction()
        {
            try
            {
                int iErrCode = 0;
                string strErrMsg = "";
                while (!m_isTerminate)
                {
                    Thread.Sleep(500);
                    if (m_mainConPlc.IsOpen && m_isConnect)
                    {
                        if (m_mainConPlc.ReadShort(40106) == 1)//自动化重启复位治具
                        {
                            if (!m_isAbort)
                            {
                                m_isAbort = true;
                                new Task(() => { IniFunction(); }).Start();
                            }
                        }
                        if (m_mainConPlc.ReadShort(40107) == 1)//解除报警
                        {
                            new Task(() => { ClearAlarm(); }).Start();
                        }

                        if (m_isAlarm)
                        {
                            if (m_mainConPlc.ReadShort(40108) == 0)
                            {
                                new Task(() => { ClearAlarm(); }).Start();
                            }
                        }
                    }

                    getCheckTime();
                    if (!plcAlarm(out iErrCode))
                    {
                        //只输出一次报警信息，报警未解除的情况下，后续报警信息不再新增
                        if (m_isAlarm) { continue; }
                        GlobalValue.getErrMsg(iErrCode, out strErrMsg);
                        WriteRunLog(strErrMsg, GlobalKey.colorRed);
                        lock (m_lockObj)
                        {
                            m_isAlarm = true;
                        }
                        if (m_mainConPlc.IsOpen && m_isConnect)
                        {
                            m_mainConPlc.WriteShort(40110, 1);
                        }
                    }

                    IniYield();
                    if (m_isAlarm) { continue; }
                    if (m_mainConPlc.IsOpen && m_isConnect)
                    {
                        if (m_mainConPlc.ReadShort(40108) == 1)//自动化停机
                        {
                            lock (m_lockObj)
                            {
                                m_isAlarm = true;
                            }
                            continue;
                        }

                        if ((m_iNowTestMode = m_mainConPlc.ReadShort(40203)) != m_iPreTestMode)//测试模式
                        {
                            if (m_iNowTestMode == 1 || m_iNowTestMode == 0)
                            {
                                m_TestMode = TestMode.oAndO; //
                            }
                            else if (m_iNowTestMode == 2 || m_iNowTestMode == 4)//复测
                            {
                                m_TestMode = TestMode.reTest;
                            }
                        }
                    }
                    if (m_isAutoMode)
                    {
                        if (LoadEnable())
                        {
                            lock (m_lockObj) { m_isLoadAlive = true; }
                            new Task(() => { LoadFunction(m_tokenSource.Token); }).Start();
                            /*
                             * 不连接自动化测试
                             * if (GetTestTurnTable(ref m_strTurnTable, ref m_station1, ref m_station2))
                             * {
                             *    if (StartTestEnable() && !m_isTesting)
                             *    {
                             *        WriteRunLog("已获取开始测试信号");
                             *        new Task(() => { TestFunction(m_tokenSource.Token, m_station1, m_station2); }).Start();
                             *    }
                             *}
                            */
                        }
                        if (StartTestEnable())
                        {
                            lock (m_lockObj) { m_isTesting = true; }
                            new Task(() => { TestFunction(m_tokenSource.Token); }).Start();
                        }
                        if (UnLoadEnable())
                        {
                            lock (m_lockObj) { m_isUnloadAlive = true; }
                            new Task(() => { UnLoadFunction(m_tokenSource.Token); }).Start();
                        }

                        //if (m_intsNgCount.Max(x => x) >= m_iNgCount)  //不确定vs2013版是否可用
                        if (getMaxValue(m_intsNgCount) >= m_iNgCount)
                        {
                            lock (m_lockObj)
                            {
                                m_isAlarm = true;
                            }
                            if (m_mainConPlc.IsOpen && m_isConnect)
                            {
                                m_mainConPlc.WriteShort(40110, 1);
                            }
                            MessageBox.Show(string.Format("连续NG已达{0}次，请停止治具进行检修", m_iNgCount), "警告");
                            WriteRunLog(string.Format("连续NG已达{0}次，请停止治具进行检修", m_iNgCount), Color.Red);
                            continue;
                        }
                    }
                    else  //手动
                    {
                        if (LoadFinish() || m_isLoad)
                        {
                            if (WaitScan())
                            {
                                ScanBarcode(ref m_station1, ref m_station2);
                            }
                            if (m_isLoad)
                            {
                                if (StartTestSignal() && !m_isTesting)
                                {
                                    m_isLoad = false;
                                    WriteRunLog("已获取开始测试信号");
                                    new Task(() => { TestFunction(m_tokenSource.Token, m_station1, m_station2); }).Start();
                                }
                            }
                        }
                    }

                }
            }
            catch (Exception ex)
            {
                WriteRunLog(string.Format("检测线程错误,请重启程序！ - {0}", ex.Message + ex.StackTrace), Color.Red);
                StopEngine();
            }
        }

        /*
      * @function：LoadFinish()
      * @pararm：
      * @return：true/false
      * @action：确定是否上料完成（仅手动单元测试）
      */
        private bool LoadFinish()
        {
            try
            {
                int iRead1 = 0;
                int iRead2 = 0;
                if (m_fixturePlc.ReadShort(120) == 0 && m_fixturePlc.ReadShort(130) == 0)
                {
                    return false;
                }
                iRead1 = m_fixturePlc.ReadShort(120);
                if (iRead1 != 0)
                {
                    m_station1 = iRead1 != 2 ? Station.stationA1 : Station.stationNone;
                    m_station2 = iRead1 != 1 ? Station.stationA2 : Station.stationNone;
                }

                iRead2 = m_fixturePlc.ReadShort(130);
                if (iRead2 != 0)
                {
                    m_station1 = iRead2 != 2 ? Station.stationB1 : Station.stationNone;
                    m_station2 = iRead2 != 1 ? Station.stationB2 : Station.stationNone;
                }

                m_fixturePlc.WriteShort(120, 0);//PLC通知PC转盘A工位1穴有料写1, 2穴有料写2，双穴有料写3
                m_fixturePlc.WriteShort(130, 0);//PLC通知PC转盘B工位1穴有料写1, 2穴有料写2，双穴有料写3
                m_isLoad = true;
                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }
        }

        /*
     * @function：WaitScan()
     * @pararm：
     * @return：true/false
     * @action：是否允许扫码（仅手动单元测试）
     */
        private bool WaitScan()
        {
            try
            {
                WriteRunLog("等待请求扫码信号");
                return m_fixturePlc.ReadShort(140) == 1;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }
        }

        /*
       * @function：ScanBarcode(ref Station station1, ref Station station2)
       * @pararm：
       * station1：当前1穴编号
       * station2：当前2穴编号
       * @return：true/false
       * @action：触发扫码（仅手动单元测试）
       */
        private bool ScanBarcode(ref Station station1, ref Station station2)
        {
            try
            {
                WriteRunLog("开始扫码");
                Result result1 = new Result { barcode = string.Format("Slot_1_Barcode{0}", m_serialNum), testTimes = 1, isSample = false };
                Result result2 = new Result { barcode = string.Format("Slot_2_Barcode{0}", m_serialNum), testTimes = 1, isSample = false };
                if (station1 != Station.stationNone)
                {
                    if (DicBarcode.Keys.Contains(station1))
                    {
                        DicBarcode[station1] = result1;
                    }
                    else
                    {
                        DicBarcode.Add(station1, result1);
                    }
                }

                if (station2 != Station.stationNone)
                {
                    if (DicBarcode.Keys.Contains(station2))
                    {
                        DicBarcode[station2] = result2;
                    }
                    else
                    {
                        DicBarcode.Add(station2, result2);
                    }
                }
                m_fixturePlc.WriteShort(140, 0);
                m_fixturePlc.WriteShort(145, 1);
                WriteRunLog("扫码完成");
                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }

        }

        /*
       * @function：StartTestSignal()
       * @pararm：
       * @return：true/false
       * @action：获取开始测试信号（仅手动单元测试）
       */
        private bool StartTestSignal()
        {
            try
            {
                return m_fixturePlc.ReadShort(100) == 1;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }
        }

        /*
         * @function：ClearAlarm()
         * @pararm：
         * @return：true/false
         * @action：清除异常报警
         */
        private bool ClearAlarm()
        {
            try
            {
                bool bClear = true;
                bClear &= m_fixturePlc.WriteMRegister(7, true);
                Thread.Sleep(2000);
                bClear &= m_fixturePlc.WriteMRegister(7, false);
                if (!bClear)
                {
                    WriteRunLog("治具PLC复位失败，请手动复位或执行初始化", Color.Red);
                }

                bClear &= m_mainConPlc.WriteShort(40107, 0);
                bClear &= m_mainConPlc.WriteShort(40110, 0);
                bClear &= m_mainConPlc.WriteShort(40111, 0);
                if (!bClear)
                {
                    WriteRunLog("发送上料机复位完成信号错误！请检查上料机连接是否正常 并重启软件!", Color.Red);
                }
                lock (m_lockObj)
                {
                    //if (m_intsNgCount.Max(x => x) >= m_iNgCount)
                    if (getMaxValue(m_intsNgCount) >= m_iNgCount)
                    {
                        m_intsNgCount = new int[] { 0, 0, 0, 0 };
                    }
                    m_isAlarm = false;
                }

                return bClear;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                StopEngine();
                return false;
            }
        }

        /*
         * @function：LoadEnable()
         * @pararm：
         * @return：true/false
         * @action：是否允许上料
         */
        private bool LoadEnable()
        {
            try
            {
                int iRead = m_fixturePlc.ReadShort(98);//98=1：A工位在外面，需要上料。98=2：当前B工位在外面，需要上料
                if (iRead == 1) { m_strTurnTable = GlobalValue.ATurnTable; }
                else if (iRead == 2) { m_strTurnTable = GlobalValue.BTurnTable; }
                else { return false; }
                if (m_strTurnTable == GlobalValue.ATurnTable) //A在外面
                {
                    if (m_fixturePlc.ReadMRegister(85) || m_fixturePlc.ReadMRegister(86))//转盘A工位光纤检测有料为1.无料为0
                    {
                        return false;
                    }
                    else
                    {
                        if (m_isAUnloadAble) { return false; }
                    }
                }
                else if (m_strTurnTable == GlobalValue.BTurnTable) //B在外面
                {
                    if (m_fixturePlc.ReadMRegister(87) || m_fixturePlc.ReadMRegister(88))//转盘B工位光纤检测有料为1.无料为0
                    {
                        return false;
                    }
                    else
                    {
                        if (m_isBUnloadAble) { return false; }
                    }
                }
                //m_isLoad = false;
                if (!m_isLoadAlive) { return true; }
                return false;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                StopEngine();
                return false;
            }
        }

        /*
         * @function：UnLoadEnable()
         * @pararm：
         * @return：true/false
         * @action：是否允许下料
         */
        private bool UnLoadEnable()
        {
            try
            {
                ushort u16Read = m_fixturePlc.ReadShort(98); //A工位: 1，B工位: 2
                if (u16Read == 1)
                { 
                    if (!m_isAUnloadAble) { return false; }
                    if (m_isInit && !m_isUnloadAlive) { return true; }
                }
                else if (u16Read == 2)
                {
                    if (!m_isBUnloadAble) { return false; }
                }
                else { return false; }
                if (m_fixturePlc.ReadShort(151) != 1) { return false; }//转盘到达测试位
                if (!m_isUnloadAlive)
                {
                    if (!m_fixturePlc.WriteShort(151, 0))
                    {
                        throw new Exception("清除治具到位信号失败，请检查治具连接并重启程序");
                    }
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, Color.Red);
                StopEngine();
                return false;
            }
        }

        /*
         * @function：StartTestEnable()
         * @pararm：
         * @return：true/false
         * @action：是否允许测试
         */
        private bool StartTestEnable()
        {
            try
            {
                if (m_isTesting) { return false; }
                if (!m_bStartTest) { return false; }
                if (m_fixturePlc.ReadShort(100) != 1) { return false; }
                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                StopEngine();
                return false;
            }
        }
        #endregion startEngine
        /*
         * @function：LoadFunction(CancellationToken token)
         * @pararm：token
         * @return：void
         * @action：自动化上料，在获取条码后卡控
         */
        private void LoadFunction(CancellationToken token)
        {
            try
            {

                PauseAndStop(token);
                WriteRunLog(string.Format("检测到治具{0}可以上料", m_strTurnTable), Color.Black, true);
                DateTime startTime1 = DateTime.Now;
                int totalAlarmMin = 0;
                int iLoadValue = 0;
                int iSerialNum = 0;
                int iBarcodeLength = 0;
                int iReTest = 0;
                int iTurnTable = 0;
                ushort u16LoadCmd = 3;
                ushort u16Station = 0;

                // PLC清料中
                //if (m_fixturePlc.ReadShort(110) != 0)
                //{
                //    m_isLoadAlive = false;
                //    return;
                //}
                lock (m_lockObj)
                {
                    m_iTaskCount++;
                }
                if (m_mainConPlc.IsOpen && m_isConnect)
                {
                    iTurnTable = m_fixturePlc.ReadShort(98); // A工位写1，当前B工位写2
                    if (iTurnTable >= 3 || iTurnTable <= 0)
                    {
                        throw new Exception("读取治具工位编号失败，请检查治具连接并重启程序");
                    }
                    #region 复测
                    if (m_TestMode == TestMode.reTest)
                    {
                        while (!m_isAbort)
                        {
                            Thread.Sleep(2000);
                            if (DateTime.Now.Subtract(startTime1).TotalMinutes >= 5)
                            {
                                totalAlarmMin += 1;
                                WriteRunLog(string.Format("等待上料机写入载板穴位号:{0}超时{1}分钟", 40217, totalAlarmMin * 5), Color.Red, true);
                                startTime1 = DateTime.Now;
                            }
                            PauseAndStop(token);
                            iReTest = m_mainConPlc.ReadShort(40217); //载版穴位号
                            if ((iReTest & 0xff00) == DicCommand[3]) { continue; }
                            if (((iReTest & 0xf0) == 0x10 && iTurnTable == 1) || ((iReTest & 0xf0) == 0x20 && iTurnTable == 2))
                            {
                                DicCommand[3] = (ushort)(iReTest & 0xff00);
                                u16LoadCmd = (ushort)(iReTest & 0xf);
                            }
                            else { u16LoadCmd = 9; }
                            WriteRunLog(string.Format("已读取主控上位机写入的载板穴位号:[{0}-{1}]", 40217, iReTest));
                            break;
                        }
                    }
                    #endregion
                    if (!m_mainConPlc.WriteShort(40122, GetUploadValue(ref m_serialNum, u16LoadCmd, 1))) //40122 等待上料
                    {
                        throw new Exception("发送等待上料信号[40122]失败，请检查上料机连接并重启程序");
                    }
                }
                while (!m_isAbort)
                {
                    Thread.Sleep(2000);
                    iLoadValue = m_mainConPlc.ReadShort(40205); //上料完毕
                    if (DateTime.Now.Subtract(startTime1).TotalMinutes >= 5)
                    {
                        totalAlarmMin += 1;
                        WriteRunLog(string.Format("等待上料机上料完成信号:{0}超时{1}分钟", 40205, totalAlarmMin * 5), Color.Red, true);
                        startTime1 = DateTime.Now;
                    }
                    PauseAndStop(token);
                    if (iLoadValue == 0)
                    { continue; }

                    //已在GetUploadValue中add，此处判断可作为一项优化内容
                    if (DicCommand.Keys.Contains(1))
                    {
                        if ((iLoadValue & 0xff00) != DicCommand[1]) { continue; }
                    }
                    iSerialNum = iLoadValue;
                    iLoadValue &= 0xff;

                    #region 等待上料完成
                    Thread.Sleep(1000);
                    if (iLoadValue == 9 || iLoadValue == 0)
                    {
                        //改成给PLC发送空转指令，并且将允许下料标志置为false，A转盘无料空转，是m_isAUnloadable，
                        //B转盘无料空转则是m_isBUnloadable。同时，如果要空转，
                        //需要有一个变量来记录哪个无料转盘空转过了，
                        //主要用于判断是否可以将对应的允许下料标志直接置为true
                        if (iTurnTable == 2)//B模在外面
                        {
                            if (m_fixturePlc.WriteShort(180, 2)) //A模空转
                            {
                                m_ModuleDryRun_B = true;
                                m_isBUnloadAble = true;
                            }
                            else
                            {
                                throw new Exception("发送治具需要空转 180=2 失败，请检查治具连接");
                            }
                        }
                        if (iTurnTable == 1) //A模在外面
                        {
                            if (m_fixturePlc.WriteShort(182, 2))
                            {
                                m_ModuleDryRun_A = true;
                                m_isAUnloadAble = true;
                            }
                            else
                            {
                                throw new Exception("发送治具需要空转 182=2 失败，请检查治具连接");
                            }
                        }
                    }
                    else
                    {
                        if (iTurnTable == 2)
                        {
                            if (!m_fixturePlc.WriteShort(180, 1))
                            {
                                throw new Exception("发送治具正常放料 180=1 失败，请检查治具连接");
                            }
                        }
                        if (iTurnTable == 1)
                        {
                            if (!m_fixturePlc.WriteShort(182, 1))
                            {
                                throw new Exception("发送治具正常放料 182=1 失败，请检查治具连接");
                            }
                        }
                        m_station1 = Station.stationNone;
                        m_station2 = Station.stationNone;
                        if (iLoadValue != 2)
                        {
                            string strBarcode = "NULL";
                            iBarcodeLength = m_mainConPlc.ReadShort(40220);//产品1条码长度，  扫码失败长度写4，条码值写NULL”
                            if (iBarcodeLength > 50)
                            {
                                throw new Exception("读取1穴条码长度失败[40220]，请检查上料机连接并重启程序");
                            }
                            WriteRunLog(string.Format("读取1穴条码长度:[{0}-{1}]", 40220, iBarcodeLength));
                            if (iBarcodeLength != 4)
                            {
                                strBarcode = m_mainConPlc.readScannedSN(40221, 10);//产品1条码开始
                            }

                            if (strBarcode == "")
                            {
                                throw new Exception("读取1穴条码失败[40221]，请检查上料机连接并重启程序");
                            }

                            ETResult tmpEtResult = ProcessControl(strBarcode);
                            if (tmpEtResult == null || !tmpEtResult.isSuccess)
                            {
                                WriteRunLog(string.Format("{0}-条码卡站失败,此条码不进行测试！-{1}", strBarcode, tmpEtResult.message), Color.Red, true);
                                m_station1 = Station.stationNone;
                            }
                            else
                            {
                                Result result = new Result { barcode = strBarcode, testTimes = tmpEtResult.extensionCode, isSample = tmpEtResult.extensionMessages.BARCODE_FAMILY == "1" };
                                if (!m_isChecked)
                                {
                                    if (!result.isSample)
                                    {
                                        WriteRunLog(string.Format("当前班次未进行样本测试，条码[{0}]不是样本，不进行测试！", result.barcode), Color.Red, true);
                                        result.testTimes = 0;
                                    }
                                }
                                if (m_strTurnTable == GlobalValue.ATurnTable)
                                {
                                    m_station1 = Station.stationA1;
                                    if (DicBarcode.Keys.Contains(Station.stationA1))
                                    {
                                        DicBarcode[Station.stationA1] = result;
                                    }
                                    else
                                    {
                                        DicBarcode.Add(Station.stationA1, result);
                                    }
                                }
                                else if (m_strTurnTable == GlobalValue.BTurnTable)
                                {
                                    m_station1 = Station.stationB1;
                                    if (DicBarcode.Keys.Contains(Station.stationB1))
                                    {
                                        DicBarcode[Station.stationB1] = result;
                                    }
                                    else
                                    {
                                        DicBarcode.Add(Station.stationB1, result);
                                    }
                                }
                            }

                        }
                        if (iLoadValue != 1)
                        {
                            string strBarcode = "NULL";
                            iBarcodeLength = m_mainConPlc.ReadShort(40235);
                            if (iBarcodeLength > 50)
                            {
                                throw new Exception("读取2穴条码长度失败[40235]，请检查上料机连接并重启程序");
                            }
                            WriteRunLog(string.Format("读取2穴条码长度:[{0}-{1}]", 40235, iBarcodeLength));
                            if (iBarcodeLength != 4)
                            {
                                strBarcode = m_mainConPlc.readScannedSN(40236, 10);
                            }

                            if (strBarcode == "")
                            {
                                throw new Exception("读取2穴条码失败[40236]，请检查上料机连接并重启程序");
                            }

                            ETResult tmpEtResult = ProcessControl(strBarcode);
                            if (tmpEtResult == null || !tmpEtResult.isSuccess)
                            {
                                WriteRunLog(string.Format("{0}-条码卡站失败,此条码不进行测试！-{1}", strBarcode, tmpEtResult.message), Color.Red, true);
                                m_station2 = Station.stationNone;
                            }
                            else
                            {
                                Result result = new Result { barcode = strBarcode, testTimes = tmpEtResult.extensionCode, isSample = tmpEtResult.extensionMessages.BARCODE_FAMILY == "1" };
                                if (!m_isChecked)
                                {
                                    if (!result.isSample)
                                    {
                                        WriteRunLog(string.Format("当前班次未进行样本测试，条码[{0}]不是样本，不进行测试！", result.barcode), Color.Red, true);
                                        result.testTimes = 0;
                                    }
                                }
                                if (m_strTurnTable == GlobalValue.ATurnTable)
                                {
                                    m_station2 = Station.stationA2;
                                    if (DicBarcode.Keys.Contains(Station.stationA2))
                                    {
                                        DicBarcode[Station.stationA2] = result;
                                    }
                                    else
                                    {
                                        DicBarcode.Add(Station.stationA2, result);
                                    }
                                }
                                else if (m_strTurnTable == GlobalValue.BTurnTable)
                                {
                                    m_station2 = Station.stationB2;
                                    if (DicBarcode.Keys.Contains(Station.stationB2))
                                    {
                                        DicBarcode[Station.stationB2] = result;
                                    }
                                    else
                                    {
                                        DicBarcode.Add(Station.stationB2, result);
                                    }
                                }
                            }
                        }
                    }
                    #endregion 等待上料完成
                    //if (m_station1 == Station.stationNone && m_station2 == Station.stationNone)
                    //{
                    //    if (!m_fixturePlc.WriteShort(110, 1))
                    //    {
                    //        throw new Exception("发送治具执行清料信号失败，请检查治具连接");
                    //    }
                    //}
                    WriteRunLog(string.Format("上料完成信号:[{0}-{1}]", 40205, iSerialNum));//40205:上料完毕
                    if (iLoadValue >= 1 && iLoadValue <= 3)
                    {
                        u16Station = (ushort)(iLoadValue == 3 ? 2 : (iLoadValue == 1 ? 3 : 4));
                        if (!m_fixturePlc.WriteShort(iTurnTable == 1 ? 104 : 105, u16Station)) //转盘A工位双穴上料完成写2，1穴上料完成写3，2穴上料完成写4
                        {
                            throw new Exception("发送上料完成信号失败，请检查治具连接并重启程序");
                        }
                        WriteRunLog(string.Format("发送给治具上料完成信号{0}-{1}", iTurnTable == 1 ? 104 : 105, u16Station));
                        m_bStartTest = true;
                        break;
                    }
                    else
                    {
                        //if (!m_fixturePlc.WriteShort(iTurnTable == 1 ? 104 : 105, 2)) //转盘A工位双穴上料完成写2，1穴上料完成写3，2穴上料完成写4
                        //{
                        //    throw new Exception("发送上料完成信号失败，请检查治具连接并重启程序");
                        //}
                        m_bStartTest = true;
                        break;
                    }
                }
                //if (!m_mainConPlc.WriteShort(40122, 0))
                //{
                //    throw new Exception("清除等待上料信号失败[40122-0]，请检查上料机连接并重启程序");
                //}
                m_isLoadAlive = false;
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, Color.Red);
                m_isLoadAlive = false;
                StopEngine();
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }

        }

        /*
         * @function：UnLoadFunction(CancellationToken token)
         * @pararm：token
         * @return：void
         * @action：自动化下料
         */
        private void UnLoadFunction(CancellationToken token)
        {
            try
            {
                m_isUnloadAlive = true;
                DateTime startTime1 = DateTime.Now;
                int totalAlarmMin = 0;
                int iLoadValue = 0;
                int iSerialNum = 0;
                ushort u16Slot1 = 2;
                ushort u16Slot2 = 2;
                int iRead = m_fixturePlc.ReadShort(98);//A工位: 1，当前B工位: 2
                bool bWrite = false;
                PauseAndStop(token);
                WriteRunLog(string.Format("治具{0}开始下料", iRead == 1 ? "A-" : "B-"));
                lock (m_lockObj)
                {
                    m_iTaskCount++;
                }
                if (iRead == 1)  //A模
                {

                    bWrite |= m_fixturePlc.ReadMRegister(85);//转盘A工位1穴光纤检测有料为1.无料为0
                    bWrite |= m_fixturePlc.ReadMRegister(86);//转盘A工位2穴光纤检测有料为1.无料为0
                    u16Slot1 = (ushort)((!m_fixturePlc.ReadMRegister(85)) ? 3 : 2);
                    u16Slot2 = (ushort)((!m_fixturePlc.ReadMRegister(86)) ? 3 : 2);

                    //初始化后第一次下料，无料的情况
                    if (m_isInit)
                    {
                        if (u16Slot1 == 3 && u16Slot2 == 3) { bWrite = true; }
                    }

                    //程序重启或未测试
                    if (!DicBarcode.Keys.Contains(Station.stationA1) && !DicBarcode.Keys.Contains(Station.stationA2))
                    {
                        u16Slot1 = 3;
                        u16Slot2 = 3;
                        bWrite = true;
                    }

                    if (m_ModuleDryRun_A) { bWrite = true; }
                    if (!bWrite)
                    {
                        m_fixturePlc.WriteShort(151, 1);
                        throw new Exception("A转盘光纤检测无料，请检查治具");
                    }
                    #region A1模
                    if (DicBarcode.Keys.Contains(Station.stationA1))
                    {
                        Result result = DicBarcode[Station.stationA1];
                        if (!m_mainConPlc.WriteShort(40118, (ushort)(result.testResult ? (result.isSample ? 2 : 1) : 2)))
                        {
                            throw new Exception("写入1穴测试结果失败[40118]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入1穴测试结果:[{0}-{1}]", 40118, result.testResult ? (result.isSample ? 2 : 1) : 2));
                        removeKey(ref DicBarcode, Station.stationA1);
                    }
                    else
                    {

                        if (!m_mainConPlc.WriteShort(40118, u16Slot1))
                        {
                            throw new Exception(string.Format("写入1穴测试结果失败[40118-{0}]，请检查主控机是否连接，并重启程序", u16Slot1));
                        }
                        WriteRunLog(string.Format("写入1穴测试结果:[{0}-{1}]", 40118, u16Slot1));
                    }
                    #endregion
                    #region A2模
                    if (DicBarcode.Keys.Contains(Station.stationA2))
                    {
                        Result result = DicBarcode[Station.stationA2];
                        if (!m_mainConPlc.WriteShort(40119, (ushort)(result.testResult ? (result.isSample ? 2 : 1) : 2)))
                        {
                            throw new Exception("写入2穴测试结果失败[40119]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入2穴测试结果:[{0}-{1}]", 40119, result.testResult ? (result.isSample ? 2 : 1) : 2));
                        removeKey(ref DicBarcode, Station.stationA2);
                    }
                    else
                    {
                        if (!m_mainConPlc.WriteShort(40119, u16Slot2))
                        {
                            throw new Exception(string.Format("写入2穴测试结果失败[40119-{0}]，请检查主控机是否连接，并重启程序", u16Slot2));
                        }
                        WriteRunLog(string.Format("写入2穴测试结果:[{0}-{1}]", 40119, u16Slot2));
                    }
                    #endregion
                }
                else if (iRead == 2) //B模
                {
                    bWrite |= m_fixturePlc.ReadMRegister(87);
                    bWrite |= m_fixturePlc.ReadMRegister(88);

                    u16Slot1 = (ushort)((!m_fixturePlc.ReadMRegister(87)) ? 3 : 2);
                    u16Slot2 = (ushort)((!m_fixturePlc.ReadMRegister(88)) ? 3 : 2);

                    //初始化后第一次下料，无料的情况
                    if (m_isInit)
                    {
                        if (u16Slot1 == 3 && u16Slot2 == 3) { bWrite = true; }
                    }

                    //重启程序或未测试
                    if (!DicBarcode.Keys.Contains(Station.stationB1) && !DicBarcode.Keys.Contains(Station.stationB2))
                    {
                        u16Slot1 = 3;
                        u16Slot2 = 3;
                        bWrite = true;
                    }

                    if (m_ModuleDryRun_B) { bWrite = true; }
                    if (!bWrite)
                    {
                        m_fixturePlc.WriteShort(151, 1);
                        throw new Exception("B转盘光纤检测无料，请检查治具");
                    }
                    #region B1模
                    if (DicBarcode.Keys.Contains(Station.stationB1))
                    {
                        Result result = DicBarcode[Station.stationB1];
                        if (!m_mainConPlc.WriteShort(40118, (ushort)(result.testResult ? 1 : 2)))
                        {
                            throw new Exception("写入1穴测试结果失败[40118]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入1穴测试结果:[{0}-{1}]", 40118, result.testResult ? 1 : 2));
                        removeKey(ref DicBarcode, Station.stationB1);
                    }
                    else
                    {
                        if (!m_mainConPlc.WriteShort(40118, u16Slot1))
                        {
                            throw new Exception("写入1穴测试结果失败[40118-3]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入1穴测试结果:[{0}-{1}]", 40118, u16Slot1));
                    }
                    #endregion
                    #region B2模
                    if (DicBarcode.Keys.Contains(Station.stationB2))
                    {
                        Result result = DicBarcode[Station.stationB2];
                        if (!m_mainConPlc.WriteShort(40119, (ushort)(result.testResult ? 1 : 2)))
                        {
                            throw new Exception("写入2穴测试结果失败[40119]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入2穴测试结果:[{0}-{1}]", 40119, result.testResult ? 1 : 2));
                        removeKey(ref DicBarcode, Station.stationB2);
                    }
                    else
                    {
                        if (!m_mainConPlc.WriteShort(40119, u16Slot2))
                        {
                            throw new Exception("写入2穴测试结果失败[40119-3]，请检查主控机是否连接，并重启程序");
                        }
                        WriteRunLog(string.Format("写入2穴测试结果:[{0}-{1}]", 40119, u16Slot2));
                    }
                    #endregion
                    
                }
                else { m_isUnloadAlive = false; return; }
                if (!m_mainConPlc.WriteShort(40117, GetUploadValue(ref m_serialNum, 1, 2)))// 等待下料
                {
                    throw new Exception("写入等待下料信号失败[40117]，请检查上料机是否连接，并重启程序");
                }


                PauseAndStop(token);
                while (!m_isAbort)
                {
                    Thread.Sleep(2000);
                    iLoadValue = m_mainConPlc.ReadShort(40204);//40204 下料完成
                    if (DateTime.Now.Subtract(startTime1).TotalMinutes >= 5)
                    {
                        totalAlarmMin += 1;
                        WriteRunLog(string.Format("等待主控机下料完成信号:{0}超时{1}分钟", 40204, totalAlarmMin * 5), Color.Red, true);
                        startTime1 = DateTime.Now;
                    }
                    PauseAndStop(token);
                    if (iLoadValue == 0) { continue; }
                    if (iLoadValue > ushort.MaxValue)
                    {
                        throw new Exception("读取下料完成信号失败[40204]，请检查主控机是否连接，并重启程序");
                    }
                    if (DicCommand.Keys.Contains(2))
                    {
                        if ((iLoadValue & 0xff00) != DicCommand[2]) { continue; }
                    }
                    iSerialNum = iLoadValue;
                    iLoadValue &= 0xff;
                    //if (iLoadValue == 0) { continue; }
                    WriteRunLog(string.Format("主控机下料完成信号:[{0}-{1}]", 40204, iSerialNum));
                    if (bWrite)
                    {
                        if (!m_fixturePlc.WriteShort(106, 2)) //PC下料完成写2
                        {
                            throw new Exception("写入下料完成信号失败，请检查治具PLC，并重启程序");
                        }
                        WriteRunLog(string.Format("通知治具下料完成"));
                    }
                    if (iRead == 1)
                    {
                        lock (m_lockObj)
                        {
                            m_isAUnloadAble = false;
                            m_ModuleDryRun_A = false;
                        }
                    }
                    else if (iRead == 2)
                    {
                        lock (m_lockObj)
                        {
                            m_isBUnloadAble = false;
                            m_ModuleDryRun_B = false;
                            if (m_isInit) { m_isInit = false; }
                        }
                    }
                    break;
                }
                m_isUnloadAlive = false;
                //m_isUnLoad = false;
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, Color.Red, true);
                m_isUnloadAlive = false;
                StopEngine();
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }
        }
        #region testing process

        /*
        * @function：TestFunction(CancellationToken token, Station station1 = Station.stationNone, Station station2 = Station.stationNone)
        * @pararm：
        * token：票据
        * station1：1穴编号
        * station2：2穴编号
        * @return：void
        * @action：测试功能，流程为：触发单片机测试->输出测试数据到程序主界面->测试数据保存至本地并上传->更新良率->点检(仅样本模式)->测试结束或复测
        */
        private void TestFunction(CancellationToken token, Station station1 = Station.stationNone, Station station2 = Station.stationNone)
        {
            int iRead = m_fixturePlc.ReadShort(98);
            string strTurnTable = iRead == 2 ? GlobalValue.ATurnTable : GlobalValue.BTurnTable;
            Result reSlot1 = new Result();
            Result reSlot2 = new Result();
            bool bRetestAble = true;
            lock (m_lockObj)
            {
                m_iTaskCount++;
            }
            try
            {
                m_bStartTest = false;
                m_dtStartTime = DateTime.Now;

                if (strTurnTable == GlobalValue.ATurnTable)
                {
                    if (DicBarcode.Keys.Contains(Station.stationA1))
                    {
                        WriteRunLog(string.Format("开始读取已保存的A1数据"));
                        reSlot1 = DicBarcode[Station.stationA1];
                        station1 = Station.stationA1;
                        WriteRunLog(string.Format("已读取保存的A1数据"));
                    }
                    if (DicBarcode.Keys.Contains(Station.stationA2))
                    {
                        WriteRunLog(string.Format("开始读取已保存的A2数据"));
                        reSlot2 = DicBarcode[Station.stationA2];
                        station2 = Station.stationA2;
                        WriteRunLog(string.Format("已读取保存的A2数据"));
                    }
                }
                else
                {
                    if (DicBarcode.Keys.Contains(Station.stationB1))
                    {
                        WriteRunLog(string.Format("开始读取已保存的B1数据"));
                        reSlot1 = DicBarcode[Station.stationB1];
                        station1 = Station.stationB1;
                        WriteRunLog(string.Format("已读取保存的B1数据"));
                    }
                    if (DicBarcode.Keys.Contains(Station.stationB2))
                    {
                        WriteRunLog(string.Format("开始读取已保存的B2数据"));
                        reSlot2 = DicBarcode[Station.stationB2];
                        station2 = Station.stationB2;
                        WriteRunLog(string.Format("已读取保存的B2数据"));
                    }
                }
                Status status1 = station1 == Station.stationNone ? Status.statusIdel : Status.statusTest;
                Status status2 = station2 == Station.stationNone ? Status.statusIdel : Status.statusTest;
                string strTestResult1 = "";
                string strTestResult2 = "";
                bool bTestResult1 = false;
                bool bTestResult2 = false;
                bool bUploadResult1 = false;
                bool bUploadResult2 = false;
                List<TestItem> testItems1 = new List<TestItem>();
                List<TestItem> testItems2 = new List<TestItem>();
                int iTestCount = 0;
                int iLoopTimes = reSlot1.testTimes >= reSlot2.testTimes ? reSlot1.testTimes : reSlot2.testTimes;
                updateBarcode(station1, reSlot1.barcode);
                updateBarcode(station2, reSlot2.barcode);
                WriteRunLog("开始测试");
                do
                {
                    if (iLoopTimes <= 0)
                    {
                        testFinish(strTurnTable, Status.statusIdel, Status.statusIdel, iTestCount < iLoopTimes);
                        break;
                    }
                    updateTestTime(strTurnTable, true);
                    updateAllTestStatus(strTurnTable, Status.statusTest);
                    GetUploadValue(ref m_serialNum, 0);
                    updateTestStatus(station1, status1);
                    updateTestStatus(station2, status2);
                    PauseAndStop(token);

                    iTestCount++;
                    reSlot1.startTime = reSlot2.startTime = DateTime.Now;
                    Task task1 = new Task(() => { if (station1 != Station.stationNone && status1 == Status.statusTest && reSlot1.testTimes > 0) { strTestResult1 = m_mcu1.Test(GlobalValue.testCommand); } });
                    Task task2 = new Task(() => { if (station2 != Station.stationNone && status2 == Status.statusTest && reSlot2.testTimes > 0) { strTestResult2 = m_mcu2.Test(GlobalValue.testCommand); } });
                    task1.Start();
                    task2.Start();
                    Task.WaitAll(task1, task2);
                    PauseAndStop(token);

                    if (station1 != Station.stationNone && status1 == Status.statusTest && reSlot1.testTimes > 0)
                    {
                        testItems1 = AnalysisMcuResult(strTestResult1, out bTestResult1);
                        reSlot1.items = testItems1;
                        reSlot1.testResult = bTestResult1;
                        showTestDataList(station1, testItems1);
                        reSlot1.endTime = DateTime.Now;
                        bUploadResult1 = WriteData(strTurnTable, station1, reSlot1.barcode, testItems1, m_dtStartTime, DateTime.Now, bTestResult1);
                        status1 = bTestResult1 & bUploadResult1 ? Status.statusPass : Status.statusFail;
                        bRetestAble &= bTestResult1;
                        if (iTestCount >= iLoopTimes && !m_isSample)
                        { updateYield(station1, bTestResult1 & bUploadResult1 ? 1 : 0, bTestResult1 & bUploadResult1 ? 0 : 1); }
                        if (reSlot1.isSample)
                        {
                            string strFailItem1 = "";
                            foreach (var item in reSlot1.items)
                            {
                                if (!item.Result)
                                {
                                    strFailItem1 += string.Format("{0};", item.Name);
                                }
                            }
                            SampleCompare(reSlot1.barcode, strTurnTable, station1, strFailItem1, bTestResult1, reSlot1.endTime);
                            m_isChecked = true;
                            configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyCheckDate, string.Format("{0:yyyyMMdd}_{1}", DateTime.Now, m_isDay ? "D" : "N"));
                        }
                        PauseAndStop(token);
                        if (station1 == Station.stationA1)
                        {
                            m_intsNgCount[0] = bTestResult1 ? 0 : m_intsNgCount[0] + 1;
                        }
                        if (station1 == Station.stationB1)
                        {
                            m_intsNgCount[1] = bTestResult1 ? 0 : m_intsNgCount[1] + 1;
                        }
                    }

                    if (station2 != Station.stationNone && status2 == Status.statusTest && reSlot2.testTimes > 0)
                    {
                        testItems2 = AnalysisMcuResult(strTestResult2, out bTestResult2);
                        reSlot2.items = testItems2;
                        reSlot2.testResult = bTestResult2;
                        showTestDataList(station2, testItems2);
                        reSlot2.endTime = DateTime.Now;
                        bUploadResult2 = WriteData(strTurnTable, station2, reSlot2.barcode, testItems2, m_dtStartTime, DateTime.Now, bTestResult2);
                        status2 = bTestResult2 & bUploadResult2 ? Status.statusPass : Status.statusFail;
                        bRetestAble &= bTestResult2;
                        if (iTestCount >= iLoopTimes && !m_isSample)
                        { updateYield(station2, bTestResult2 & bUploadResult2 ? 1 : 0, bTestResult2 & bUploadResult2 ? 0 : 1); }
                        if (reSlot2.isSample)
                        {
                            string strFailItem2 = "";
                            foreach (var item in reSlot2.items)
                            {
                                if (!item.Result)
                                {
                                    strFailItem2 += string.Format("{0};", item.Name);
                                }
                            }
                            SampleCompare(reSlot2.barcode, strTurnTable, station2, strFailItem2, bTestResult2, reSlot2.endTime);
                            m_isChecked = true;
                            configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyCheckDate, string.Format("{0:yyyyMMdd}_{1}", DateTime.Now, m_isDay ? "D" : "N"));
                        }
                        PauseAndStop(token);
                        if (station2 == Station.stationA2)
                        {
                            m_intsNgCount[2] = bTestResult2 ? 0 : m_intsNgCount[2] + 1;
                        }
                        if (station2 == Station.stationB2)
                        {
                            m_intsNgCount[3] = bTestResult2 ? 0 : m_intsNgCount[3] + 1;
                        }
                    }

                    testFinish(strTurnTable, status1, status2, iTestCount < iLoopTimes && bRetestAble);
                    reSlot1.testTimes--;
                    reSlot2.testTimes--;
                    DicBarcode[station1] = reSlot1;
                    DicBarcode[station2] = reSlot2;
                    m_iUseCount += 1;
                    if (m_iUseCount >= m_iProbeCount)
                    {
                        DialogResult result = MessageBox.Show(string.Format("探针使用次数已达上限{0}, 请更换探针！", m_iProbeCount), "提示", MessageBoxButtons.OKCancel, MessageBoxIcon.Information, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                        if (result == DialogResult.OK)
                        {
                            m_iUseCount = 0;
                        }
                    }
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyUseCount, m_iUseCount.ToString());
                    if (!bRetestAble) { break; }
                    if (m_TestMode == TestMode.reTest && iTestCount < iLoopTimes)
                    {
                        //全部测两次
                        //status1 = status1 == Status.statusIdel ? Status.statusIdel : Status.statusTest;
                        //status2 = status2 == Status.statusIdel ? Status.statusIdel : Status.statusTest;

                        //NG的不测第二次
                        status1 = status1 == Status.statusIdel ? Status.statusIdel : status1 != Status.statusPass ? Status.statusFail : Status.statusTest;
                        status2 = status2 == Status.statusIdel ? Status.statusIdel : status2 != Status.statusPass ? Status.statusFail : Status.statusTest;
                        if (!waitReTest()) { break; }
                    }
                }
                while (iTestCount < iLoopTimes && !m_isAbort);
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                testFinish(strTurnTable, Status.statusError, Status.statusError);
                StopEngine();
                lock (m_lockObj)
                {
                    m_iTaskCount--;
                }
            }
        }

        /*
       * @function：testStatus(string strTurnTable, Status status1, Status status2)
       * @pararm：
       * strTurnTable：转盘编号
       * status1：1穴状态
       * status2：2穴状态
       * @return：void
       * @action：更新测试状态
       */
        private void testStatus(string strTurnTable, Status status1, Status status2)
        {
            Status status = Status.statusIdel;
            if (status1 == Status.statusIdel || status2 == Status.statusIdel)
            {
                status = status1 == Status.statusIdel ? status2 : status1;
            }
            else if (status1 != Status.statusPass || status2 != Status.statusPass)
            {
                status = status1 != Status.statusPass ? status1 : status2;
            }
            else
            {
                status = status1 == Status.statusFail ? status2 : status1;
            }
            if (strTurnTable == GlobalValue.ATurnTable)
            {
                updateTestStatus(Station.stationA1, status1);
                updateTestStatus(Station.stationA2, status2);
            }
            else if (strTurnTable == GlobalValue.BTurnTable)
            {
                updateTestStatus(Station.stationB1, status1);
                updateTestStatus(Station.stationB2, status2);
            }
            updateAllTestStatus(strTurnTable, status);
        }


        /*
         * @function：testFinish(string strTurnTable, Status status1, Status status2, bool bWhetherRe = false)
         * @pararm：
         * strTurnTable：转盘编号
         * status1：1穴状态
         * status2：2穴状态
         * bWhetherRe：是否复测
         * @return：void
         * @action：测试结束
         */
        private void testFinish(string strTurnTable, Status status1, Status status2, bool bWhetherRe = false)
        {
            try
            {
                testStatus(strTurnTable, status1, status2);
                updateTestTime(strTurnTable, false);

                if (!bWhetherRe)
                {
                    if (!m_isAutoMode)
                    {
                        if (strTurnTable == GlobalValue.ATurnTable)
                        {
                            removeKey(ref DicBarcode, Station.stationA1);
                            removeKey(ref DicBarcode, Station.stationA2);
                        }
                        else if (strTurnTable == GlobalValue.BTurnTable)
                        {
                            removeKey(ref DicBarcode, Station.stationB1);
                            removeKey(ref DicBarcode, Station.stationB2);
                        }
                    }

                    if (!m_fixturePlc.WriteShort(102, 1))
                    {
                        WriteRunLog("发送治具PLC测试完成信号失败！请检查治具PLC连接是否正常 并重启软件!", GlobalKey.colorRed);
                    }
                    WriteRunLog("发送测试完成信号");
                    Thread.Sleep(300);
                    m_isTesting = false;
                    m_isAlarm = false;
                    if (strTurnTable == GlobalValue.ATurnTable) { m_isAUnloadAble = true; }
                    if (strTurnTable == GlobalValue.BTurnTable) { m_isBUnloadAble = true; }
                }
                else
                {
                    if (!m_fixturePlc.WriteShort(102, 3))
                    {
                        WriteRunLog("发送治具PLC测试完成信号失败！请检查治具PLC连接是否正常 并重启软件!", GlobalKey.colorRed);
                    }
                    WriteRunLog("发送复测完成信号");
                }

            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                StopEngine();
            }
        }

        /*
       * @function：CheckSn(string strBarcode)
       * @pararm：
       * strBarcode：条码
       * @return：true/false
       * @action：检测条码是否符合规则（暂不启用）
       */
        public bool CheckSn(string strBarcode)
        {
            try
            {
                return strBarcode.Replace("\r\n", "").Length == int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyBarcodeLenth]);
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }

        }

        /*
      * @function：ProcessControl(string strBarcode)
      * @pararm：
      * strBarcode：条码
      * @return：
      * ETResult：卡控返回信息      
      * @action：条码卡控
      */
        public ETResult ProcessControl(string strBarcode)
        {
            ETResult result = new ETResult();

            string tmpProgram = configure.configData[GlobalValue.secApp][GlobalValue.keyProgram];
            string tmpApiAddress = configure.configData[GlobalValue.secApp][GlobalValue.keyApiAddress];
            string tmpApiPath = configure.configData[GlobalValue.secApp][GlobalValue.keyApiProcessPath];
            string tmpOperatorID = configure.configData[GlobalValue.secApp][GlobalValue.keyOperator];
            string tmpToolNumber = configure.configData[GlobalValue.secApp][GlobalValue.keyFixtureId];
            string tmpTestType = configure.configData[GlobalValue.secApp][GlobalValue.keyTestType];
            string tmpPreviousTestType = configure.configData[GlobalValue.secApp][GlobalValue.keyPreTestType];
            string tmpProductName = configure.configData[GlobalValue.secApp][GlobalValue.keyProductName];
            string tmpWorkArea = configure.configData[GlobalValue.secApp][GlobalValue.keyWorkArea];
            string tmpSite = configure.configData[GlobalValue.secApp][GlobalValue.keySite];
            string tmpLot = configure.configData[GlobalValue.secApp][GlobalValue.keyLot];
            string tmpProjectName = configure.configData[GlobalValue.secApp][GlobalValue.keyProjectName];
            if (configure.configData[GlobalValue.secApp][GlobalValue.keyProcess] != "Y")
            {
                result.extensionCode = 1;
                result.isSuccess = true;
                result.extensionMessages = new extensionMessages { BARCODE_FAMILY = "0", TESTED_COUNT = "0" };
                result.extensionMessages.BARCODE_FAMILY = "0";
                return result;
            }
            MFLEXMes mfetTest = new MFLEXMes
            {
                ApiAddress = tmpApiAddress,
                ApiPath = tmpApiPath,
                Barcode = strBarcode,
                OperatorID = tmpOperatorID,
                ToolNumber = tmpToolNumber,
                TestType = tmpTestType,
                PreviousTestType = tmpPreviousTestType,
                ProductName = tmpProductName,
                WorkArea = tmpWorkArea,
                Site = tmpSite,
                Program = tmpProgram,
                Lot = tmpLot,
                IpAddress = m_strLocalIp,
                StationTime = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss")
            };

            //string[] tmpProgramComponents = tmpProgram.Split(new[] { "-" }, StringSplitOptions.RemoveEmptyEntries);
            //if (tmpProgramComponents == null || tmpProgramComponents.Length != 4)
            //{
            //    MessageBox.Show("参数测试程序设置错误，请重新配置！配置规则为:内部料号-站位-阶段-版本", "警告", MessageBoxButtons.OK, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
            //    return null;
            //}

            string tmpSfcCommand, tmpSfcMessage;
            DateTime startTime = DateTime.Now;
            object tmpSfcObject = mfetTest.PreviousValidation(out tmpSfcCommand, out tmpSfcMessage);
            WriteRunLog(tmpSfcCommand);
            WriteRunLog(tmpSfcMessage);
            DateTime endTime = DateTime.Now;
            if (tmpSfcObject == null)
            {
                MessageBox.Show(string.Format("获取卡站数据错误，请检查网络或参数设置是否正确-{0}", tmpSfcMessage), "警告", MessageBoxButtons.OK, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                return null;
            }

            ETResult tmpResult = (ETResult)tmpSfcObject;
            AllLog csvLog = new AllLog();
            txtLog.writeTxtLog(string.Format("barcode:{0},result:{1},command:{2},message:{3}", strBarcode, tmpResult.isSuccess, tmpSfcCommand, tmpSfcMessage));
            string dirName = configure.configData[GlobalValue.secMes][GlobalValue.keyProcessUrl] + tmpProductName;
            csvLog.setDir(dirName);
            string strTitle = "";
            string strValue = "";
            csvLog.path = combineProcessData(out strTitle, out strValue, strBarcode, startTime, endTime, startTime.Subtract(endTime).TotalMilliseconds, tmpResult.isSuccess, tmpResult.extensionCode, tmpResult.message, tmpProjectName, tmpToolNumber, tmpProgram, m_strLocalIp, tmpTestType);
            csvLog.writeCsvLog(strValue, strTitle);
            WriteRunLog(string.Format("卡站结果：{0}", tmpResult.isSuccess ? "PASS" : "FAIL"), tmpResult.isSuccess ? Color.Green : Color.Red);

            string tmpInfo = tmpResult.message;
            WriteRunLog(tmpInfo, tmpResult.isSuccess ? Color.Black : Color.Red);
            return tmpResult;
        }

        /*
         * @function：combineProcessData(out string strTitle, out string strValue, string barcode, DateTime startTime, DateTime endTime, double ms, bool result, int extensionCode, string reason, string projectName, string fixtureID, string program, string localIP, string testType)
         * @pararm：
         * strTitle：标题
         * strValue：保存数据
         * @return：
         * string：保存文件名
         * @action：条码卡控
         */
        public string combineProcessData(out string strTitle, out string strValue, string barcode, DateTime startTime, DateTime endTime, double ms, bool result, int extensionCode, string reason, string projectName, string fixtureID, string program, string localIP, string testType)
        {
            strTitle = "Barcode,StartTime,EndTime,ElapsedTime(ms),CheckResult,extensionCode,Reason";
            strValue = string.Format("{0},{1},{2},{3},{4},{5},{6}", barcode, startTime, endTime, ms, result, extensionCode, reason);
            int date = Convert.ToInt32(DateTime.Now.ToString("HH"));
            string DorN = date >= 7 && date < 19 ? "D" : "N";
            if (date >= 0 && date < 7)
            {
                endTime = endTime.AddDays(-1);
            }
            string tmpLocalName = string.Format("{0}_{1}_{2}_{3:yyyyMMdd}_{4}_{5}_{6}_{7}.csv", projectName, fixtureID, program.Replace("-", "_"), endTime, localIP, "GTS", testType, DorN);
            return tmpLocalName;
        }

        /*
         * @function：WriteData(string strTurnTable ,string barcode, List<TestItem> items, DateTime startTime, DateTime endTime, bool testResult)
         * @pararm：
         * strTurnTable：转盘编号
         * barcode：条码
         * items：测试数据
         * startTime：测试开始时间
         * endTime：测试结束时间
         * testResult：测试结果
         * @return：true/false
         * @action：保存并上传测试数据
         */
        public bool WriteData(string strTurnTable, Station station, string barcode, List<TestItem> items, DateTime startTime, DateTime endTime, bool testResult)
        {
            try
            {
                if (!m_isAutoMode) { return true; }
                string tmpWorkArea = configure.configData[GlobalValue.secApp][GlobalValue.keyWorkArea];
                string tmpResourceName = configure.configData[GlobalValue.secApp][GlobalValue.keyResourceName];
                string tmpProgram = configure.configData[GlobalValue.secApp][GlobalValue.keyProgram];
                string tmpOperatorID = configure.configData[GlobalValue.secApp][GlobalValue.keyOperator];
                string tmpPartNumber = configure.configData[GlobalValue.secApp][GlobalValue.keySerialNumber];
                string tmpLineID = configure.configData[GlobalValue.secApp][GlobalValue.keyLineId];
                string tmpFixtureID = configure.configData[GlobalValue.secApp][GlobalValue.keyFixtureId];
                string tmpProjectName = configure.configData[GlobalValue.secApp][GlobalValue.keyProductName];
                string testType = configure.configData[GlobalValue.secApp][GlobalValue.keyTestType];
                string tmpSWVersion = configure.configData[GlobalValue.secApp][GlobalValue.keyVersion];
                if (string.IsNullOrEmpty(tmpPartNumber))
                {
                    WriteRunLog("料号不能为空，请先设置料号!", GlobalKey.colorRed);
                    return false;
                }
                if (string.IsNullOrEmpty(barcode))
                {
                    WriteRunLog("条码为空!", GlobalKey.colorRed);
                    return false;
                }
                if (items == null || items.Count <= 0)
                {
                    WriteRunLog("测试数据为空!", GlobalKey.colorRed);
                    return false;
                }

                string failitems = "";
                string failValue = "";
                foreach (TestItem item in items)
                {
                    if (!item.Result)
                    {
                        failitems += item.Name + ";";
                        failValue += item.Value + ";";
                        //if (isSample) break;
                    }

                }
                string tmpGuid = Guid.NewGuid().ToString("N").ToUpper();

                TimeSpan ts = DateTime.Now - new DateTime(1970, 1, 1, 0, 0, 0, 0);
                string tmpTimeStamp = Convert.ToInt64(ts.TotalMilliseconds).ToString();
                string tmpTestResult = testResult ? "PASS" : "FAIL";
                int date = Convert.ToInt32(DateTime.Now.ToString("HH"));
                string DorN = date >= 7 && date < 19 ? "D" : "N";
                if (date >= 0 && date < 7)
                {
                    endTime = endTime.AddDays(-1);
                }
                string tmpLocalName = string.Format("{0}_{1}_{2}_{3:yyyyMMdd}_{4}_{5}_{6}_{7}.csv", tmpProjectName, tmpFixtureID, tmpProgram.Replace("-", "_"), endTime, m_strLocalIp, "GTS", testType, DorN);
                string csvTitle = "Test\nSerialNumber,Test Pass/Fail Status,errCode,errStr,TesterID,config,timeStamp,StartTime,EndTime,TestTime,Failing items,errValue,holder,slot,testModel,swversion,attribute1,attribute2,attribute3,attribute4";
                string csvLowLimit = "Lower Limit----->,,,,,,,,,,,,,,,,,,,";
                string csvUpperLimit = "Upper Limit----->,,,,,,,,,,,,,,,,,,,";
                string csvUnit = "Measurement Unit----->,,,,,,,,,Sec,,,,,,,,,,";
                string failItems = "";
                string failvalue = "";
                string csvValue = "";
                List<string> ErrorCode = new List<string>();
                List<string> ErrorStr = new List<string>();
                foreach (TestItem item in items)
                {
                    csvTitle += string.Format(",{0}", item.Name);
                    csvLowLimit += string.Format(",{0}", item.Low);
                    csvUpperLimit += string.Format(",{0}", item.High);
                    csvUnit += string.Format(",{0}", item.Unit);
                    csvValue += string.Format(",{0}", item.Value);

                    if (item.Result == false)
                    {
                        failvalue += string.Format("{0};", item.Value);
                        failItems += string.Format("{0};", item.Name);

                        if (item.Name.ToUpper().Contains("SHORT"))
                        {
                            if (!ErrorCode.Contains("90")) ErrorCode.Add("90");
                            if (!ErrorStr.Contains("Short")) ErrorStr.Add("Short");
                        }
                        else if (item.Name.ToUpper().Contains("OPEN"))
                        {
                            if (!ErrorCode.Contains("70")) ErrorCode.Add("70");
                            if (!ErrorStr.Contains("Open")) ErrorStr.Add("Open");
                        }
                        else
                        {
                            if (!ErrorCode.Contains("100")) ErrorCode.Add("100");
                            if (!ErrorStr.Contains("Components")) ErrorStr.Add("Components");
                        }
                    }
                }

                TimeSpan sp = endTime - startTime;

                string tmpErrorCode = string.Join(";", ErrorCode.Distinct().ToArray());
                string tmpErrorStr = string.Join(";", ErrorStr.Distinct().ToArray());
                AllLog csvLog = new AllLog();
                string csvTestValue = string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},,",
                    barcode, tmpTestResult, failItems, "", tmpFixtureID, tmpPartNumber, tmpTimeStamp, startTime,
                    endTime, sp.TotalSeconds.ToString(), failItems, failvalue,
                    strTurnTable == GlobalValue.ATurnTable ? "1" : "2", (station == Station.stationA1 || station == Station.stationB1) ? "1" : "2",
                    testType, tmpSWVersion, tmpGuid, tmpOperatorID);
                csvLog.setDir(@"D:/Log/CSVLog");
                csvLog.path = tmpLocalName;
                if (!csvLog.writeCsvLog(csvTestValue + csvValue, csvTitle + "\n" + csvLowLimit + "\n" + csvUpperLimit + "\n" + csvUnit))
                {
                    WriteRunLog("保存本地测试数据失败，请检查本地保存路径是否存在", GlobalKey.colorRed);
                    //return false;
                }

                if (!m_isUpload) { return true; }
                MFLEXMes mfetTest = new MFLEXMes
                {
                    ApiAddress = configure.configData[GlobalValue.secApp][GlobalValue.keyApiAddress],
                    ApiPath = configure.configData[GlobalValue.secApp][GlobalValue.keyApiUploadPath],
                    Barcode = barcode,
                    OperatorID = tmpOperatorID,
                    WorkArea = tmpWorkArea,
                    ResourceName = tmpResourceName,
                    IpAddress = m_strLocalIp,
                    ToolNumber = tmpFixtureID,
                    ProductName = tmpPartNumber,
                    Program = tmpProgram,
                    TestTime = endTime,
                    slotName = strTurnTable == GlobalValue.ATurnTable ? "1" : "2",
                    subslotName = (station == Station.stationA1 || station == Station.stationB1) ? "1" : "2"
                };

                //string tmpSoundErrorCode, tmpSoundErrorValue;
                //GenerateErrorInformation(items, out tmpSoundErrorCode, out tmpSoundErrorValue);
                List<ETDetail> tmpTestDetails = new List<ETDetail>
                    {
                        //new ETDetail {header = "serialNumber", value = result.Barcode},
                        //new ETDetail {header = "startTime", value = result.EndTime.ToString()}

                        new ETDetail {header = "serialNumber", value = barcode},
                        new ETDetail {header = "Test Pass/Fail Status",value=testResult ? "PASS" : "FAIL"},
                        new ETDetail {header = "errCode",value=failitems},
                        new ETDetail {header = "errStr",value=null},
                         new ETDetail {header = "TesterID",value=tmpFixtureID},//设备编号
                        new ETDetail {header = "config",value=tmpProjectName},//产品料号
                        new ETDetail {header = "timeStamp",value=tmpTimeStamp},
                        new ETDetail {header = "startTime", value = startTime.ToString("yyyy/MM/dd HH:mm:ss")},
                        new ETDetail {header = "EndTime", value=endTime.ToString("yyyy/MM/dd HH:mm:ss")},
                        new ETDetail {header = "TestTime",measureUnit="sec",value=new TimeSpan(endTime.Ticks-startTime.Ticks).TotalSeconds.ToString()},

                        new ETDetail {header = "Failing items",value=failitems},//为产品测试不良明细，长度小于 100，产品 PASS 为空,命名规则是原理图元件名+点位，比如：J101.1
                        new ETDetail {header = "errValue",value=failValue},//产品测试不良测试值，长度小于 20，产品 PASS 为空。
                        new ETDetail {header = "holder",value=strTurnTable == GlobalValue.ATurnTable ? "1" : "2"},//治具载板编号。
                        new ETDetail {header = "slot",value= (station == Station.stationA1 || station == Station.stationB1) ? "1" : "2"},//治具穴位编号
                        new ETDetail {header = "testModel",value=testType},//产品测试类型
                        new ETDetail {header = "swversion",value=tmpSWVersion},//为下位机测试程式
                        new ETDetail {header = "attribute1",value=tmpGuid},//GUID
                        new ETDetail {header = "attribute2",value=tmpOperatorID},
                        new ETDetail {header = "attribute3",value=null},
                        new ETDetail {header = "attribute4",value=null}
                    };

                foreach (TestItem tmpItem in items)
                {
                    tmpTestDetails.Add(new ETDetail { header = tmpItem.Name, lowerLimit = tmpItem.Low, upperLimit = tmpItem.High, measureUnit = tmpItem.Unit, value = tmpItem.Value });
                }

                ETItem tmpETItem = new ETItem
                {
                    barcode = barcode,
                    Operator = tmpOperatorID,
                    errorCode = failitems,
                    ipAddress = m_strLocalIp,
                    productName = tmpPartNumber,
                    program = tmpProgram,
                    resourceName = tmpResourceName,
                    toolNumber = tmpFixtureID,
                    workArea = tmpWorkArea,
                    testResult = testResult ? "PASS" : "FAIL",
                    testTime = endTime.ToString("yyyy-MM-ddTHH:mm:ss"),
                    testType = testType,
                    errorValue = null,
                    testDetailId = tmpGuid,
                    testDetails = tmpTestDetails,
                    slotName = strTurnTable == GlobalValue.ATurnTable ? "1" : "2",
                    subslotName = (station == Station.stationA1 || station == Station.stationB1) ? "1" : "2",
                    extendInfo = "A:GTS;B:RCR"
                };
                string tmpSfcCommand, tmpSfcMessage;
                bool flag = mfetTest.UploadTestResult(tmpETItem, out tmpSfcCommand, out tmpSfcMessage);
                //barcode, flag, string.Format("{0} POST", testType ?? ""), tmpSfcCommand, tmpSfcMessage
                txtLog.writeTxtLog(string.Format("BARCODE:{0},UPLOAD:{1},COMMAND:{2},MESSAGE:{3}", barcode, flag ? "SUCCESS" : "FAIL", tmpSfcCommand, tmpSfcMessage));
                WriteRunLog(string.Format("{0}测试数据上传{1}", barcode, flag ? "成功" : "失败"), flag ? Color.Black : Color.Red);
                if (flag)
                {
                    string tmpDayDir = Path.Combine(configure.configData[GlobalValue.secMes][GlobalValue.keyMesUrl], tmpPartNumber.Substring(0, 5));
                    csvLog.setDir(tmpDayDir);
                    csvLog.path = tmpLocalName;
                    if (!csvLog.writeCsvLog(csvTestValue + csvValue, csvTitle + "\n" + csvLowLimit + "\n" + csvUpperLimit + "\n" + csvUnit))
                    {
                        WriteRunLog("csv写入错误，请检查day csv路径是否存在，是否有写入权限", Color.Red, true);
                    }
                }
                return true;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, GlobalKey.colorRed);
                return false;
            }
        }

        /*
        * @function：SampleCompare(string sn, string strTurnTable, Station station, string failItems, bool testResult, DateTime endTime)
        * @pararm：
        * sn：条码
        * strTurnTable：转盘编号
        * station：穴位编号
        * failItems：测试失败项
        * testResult：测试结果
        * endTime：测试结束时间
        * @return：void
        * @action：点检功能
        */
        private void SampleCompare(string sn, string strTurnTable, Station station, string failItems, bool testResult, DateTime endTime)
        {
            string tmpPartNumber = configure.configData[GlobalValue.secApp][GlobalValue.keySerialNumber];
            string tmpFixtureID = configure.configData[GlobalValue.secApp][GlobalValue.keyFixtureId];
            string tmpTestType = configure.configData[GlobalValue.secApp][GlobalValue.keyTestType];
            string tmpSampleSave = configure.configData[GlobalValue.secMes][GlobalValue.keySampleUrl];

            List<ETsample> tmpSamples = GetETShiftSamples();
            if (tmpSamples == null || tmpSamples.Count == 0)
            {
                return;
            }

            ETsample eTsample = tmpSamples.Find((item) => item.barcode.Equals(sn));
            if (eTsample == null)
            {
                WriteRunLog(string.Format("未找到样品板{0}当班有效记录，请检查！", sn), Color.Red, true);
                return;
            }
            string tmpTargetFailItems = eTsample.defectCode;
            WriteRunLog(string.Format("TargetFailItems:{0}", tmpTargetFailItems), Color.Black, true);

            bool tmpCompareResult = eTsample.isResultMatched;
            if (tmpSampleSave == "")
            {
                WriteRunLog("样品板当班有效记录保存路径为空，请检查！", Color.Red, true);
                return;
            }
            tmpSampleSave = tmpSampleSave.EndsWith("\\") ? tmpSampleSave : tmpSampleSave + "\\";
            int date = Convert.ToInt32(DateTime.Now.ToString("HH"));
            string DorN = date >= 7 && date < 19 ? "D" : "N";
            string csvTitle = "Barcode,Module,PlateID,TestResult,FailItems,CompareResult,Date,DorN,TestTime";
            string value = string.Format("{0},{1},{2},{3},{4},{5},{6:yyyyMMdd},{7},{8:yyyyMMdd HHmmss}",
                sn, strTurnTable.Replace("-", ""),
                (station == Station.stationA1 || station == Station.stationB1) ? 1 : 2, testResult, failItems, tmpCompareResult, DateTime.Now, DorN, endTime);
            string tmpLocalName = string.Format("{0}_{1}_{2}_{3}_{4}_{5:yyyyMM}.csv", tmpPartNumber, tmpFixtureID, tmpTestType, m_strLocalIp, "GTS", DateTime.Now);

            //服务器保存csv
            AllLog csvLog = new AllLog();
            csvLog.setDir(tmpSampleSave + tmpPartNumber);
            csvLog.path = tmpLocalName;
            csvLog.writeCsvLog(value, csvTitle);

            //本地保存csv
            AllLog localLog = new AllLog();
            localLog.setDir(@"D:/Log/SampleCSVLog");
            localLog.path = tmpLocalName;
            localLog.writeCsvLog(value, csvTitle);

            if (!tmpCompareResult)
            {
                WriteRunLog(string.Format("样本{0}比对结果FAIL\r\n不良问题点：{1}\r\n当前测试问题点：{2}", sn, tmpTargetFailItems, failItems), Color.Red, true);
            }
        }

        /*
        * @function：GetETShiftSamples()
        * @pararm：
        * @return：
        * List<ETsample>：样本数据
        * @action：获取服务器样本数据
        */
        protected List<ETsample> GetETShiftSamples()
        {
            // http://ot-ithzwin002.mflex.com.cn/ettest/
            // http://ot-ithzwin002.mflex.com.cn/ettest/api/ettestrecords/validation?

            string tmpApiAddress = configure.StringFromConfigure(GlobalValue.secApp, GlobalValue.keyApiAddress);
            string tmpApiPath = configure.StringFromConfigure(GlobalValue.secApp, GlobalValue.keyApiSamplePath);
            string tmpToolNumber = configure.StringFromConfigure(GlobalValue.secApp, GlobalValue.keyFixtureId);
            MFLEXMes mfetTest = new MFLEXMes
            {
                ApiAddress = tmpApiAddress,
                ApiPath = tmpApiPath,
                ToolNumber = tmpToolNumber,
            };

            if (tmpApiAddress == "" || tmpApiPath == "")
            {
                WriteRunLog("获取样品板当班有效记录错误，请检查网络或参数设置是否正确", Color.Red, true);
                return null;
            }
            string tmpCommand, tmpMessage;
            DateTime startTime = DateTime.Now;
            List<ETsample> tmpETsamples = mfetTest.GetShiftSamples(out tmpCommand, out tmpMessage);
            WriteRunLog(tmpCommand, Color.Black, true);
            WriteRunLog(tmpMessage, Color.Black, true);
            if (tmpETsamples == null)
            {
                WriteRunLog("获取样品板当班有效记录错误，请检查网络或参数设置是否正确", Color.Red, true);
                //MessageBox.Show("获取样品板当班有效记录错误，请检查网络或参数设置是否正确", "警告", MessageBoxButtons.OK, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                return null;
            }
            updateSampleListview(tmpETsamples);
            return tmpETsamples;
        }

        /*
        * @function：AnalysisMcuResult(string data, out bool result)
        * @pararm：
        * data：未解析的测试数据
        * result：解析结果
        * @return：
        * List<TestItem>：解析后的测试数据
        * @action：解析测试数据
        */
        public List<TestItem> AnalysisMcuResult(string data, out bool result)
        {
            List<TestItem> testItems = new List<TestItem>();
            result = false;
            if (string.IsNullOrEmpty(data)) return testItems;

            string[] items = data.Replace("\r", "").Split(new[] { '\n' }, StringSplitOptions.RemoveEmptyEntries);
            result = true;

            foreach (string tmpItem in items)
            {
                string item = tmpItem;
                if (item.ToUpper().Contains("XW_"))
                {
                    //string[] plateComponents = item.Split(new[] { ':' }, StringSplitOptions.RemoveEmptyEntries);
                    //if (plateComponents.Length >= 2) module = plateComponents[1];
                    //module = item.ToUpper().Contains("_OK") ? "1" : "0";
                    continue;
                }
                if (item.ToUpper().Contains("PLATE")) { continue; }
                if (item.ToUpper().Contains("VERSION")) { continue; }

                if (item.Length < 5) { continue; }

                //PLATE_OK(4 ,1 ):1
                //J0201.1-J0201.3_NG(10 ohm,0 ohm):9999.39
                //J0201.1-J0201.5_NG(10 ohm,0 ohm):9999.32
                //J0201.1-SP0200.1-13_NG(10 ohm,0 ohm):9999.52
                //J0201.1-SP0200.1-14_NG(10 ohm,0 ohm):9999.20
                //J0201.7-J0201.11_NG(10 ohm,0 ohm):9999.95
                //J0201.7-J0201.12_NG(10 ohm,0 ohm):9999.63
                //J0201.7-SP0200.2-15_NG(10 ohm,0 ohm):9999.31
                //J0201.7-SP0200.2-16_NG(10 ohm,0 ohm):9999.99
                //J0201.6-J0201.9_NG(10 ohm,0 ohm):9999.39
                //J0201.6-J0201.10_NG(10 ohm,0 ohm):9999.84
                //J0201.6-J0201.17_NG(10 ohm,0 ohm):9999.52
                //J0201.6-J0201.18_NG(10 ohm,0 ohm):9999.98
                //SHORT_OK(65535 Kohm,3000 Kohm):pass
                //G-G-J0201.2_NG(1.500 V,0.300 V):3.299
                //G-G-J0201.4_NG(1.500 V,0.300 V):3.299
                //G-G-J0201.8_NG(1.500 V,0.300 V):3.299
                //C0300_NG(0 nF,0 nF):1
                //LEAK-100_NG(-45.00 db,-200.00 db):Open
                //LEAK-300_NG(-45.00 db,-200.00 db):Open
                //LEAK-500_NG(-45.00 db,-200.00 db):Open
                //Software:ZE12491-ICT
                //Version:V01
                //end

                // MIC-NP-Vol-N_OK(1.680 V,1.045 V):1.370
                item = item.Replace("::", ">>");
                item = item.Replace("_OK", ";OK");
                item = item.Replace("_NG", ";NG");
                string[] tmpSplitStrings = item.Split(new[] { ";", "(", ",", "):" }, StringSplitOptions.RemoveEmptyEntries);
                if (tmpSplitStrings.Length < 5) continue;

                TestItem tmpTestItem = new TestItem { Name = tmpSplitStrings[0].Replace(">>", "::"), Result = !tmpSplitStrings[1].ToUpper().Contains("NG") };

                string[] tmpHighStrings = tmpSplitStrings[2].Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                tmpTestItem.High = tmpHighStrings.Length >= 1 ? tmpHighStrings[0] : "";
                string tmpHighUnit = tmpHighStrings.Length > 1 ? tmpHighStrings[1] : "";

                string[] tmpLowStrings = tmpSplitStrings[3].Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                tmpTestItem.Low = tmpLowStrings.Length >= 1 ? tmpLowStrings[0] : "";
                string tmpLowUnit = tmpLowStrings.Length > 1 ? tmpLowStrings[1] : "";

                tmpTestItem.Unit = tmpLowUnit.ToUpper().Equals(tmpHighUnit.ToUpper()) ? tmpLowUnit : string.Format("{0}_{1}", tmpLowUnit, tmpHighUnit);
                tmpTestItem.Value = item.Split(new[] { "):" }, StringSplitOptions.RemoveEmptyEntries)[1];

                testItems.Add(tmpTestItem);
                result &= tmpTestItem.Result;
            }

            return testItems;
        }

        public void StopEngine()
        {
            if (m_isConnect)
            {
                m_mainConPlc.WriteShort(40110, 1);//治具状态。- 流程异常
            }
            lock (m_lockObj)
            {
                m_isAlarm = true;
            }
        }
        #endregion testing process

        #region not related to testing
        /*
        * @function：getLocalIp()
        * @pararm：
        * @return：void
        * @action：获取本地ip，暂时只获取192.的ip，未获取到则使用127.0.0.1
        */
        public void getLocalIp()
        {
            var host = Dns.GetHostEntry(Dns.GetHostName());
            foreach (var hostEntry in host.AddressList)
            {
                //showLog(hostEntry.ToString());
                if (hostEntry.ToString().StartsWith("192."))
                {
                    m_strLocalIp = hostEntry.ToString();
                    return;
                }
            }
            m_strLocalIp = "127.0.0.1";
        }

        public int getMaxValue(int[] intsArr)
        {
            int iMaxValue = 0;
            foreach (int i in intsArr)
            {
                iMaxValue = i >= iMaxValue ? i : iMaxValue;
            }
            return iMaxValue;
        }

        /*
        * @function：getClearDate()
        * @pararm：
        * @return：void
        * @action：获取良率清除日期
        */
        public void getClearDate()
        {
            m_iDayStartTime = int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyClearTime]);
            string strDate = DateTime.Now.Date.ToString("yyyyMMdd");
            string[] strTime = (configure.configData[GlobalValue.secApp][GlobalValue.keyClearDate]).Split('_');
            if (strTime.Length < 2) { return; }
            if (strTime[0] == strDate)
            {
                if (strTime[1] == "D") { m_isDayClear = true; }
                else if (strTime[1] == "N") { m_isNightClear = true; }
            }
            else
            {
                if (strTime[0] == DateTime.Now.Date.AddDays(-1).ToString("yyyyMMdd") && strTime[1] == "N" && m_iDayStartTime > DateTime.Now.Hour)
                {
                    m_isNightClear = true;
                }
            }
        }

        public bool getCheckDate()
        {
            string[] strTime = (configure.configData[GlobalValue.secApp][GlobalValue.keyCheckDate]).Split('_');
            string strDate = DateTime.Now.Date.ToString("yyyyMMdd");
            DateTime dtCheckStartTime = Convert.ToDateTime(configure.configData[GlobalValue.secApp][GlobalValue.keyCheckStartTime]);
            DateTime dtDateTime = DateTime.Now;
            bool bResult = false;
            if (dtDateTime >= dtCheckStartTime && dtDateTime < dtCheckStartTime.AddHours(12))
            {
                m_isDay = true;
                if (strTime[0] == strDate && strTime[1] == "D")
                {
                    bResult = true;
                    m_isChecked = true;
                }
            }
            else
            {
                m_isDay = false;
                if (strTime[0] == strDate && strTime[1] == "N")
                {
                    bResult = true;
                    m_isChecked = true;
                }
                else
                {
                    if (strTime[0] == DateTime.Now.AddDays(-1).Date.ToString("yyyyMMdd") && dtDateTime < dtCheckStartTime && strTime[1] == "N")
                    {
                        bResult= true;
                        m_isChecked = true;
                    }
                }
            }
            return bResult;
                
        }

        public void getCheckTime()
        {
            try
            {
                DateTime dtCheckStartTime = Convert.ToDateTime(configure.configData[GlobalValue.secApp][GlobalValue.keyCheckStartTime]);
                DateTime dtCheckEndTime = dtCheckStartTime.AddHours(12);
                DateTime dtDateTime = DateTime.Now;
                if (dtDateTime > dtCheckStartTime && dtDateTime <= dtCheckEndTime)
                {
                    if (!m_isDay)
                    {
                        m_isDay = true;
                        clearSampleListView();
                        m_isChecked=false;
                        WriteRunLog("已切换为夜班，需要重新进行样品板测试", Color.Blue);
                    }
                }
                else
                {
                    if (m_isDay)
                    {
                        m_isDay = false;
                        clearSampleListView();
                        m_isChecked = false;
                        WriteRunLog("已切换为白班，需要重新进行样品板测试", Color.Blue);
                    }
                }
            }
            catch(Exception ex){
                WriteRunLog(ex.Message, GlobalKey.colorRed);
            }
        }

        /*
        * @function：GetUploadValue(ref ushort usSerialNum, ushort usAddValue)
        * @pararm：
        * usSerialNum：流水号
        * usAddValue：数值
        * @return：
        * ushort：流水号+数值
        * @action：获取加流水号的通讯信息，流水号超过255时，重置为1
        */
        public ushort GetUploadValue(ref ushort usSerialNum, ushort usAddValue, int loadMode = 0)
        {
            if (loadMode == 1)
            {
                if (DicCommand.Keys.Contains(loadMode))
                {
                    DicCommand[1] = usSerialNum;
                }
                else
                {
                    DicCommand.Add(1, usSerialNum);
                }
                WriteRunLog(string.Format("发送等待上料信号:[{0}-{1}]", 40122, usSerialNum + usAddValue));
            }
            else if (loadMode == 2)
            {
                if (DicCommand.Keys.Contains(loadMode))
                {
                    DicCommand[2] = usSerialNum;
                }
                else
                {
                    DicCommand.Add(2, usSerialNum);
                }
                WriteRunLog(string.Format("写入等待下料信号:[{0}-{1}]", 40117, usSerialNum + usAddValue));
            }
            ushort usValue = (ushort)(usSerialNum + usAddValue);
            if (usSerialNum >= (ushort.MaxValue - 0x100))
            {
                usSerialNum = 0x100;
            }
            else
            {
                usSerialNum += 0x100;
            }
            return usValue;
        }

        /*
        * @function：removeKey(ref Dictionary<Station, Result> dicSn, Station station)
        * @pararm：
        * dicSn：条码字典
        * station：穴位编号
        * @return：true/false
        * @action：根据指定穴位编号去除字典项
        */
        public bool removeKey(ref Dictionary<Station, Result> dicSn, Station station)
        {
            try
            {
                if (dicSn.ContainsKey(station))
                {
                    dicSn.Remove(station);
                }
                return true;
            }
            catch { return false; }
        }
        #endregion not related to testing


        #region outside the testing process
        /*
        * @function：WriteRunLog(string strContent, Color color = default(Color), bool bWrite = true)
        * @pararm：
        * strContent：输出信息
        * color：颜色
        * bWrite：是否写入文件
        * @return：void
        * @action：输出实时日志并保存至本地文件
        */
        public void WriteRunLog(string strContent, Color color = default(Color), bool bWrite = true)
        {
            try
            {
                updateLog(strContent, color);
                if (bWrite) { txtLog.writeTxtLog(strContent); }

            }
            catch (Exception ex)
            {
                if (updateLog != null) { updateLog("写LOG文件失败 - " + ex.Message, GlobalKey.colorRed); }
            }

        }

        /*
        * @function：PauseAndStop(CancellationToken token)
        * @pararm：
        * @return：void
        * @action：保证线程能快速退出
        */
        private void PauseAndStop(CancellationToken token)
        {
            if (m_resetEvent != null)
            {
                m_resetEvent.WaitOne();
            }

            token.ThrowIfCancellationRequested();
        }

        /*
        * @function：ConnectIngUpload()
        * @pararm：
        * @return：void
        * @action：与主控上位机的连接心跳
        */
        private void ConnectIngUpload()
        {
            while (m_mainConPlc.IsOpen)
            {
                Thread.Sleep(1000);
                m_mainConPlc.FixtureKeepConnect();
            }
        }

        /*
        * @function：plcAlarm(out int iErrorCode)
        * @pararm：
        * iErrorCode：报警信号ID
        * @return：true/false
        * @action：读取治具PLC是否有报警信号
        */
        public bool plcAlarm(out int iErrorCode)
        {
            iErrorCode = 0;
            try
            {
                foreach (int iAddress in GlobalValue.ERR_MSG.Keys)
                {
                    bool[] bResults = m_fixturePlc.ReadMRegister(iAddress, 1);
                    if (bResults != null && bResults[0])
                    {
                        iErrorCode = iAddress;
                        return false;
                    }
                }
                return true;
            }
            catch
            {
                return false;
            }
        }

        /*
       * @function：waitReTest()
       * @pararm：
       * @return：true/false
       * @action：是否收到开始复测信号
       */
        public bool waitReTest()
        {
            try
            {
                int iDelay = int.Parse(configure.configData[GlobalValue.secApp][GlobalValue.keyDelay]);
                int iTimeCount = 0;
                while (iTimeCount < iDelay)
                {
                    Thread.Sleep(1000);
                    iTimeCount++;
                    if (m_fixturePlc.ReadShort(100) == 1)
                    {
                        return true;
                    }
                }
                WriteRunLog("等待PLC信号超时", Color.Red);
                return false;
            }
            catch (Exception ex)
            {
                WriteRunLog(ex.Message, Color.Red);
                return false;
            }

        }
        #endregion outside the testing process

        #region 模拟自动化信号
        private bool GetTestTurnTable(ref string strTurnTable, ref Station station1, ref Station station2)
        {

            try
            {
                if (m_isLoad) { return true; }
                strTurnTable = m_strTurnTable;
                station1 = station2 = Station.stationNone;
                Result result1 = new Result { barcode = "" };
                Result result2 = new Result { barcode = "" };
                if (strTurnTable == GlobalValue.ATurnTable)
                {
                    if (m_iType == 1)
                    {
                        station1 = Station.stationA1;
                        if (DicBarcode.Keys.Contains(station1))
                        {
                            DicBarcode[station1] = result1;
                        }
                        else
                        {
                            DicBarcode.Add(station1, result1);
                        }
                    }
                    else if (m_iType == 2)
                    {
                        station2 = Station.stationA2;
                        if (DicBarcode.Keys.Contains(station2))
                        {
                            DicBarcode[station2] = result2;
                        }
                        else
                        {
                            DicBarcode.Add(station2, result2);
                        }
                    }
                    else if (m_iType == 3)
                    {
                        station1 = Station.stationA1;
                        station2 = Station.stationA2;
                        if (DicBarcode.Keys.Contains(station1))
                        {
                            DicBarcode[station1] = result1;
                        }
                        else
                        {
                            DicBarcode.Add(station1, result1);
                        }
                        if (DicBarcode.Keys.Contains(station2))
                        {
                            DicBarcode[station2] = result2;
                        }
                        else
                        {
                            DicBarcode.Add(station2, result2);
                        }
                    }
                }
                else if (strTurnTable == GlobalValue.BTurnTable)
                {
                    if (m_iType == 1)
                    {
                        station1 = Station.stationB1;
                        if (DicBarcode.Keys.Contains(station1))
                        {
                            DicBarcode[station1] = result1;
                        }
                        else
                        {
                            DicBarcode.Add(station1, result1);
                        }
                    }
                    else if (m_iType == 2)
                    {
                        station2 = Station.stationB2;
                        if (DicBarcode.Keys.Contains(station2))
                        {
                            DicBarcode[station2] = result2;
                        }
                        else
                        {
                            DicBarcode.Add(station2, result2);
                        }
                    }
                    else if (m_iType == 3)
                    {
                        station1 = Station.stationB1;
                        station2 = Station.stationB2;
                        if (DicBarcode.Keys.Contains(station1))
                        {
                            DicBarcode[station1] = result1;
                        }
                        else
                        {
                            DicBarcode.Add(station1, result1);
                        }
                        if (DicBarcode.Keys.Contains(station2))
                        {
                            DicBarcode[station2] = result2;
                        }
                        else
                        {
                            DicBarcode.Add(station2, result2);
                        }
                    }
                }
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }

        //private bool StartTestEnable()
        //{
        //    try
        //    {
        //        if (!m_bStartTest) { return false; }
        //        if (!m_isLoad)
        //        {
        //            if (m_iTurnTable == 1)
        //            {
        //                if (m_iType == 1)
        //                {
        //                    if (!m_fixturePlc.WriteShort(104, 3))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //                else if (m_iType == 2)
        //                {
        //                    WriteRunLog("发送信号");
        //                    if (!m_fixturePlc.WriteShort(104, 4))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //                else if (m_iType == 3)
        //                {
        //                    if (!m_fixturePlc.WriteShort(104, 2))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //            }
        //            else if (m_iTurnTable == 2)
        //            {
        //                if (m_iType == 1)
        //                {
        //                    if (!m_fixturePlc.WriteShort(105, 3))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //                else if (m_iType == 2)
        //                {
        //                    if (!m_fixturePlc.WriteShort(105, 4))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //                else if (m_iType == 3)
        //                {
        //                    if (!m_fixturePlc.WriteShort(105, 2))
        //                    {
        //                        WriteRunLog("发送信号失败，请检查治具PLC连接是否正常，并重启程序");
        //                    }
        //                }
        //            }
        //            m_isLoad = true;
        //            m_bStartTest = true;
        //        }
        //        Thread.Sleep(300);
        //        if (m_fixturePlc.ReadShort(100) != 1)
        //        {
        //            return false;
        //        }
        //        m_isLoad = false;
        //        return true;
        //    }
        //    catch (Exception ex)
        //    {
        //        WriteRunLog(ex.Message, GlobalKey.colorRed);
        //        return false;
        //    }
        //}
        #endregion 模拟自动化信号
    }
}
