using MFLEX_Compass.GlobalDir;
using MFLEX_Compass.TestDir;
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
//using System.Collections.Specialized.BitVector32;

namespace MFLEX_Compass.UI
{
    public partial class DebugForm : Form
    {
        public TelPlc telPlc;
        public GetTestItem getTestItem;
        public bool bA1On = false;
        public bool bA2On = false;
        public bool bB1On = false;
        public bool bB2On = false;
        public DebugForm()
        {
            InitializeComponent();
        }

        private void btCylinderDown_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 20, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 20, 0);
        }

        private void btCylinderUp_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 20, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 20, 0);
        }

        private void btASidePush_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 60, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 60, 0);
        }

        private void btBSidePush_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 65, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 65, 0);
        }

        private void btACylinder_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 70, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 70, 0);
        }

        private void btBCylinder_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 80, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 80, 0);
        }

        private void btA1VacuumOn_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 47, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 47, 0);
            if (bA1On)
            {
                btA1VacuumOn.Text = "转盘A工位1穴吸真空开启";
                btA1VacuumOn.BackColor = Color.Gray;
                bA1On = false;
            }
            else
            {
                btA1VacuumOn.Text = "转盘A工位1穴吸真空关闭";
                btA1VacuumOn.BackColor = Color.Green;
                bA1On = true;
            }
        }


        private void btA2VacuumOn_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 500, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 500, 0);
            if (bA2On)
            {
                btA2VacuumOn.Text = "转盘A工位2穴吸真空开启";
                btA2VacuumOn.BackColor = Color.Gray;
                bA2On = false;
            }
            else
            {
                btA2VacuumOn.Text = "转盘A工位2穴吸真空关闭";
                btA2VacuumOn.BackColor = Color.Green;
                bA2On = true;
            }
        }

        private void btB1VacuumOn_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 54, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 54, 0);
            if (bB1On)
            {
                btB1VacuumOn.Text = "转盘B工位1穴吸真空开启";
                btB1VacuumOn.BackColor = Color.Gray;
                bB1On = false;
            }
            else
            {
                btB1VacuumOn.Text = "转盘B工位1穴吸真空关闭";
                btB1VacuumOn.BackColor = Color.Green;
                bB1On = true;
            }
        }

        private void btB2VacuumOn_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 510, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 510, 0);
            if (bB2On)
            {
                btB2VacuumOn.Text = "转盘B工位2穴吸真空开启";
                btB2VacuumOn.BackColor = Color.Gray;
                bB2On = false;
            }
            else
            {
                btB2VacuumOn.Text = "转盘B工位2穴吸真空关闭";
                btB2VacuumOn.BackColor = Color.Green;
                bB2On = true;
            }
        }

        private void btASidePushOff_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 60, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 60, 0);
        }

        private void btBSidePushOff_Click(object sender, EventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 65, 1);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 65, 0);
        }

        private void ChangeAutoMode(object sender, FormClosedEventArgs e)
        {
            int iTarget1, iTarget2;
            telPlc(PLCCmdMode.writeCoil, out iTarget1, 3, 0);
            Thread.Sleep(800);
            telPlc(PLCCmdMode.writeCoil, out iTarget2, 4, 1);
        }

        private void btTest1_Click(object sender, EventArgs e)
        {
            BeginInvoke(new Action(() =>
            {
                List<TestItem> items = new List<TestItem>();
                List<TestItem> list = new List<TestItem>();
                getTestItem(1, ref items, ref list);
                int iIndex = 0;
                dgvTestData1.Rows.Clear();
                foreach (TestItem testItem in items)
                {
                    string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                        testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                        testItem.High ?? "", testItem.Unit ?? "" };
                    dgvTestData1.Rows.Add(strTemp);
                    dgvTestData1.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                    iIndex++;
                }
            }));
        }

        private void btTest2_Click(object sender, EventArgs e)
        {
            BeginInvoke(new Action(() =>
            {
                List<TestItem> items = new List<TestItem>();
                List<TestItem> list = new List<TestItem>();
                getTestItem(2, ref list, ref items);
                int iIndex = 0;
                dgvTestData2.Rows.Clear();
                foreach (TestItem testItem in items)
                {
                    string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                        testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                        testItem.High ?? "", testItem.Unit ?? "" };
                    dgvTestData2.Rows.Add(strTemp);
                    dgvTestData2.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                    iIndex++;
                }
            }));
        }

        private void btTest3_Click(object sender, EventArgs e)
        {
            BeginInvoke(new Action(() =>
            {
                List<TestItem> items1 = new List<TestItem>();
                List<TestItem> items2 = new List<TestItem>();
                getTestItem(3, ref items1, ref items2);
                int iIndex = 0;

                dgvTestData1.Rows.Clear();
                dgvTestData2.Rows.Clear();
                foreach (TestItem testItem in items1)
                {
                    string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                        testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                        testItem.High ?? "", testItem.Unit ?? "" };
                    dgvTestData1.Rows.Add(strTemp);
                    dgvTestData1.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                    iIndex++;
                }

                iIndex = 0;
                foreach (TestItem testItem in items2)
                {
                    string[] strTemp = {testItem.Name ?? "", testItem.Value ?? "",
                        testItem.Result ? "Pass" : "Fail", testItem.Low ?? "",
                        testItem.High ?? "", testItem.Unit ?? "" };
                    dgvTestData2.Rows.Add(strTemp);
                    dgvTestData2.Rows[iIndex].Cells[2].Style.BackColor = strTemp[2] == "Pass" ? Color.Green : Color.Red;
                    iIndex++;
                }
            }));
        }
    }
}
