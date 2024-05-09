using MFLEX_Compass.UI;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using MFLEX_Compass.GlobalDir;
using MFLEX_Compass.TestDir;
//using System.Collections.Specialized.BitVector32;
using MFLEX_Compass.ConfigDir;
using MFLEX_Compass.MesDir;
using System.Net;
//using static System.Collections.Specialized.BitVector32;

namespace MFLEX_Compass
{
    public partial class MainWindow : Form
    {
        public TestEngine testEngine;
        public int m_iPassNum;
        public int m_iFailNum;
        public int m_iTotalNum;
        public int m_iAPassNum1;
        public int m_iAPassNum2;
        public int m_iBPassNum1;
        public int m_iBPassNum2;
        public int m_iATotalNum1;
        public int m_iATotalNum2;
        public int m_iBTotalNum1;
        public int m_iBTotalNum2;
        public bool m_isOperator;
        public static Configure configure = new Configure();
        public static Count counter = new Count();
        private bool m_bIsTesting;
        private readonly object m_lock = new object();
        public DebugForm debugForm;
        public MainWindow(bool bIsOperator)
        {
            InitializeComponent();
            Thread runTimeTh = new Thread(ShowRunTime);
            runTimeTh.IsBackground = true;
            runTimeTh.Start();
            m_isOperator = bIsOperator;
        }

        private void showLog(string strContent, Color color = default(Color))
        {
            BeginInvoke(new EventHandler(delegate
            {
                try
                {
                    string tmpMessage = rtbLog.Text;
                    rtbLog.AppendText(string.Format("[{0:HH:mm:ss.fff}] {1}", DateTime.Now, strContent.EndsWith("\n") ? strContent : strContent + "\n"));
                    rtbLog.Select(tmpMessage.Length, strContent.Length + 15);
                    rtbLog.SelectionColor = color;
                    rtbLog.ScrollToCaret();
                    rtbLog.Select(rtbLog.TextLength, 0);
                }
                catch (Exception ex)
                {
                    rtbLog.AppendText(string.Format("[{0:HH:mm:ss.fff}] {1}", DateTime.Now, ex.Message));
                }
            }));
        }


        private void ShowRunTime()
        {
                try
                {
                    //Timer timer = new Timer();
                    DateTime startTime = DateTime.Now;
                    //timer.Interval = 1000;
                    while (true)
                    {
                        Thread.Sleep(1000);
                        DateTime endTime = DateTime.Now;
                        int iSecond = (int)(endTime - startTime).TotalSeconds;
                    if (runTime.InvokeRequired)
                    {
                        runTime.Invoke((MethodInvoker)(() => runTime.Text = string.Format("{0}:{1}:{2}", iSecond / 3600, iSecond % 3600 / 60, iSecond % 3600 % 60)));
                    }
                    else { 
                        runTime.Text = string.Format("{0}:{1}:{2}", iSecond / 3600, iSecond % 3600 / 60, iSecond % 3600 % 60);
                    }
                }
                }
                catch (Exception ex)
                {
                    showLog(ex.Message, GlobalKey.colorRed);
                }
            
        }

        public void UpdateAllTestStatus(string strTurnTable, Status status)
        {
            BeginInvoke(new Action(() => {
                string strContent = "ERROR";
                Color color = GlobalKey.colorRed;
                if (status == Status.statusIdel)
                {
                    strContent = strTurnTable + GlobalKey.idelTxt;
                    color = GlobalKey.colorGray;
                }
                else if (status == Status.statusTest)
                {
                    strContent = strTurnTable + GlobalKey.testTxt;
                    color = GlobalKey.colorYellow;
                }
                else if (status == Status.statusPass)
                {
                    strContent = strTurnTable + GlobalKey.passTxt;
                    color = GlobalKey.colorGreen;
                }
                else if (status == Status.statusFail)
                {
                    strContent = strTurnTable + GlobalKey.failTxt;
                    color = GlobalKey.colorRed;
                }

                if (strTurnTable == GlobalValue.ATurnTable)
                {
                    A_AllStatus.Text = strContent;
                    A_AllStatus.BackColor = color;
                }
                else if (strTurnTable == GlobalValue.BTurnTable)
                {
                    B_AllStatus.Text = strContent;
                    B_AllStatus.BackColor = color;
                }
            }));
            
        }

