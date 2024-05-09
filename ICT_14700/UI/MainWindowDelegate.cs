using MFLEX_Compass.GlobalDir;
using MFLEX_Compass.TestDir;
using MFLEX_Compass.MesDir;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace MFLEX_Compass.UI
{
    public delegate void showLog(string strContent, Color color = default(Color));
    public delegate void UpdateBarcode(Station station, string strBarcode);
    public delegate void UpdateAllTestStatus(string strTurnTable, Status status);
    public delegate void UpdateTestStatus(Station station, Status status);
    public delegate void UpdateDevicesStatus(DevicesNum devicesNum, DevicesStatus devicesStatus);
    public delegate void ShowTestDataSingle(Station station, TestItem testItem);
    public delegate void ShowTestDataList(Station station, List<TestItem> testItems);
    public delegate void UpdateYield(Station station, int iPassNum, int iFailNum);
    public delegate void UpdateTestTime(string strTurnTable, bool bIsTestIng);
    public delegate bool TelPlc(PLCCmdMode plcCmdMode, out int iTarget, int iAddress, int iSource);
    public delegate bool GetTestItem(int iSlot, ref List<TestItem> items1, ref List<TestItem> items2);
    public delegate void UpdateSampleListview(List<ETsample> items);
    public delegate void MainInit();
    public delegate void ClearYield();
    public delegate void ClearSampleListView();
}