        public void UpdateBarcode(Station station, string strBarcode)
        {
            BeginInvoke(new EventHandler(delegate 
            {

                if (station == Station.stationA1)
                {
                    tbABarcode1.Text = strBarcode;
                }
                else if (station == Station.stationA2)
                {
                    tbABarcode2.Text = strBarcode;
                }
                else if (station == Station.stationB1)
                {
                    tbBBarcode1.Text = strBarcode;
                }
                else if (station == Station.stationB2)
                {
                    tbBBarcode2.Text = strBarcode;
                }
            }));
        }

        public void UpdateTestStatus(Station station, Status status)
        {
            BeginInvoke(new EventHandler(delegate
            {
                string strContent = "ERROR";
                Color color = GlobalKey.colorRed;
                if (status == Status.statusIdel)
                {
                    strContent = GlobalKey.idelTxt;
                    color = GlobalKey.colorGray;
                }
                else if (status == Status.statusTest)
                {
                    strContent = GlobalKey.testTxt;
                    color = GlobalKey.colorYellow;
                    ClearTestData(station);
                }
                else if (status == Status.statusPass)
                {
                    strContent = GlobalKey.passTxt;
                    color = GlobalKey.colorGreen;
                }
                else if (status == Status.statusFail)
                {
                    strContent = GlobalKey.failTxt;
                    color = GlobalKey.colorRed;
                }

                if (station == Station.stationA1)
                {
                    lbAStatus1.Text = strContent;
                    lbAStatus1.BackColor = color;
                }
                else if (station == Station.stationA2)
                {
                    lbAStatus2.Text = strContent;
                    lbAStatus2.BackColor = color;
                }
                else if (station == Station.stationB1)
                {
                    lbBStatus1.Text = strContent;
                    lbBStatus1.BackColor = color;
                }
                else if (station == Station.stationB2)
                {
                    lbBStatus2.Text = strContent;
                    lbBStatus2.BackColor = color;
                }
            }));
        }

        public void UpdateDevicesStatus(DevicesNum devicesNum, DevicesStatus devicesStatus)
        {
            BeginInvoke(new EventHandler(delegate
            {
                if (devicesNum == DevicesNum.MCU1)
                {
                    MCULabel1.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen : GlobalKey.colorRed;
                }
                else if (devicesNum == DevicesNum.MCU2)
                {
                    MCULabel2.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen : GlobalKey.colorRed;
                }
                //else if (devicesNum == DevicesNum.Scan1)
                //{
                //    ScanLabel1.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen : GlobalKey.colorRed;
                //}
                //else if (devicesNum == DevicesNum.Scan2)
                //{
                //    ScanLabel2.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen: GlobalKey.colorRed;
                //}
                else if (devicesNum == DevicesNum.FIXTURE_PLC)
                {
                    PlcLabel1.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen : GlobalKey.colorRed;
                }
                else if (devicesNum == DevicesNum.LOAD_PLC)
                {
                    PlcLabel2.BackColor = devicesStatus == DevicesStatus.connected ? GlobalKey.colorGreen : GlobalKey.colorRed;
                }
            }));
        }

        public void ShowTestDataSingle(Station station, TestItem testItem)
        {
            try {
                this.Invoke((EventHandler)(delegate
                {
                    string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                    testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                    testItem.High ?? "", testItem.Unit ?? "" };
                    if (station == Station.stationA1)
                    {
                        tableA1Result.Rows.Clear();
                        tableA1Result.Rows.Add(strTemp);
                    }
                    else if (station == Station.stationA2)
                    {
                        tableA2Result.Rows.Clear();
                        tableA2Result.Rows.Add(strTemp);
                    }
                    else if (station == Station.stationB1)
                    {
                        tableB1Result.Rows.Clear();
                        tableB1Result.Rows.Add(strTemp);
                    }
                    else if (station == Station.stationB2)
                    {
                        tableB2Result.Rows.Clear();
                        tableB2Result.Rows.Add(strTemp);
                    }
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
            
        }

        public void ShowTestDataList(Station station, List<TestItem> testItems)
        {
            try
            {
                this.Invoke((EventHandler)(delegate
                {
                    List<string[]> listData = new List<string[]>();
                    int iIndex = 0;
                    if (station == Station.stationA1)
                    {
                        tableA1Result.Rows.Clear();
                    }
                    else if (station == Station.stationA2)
                    {
                        tableA2Result.Rows.Clear();
                    }
                    else if (station == Station.stationB1)
                    {
                        tableB1Result.Rows.Clear();
                    }
                    else if (station == Station.stationB2)
                    {
                        tableB2Result.Rows.Clear();
                    }

                    foreach (TestItem testItem in testItems)
                    {
                        string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                        testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                        testItem.High ?? "", testItem.Unit ?? "" };
                        if (station == Station.stationA1)
                        {
                            tableA1Result.Rows.Add(strTemp);
                            tableA1Result.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                        }
                        else if (station == Station.stationA2)
                        {
                            tableA2Result.Rows.Add(strTemp);
                            tableA2Result.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                        }
                        else if (station == Station.stationB1)
                        {
                            tableB1Result.Rows.Add(strTemp);
                            tableB1Result.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                        }
                        else if (station == Station.stationB2)
                        {
                            tableB2Result.Rows.Add(strTemp);
                            tableB2Result.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                        }
                        iIndex++;
                    }     
                }));
                
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
            
        }

        public void ClearTestData(Station station)
        {
            BeginInvoke(new EventHandler(delegate
            {
                if (station == Station.stationA1) { tableA1Result.Rows.Clear(); }
                else if (station == Station.stationA2) { tableA2Result.Rows.Clear(); }
                else if (station == Station.stationB1) { tableB1Result.Rows.Clear(); }
                else if (station == Station.stationB2) { tableB2Result.Rows.Clear(); }
            }));
        }

        public void ClearYield()
        {
            try
            {
                this.Invoke((EventHandler)(delegate
                {
                    lbATotal1.Text = "0";
                    lbAYield1.Text = "100%";
                    lbATotal2.Text = "0";
                    lbAYield2.Text = "100%";
                    lbBTotal1.Text = "0";
                    lbBYield1.Text = "100%";
                    lbBTotal2.Text = "0";
                    lbBYield2.Text = "100%";
                    lbTPass.Text = "0";
                    lbTFail.Text = "0";
                    lbTTotal.Text = "0";
                    lbTYield.Text = "100%";
                    m_iPassNum = 0;
                    m_iFailNum = 0;
                    m_iTotalNum = 0;
                    m_iAPassNum1 = 0;
                    m_iAPassNum2 = 0;
                    m_iBPassNum1 = 0;
                    m_iBPassNum2 = 0;
                    m_iATotalNum1 = 0;
                    m_iATotalNum2 = 0;
                    m_iBTotalNum1 = 0;
                    m_iBTotalNum2 = 0;
                    counter.ClearCounter();
                }));

            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        public void ClearSampleListView()
        {
            this.Invoke((EventHandler)(delegate
            {
                lvSample.Items.Clear();
            }));
        }

        private void UpdateSampleListview(List<ETsample> items)
        {
            this.Invoke((EventHandler)(delegate
            {
                lvSample.Items.Clear();
                if (items.Count == 0)
                {
                    return;
                }
                foreach (ETsample item in items)
                {
                    ListViewItem listViewItem = new ListViewItem();
                    listViewItem.Text = (item.barcode ?? "");
                    listViewItem.SubItems.Add(item.testType ?? "");
                    listViewItem.SubItems.Add(item.testTime ?? "");
                    listViewItem.SubItems.Add(item.defectCode ?? "");
                    listViewItem.SubItems.Add(item.isResultMatched ? "OK" : "NG");
                    listViewItem.ForeColor = item.isResultMatched ? Color.Green : Color.Red;
                    lvSample.Items.Add(listViewItem);
                }

                lvSample.EnsureVisible(lvSample.Items.Count - 1);
            }));
        }
        public bool GetTestItem(int iSlot, ref List<TestItem> items1, ref List<TestItem> items2)
        {

            try
            {
                List<TestItem> item1 = new List<TestItem>();
                List<TestItem> item2 = new List<TestItem>();
                this.Invoke((EventHandler)(delegate
                {
                    string str1 = "";
                    string str2 = "";
                    bool bResult = false;
                    if (iSlot == 1)
                    {
                        Task task = new Task(() => { str1 = testEngine.m_mcu1.Test(GlobalValue.testCommand); });
                        task.Start();
                        Task.WaitAll(task);
                        item1 = testEngine.AnalysisMcuResult(str1, out bResult);
                    }
                    else if (iSlot == 2) 
                    {
                        Task task = new Task(() => { str2 = testEngine.m_mcu2.Test(GlobalValue.testCommand); });
                        task.Start();
                        Task.WaitAll(task);
                        item2 = testEngine.AnalysisMcuResult(str2, out bResult);
                    }
                    else if (iSlot == 3) 
                    {
                        Task task1 = new Task(() => { str1 = testEngine.m_mcu1.Test(GlobalValue.testCommand); });
                        Task task2 = new Task(() => { str2 = testEngine.m_mcu2.Test(GlobalValue.testCommand); });
                        task1.Start();
                        task2.Start();
                        Task.WaitAll(task1,task2);
                        item1 = testEngine.AnalysisMcuResult(str1, out bResult);
                        item2 = testEngine.AnalysisMcuResult(str2, out bResult);
                    }
                }));
                items1 = item1;
                items2 = item2;
                return true;
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
                return false;
            }
        }
        public void UpdateYield(Station station, int iPassNum, int iFailNum)
        {
            BeginInvoke(new EventHandler(delegate
            {
                if (station == Station.stationA1)
                {
                    m_iAPassNum1 += iPassNum;
                    m_iATotalNum1 += iPassNum + iFailNum;
                    lbATotal1.Text = m_iATotalNum1.ToString();
                    lbAYield1.Text = m_iATotalNum1 == 0 ? "100%" : string.Format("{0}%", m_iAPassNum1 * 100 / m_iATotalNum1);
                    counter.SaveCounter(GlobalValue.secAStation1, GlobalValue.keyPass, m_iAPassNum1.ToString());
                    counter.SaveCounter(GlobalValue.secAStation1, GlobalValue.keyTotal, m_iATotalNum1.ToString());
                    counter.SaveCounter(GlobalValue.secAStation1, GlobalValue.keyYield, m_iATotalNum1 == 0 ? "100" : (m_iAPassNum1 * 100 / m_iATotalNum1).ToString());
                }
                else if (station == Station.stationA2)
                {
                    m_iAPassNum2 += iPassNum;
                    m_iATotalNum2 += iPassNum + iFailNum;
                    lbATotal2.Text = m_iATotalNum2.ToString();
                    lbAYield2.Text = m_iATotalNum2 == 0 ? "100%" : string.Format("{0}%", m_iAPassNum2 * 100 / m_iATotalNum2);
                    counter.SaveCounter(GlobalValue.secAStation2, GlobalValue.keyPass, m_iAPassNum2.ToString());
                    counter.SaveCounter(GlobalValue.secAStation2, GlobalValue.keyTotal, m_iATotalNum2.ToString());
                    counter.SaveCounter(GlobalValue.secAStation2, GlobalValue.keyYield, m_iATotalNum2 == 0 ? "100" : (m_iAPassNum2 * 100 / m_iATotalNum2).ToString());
                }
                else if (station == Station.stationB1)
                {
                    m_iBPassNum1 += iPassNum;
                    m_iBTotalNum1 += iPassNum + iFailNum;
                    lbBTotal1.Text = m_iBTotalNum1.ToString();
                    lbBYield1.Text = m_iBTotalNum1 == 0 ? "100%" : string.Format("{0}%", m_iBPassNum1 * 100 / m_iBTotalNum1);
                    counter.SaveCounter(GlobalValue.secBStation1, GlobalValue.keyPass, m_iBPassNum1.ToString());
                    counter.SaveCounter(GlobalValue.secBStation1, GlobalValue.keyTotal, m_iBTotalNum1.ToString());
                    counter.SaveCounter(GlobalValue.secBStation1, GlobalValue.keyYield, m_iBTotalNum1 == 0 ? "100" : (m_iBPassNum1 * 100 / m_iBTotalNum1).ToString());
                }
                else if (station == Station.stationB2)
                {
                    m_iBPassNum2 += iPassNum;
                    m_iBTotalNum2 += iPassNum + iFailNum;
                    lbBTotal2.Text = m_iBTotalNum2.ToString();
                    lbBYield2.Text = m_iBTotalNum2 == 0 ? "100%" : string.Format("{0}%", m_iBPassNum2 * 100 / m_iBTotalNum2);
                    counter.SaveCounter(GlobalValue.secBStation2, GlobalValue.keyPass, m_iBPassNum2.ToString());
                    counter.SaveCounter(GlobalValue.secBStation2, GlobalValue.keyTotal, m_iBTotalNum2.ToString());
                    counter.SaveCounter(GlobalValue.secBStation2, GlobalValue.keyYield, m_iBTotalNum2 == 0 ? "100" : (m_iBPassNum2 * 100 / m_iBTotalNum2).ToString());
                }
                else
                {
                    return;
                }
                m_iPassNum += iPassNum;
                m_iFailNum += iFailNum;
                m_iTotalNum += iPassNum + iFailNum;
                if (m_iTotalNum == 0)
                {
                    lbTYield.Text = "100%";
                    counter.SaveCounter(GlobalValue.secTotal, GlobalValue.keyYield, "100");
                }
                else
                {
                    lbTYield.Text = string.Format("{0}%", m_iPassNum * 100 / m_iTotalNum);
                    counter.SaveCounter(GlobalValue.secTotal, GlobalValue.keyYield, (m_iPassNum * 100 / m_iTotalNum).ToString());
                }
                lbTPass.Text = m_iPassNum.ToString();
                lbTFail.Text = m_iFailNum.ToString();
                lbTTotal.Text = m_iTotalNum.ToString();
                counter.SaveCounter(GlobalValue.secTotal, GlobalValue.keyPass, lbTPass.Text);
                counter.SaveCounter(GlobalValue.secTotal, GlobalValue.keyFail, lbTFail.Text);
                counter.SaveCounter(GlobalValue.secTotal, GlobalValue.keyTotal, lbTTotal.Text);
            }));
            
        }

        public void UpdateTestTime(string strTurnTable, bool bIsTestIng)
        {
            bool bIsClose = m_bIsTesting & bIsTestIng;
            lock (m_lock)
            {
                m_bIsTesting = bIsTestIng;
            }
            if (bIsTestIng && !bIsClose)
            {
                Thread thread = new Thread(showTestTime);
                thread.IsBackground = true;
                thread.Start(strTurnTable);
            }
        }

        public void showTestTime(object o)
        {
            try
            {
                string strTurnTable = (string)o;
                DateTime startTime = DateTime.Now;
                if (strTurnTable == GlobalValue.ATurnTable)
                {
                    while (m_bIsTesting)
                    {
                        Thread.Sleep(1000);
                        DateTime endTime = DateTime.Now;
                        int iSecond = (int)(endTime - startTime).TotalSeconds;
                        if (lbATestTime.InvokeRequired)
                        {
                            lbATestTime.Invoke((MethodInvoker)(() => lbATestTime.Text = string.Format("{0}S", iSecond)));
                        }
                        else
                        {
                            lbATestTime.Text = string.Format("{0}S", iSecond);
                        }
                    }
                }
                else if (strTurnTable == GlobalValue.BTurnTable)
                {
                    while (m_bIsTesting)
                    {
                        Thread.Sleep(1000);
                        DateTime endTime = DateTime.Now;
                        int iSecond = (int)(endTime - startTime).TotalSeconds;
                        if (lbBTestTime.InvokeRequired)
                        {
                            lbBTestTime.Invoke((MethodInvoker)(() => lbBTestTime.Text = string.Format("{0}S", iSecond)));
                        }
                        else
                        {
                            lbBTestTime.Text = string.Format("{0}S", iSecond);
                        }
                    }
                }


            }
            catch (Exception ex)
            {
                showLog(ex.Message, GlobalKey.colorRed);
            }
        }

        private void adminLogin(string strUser, string strPwd)
        {
            //showLog($"user:{strUser}, pwd:{strPwd}", Color.Green);
            settleConfigToolStripMenuItem.Visible = true;
            fixtureDebug.Enabled = true;
            if (strUser.ToLower() == "test")
            {
                commmandTool.Visible = true;
            }
        }

        private void adminLoginToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                Admin admin = new Admin();
                admin.loginEvent += new AdminDelegate(adminLogin);
                admin.Show();
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void adminExitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                settleConfigToolStripMenuItem.Visible = false;
                fixtureDebug.Enabled = false;
                commmandTool.Visible = false;
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void settleConfigToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                SettleConfig settleConfig = new SettleConfig();
                settleConfig.updataLog += showLog;
                settleConfig.ShowDialog();
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void testConfigToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void clearYieldToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                BeginInvoke(new Action(() =>
                {
                    lbATotal1.Text = "0";
                    lbAYield1.Text = "100%";
                    lbATotal2.Text = "0";
                    lbAYield2.Text = "100%";
                    lbBTotal1.Text = "0";
                    lbBYield1.Text = "100%";
                    lbBTotal2.Text = "0";
                    lbBYield2.Text = "100%";
                    lbTPass.Text = "0";
                    lbTFail.Text = "0";
                    lbTTotal.Text = "0";
                    lbTYield.Text = "100%";
                    m_iPassNum = 0;
                    m_iFailNum = 0;
                    m_iTotalNum = 0;
                    m_iAPassNum1 = 0;
                    m_iAPassNum2 = 0;
                    m_iBPassNum1 = 0;
                    m_iBPassNum2 = 0;
                    m_iATotalNum1 = 0;
                    m_iATotalNum2 = 0;
                    m_iBTotalNum1 = 0;
                    m_iBTotalNum2 = 0;
                    counter.ClearCounter();
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        public void initializeEngine()
        {
            testEngine = new TestEngine();
            testEngine.updateLog += showLog;
            testEngine.updateBarcode += UpdateBarcode;
            testEngine.updateDevicesStatus += UpdateDevicesStatus;
            testEngine.updateAllTestStatus += UpdateAllTestStatus;
            testEngine.updateSampleListview += UpdateSampleListview;
            testEngine.flushWindow += MainInit;
            testEngine.clearYield += ClearYield;
            testEngine.updateTestStatus += UpdateTestStatus;
            testEngine.updateTestTime += UpdateTestTime;
            testEngine.updateYield += UpdateYield;
            testEngine.showTestDataList += ShowTestDataList;
            testEngine.showTestDataSingle += ShowTestDataSingle;
            testEngine.m_mcu1.updateMessage += showLog;
            testEngine.m_mcu2.updateMessage += showLog;
            testEngine.clearSampleListView += ClearSampleListView;
            testEngine.m_isOperator = m_isOperator;
        }

        public void loadTxtBoxTrigger()
        {
            this.tbABarcode1.KeyDown += TbABarcode1_KeyDown;
            this.tbABarcode2.KeyDown += TbABarcode2_KeyDown;
            this.tbBBarcode1.KeyDown += TbBBarcode1_KeyDown;
            this.tbBBarcode2.KeyDown += TbBBarcode2_KeyDown;
        }

        public void setTableCount(int iCount = 15)
        {
            this.tableA1Result.RowCount = iCount;
            this.tableB1Result.RowCount = iCount;
            this.tableA2Result.RowCount = iCount;
            this.tableB2Result.RowCount = iCount;
        }

        public void loadCounter()
        {
            try
            {
                BeginInvoke(new Action(() =>
                {
                    bool bLoad = true;
                    lbTPass.Text = counter.counterData[GlobalValue.secTotal][GlobalValue.keyPass];
                    lbTFail.Text = counter.counterData[GlobalValue.secTotal][GlobalValue.keyFail];
                    lbTTotal.Text = counter.counterData[GlobalValue.secTotal][GlobalValue.keyTotal];
                    lbTYield.Text = counter.counterData[GlobalValue.secTotal][GlobalValue.keyYield] + "%";
                    lbATotal1.Text = counter.counterData[GlobalValue.secAStation1][GlobalValue.keyTotal];
                    lbAYield1.Text = counter.counterData[GlobalValue.secAStation1][GlobalValue.keyYield] + "%";
                    lbATotal2.Text = counter.counterData[GlobalValue.secAStation2][GlobalValue.keyTotal];
                    lbAYield2.Text = counter.counterData[GlobalValue.secAStation2][GlobalValue.keyYield] + "%";
                    lbBTotal1.Text = counter.counterData[GlobalValue.secBStation1][GlobalValue.keyTotal];
                    lbBYield1.Text = counter.counterData[GlobalValue.secBStation1][GlobalValue.keyYield] + "%";
                    lbBTotal2.Text = counter.counterData[GlobalValue.secBStation2][GlobalValue.keyTotal];
                    lbBYield2.Text = counter.counterData[GlobalValue.secBStation2][GlobalValue.keyYield] + "%";
                    bLoad &= int.TryParse(lbTPass.Text,out m_iPassNum);
                    bLoad &= int.TryParse(lbTFail.Text, out m_iFailNum);
                    bLoad &= int.TryParse(lbTTotal.Text, out m_iTotalNum);
                    bLoad &= int.TryParse(lbATotal1.Text, out m_iATotalNum1);
                    bLoad &= int.TryParse(lbATotal2.Text, out m_iATotalNum2);
                    bLoad &= int.TryParse(lbBTotal1.Text, out m_iBTotalNum1);
                    bLoad &= int.TryParse(lbBTotal2.Text, out m_iBTotalNum2);
                    bLoad &= int.TryParse(counter.counterData[GlobalValue.secAStation1][GlobalValue.keyPass], out m_iAPassNum1);
                    bLoad &= int.TryParse(counter.counterData[GlobalValue.secAStation2][GlobalValue.keyPass], out m_iAPassNum2);
                    bLoad &= int.TryParse(counter.counterData[GlobalValue.secBStation1][GlobalValue.keyPass], out m_iBPassNum1);
                    bLoad &= int.TryParse(counter.counterData[GlobalValue.secBStation2][GlobalValue.keyPass], out m_iBPassNum2);
                    if (!bLoad)
                    {
                        showLog("加载良率信息失败", GlobalKey.colorRed);
                    }
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        public void loadLoginMsg()
        {
            try
            {
                BeginInvoke(new Action(() =>
                {
                    lbOperator.Text = configure.configData[GlobalValue.secApp][GlobalValue.keyOperator];
                    lbLineId.Text = configure.configData[GlobalValue.secApp][GlobalValue.keyLineId];
                    lbProgram.Text = configure.configData[GlobalValue.secApp][GlobalValue.keyProgram];
                    lbToolNum.Text = configure.configData[GlobalValue.secApp][GlobalValue.keySerialNumber];
                    lbWorkArea.Text = configure.configData[GlobalValue.secApp][GlobalValue.keyWorkArea];
                    lbFixtureId.Text = configure.configData[GlobalValue.secApp][GlobalValue.keyFixtureId];
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void MainWindow_Load(object sender, EventArgs e)
        {
            loadTxtBoxTrigger();
            setTableCount();
            loadCounter();
            loadLoginMsg();
            m_bIsTesting = false;
            initializeEngine();
            
            Thread THR1 = new Thread(testEngine.InitializeEngine);
            THR1.IsBackground = true;
            THR1.Start();
            counter.updateLog += showLog;
            btnVis(false);
        }

        private void MainInit()
        {
            this.Invoke((EventHandler)(delegate
            {
                rtbLog.Text = "";
                showLog("等待界面初始化...");
                //lvSample.Items.Clear();
                ClearTestData(Station.stationA1);
                ClearTestData(Station.stationA2);
                ClearTestData(Station.stationB1);
                ClearTestData(Station.stationB2);
                UpdateTestStatus(Station.stationA1, Status.statusIdel);
                UpdateTestStatus(Station.stationA2, Status.statusIdel);
                UpdateTestStatus(Station.stationB1, Status.statusIdel);
                UpdateTestStatus(Station.stationB2, Status.statusIdel);
                UpdateBarcode(Station.stationA1, "");
                UpdateBarcode(Station.stationA2, "");
                UpdateBarcode(Station.stationB1, "");
                UpdateBarcode(Station.stationB2, "");
                UpdateAllTestStatus(GlobalValue.ATurnTable, Status.statusIdel);
                UpdateAllTestStatus(GlobalValue.BTurnTable, Status.statusIdel);
                showLog("界面初始化完成");
            }));
        }

        private void btReset_Click(object sender, EventArgs e)
        {
            try
            {
                BeginInvoke(new Action(() =>
                {
                    showLog("开始复位");
                    testEngine.m_fixturePlc.WriteMRegister(7, true);
                    Thread.Sleep(1000);
                    testEngine.m_fixturePlc.WriteMRegister(7, false);
                    Thread.Sleep(300);
                    lock(m_lock)
                    {
                        testEngine.m_isAlarm = false;
                    }
                    
                    showLog("复位结束");
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void fixtureDebug_Click(object sender, EventArgs e)
        {
            try
            {
                debugForm = new DebugForm();
                debugForm.telPlc += TelPlc;
                debugForm.getTestItem += GetTestItem;
                debugForm.Show();
                int iTarget;
                TelPlc(PLCCmdMode.writeCoil, out iTarget, 3, 1);
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        public bool TelPlc(PLCCmdMode plcCmdMode, out int iTarget, int iAddress, int iSource)
        {
            iTarget = ushort.MaxValue;
            try
            {
                if (!testEngine.m_fixturePlc.IsOpen)
                {
                    showLog("治具PLC未连接", Color.Red);
                    return false;
                }
                if (plcCmdMode == PLCCmdMode.readCoil)
                {
                    bool[] bRead = testEngine.m_fixturePlc.ReadMRegister(iAddress, 1);
                    if (bRead == null) 
                    {
                        showLog("读取治具PLC数据失败", Color.Red);
                        return false; 
                    }
                    return bRead[0];

                }
                else if (plcCmdMode == PLCCmdMode.writeCoil)
                {
                    bool bWrite = testEngine.m_fixturePlc.WriteMRegister(iAddress, iSource == 1);
                    if (!bWrite)
                    {
                        showLog("写入治具PLC失败", Color.Red);
                        return false;
                    }
                }
                else if (plcCmdMode == PLCCmdMode.readHold)
                {
                    iTarget = testEngine.m_fixturePlc.ReadInt32(iAddress);
                }
                else if (plcCmdMode == PLCCmdMode.writeHold)
                {
                    bool bWrite = testEngine.m_fixturePlc.WriteInt32(iAddress, iSource);
                    if (!bWrite)
                    {
                        showLog("写入治具PLC失败", Color.Red);
                        return false;
                    }
                }
                return true;
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
                return false;
            }
        }

        private void oAndOTool_Click(object sender, EventArgs e)
        {
            testEngine.m_TestMode = TestMode.oAndO;
            showLog("已切换为正常测试模式", Color.Blue);
        }

        private void reTestTool_Click(object sender, EventArgs e)
        {
            testEngine.m_TestMode = TestMode.reTest;
            showLog("已切换为集中复测模式", Color.Blue);
        }

        private void sampleTool_Click(object sender, EventArgs e)
        {
            testEngine.m_TestMode = TestMode.sample;
            showLog("已切换为样本测试模式", Color.Blue);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 1;
            testEngine.m_iTurnTable = 1;
            showLog("机械手上料完成");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 2;
            testEngine.m_iTurnTable = 1;
            showLog("机械手上料完成");
        }

        private void button3_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 1;
            testEngine.m_iTurnTable = 2;
            showLog("机械手上料完成");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 2;
            testEngine.m_iTurnTable = 2;
            showLog("机械手上料完成");
        }

        private void button5_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 3;
            testEngine.m_iTurnTable = 1;
            showLog("机械手上料完成");
        }

        private void button6_Click(object sender, EventArgs e)
        {
            testEngine.m_bStartTest = true;
            testEngine.m_iType = 3;
            testEngine.m_iTurnTable = 2;
            showLog("机械手上料完成");
        }

        private void button7_Click(object sender, EventArgs e)
        {
            testEngine.m_bTestEnd = true;
            showLog("机械手下料完成");
        }

        private void button8_Click(object sender, EventArgs e)
        {
            testEngine.m_fixturePlc.WriteInt32(110, 1);
            showLog("执行清料");
        }

        private void humenToolStripMenuItem_Click(object sender, EventArgs e)
        {
            bool bWrite = testEngine.m_fixturePlc.WriteMRegister(15, true);
            Thread.Sleep(1000);
            bWrite &= testEngine.m_fixturePlc.WriteMRegister(15, false);
            if (!bWrite)
            {
                showLog("写入治具PLC失败", Color.Red);
                return;
            }
            testEngine.m_isAutoMode = false;
            //btnVis(true);
            showLog("切换为手动模式");
        }

        private void autoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            bool bWrite = testEngine.m_fixturePlc.WriteMRegister(16, true);
            Thread.Sleep(1000);
            bWrite &= testEngine.m_fixturePlc.WriteMRegister(16, false);
            if (!bWrite)
            {
                showLog("写入治具PLC失败", Color.Red);
                return;
            }
            testEngine.m_isAutoMode = true;
            //btnVis(false);
            showLog("切换为自动模式");
        }

        private void btnVis(bool bShow)
        {
            try
            {
                BeginInvoke(new Action(() =>
                {
                    if (bShow)
                    {
                        button1.Visible = true;
                        button2.Visible = true;
                        button3.Visible = true;
                        button4.Visible = true;
                        button5.Visible = true;
                        button6.Visible = true;
                        button7.Visible = true;
                        button8.Visible = true;
                    }
                    else
                    {
                        button1.Visible = false;
                        button2.Visible = false;
                        button3.Visible = false;
                        button4.Visible = false;
                        button5.Visible = false;
                        button6.Visible = false;
                        button7.Visible = false;
                        button8.Visible = false;
                    }
                }));
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
            
        }
    }
}
