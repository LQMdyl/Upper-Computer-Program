using System;
using System.Collections.Generic;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;
using MFLEX_Compass.GlobalDir;
using MFLEX_Compass.TestDir;
using MFLEX_Compass.UI;
using Newtonsoft.Json.Linq;
//using System.Collections.Specialized.BitVector32;

namespace MFLEX_Compass
{
    partial class MainWindow
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainWindow));
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.adminToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.adminLoginToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.adminExitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.modifyToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.settleConfigToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.clearYieldToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.debugToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.fixtureDebug = new System.Windows.Forms.ToolStripMenuItem();
            this.commmandTool = new System.Windows.Forms.ToolStripMenuItem();
            this.testModeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.oAndOTool = new System.Windows.Forms.ToolStripMenuItem();
            this.reTestTool = new System.Windows.Forms.ToolStripMenuItem();
            this.sampleTool = new System.Windows.Forms.ToolStripMenuItem();
            this.opmodeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.humenToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.autoToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.MCULabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.MCULabel2 = new System.Windows.Forms.ToolStripStatusLabel();
            this.PlcLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.PlcLabel2 = new System.Windows.Forms.ToolStripStatusLabel();
            this.lbProgram = new System.Windows.Forms.Label();
            this.A_AllStatus = new System.Windows.Forms.Label();
            this.B_AllStatus = new System.Windows.Forms.Label();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.panel1 = new System.Windows.Forms.Panel();
            this.lbAStatus2 = new System.Windows.Forms.Label();
            this.lbAStatus1 = new System.Windows.Forms.Label();
            this.lbAYield2 = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.lbATotal2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.tbABarcode2 = new System.Windows.Forms.TextBox();
            this.lbATestTime = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.lbAYield1 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.lbATotal1 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.tbABarcode1 = new System.Windows.Forms.TextBox();
            this.panel2 = new System.Windows.Forms.Panel();
            this.lbBStatus1 = new System.Windows.Forms.Label();
            this.lbBStatus2 = new System.Windows.Forms.Label();
            this.lbBYield2 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.lbBTotal2 = new System.Windows.Forms.Label();
            this.label16 = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            this.label18 = new System.Windows.Forms.Label();
            this.tbBBarcode2 = new System.Windows.Forms.TextBox();
            this.lbBTestTime = new System.Windows.Forms.Label();
            this.label20 = new System.Windows.Forms.Label();
            this.lbBYield1 = new System.Windows.Forms.Label();
            this.label22 = new System.Windows.Forms.Label();
            this.lbBTotal1 = new System.Windows.Forms.Label();
            this.label24 = new System.Windows.Forms.Label();
            this.tbBBarcode1 = new System.Windows.Forms.TextBox();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.label35 = new System.Windows.Forms.Label();
            this.lbTPass = new System.Windows.Forms.Label();
            this.label37 = new System.Windows.Forms.Label();
            this.lbTFail = new System.Windows.Forms.Label();
            this.label39 = new System.Windows.Forms.Label();
            this.lbTTotal = new System.Windows.Forms.Label();
            this.label41 = new System.Windows.Forms.Label();
            this.lbTYield = new System.Windows.Forms.Label();
            this.btReset = new System.Windows.Forms.Button();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.button5 = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.label25 = new System.Windows.Forms.Label();
            this.lbOperator = new System.Windows.Forms.Label();
            this.label27 = new System.Windows.Forms.Label();
            this.lbLineId = new System.Windows.Forms.Label();
            this.label29 = new System.Windows.Forms.Label();
            this.lbToolNum = new System.Windows.Forms.Label();
            this.label31 = new System.Windows.Forms.Label();
            this.lbFixtureId = new System.Windows.Forms.Label();
            this.label33 = new System.Windows.Forms.Label();
            this.lbWorkArea = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.rtbLog = new System.Windows.Forms.RichTextBox();
            this.tabResult = new System.Windows.Forms.TabControl();
            this.A1TabResult = new System.Windows.Forms.TabPage();
            this.tableA1Result = new System.Windows.Forms.DataGridView();
            this.A_tableItem = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A_tableValue = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A_tableResult = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A_tableLimitL = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A_tableLimitH = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A_tableUnit = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.A2TabResult = new System.Windows.Forms.TabPage();
            this.tableA2Result = new System.Windows.Forms.DataGridView();
            this.dataGridViewTextBoxColumn1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn3 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn4 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn5 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn6 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B1TabResult = new System.Windows.Forms.TabPage();
            this.tableB1Result = new System.Windows.Forms.DataGridView();
            this.B_tableItem = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B_tableValue = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B_tableResult = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B_tableLimitL = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B_tableLimitH = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B_tableUnit = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.B2TabResult = new System.Windows.Forms.TabPage();
            this.tableB2Result = new System.Windows.Forms.DataGridView();
            this.dataGridViewTextBoxColumn7 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn8 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn9 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn10 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn11 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn12 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Sample = new System.Windows.Forms.TabPage();
            this.lvSample = new System.Windows.Forms.ListView();
            this.columnHeader1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader3 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader4 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader5 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.runTime = new System.Windows.Forms.Label();
            this.button7 = new System.Windows.Forms.Button();
            this.button8 = new System.Windows.Forms.Button();
            this.menuStrip1.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            this.flowLayoutPanel1.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.tabResult.SuspendLayout();
            this.A1TabResult.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tableA1Result)).BeginInit();
            this.A2TabResult.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tableA2Result)).BeginInit();
            this.B1TabResult.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tableB1Result)).BeginInit();
            this.B2TabResult.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.tableB2Result)).BeginInit();
            this.Sample.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.adminToolStripMenuItem,
            this.modifyToolStripMenuItem,
            this.debugToolStripMenuItem,
            this.testModeToolStripMenuItem,
            this.opmodeToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(1046, 25);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // adminToolStripMenuItem
            // 
            this.adminToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.adminLoginToolStripMenuItem,
            this.adminExitToolStripMenuItem});
            this.adminToolStripMenuItem.Name = "adminToolStripMenuItem";
            this.adminToolStripMenuItem.Size = new System.Drawing.Size(80, 21);
            this.adminToolStripMenuItem.Text = "管理员功能";
            // 
            // adminLoginToolStripMenuItem
            // 
            this.adminLoginToolStripMenuItem.Name = "adminLoginToolStripMenuItem";
            this.adminLoginToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.adminLoginToolStripMenuItem.Text = "管理员登录";
            this.adminLoginToolStripMenuItem.Click += new System.EventHandler(this.adminLoginToolStripMenuItem_Click);
            // 
            // adminExitToolStripMenuItem
            // 
            this.adminExitToolStripMenuItem.Name = "adminExitToolStripMenuItem";
            this.adminExitToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.adminExitToolStripMenuItem.Text = "管理员登出";
            this.adminExitToolStripMenuItem.Click += new System.EventHandler(this.adminExitToolStripMenuItem_Click);
            // 
            // modifyToolStripMenuItem
            // 
            this.modifyToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.settleConfigToolStripMenuItem,
            this.clearYieldToolStripMenuItem});
            this.modifyToolStripMenuItem.Name = "modifyToolStripMenuItem";
            this.modifyToolStripMenuItem.Size = new System.Drawing.Size(68, 21);
            this.modifyToolStripMenuItem.Text = "修改功能";
            // 
            // settleConfigToolStripMenuItem
            // 
            this.settleConfigToolStripMenuItem.Name = "settleConfigToolStripMenuItem";
            this.settleConfigToolStripMenuItem.Size = new System.Drawing.Size(124, 22);
            this.settleConfigToolStripMenuItem.Text = "程序配置";
            this.settleConfigToolStripMenuItem.Visible = false;
            this.settleConfigToolStripMenuItem.Click += new System.EventHandler(this.settleConfigToolStripMenuItem_Click);
            // 
            // clearYieldToolStripMenuItem
            // 
            this.clearYieldToolStripMenuItem.Name = "clearYieldToolStripMenuItem";
            this.clearYieldToolStripMenuItem.Size = new System.Drawing.Size(124, 22);
            this.clearYieldToolStripMenuItem.Text = "良率清除";
            this.clearYieldToolStripMenuItem.Click += new System.EventHandler(this.clearYieldToolStripMenuItem_Click);
            // 
            // debugToolStripMenuItem
            // 
            this.debugToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fixtureDebug,
            this.commmandTool});
            this.debugToolStripMenuItem.Name = "debugToolStripMenuItem";
            this.debugToolStripMenuItem.Size = new System.Drawing.Size(68, 21);
            this.debugToolStripMenuItem.Text = "调试功能";
            // 
            // fixtureDebug
            // 
            this.fixtureDebug.Enabled = false;
            this.fixtureDebug.Name = "fixtureDebug";
            this.fixtureDebug.Size = new System.Drawing.Size(124, 22);
            this.fixtureDebug.Text = "动作调试";
            this.fixtureDebug.Click += new System.EventHandler(this.fixtureDebug_Click);
            // 
            // commmandTool
            // 
            this.commmandTool.Name = "commmandTool";
            this.commmandTool.Size = new System.Drawing.Size(124, 22);
            this.commmandTool.Text = "指令模式";
            this.commmandTool.Visible = false;
            // 
            // testModeToolStripMenuItem
            // 
            this.testModeToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.oAndOTool,
            this.reTestTool,
            this.sampleTool});
            this.testModeToolStripMenuItem.Name = "testModeToolStripMenuItem";
            this.testModeToolStripMenuItem.Size = new System.Drawing.Size(68, 21);
            this.testModeToolStripMenuItem.Text = "测试模式";
            // 
            // oAndOTool
            // 
            this.oAndOTool.Name = "oAndOTool";
            this.oAndOTool.Size = new System.Drawing.Size(148, 22);
            this.oAndOTool.Text = "正常模式";
            this.oAndOTool.Click += new System.EventHandler(this.oAndOTool_Click);
            // 
            // reTestTool
            // 
            this.reTestTool.Name = "reTestTool";
            this.reTestTool.Size = new System.Drawing.Size(148, 22);
            this.reTestTool.Text = "集中复测模式";
            this.reTestTool.Click += new System.EventHandler(this.reTestTool_Click);
            // 
            // sampleTool
            // 
            this.sampleTool.Name = "sampleTool";
            this.sampleTool.Size = new System.Drawing.Size(148, 22);
            this.sampleTool.Text = "样本模式";
            this.sampleTool.Click += new System.EventHandler(this.sampleTool_Click);
            // 
            // opmodeToolStripMenuItem
            // 
            this.opmodeToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.humenToolStripMenuItem,
            this.autoToolStripMenuItem});
            this.opmodeToolStripMenuItem.Name = "opmodeToolStripMenuItem";
            this.opmodeToolStripMenuItem.Size = new System.Drawing.Size(68, 21);
            this.opmodeToolStripMenuItem.Text = "操作模式";
            // 
            // humenToolStripMenuItem
            // 
            this.humenToolStripMenuItem.Name = "humenToolStripMenuItem";
            this.humenToolStripMenuItem.Size = new System.Drawing.Size(124, 22);
            this.humenToolStripMenuItem.Text = "手动模式";
            this.humenToolStripMenuItem.Visible = false;
            this.humenToolStripMenuItem.Click += new System.EventHandler(this.humenToolStripMenuItem_Click);
            // 
            // autoToolStripMenuItem
            // 
            this.autoToolStripMenuItem.Name = "autoToolStripMenuItem";
            this.autoToolStripMenuItem.Size = new System.Drawing.Size(124, 22);
            this.autoToolStripMenuItem.Text = "自动模式";
            this.autoToolStripMenuItem.Click += new System.EventHandler(this.autoToolStripMenuItem_Click);
            // 
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.MCULabel1,
            this.MCULabel2,
            this.PlcLabel1,
            this.PlcLabel2});
            this.statusStrip1.Location = new System.Drawing.Point(0, 724);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(1046, 26);
            this.statusStrip1.TabIndex = 1;
            this.statusStrip1.Text = "statusStrip1";
            // 
            // MCULabel1
            // 
            this.MCULabel1.BackColor = System.Drawing.Color.Red;
            this.MCULabel1.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.MCULabel1.Name = "MCULabel1";
            this.MCULabel1.Size = new System.Drawing.Size(55, 21);
            this.MCULabel1.Text = "单片机1";
            // 
            // MCULabel2
            // 
            this.MCULabel2.BackColor = System.Drawing.Color.Red;
            this.MCULabel2.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.MCULabel2.Name = "MCULabel2";
            this.MCULabel2.Size = new System.Drawing.Size(55, 21);
            this.MCULabel2.Text = "单片机2";
            // 
            // PlcLabel1
            // 
            this.PlcLabel1.BackColor = System.Drawing.Color.Red;
            this.PlcLabel1.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.PlcLabel1.Name = "PlcLabel1";
            this.PlcLabel1.Size = new System.Drawing.Size(87, 21);
            this.PlcLabel1.Text = "FIXTURE_PLC";
            // 
            // PlcLabel2
            // 
            this.PlcLabel2.BackColor = System.Drawing.Color.Red;
            this.PlcLabel2.BorderSides = ((System.Windows.Forms.ToolStripStatusLabelBorderSides)((((System.Windows.Forms.ToolStripStatusLabelBorderSides.Left | System.Windows.Forms.ToolStripStatusLabelBorderSides.Top) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Right) 
            | System.Windows.Forms.ToolStripStatusLabelBorderSides.Bottom)));
            this.PlcLabel2.Name = "PlcLabel2";
            this.PlcLabel2.Size = new System.Drawing.Size(71, 21);
            this.PlcLabel2.Text = "LOAD_PLC";
            // 
            // lbProgram
            // 
            this.lbProgram.AutoSize = true;
            this.lbProgram.Font = new System.Drawing.Font("微软雅黑", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.lbProgram.Location = new System.Drawing.Point(429, 30);
            this.lbProgram.Name = "lbProgram";
            this.lbProgram.Size = new System.Drawing.Size(185, 27);
            this.lbProgram.TabIndex = 2;
            this.lbProgram.Text = "MFLEX_COMPASS";
            // 
            // A_AllStatus
            // 
            this.A_AllStatus.BackColor = System.Drawing.Color.Gray;
            this.A_AllStatus.Font = new System.Drawing.Font("微软雅黑", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.A_AllStatus.Location = new System.Drawing.Point(3, 0);
            this.A_AllStatus.Name = "A_AllStatus";
            this.A_AllStatus.Size = new System.Drawing.Size(517, 38);
            this.A_AllStatus.TabIndex = 3;
            this.A_AllStatus.Text = "A-IDEL";
            this.A_AllStatus.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // B_AllStatus
            // 
            this.B_AllStatus.BackColor = System.Drawing.Color.Gray;
            this.B_AllStatus.Font = new System.Drawing.Font("微软雅黑", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.B_AllStatus.Location = new System.Drawing.Point(523, 0);
            this.B_AllStatus.Margin = new System.Windows.Forms.Padding(0);
            this.B_AllStatus.Name = "B_AllStatus";
            this.B_AllStatus.Size = new System.Drawing.Size(523, 38);
            this.B_AllStatus.TabIndex = 4;
            this.B_AllStatus.Text = "B-IDEL";
            this.B_AllStatus.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.tableLayoutPanel1.AutoScroll = true;
            this.tableLayoutPanel1.ColumnCount = 2;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel1.Controls.Add(this.A_AllStatus, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.B_AllStatus, 1, 0);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 60);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 1;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(1046, 42);
            this.tableLayoutPanel1.TabIndex = 5;
            // 
            // panel1
            // 
            this.panel1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.panel1.Controls.Add(this.lbAStatus2);
            this.panel1.Controls.Add(this.lbAStatus1);
            this.panel1.Controls.Add(this.lbAYield2);
            this.panel1.Controls.Add(this.label11);
            this.panel1.Controls.Add(this.lbATotal2);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Controls.Add(this.tbABarcode2);
            this.panel1.Controls.Add(this.lbATestTime);
            this.panel1.Controls.Add(this.label9);
            this.panel1.Controls.Add(this.lbAYield1);
            this.panel1.Controls.Add(this.label7);
            this.panel1.Controls.Add(this.lbATotal1);
            this.panel1.Controls.Add(this.label5);
            this.panel1.Controls.Add(this.tbABarcode1);
            this.panel1.Location = new System.Drawing.Point(1, 20);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(246, 246);
            this.panel1.TabIndex = 7;
            // 
            // lbAStatus2
            // 
            this.lbAStatus2.AutoSize = true;
            this.lbAStatus2.BackColor = System.Drawing.Color.Gray;
            this.lbAStatus2.Location = new System.Drawing.Point(3, 137);
            this.lbAStatus2.MinimumSize = new System.Drawing.Size(250, 0);
            this.lbAStatus2.Name = "lbAStatus2";
            this.lbAStatus2.Size = new System.Drawing.Size(250, 20);
            this.lbAStatus2.TabIndex = 15;
            this.lbAStatus2.Text = "IDEL";
            this.lbAStatus2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // lbAStatus1
            // 
            this.lbAStatus1.AutoSize = true;
            this.lbAStatus1.BackColor = System.Drawing.Color.Gray;
            this.lbAStatus1.Location = new System.Drawing.Point(3, 3);
            this.lbAStatus1.MinimumSize = new System.Drawing.Size(250, 0);
            this.lbAStatus1.Name = "lbAStatus1";
            this.lbAStatus1.Size = new System.Drawing.Size(250, 20);
            this.lbAStatus1.TabIndex = 14;
            this.lbAStatus1.Text = "IDEL";
            this.lbAStatus1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // lbAYield2
            // 
            this.lbAYield2.AutoSize = true;
            this.lbAYield2.Location = new System.Drawing.Point(59, 209);
            this.lbAYield2.Name = "lbAYield2";
            this.lbAYield2.Size = new System.Drawing.Size(56, 20);
            this.lbAYield2.TabIndex = 13;
            this.lbAYield2.Text = "97.23%";
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(3, 209);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(56, 20);
            this.label11.TabIndex = 12;
            this.label11.Text = "Yield：";
            // 
            // lbATotal2
            // 
            this.lbATotal2.AutoSize = true;
            this.lbATotal2.Location = new System.Drawing.Point(59, 189);
            this.lbATotal2.Name = "lbATotal2";
            this.lbATotal2.Size = new System.Drawing.Size(33, 20);
            this.lbATotal2.TabIndex = 11;
            this.lbATotal2.Text = "136";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(3, 189);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(57, 20);
            this.label3.TabIndex = 10;
            this.label3.Text = "Total：";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label2.ForeColor = System.Drawing.Color.Blue;
            this.label2.Location = new System.Drawing.Point(227, 162);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(19, 22);
            this.label2.TabIndex = 9;
            this.label2.Text = "2";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label1.ForeColor = System.Drawing.Color.Blue;
            this.label1.Location = new System.Drawing.Point(227, 28);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(19, 22);
            this.label1.TabIndex = 8;
            this.label1.Text = "1";
            // 
            // tbABarcode2
            // 
            this.tbABarcode2.Location = new System.Drawing.Point(3, 160);
            this.tbABarcode2.Name = "tbABarcode2";
            this.tbABarcode2.Size = new System.Drawing.Size(218, 26);
            this.tbABarcode2.TabIndex = 7;
            // 
            // lbATestTime
            // 
            this.lbATestTime.AutoSize = true;
            this.lbATestTime.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lbATestTime.Location = new System.Drawing.Point(96, 104);
            this.lbATestTime.Name = "lbATestTime";
            this.lbATestTime.Size = new System.Drawing.Size(27, 22);
            this.lbATestTime.TabIndex = 6;
            this.lbATestTime.Text = "0S";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label9.Location = new System.Drawing.Point(3, 104);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(89, 22);
            this.label9.TabIndex = 5;
            this.label9.Text = "Test Time：";
            // 
            // lbAYield1
            // 
            this.lbAYield1.AutoSize = true;
            this.lbAYield1.Location = new System.Drawing.Point(59, 75);
            this.lbAYield1.Name = "lbAYield1";
            this.lbAYield1.Size = new System.Drawing.Size(56, 20);
            this.lbAYield1.TabIndex = 4;
            this.lbAYield1.Text = "95.52%";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(3, 75);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(56, 20);
            this.label7.TabIndex = 3;
            this.label7.Text = "Yield：";
            // 
            // lbATotal1
            // 
            this.lbATotal1.AutoSize = true;
            this.lbATotal1.Location = new System.Drawing.Point(59, 55);
            this.lbATotal1.Name = "lbATotal1";
            this.lbATotal1.Size = new System.Drawing.Size(25, 20);
            this.lbATotal1.TabIndex = 2;
            this.lbATotal1.Text = "94";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(3, 55);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(57, 20);
            this.label5.TabIndex = 1;
            this.label5.Text = "Total：";
            // 
            // tbABarcode1
            // 
            this.tbABarcode1.Location = new System.Drawing.Point(3, 25);
            this.tbABarcode1.Name = "tbABarcode1";
            this.tbABarcode1.Size = new System.Drawing.Size(221, 26);
            this.tbABarcode1.TabIndex = 0;
            // 
            // panel2
            // 
            this.panel2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.panel2.Controls.Add(this.lbBStatus1);
            this.panel2.Controls.Add(this.lbBStatus2);
            this.panel2.Controls.Add(this.lbBYield2);
            this.panel2.Controls.Add(this.label14);
            this.panel2.Controls.Add(this.lbBTotal2);
            this.panel2.Controls.Add(this.label16);
            this.panel2.Controls.Add(this.label17);
            this.panel2.Controls.Add(this.label18);
            this.panel2.Controls.Add(this.tbBBarcode2);
            this.panel2.Controls.Add(this.lbBTestTime);
            this.panel2.Controls.Add(this.label20);
            this.panel2.Controls.Add(this.lbBYield1);
            this.panel2.Controls.Add(this.label22);
            this.panel2.Controls.Add(this.lbBTotal1);
            this.panel2.Controls.Add(this.label24);
            this.panel2.Controls.Add(this.tbBBarcode1);
            this.panel2.Location = new System.Drawing.Point(3, 20);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(247, 246);
            this.panel2.TabIndex = 8;
            // 
            // lbBStatus1
            // 
            this.lbBStatus1.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbBStatus1.AutoSize = true;
            this.lbBStatus1.BackColor = System.Drawing.Color.Gray;
            this.lbBStatus1.Location = new System.Drawing.Point(3, 2);
            this.lbBStatus1.MinimumSize = new System.Drawing.Size(250, 0);
            this.lbBStatus1.Name = "lbBStatus1";
            this.lbBStatus1.Size = new System.Drawing.Size(250, 20);
            this.lbBStatus1.TabIndex = 15;
            this.lbBStatus1.Text = "IDEL";
            this.lbBStatus1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // lbBStatus2
            // 
            this.lbBStatus2.AutoSize = true;
            this.lbBStatus2.BackColor = System.Drawing.Color.Gray;
            this.lbBStatus2.Location = new System.Drawing.Point(3, 136);
            this.lbBStatus2.MinimumSize = new System.Drawing.Size(250, 0);
            this.lbBStatus2.Name = "lbBStatus2";
            this.lbBStatus2.Size = new System.Drawing.Size(250, 20);
            this.lbBStatus2.TabIndex = 14;
            this.lbBStatus2.Text = "IDEL";
            this.lbBStatus2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // lbBYield2
            // 
            this.lbBYield2.AutoSize = true;
            this.lbBYield2.Location = new System.Drawing.Point(59, 209);
            this.lbBYield2.Name = "lbBYield2";
            this.lbBYield2.Size = new System.Drawing.Size(56, 20);
            this.lbBYield2.TabIndex = 13;
            this.lbBYield2.Text = "95.92%";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(3, 209);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(56, 20);
            this.label14.TabIndex = 12;
            this.label14.Text = "Yield：";
            // 
            // lbBTotal2
            // 
            this.lbBTotal2.AutoSize = true;
            this.lbBTotal2.Location = new System.Drawing.Point(59, 189);
            this.lbBTotal2.Name = "lbBTotal2";
            this.lbBTotal2.Size = new System.Drawing.Size(33, 20);
            this.lbBTotal2.TabIndex = 11;
            this.lbBTotal2.Text = "116";
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(3, 189);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(57, 20);
            this.label16.TabIndex = 10;
            this.label16.Text = "Total：";
            // 
            // label17
            // 
            this.label17.AutoSize = true;
            this.label17.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label17.ForeColor = System.Drawing.Color.Blue;
            this.label17.Location = new System.Drawing.Point(228, 162);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(19, 22);
            this.label17.TabIndex = 9;
            this.label17.Text = "2";
            // 
            // label18
            // 
            this.label18.AutoSize = true;
            this.label18.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label18.ForeColor = System.Drawing.Color.Blue;
            this.label18.Location = new System.Drawing.Point(228, 28);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(19, 22);
            this.label18.TabIndex = 8;
            this.label18.Text = "1";
            // 
            // tbBBarcode2
            // 
            this.tbBBarcode2.Location = new System.Drawing.Point(3, 160);
            this.tbBBarcode2.Name = "tbBBarcode2";
            this.tbBBarcode2.Size = new System.Drawing.Size(219, 26);
            this.tbBBarcode2.TabIndex = 7;
            // 
            // lbBTestTime
            // 
            this.lbBTestTime.AutoSize = true;
            this.lbBTestTime.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lbBTestTime.Location = new System.Drawing.Point(96, 104);
            this.lbBTestTime.Name = "lbBTestTime";
            this.lbBTestTime.Size = new System.Drawing.Size(38, 22);
            this.lbBTestTime.TabIndex = 6;
            this.lbBTestTime.Text = "0.0S";
            // 
            // label20
            // 
            this.label20.AutoSize = true;
            this.label20.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label20.Location = new System.Drawing.Point(3, 104);
            this.label20.Name = "label20";
            this.label20.Size = new System.Drawing.Size(89, 22);
            this.label20.TabIndex = 5;
            this.label20.Text = "Test Time：";
            // 
            // lbBYield1
            // 
            this.lbBYield1.AutoSize = true;
            this.lbBYield1.Location = new System.Drawing.Point(59, 75);
            this.lbBYield1.Name = "lbBYield1";
            this.lbBYield1.Size = new System.Drawing.Size(56, 20);
            this.lbBYield1.TabIndex = 4;
            this.lbBYield1.Text = "96.26%";
            // 
            // label22
            // 
            this.label22.AutoSize = true;
            this.label22.Location = new System.Drawing.Point(3, 75);
            this.label22.Name = "label22";
            this.label22.Size = new System.Drawing.Size(56, 20);
            this.label22.TabIndex = 3;
            this.label22.Text = "Yield：";
            // 
            // lbBTotal1
            // 
            this.lbBTotal1.AutoSize = true;
            this.lbBTotal1.Location = new System.Drawing.Point(59, 54);
            this.lbBTotal1.Name = "lbBTotal1";
            this.lbBTotal1.Size = new System.Drawing.Size(33, 20);
            this.lbBTotal1.TabIndex = 2;
            this.lbBTotal1.Text = "135";
            // 
            // label24
            // 
            this.label24.AutoSize = true;
            this.label24.Location = new System.Drawing.Point(3, 54);
            this.label24.Name = "label24";
            this.label24.Size = new System.Drawing.Size(57, 20);
            this.label24.TabIndex = 1;
            this.label24.Text = "Total：";
            // 
            // tbBBarcode1
            // 
            this.tbBBarcode1.Location = new System.Drawing.Point(3, 25);
            this.tbBBarcode1.Name = "tbBBarcode1";
            this.tbBBarcode1.Size = new System.Drawing.Size(222, 26);
            this.tbBBarcode1.TabIndex = 0;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tableLayoutPanel3.AutoSize = true;
            this.tableLayoutPanel3.ColumnCount = 3;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 34.45378F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 31.09244F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 34F));
            this.tableLayoutPanel3.Controls.Add(this.label35, 0, 0);
            this.tableLayoutPanel3.Controls.Add(this.lbTPass, 1, 0);
            this.tableLayoutPanel3.Controls.Add(this.label37, 0, 1);
            this.tableLayoutPanel3.Controls.Add(this.lbTFail, 1, 1);
            this.tableLayoutPanel3.Controls.Add(this.label39, 0, 2);
            this.tableLayoutPanel3.Controls.Add(this.lbTTotal, 1, 2);
            this.tableLayoutPanel3.Controls.Add(this.label41, 0, 3);
            this.tableLayoutPanel3.Controls.Add(this.lbTYield, 1, 3);
            this.tableLayoutPanel3.Controls.Add(this.btReset, 0, 4);
            this.tableLayoutPanel3.Controls.Add(this.button1, 2, 0);
            this.tableLayoutPanel3.Controls.Add(this.button2, 2, 1);
            this.tableLayoutPanel3.Controls.Add(this.button3, 2, 2);
            this.tableLayoutPanel3.Controls.Add(this.button4, 2, 3);
            this.tableLayoutPanel3.Controls.Add(this.button5, 1, 4);
            this.tableLayoutPanel3.Controls.Add(this.button6, 2, 4);
            this.tableLayoutPanel3.Location = new System.Drawing.Point(6, 25);
            this.tableLayoutPanel3.MinimumSize = new System.Drawing.Size(200, 0);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 5;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(238, 239);
            this.tableLayoutPanel3.TabIndex = 10;
            // 
            // label35
            // 
            this.label35.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label35.AutoSize = true;
            this.label35.Location = new System.Drawing.Point(38, 13);
            this.label35.Name = "label35";
            this.label35.Size = new System.Drawing.Size(41, 20);
            this.label35.TabIndex = 0;
            this.label35.Text = "Pass:";
            // 
            // lbTPass
            // 
            this.lbTPass.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbTPass.AutoSize = true;
            this.lbTPass.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbTPass.ForeColor = System.Drawing.Color.Green;
            this.lbTPass.Location = new System.Drawing.Point(85, 12);
            this.lbTPass.Name = "lbTPass";
            this.lbTPass.Size = new System.Drawing.Size(35, 22);
            this.lbTPass.TabIndex = 1;
            this.lbTPass.Text = "100";
            // 
            // label37
            // 
            this.label37.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label37.AutoSize = true;
            this.label37.Location = new System.Drawing.Point(44, 60);
            this.label37.Name = "label37";
            this.label37.Size = new System.Drawing.Size(35, 20);
            this.label37.TabIndex = 2;
            this.label37.Text = "Fail:";
            // 
            // lbTFail
            // 
            this.lbTFail.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbTFail.AutoSize = true;
            this.lbTFail.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbTFail.ForeColor = System.Drawing.Color.Red;
            this.lbTFail.Location = new System.Drawing.Point(85, 59);
            this.lbTFail.Name = "lbTFail";
            this.lbTFail.Size = new System.Drawing.Size(19, 22);
            this.lbTFail.TabIndex = 3;
            this.lbTFail.Text = "3";
            // 
            // label39
            // 
            this.label39.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label39.AutoSize = true;
            this.label39.Location = new System.Drawing.Point(33, 107);
            this.label39.Name = "label39";
            this.label39.Size = new System.Drawing.Size(46, 20);
            this.label39.TabIndex = 4;
            this.label39.Text = "Total:";
            // 
            // lbTTotal
            // 
            this.lbTTotal.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbTTotal.AutoSize = true;
            this.lbTTotal.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbTTotal.ForeColor = System.Drawing.Color.Blue;
            this.lbTTotal.Location = new System.Drawing.Point(85, 106);
            this.lbTTotal.Name = "lbTTotal";
            this.lbTTotal.Size = new System.Drawing.Size(35, 22);
            this.lbTTotal.TabIndex = 5;
            this.lbTTotal.Text = "103";
            // 
            // label41
            // 
            this.label41.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label41.AutoSize = true;
            this.label41.Location = new System.Drawing.Point(34, 154);
            this.label41.Name = "label41";
            this.label41.Size = new System.Drawing.Size(45, 20);
            this.label41.TabIndex = 6;
            this.label41.Text = "Yield:";
            // 
            // lbTYield
            // 
            this.lbTYield.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbTYield.AutoSize = true;
            this.lbTYield.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbTYield.Location = new System.Drawing.Point(85, 153);
            this.lbTYield.Name = "lbTYield";
            this.lbTYield.Size = new System.Drawing.Size(58, 22);
            this.lbTYield.TabIndex = 7;
            this.lbTYield.Text = "97.09%";
            // 
            // btReset
            // 
            this.btReset.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.btReset.AutoSize = true;
            this.btReset.Location = new System.Drawing.Point(4, 198);
            this.btReset.Name = "btReset";
            this.btReset.Size = new System.Drawing.Size(75, 30);
            this.btReset.TabIndex = 8;
            this.btReset.Text = "报警清除";
            this.btReset.UseVisualStyleBackColor = true;
            this.btReset.Click += new System.EventHandler(this.btReset_Click);
            // 
            // button1
            // 
            this.button1.AutoSize = true;
            this.button1.Location = new System.Drawing.Point(159, 3);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(76, 30);
            this.button1.TabIndex = 9;
            this.button1.Text = "A转盘1穴上料";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.AutoSize = true;
            this.button2.Location = new System.Drawing.Point(159, 50);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(76, 30);
            this.button2.TabIndex = 10;
            this.button2.Text = "A转盘2穴上料";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // button3
            // 
            this.button3.AutoSize = true;
            this.button3.Location = new System.Drawing.Point(159, 97);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(76, 30);
            this.button3.TabIndex = 11;
            this.button3.Text = "B转盘1穴上料";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button4
            // 
            this.button4.AutoSize = true;
            this.button4.Location = new System.Drawing.Point(159, 144);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(76, 30);
            this.button4.TabIndex = 12;
            this.button4.Text = "B转盘2穴上料";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // button5
            // 
            this.button5.AutoSize = true;
            this.button5.Location = new System.Drawing.Point(85, 191);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(67, 30);
            this.button5.TabIndex = 13;
            this.button5.Text = "A1、2";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new System.EventHandler(this.button5_Click);
            // 
            // button6
            // 
            this.button6.AutoSize = true;
            this.button6.Location = new System.Drawing.Point(159, 191);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(75, 30);
            this.button6.TabIndex = 14;
            this.button6.Text = "B1、2";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new System.EventHandler(this.button6_Click);
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.Controls.Add(this.groupBox4);
            this.flowLayoutPanel1.Controls.Add(this.groupBox1);
            this.flowLayoutPanel1.Controls.Add(this.groupBox2);
            this.flowLayoutPanel1.Controls.Add(this.groupBox3);
            this.flowLayoutPanel1.Location = new System.Drawing.Point(8, 120);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(1032, 278);
            this.flowLayoutPanel1.TabIndex = 11;
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.panel1);
            this.groupBox4.Location = new System.Drawing.Point(3, 3);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(253, 272);
            this.groupBox4.TabIndex = 16;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "A转盘信息";
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.tableLayoutPanel3);
            this.groupBox1.Location = new System.Drawing.Point(262, 3);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(250, 270);
            this.groupBox1.TabIndex = 15;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "良率信息";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.tableLayoutPanel2);
            this.groupBox2.Location = new System.Drawing.Point(518, 3);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(245, 272);
            this.groupBox2.TabIndex = 16;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "登录信息";
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tableLayoutPanel2.AutoSize = true;
            this.tableLayoutPanel2.ColumnCount = 2;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.Controls.Add(this.label25, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.lbOperator, 1, 0);
            this.tableLayoutPanel2.Controls.Add(this.label27, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.lbLineId, 1, 1);
            this.tableLayoutPanel2.Controls.Add(this.label29, 0, 2);
            this.tableLayoutPanel2.Controls.Add(this.lbToolNum, 1, 2);
            this.tableLayoutPanel2.Controls.Add(this.label31, 0, 3);
            this.tableLayoutPanel2.Controls.Add(this.lbFixtureId, 1, 3);
            this.tableLayoutPanel2.Controls.Add(this.label33, 0, 4);
            this.tableLayoutPanel2.Controls.Add(this.lbWorkArea, 1, 4);
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 25);
            this.tableLayoutPanel2.MinimumSize = new System.Drawing.Size(200, 0);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 5;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(236, 239);
            this.tableLayoutPanel2.TabIndex = 11;
            // 
            // label25
            // 
            this.label25.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label25.AutoSize = true;
            this.label25.Location = new System.Drawing.Point(75, 13);
            this.label25.Name = "label25";
            this.label25.Size = new System.Drawing.Size(40, 20);
            this.label25.TabIndex = 0;
            this.label25.Text = "工号:";
            // 
            // lbOperator
            // 
            this.lbOperator.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbOperator.AutoSize = true;
            this.lbOperator.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbOperator.ForeColor = System.Drawing.Color.Black;
            this.lbOperator.Location = new System.Drawing.Point(121, 12);
            this.lbOperator.Name = "lbOperator";
            this.lbOperator.Size = new System.Drawing.Size(35, 22);
            this.lbOperator.TabIndex = 1;
            this.lbOperator.Text = "100";
            // 
            // label27
            // 
            this.label27.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label27.AutoSize = true;
            this.label27.Location = new System.Drawing.Point(75, 60);
            this.label27.Name = "label27";
            this.label27.Size = new System.Drawing.Size(40, 20);
            this.label27.TabIndex = 2;
            this.label27.Text = "线体:";
            // 
            // lbLineId
            // 
            this.lbLineId.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbLineId.AutoSize = true;
            this.lbLineId.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbLineId.ForeColor = System.Drawing.Color.Black;
            this.lbLineId.Location = new System.Drawing.Point(121, 59);
            this.lbLineId.Name = "lbLineId";
            this.lbLineId.Size = new System.Drawing.Size(19, 22);
            this.lbLineId.TabIndex = 3;
            this.lbLineId.Text = "3";
            // 
            // label29
            // 
            this.label29.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label29.AutoSize = true;
            this.label29.Location = new System.Drawing.Point(75, 107);
            this.label29.Name = "label29";
            this.label29.Size = new System.Drawing.Size(40, 20);
            this.label29.TabIndex = 4;
            this.label29.Text = "料号:";
            // 
            // lbToolNum
            // 
            this.lbToolNum.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbToolNum.AutoSize = true;
            this.lbToolNum.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbToolNum.ForeColor = System.Drawing.Color.Black;
            this.lbToolNum.Location = new System.Drawing.Point(121, 106);
            this.lbToolNum.Name = "lbToolNum";
            this.lbToolNum.Size = new System.Drawing.Size(35, 22);
            this.lbToolNum.TabIndex = 5;
            this.lbToolNum.Text = "103";
            // 
            // label31
            // 
            this.label31.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label31.AutoSize = true;
            this.label31.Location = new System.Drawing.Point(47, 154);
            this.label31.Name = "label31";
            this.label31.Size = new System.Drawing.Size(68, 20);
            this.label31.TabIndex = 6;
            this.label31.Text = "治具编号:";
            // 
            // lbFixtureId
            // 
            this.lbFixtureId.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbFixtureId.AutoSize = true;
            this.lbFixtureId.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbFixtureId.ForeColor = System.Drawing.Color.Black;
            this.lbFixtureId.Location = new System.Drawing.Point(121, 153);
            this.lbFixtureId.Name = "lbFixtureId";
            this.lbFixtureId.Size = new System.Drawing.Size(59, 22);
            this.lbFixtureId.TabIndex = 7;
            this.lbFixtureId.Text = "123456";
            // 
            // label33
            // 
            this.label33.Anchor = System.Windows.Forms.AnchorStyles.Right;
            this.label33.AutoSize = true;
            this.label33.Location = new System.Drawing.Point(64, 203);
            this.label33.Name = "label33";
            this.label33.Size = new System.Drawing.Size(51, 20);
            this.label33.TabIndex = 8;
            this.label33.Text = "车间：";
            // 
            // lbWorkArea
            // 
            this.lbWorkArea.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.lbWorkArea.AutoSize = true;
            this.lbWorkArea.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.lbWorkArea.ForeColor = System.Drawing.Color.Black;
            this.lbWorkArea.Location = new System.Drawing.Point(121, 202);
            this.lbWorkArea.Name = "lbWorkArea";
            this.lbWorkArea.Size = new System.Drawing.Size(31, 22);
            this.lbWorkArea.TabIndex = 9;
            this.lbWorkArea.Text = "12 ";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.panel2);
            this.groupBox3.Location = new System.Drawing.Point(769, 3);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(253, 272);
            this.groupBox3.TabIndex = 16;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "B转盘信息";
            // 
            // rtbLog
            // 
            this.rtbLog.BackColor = System.Drawing.Color.White;
            this.rtbLog.Location = new System.Drawing.Point(8, 403);
            this.rtbLog.Name = "rtbLog";
            this.rtbLog.ReadOnly = true;
            this.rtbLog.Size = new System.Drawing.Size(445, 318);
            this.rtbLog.TabIndex = 12;
            this.rtbLog.Text = "";
            // 
            // tabResult
            // 
            this.tabResult.Controls.Add(this.A1TabResult);
            this.tabResult.Controls.Add(this.A2TabResult);
            this.tabResult.Controls.Add(this.B1TabResult);
            this.tabResult.Controls.Add(this.B2TabResult);
            this.tabResult.Controls.Add(this.Sample);
            this.tabResult.Location = new System.Drawing.Point(459, 403);
            this.tabResult.Name = "tabResult";
            this.tabResult.SelectedIndex = 0;
            this.tabResult.Size = new System.Drawing.Size(583, 318);
            this.tabResult.TabIndex = 13;
            // 
            // A1TabResult
            // 
            this.A1TabResult.Controls.Add(this.tableA1Result);
            this.A1TabResult.Location = new System.Drawing.Point(4, 29);
            this.A1TabResult.Name = "A1TabResult";
            this.A1TabResult.Padding = new System.Windows.Forms.Padding(3);
            this.A1TabResult.Size = new System.Drawing.Size(575, 285);
            this.A1TabResult.TabIndex = 0;
            this.A1TabResult.Text = "A1测试结果";
            this.A1TabResult.UseVisualStyleBackColor = true;
            // 
            // tableA1Result
            // 
            this.tableA1Result.AllowUserToAddRows = false;
            this.tableA1Result.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells;
            this.tableA1Result.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tableA1Result.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.A_tableItem,
            this.A_tableValue,
            this.A_tableResult,
            this.A_tableLimitL,
            this.A_tableLimitH,
            this.A_tableUnit});
            this.tableA1Result.Location = new System.Drawing.Point(6, 6);
            this.tableA1Result.Name = "tableA1Result";
            this.tableA1Result.ReadOnly = true;
            this.tableA1Result.RowTemplate.Height = 30;
            this.tableA1Result.Size = new System.Drawing.Size(567, 273);
            this.tableA1Result.TabIndex = 0;
            // 
            // A_tableItem
            // 
            this.A_tableItem.HeaderText = "Item";
            this.A_tableItem.Name = "A_tableItem";
            this.A_tableItem.ReadOnly = true;
            // 
            // A_tableValue
            // 
            this.A_tableValue.HeaderText = "Vaule";
            this.A_tableValue.Name = "A_tableValue";
            this.A_tableValue.ReadOnly = true;
            // 
            // A_tableResult
            // 
            this.A_tableResult.HeaderText = "Result";
            this.A_tableResult.Name = "A_tableResult";
            this.A_tableResult.ReadOnly = true;
            // 
            // A_tableLimitL
            // 
            this.A_tableLimitL.HeaderText = "Limit-L";
            this.A_tableLimitL.Name = "A_tableLimitL";
            this.A_tableLimitL.ReadOnly = true;
            // 
            // A_tableLimitH
            // 
            this.A_tableLimitH.HeaderText = "Limit-H";
            this.A_tableLimitH.Name = "A_tableLimitH";
            this.A_tableLimitH.ReadOnly = true;
            // 
            // A_tableUnit
            // 
            this.A_tableUnit.HeaderText = "Unit";
            this.A_tableUnit.Name = "A_tableUnit";
            this.A_tableUnit.ReadOnly = true;
            // 
            // A2TabResult
            // 
            this.A2TabResult.Controls.Add(this.tableA2Result);
            this.A2TabResult.Location = new System.Drawing.Point(4, 29);
            this.A2TabResult.Name = "A2TabResult";
            this.A2TabResult.Padding = new System.Windows.Forms.Padding(3);
            this.A2TabResult.Size = new System.Drawing.Size(575, 285);
            this.A2TabResult.TabIndex = 2;
            this.A2TabResult.Text = "A2测试结果";
            this.A2TabResult.UseVisualStyleBackColor = true;
            // 
            // tableA2Result
            // 
            this.tableA2Result.AllowUserToAddRows = false;
            this.tableA2Result.AllowUserToDeleteRows = false;
            this.tableA2Result.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells;
            this.tableA2Result.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tableA2Result.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dataGridViewTextBoxColumn1,
            this.dataGridViewTextBoxColumn2,
            this.dataGridViewTextBoxColumn3,
            this.dataGridViewTextBoxColumn4,
            this.dataGridViewTextBoxColumn5,
            this.dataGridViewTextBoxColumn6});
            this.tableA2Result.Location = new System.Drawing.Point(4, 6);
            this.tableA2Result.Name = "tableA2Result";
            this.tableA2Result.ReadOnly = true;
            this.tableA2Result.RowTemplate.Height = 30;
            this.tableA2Result.Size = new System.Drawing.Size(567, 273);
            this.tableA2Result.TabIndex = 1;
            // 
            // dataGridViewTextBoxColumn1
            // 
            this.dataGridViewTextBoxColumn1.HeaderText = "Item";
            this.dataGridViewTextBoxColumn1.Name = "dataGridViewTextBoxColumn1";
            this.dataGridViewTextBoxColumn1.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn2
            // 
            this.dataGridViewTextBoxColumn2.HeaderText = "Vaule";
            this.dataGridViewTextBoxColumn2.Name = "dataGridViewTextBoxColumn2";
            this.dataGridViewTextBoxColumn2.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn3
            // 
            this.dataGridViewTextBoxColumn3.HeaderText = "Result";
            this.dataGridViewTextBoxColumn3.Name = "dataGridViewTextBoxColumn3";
            this.dataGridViewTextBoxColumn3.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn4
            // 
            this.dataGridViewTextBoxColumn4.HeaderText = "Limit-L";
            this.dataGridViewTextBoxColumn4.Name = "dataGridViewTextBoxColumn4";
            this.dataGridViewTextBoxColumn4.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn5
            // 
            this.dataGridViewTextBoxColumn5.HeaderText = "Limit-H";
            this.dataGridViewTextBoxColumn5.Name = "dataGridViewTextBoxColumn5";
            this.dataGridViewTextBoxColumn5.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn6
            // 
            this.dataGridViewTextBoxColumn6.HeaderText = "Unit";
            this.dataGridViewTextBoxColumn6.Name = "dataGridViewTextBoxColumn6";
            this.dataGridViewTextBoxColumn6.ReadOnly = true;
            // 
            // B1TabResult
            // 
            this.B1TabResult.Controls.Add(this.tableB1Result);
            this.B1TabResult.Location = new System.Drawing.Point(4, 29);
            this.B1TabResult.Name = "B1TabResult";
            this.B1TabResult.Padding = new System.Windows.Forms.Padding(3);
            this.B1TabResult.Size = new System.Drawing.Size(575, 285);
            this.B1TabResult.TabIndex = 1;
            this.B1TabResult.Text = "B1测试结果";
            this.B1TabResult.UseVisualStyleBackColor = true;
            // 
            // tableB1Result
            // 
            this.tableB1Result.AllowUserToAddRows = false;
            this.tableB1Result.AllowUserToDeleteRows = false;
            this.tableB1Result.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells;
            this.tableB1Result.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tableB1Result.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.B_tableItem,
            this.B_tableValue,
            this.B_tableResult,
            this.B_tableLimitL,
            this.B_tableLimitH,
            this.B_tableUnit});
            this.tableB1Result.Location = new System.Drawing.Point(6, 6);
            this.tableB1Result.Name = "tableB1Result";
            this.tableB1Result.ReadOnly = true;
            this.tableB1Result.RowTemplate.Height = 30;
            this.tableB1Result.Size = new System.Drawing.Size(567, 273);
            this.tableB1Result.TabIndex = 1;
            // 
            // B_tableItem
            // 
            this.B_tableItem.HeaderText = "Item";
            this.B_tableItem.Name = "B_tableItem";
            this.B_tableItem.ReadOnly = true;
            // 
            // B_tableValue
            // 
            this.B_tableValue.HeaderText = "Vaule";
            this.B_tableValue.Name = "B_tableValue";
            this.B_tableValue.ReadOnly = true;
            // 
            // B_tableResult
            // 
            this.B_tableResult.HeaderText = "Result";
            this.B_tableResult.Name = "B_tableResult";
            this.B_tableResult.ReadOnly = true;
            // 
            // B_tableLimitL
            // 
            this.B_tableLimitL.HeaderText = "Limit-L";
            this.B_tableLimitL.Name = "B_tableLimitL";
            this.B_tableLimitL.ReadOnly = true;
            // 
            // B_tableLimitH
            // 
            this.B_tableLimitH.HeaderText = "Limit-H";
            this.B_tableLimitH.Name = "B_tableLimitH";
            this.B_tableLimitH.ReadOnly = true;
            // 
            // B_tableUnit
            // 
            this.B_tableUnit.HeaderText = "Unit";
            this.B_tableUnit.Name = "B_tableUnit";
            this.B_tableUnit.ReadOnly = true;
            // 
            // B2TabResult
            // 
            this.B2TabResult.Controls.Add(this.tableB2Result);
            this.B2TabResult.Location = new System.Drawing.Point(4, 29);
            this.B2TabResult.Name = "B2TabResult";
            this.B2TabResult.Padding = new System.Windows.Forms.Padding(3);
            this.B2TabResult.Size = new System.Drawing.Size(575, 285);
            this.B2TabResult.TabIndex = 3;
            this.B2TabResult.Text = "B2测试结果";
            this.B2TabResult.UseVisualStyleBackColor = true;
            // 
            // tableB2Result
            // 
            this.tableB2Result.AllowUserToAddRows = false;
            this.tableB2Result.AllowUserToDeleteRows = false;
            this.tableB2Result.AutoSizeRowsMode = System.Windows.Forms.DataGridViewAutoSizeRowsMode.AllCells;
            this.tableB2Result.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tableB2Result.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dataGridViewTextBoxColumn7,
            this.dataGridViewTextBoxColumn8,
            this.dataGridViewTextBoxColumn9,
            this.dataGridViewTextBoxColumn10,
            this.dataGridViewTextBoxColumn11,
            this.dataGridViewTextBoxColumn12});
            this.tableB2Result.Location = new System.Drawing.Point(4, 6);
            this.tableB2Result.Name = "tableB2Result";
            this.tableB2Result.ReadOnly = true;
            this.tableB2Result.RowTemplate.Height = 30;
            this.tableB2Result.Size = new System.Drawing.Size(567, 273);
            this.tableB2Result.TabIndex = 1;
            // 
            // dataGridViewTextBoxColumn7
            // 
            this.dataGridViewTextBoxColumn7.HeaderText = "Item";
            this.dataGridViewTextBoxColumn7.Name = "dataGridViewTextBoxColumn7";
            this.dataGridViewTextBoxColumn7.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn8
            // 
            this.dataGridViewTextBoxColumn8.HeaderText = "Vaule";
            this.dataGridViewTextBoxColumn8.Name = "dataGridViewTextBoxColumn8";
            this.dataGridViewTextBoxColumn8.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn9
            // 
            this.dataGridViewTextBoxColumn9.HeaderText = "Result";
            this.dataGridViewTextBoxColumn9.Name = "dataGridViewTextBoxColumn9";
            this.dataGridViewTextBoxColumn9.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn10
            // 
            this.dataGridViewTextBoxColumn10.HeaderText = "Limit-L";
            this.dataGridViewTextBoxColumn10.Name = "dataGridViewTextBoxColumn10";
            this.dataGridViewTextBoxColumn10.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn11
            // 
            this.dataGridViewTextBoxColumn11.HeaderText = "Limit-H";
            this.dataGridViewTextBoxColumn11.Name = "dataGridViewTextBoxColumn11";
            this.dataGridViewTextBoxColumn11.ReadOnly = true;
            // 
            // dataGridViewTextBoxColumn12
            // 
            this.dataGridViewTextBoxColumn12.HeaderText = "Unit";
            this.dataGridViewTextBoxColumn12.Name = "dataGridViewTextBoxColumn12";
            this.dataGridViewTextBoxColumn12.ReadOnly = true;
            // 
            // Sample
            // 
            this.Sample.Controls.Add(this.lvSample);
            this.Sample.Location = new System.Drawing.Point(4, 29);
            this.Sample.Name = "Sample";
            this.Sample.Size = new System.Drawing.Size(575, 285);
            this.Sample.TabIndex = 4;
            this.Sample.Text = "当班样本记录";
            this.Sample.UseVisualStyleBackColor = true;
            // 
            // lvSample
            // 
            this.lvSample.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeader1,
            this.columnHeader2,
            this.columnHeader3,
            this.columnHeader4,
            this.columnHeader5});
            this.lvSample.Dock = System.Windows.Forms.DockStyle.Fill;
            this.lvSample.Font = new System.Drawing.Font("楷体", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.lvSample.GridLines = true;
            this.lvSample.HideSelection = false;
            this.lvSample.Location = new System.Drawing.Point(0, 0);
            this.lvSample.Margin = new System.Windows.Forms.Padding(2);
            this.lvSample.Name = "lvSample";
            this.lvSample.Size = new System.Drawing.Size(575, 285);
            this.lvSample.TabIndex = 62;
            this.lvSample.UseCompatibleStateImageBehavior = false;
            this.lvSample.View = System.Windows.Forms.View.Details;
            // 
            // columnHeader1
            // 
            this.columnHeader1.Text = "Barcode";
            this.columnHeader1.Width = 137;
            // 
            // columnHeader2
            // 
            this.columnHeader2.Text = "TestType";
            this.columnHeader2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.columnHeader2.Width = 123;
            // 
            // columnHeader3
            // 
            this.columnHeader3.Text = "Time";
            this.columnHeader3.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.columnHeader3.Width = 128;
            // 
            // columnHeader4
            // 
            this.columnHeader4.Text = "FailItems";
            this.columnHeader4.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.columnHeader4.Width = 121;
            // 
            // columnHeader5
            // 
            this.columnHeader5.Text = "Result";
            this.columnHeader5.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // runTime
            // 
            this.runTime.AutoSize = true;
            this.runTime.Location = new System.Drawing.Point(899, 724);
            this.runTime.MinimumSize = new System.Drawing.Size(70, 0);
            this.runTime.Name = "runTime";
            this.runTime.Size = new System.Drawing.Size(70, 20);
            this.runTime.TabIndex = 14;
            this.runTime.Text = "0:0:0";
            // 
            // button7
            // 
            this.button7.AutoSize = true;
            this.button7.Location = new System.Drawing.Point(387, 0);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(75, 30);
            this.button7.TabIndex = 15;
            this.button7.Text = "下料";
            this.button7.UseVisualStyleBackColor = true;
            this.button7.Click += new System.EventHandler(this.button7_Click);
            // 
            // button8
            // 
            this.button8.AutoSize = true;
            this.button8.Location = new System.Drawing.Point(483, 0);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(75, 30);
            this.button8.TabIndex = 16;
            this.button8.Text = "清料";
            this.button8.UseVisualStyleBackColor = true;
            this.button8.Click += new System.EventHandler(this.button8_Click);
            // 
            // MainWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.WhiteSmoke;
            this.ClientSize = new System.Drawing.Size(1046, 750);
            this.Controls.Add(this.button8);
            this.Controls.Add(this.button7);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.runTime);
            this.Controls.Add(this.tabResult);
            this.Controls.Add(this.rtbLog);
            this.Controls.Add(this.lbProgram);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.menuStrip1);
            this.Font = new System.Drawing.Font("微软雅黑", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MainMenuStrip = this.menuStrip1;
            this.Margin = new System.Windows.Forms.Padding(4, 5, 4, 5);
            this.Name = "MainWindow";
            this.Text = "MFLEX";
            this.Load += new System.EventHandler(this.MainWindow_Load);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.tableLayoutPanel1.ResumeLayout(false);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.tableLayoutPanel3.ResumeLayout(false);
            this.tableLayoutPanel3.PerformLayout();
            this.flowLayoutPanel1.ResumeLayout(false);
            this.groupBox4.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.tabResult.ResumeLayout(false);
            this.A1TabResult.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.tableA1Result)).EndInit();
            this.A2TabResult.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.tableA2Result)).EndInit();
            this.B1TabResult.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.tableB1Result)).EndInit();
            this.B2TabResult.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.tableB2Result)).EndInit();
            this.Sample.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        private void TbBBarcode1_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            try {
                if (e.KeyCode == Keys.Return)
                {
                    if (tbBBarcode1.Text.Length > 0)
                    {
                        showLog(tbBBarcode1.Text);
                    }
                    if (tbBBarcode1.Text.Contains("pass,"))
                    {
                        string[] strings = tbBBarcode1.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationB1, int.Parse(strings[1]), 0);
                        }
                    }
                    else if (tbBBarcode1.Text.Contains("fail,"))
                    {
                        string[] strings = tbBBarcode1.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationB1, 0, int.Parse(strings[1]));
                        }
                    }
                    else if (tbBBarcode1.Text.Contains("show"))
                    {
                        foreach (var item in counter.counterData.Keys)
                        {
                            foreach (var item1 in counter.counterData[item].Keys)
                            {
                                //showLog($"sec:{item},node:{item1},value:{counter.counterData[item][item1]}");
                            }
                        }
                    }
                    else if (tbBBarcode1.Text.Contains("plc,"))
                    {
                        string[] strings = tbBBarcode1.Text.Split(',');
                        if (strings.Length >= 4)
                        {
                            if (strings[1] == "write")
                            {
                                testEngine.m_fixturePlc.WriteInt32(int.Parse(strings[2]), int.Parse(strings[3]));
                            }
                            else if (strings[1] == "read")
                            {
                                int iRead = testEngine.m_fixturePlc.ReadInt32(int.Parse(strings[2]));
                                showLog(string.Format("D{0} = {1}", strings[2], iRead));
                            }
                        }
                    }
                    else if (tbBBarcode1.Text.Contains("plcm,"))
                    {
                        string[] strings = tbBBarcode1.Text.Split(',');
                        if (strings.Length >= 4)
                        {
                            if (strings[1] == "write")
                            {
                                testEngine.m_fixturePlc.WriteMRegister(int.Parse(strings[2]), int.Parse(strings[3]) == 1);
                            }
                            else if (strings[1] == "read")
                            {
                                bool[] bRead = testEngine.m_fixturePlc.ReadMRegister(int.Parse(strings[2]), 1);
                                if (bRead == null) { return; }

                                showLog(string.Format("M{0} = {1}", strings[2], bRead[0] ? "1" : "0"));
                            }
                            
                        }
                    }
                    else if (tbBBarcode1.Text.Contains("cont,"))
                    {
                        string[] strings = tbBBarcode1.Text.Split(',');
                        if (strings.Length >= 4)
                        {
                            if (strings[1] == "write")
                            {
                                testEngine.m_mainConPlc.WriteShort(int.Parse(strings[2]), ushort.Parse(strings[3]));
                            }
                            else if (strings[1] == "read")
                            {
                                int iRead = testEngine.m_mainConPlc.ReadShort(int.Parse(strings[2]));
                                showLog(string.Format("D{0} = {1}", strings[2], iRead));
                            }
                        }
                    }
                }
            } catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void TbBBarcode2_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            try { 
                if (e.KeyCode == Keys.Return)
                {
                    if (tbBBarcode2.Text.Length > 0)
                    {
                        showLog(tbBBarcode2.Text);
                    }
                    if (tbBBarcode2.Text == "idel")
                    {
                        lbAStatus1.Text = "IDEL";
                        lbAStatus1.BackColor = Color.Gray;
                        lbAStatus2.Text = "IDEL";
                        lbAStatus2.BackColor = Color.Gray;
                        lbBStatus1.Text = "IDEL";
                        lbBStatus1.BackColor = Color.Gray;
                        lbBStatus2.Text = "IDEL";
                        lbBStatus2.BackColor = Color.Gray;
                        A_AllStatus.Text = "A-IDEL";
                        A_AllStatus.BackColor = Color.Gray;
                        B_AllStatus.Text = "B-IDEL";
                        B_AllStatus.BackColor = Color.Gray;
                    }
                    else if (tbBBarcode2.Text == "test")
                    {
                        lbAStatus1.Text = "TEST";
                        lbAStatus1.BackColor = Color.Yellow;
                        lbAStatus2.Text = "TEST";
                        lbAStatus2.BackColor = Color.Yellow;
                        lbBStatus1.Text = "TEST";
                        lbBStatus1.BackColor = Color.Yellow;
                        lbBStatus2.Text = "TEST";
                        lbBStatus2.BackColor = Color.Yellow;
                        A_AllStatus.Text = "A-TEST";
                        A_AllStatus.BackColor = Color.Yellow;
                        B_AllStatus.Text = "B-TEST";
                        B_AllStatus.BackColor = Color.Yellow;
                    }
                    else if (tbBBarcode2.Text == "pass")
                    {
                        lbAStatus1.Text = "PASS";
                        lbAStatus1.BackColor = Color.Green;
                        lbAStatus2.Text = "PASS";
                        lbAStatus2.BackColor = Color.Green;
                        lbBStatus1.Text = "PASS";
                        lbBStatus1.BackColor = Color.Green;
                        lbBStatus2.Text = "PASS";
                        lbBStatus2.BackColor = Color.Green;
                        A_AllStatus.Text = "A-PASS";
                        A_AllStatus.BackColor = Color.Green;
                        B_AllStatus.Text = "B-PASS";
                        B_AllStatus.BackColor = Color.Green;
                    }
                    else if (tbBBarcode2.Text == "fail")
                    {
                        lbAStatus1.Text = "FAIL";
                        lbAStatus1.BackColor = Color.Red;
                        lbAStatus2.Text = "FAIL";
                        lbAStatus2.BackColor = Color.Red;
                        lbBStatus1.Text = "FAIL";
                        lbBStatus1.BackColor = Color.Red;
                        lbBStatus2.Text = "FAIL";
                        lbBStatus2.BackColor = Color.Red;
                        A_AllStatus.Text = "A-FAIL";
                        A_AllStatus.BackColor = Color.Red;
                        B_AllStatus.Text = "B-FAIL";
                        B_AllStatus.BackColor = Color.Red;
                    }
                    if (tbBBarcode2.Text.Contains("pass,"))
                    {
                        string[] strings = tbBBarcode2.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationB2, int.Parse(strings[1]), 0);
                        }
                    }
                    else if (tbBBarcode2.Text.Contains("fail,"))
                    {
                        string[] strings = tbBBarcode2.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationB2, 0, int.Parse(strings[1]));
                        }
                    }
                    else if (tbBBarcode2.Text == "alarm")
                    {
                        testEngine.m_isAlarm = false;
                    }
                }
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void TbABarcode2_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            try {
                if (e.KeyCode == Keys.Return)
                {
                    if (tbABarcode2.Text.Length > 0)
                    {
                        showLog(tbABarcode2.Text);
                    }

                    if (tbABarcode2.Text == "data1")
                    {
                        List<TestItem> testItems = new List<TestItem>();
                        for (int i = 0; i < 30;  i++)
                        {
                            TestItem item = new TestItem();
                            //item.Name = $"data1_name_{i}";
                            //item.Value = $"value_{i}";
                            //item.Result = i % 3 == 0;
                            //item.Low = $"low_{i}";
                            //item.High = $"high_{i}";
                            //item.Unit = $"unit_{i}";
                            testItems.Add(item);
                        }
                        ShowTestDataList(Station.stationA1, testItems);
                    }
                    else if (tbABarcode2.Text == "data2")
                    {
                        List<TestItem> testItems = new List<TestItem>();
                        for (int i = 0; i < 30; i++)
                        {
                            TestItem item = new TestItem();
                            //item.Name = $"data2_name_{i}";
                            //item.Value = $"value_{i}";
                            //item.Result = i % 3 == 0;
                            //item.Low = $"low_{i}";
                            //item.High = $"high_{i}";
                            //item.Unit = $"unit_{i}";
                            testItems.Add(item);
                        }
                        ShowTestDataList(Station.stationA2, testItems);
                    }
                    else if (tbABarcode2.Text == "data3")
                    {
                        List<TestItem> testItems = new List<TestItem>();
                        for (int i = 0; i < 30; i++)
                        {
                            TestItem item = new TestItem();
                            //item.Name = $"data3_name_{i}";
                            //item.Value = $"value_{i}";
                            //item.Result = i % 3 == 0;
                            //item.Low = $"low_{i}";
                            //item.High = $"high_{i}";
                            //item.Unit = $"unit_{i}";
                            testItems.Add(item);
                        }
                        ShowTestDataList(Station.stationB1, testItems);
                    }
                    else if (tbABarcode2.Text == "data4")
                    {
                        List<TestItem> testItems = new List<TestItem>();
                        for (int i = 0; i < 30; i++)
                        {
                            TestItem item = new TestItem();
                            //item.Name = $"data4_name_{i}";
                            //item.Value = $"value_{i}";
                            //item.Result = i % 3 == 0;
                            //item.Low = $"low_{i}";
                            //item.High = $"high_{i}";
                            //item.Unit = $"unit_{i}";
                            testItems.Add(item);
                        }
                        ShowTestDataList(Station.stationB2, testItems);
                    }
                    if (tbABarcode2.Text.Contains("pass,"))
                    {
                        string[] strings = tbABarcode2.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationA2, int.Parse(strings[1]), 0);
                        }
                    }
                    else if (tbABarcode2.Text.Contains("fail,"))
                    {
                        string[] strings = tbABarcode2.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationA2, 0, int.Parse(strings[1]));
                        }
                    }
                    else if (tbABarcode2.Text.Contains("test,"))
                    {
                        BeginInvoke(new Action(() =>
                        {
                            string[] strings = tbABarcode2.Text.Split(',');
                            if (strings.Length > 1)
                            {
                                if (strings[1] == "start")
                                {
                                    if (strings.Length >= 2)
                                    {
                                        string str1 = "";
                                        string str2 = "";
                                        List<TestItem> item1 = new List<TestItem>();
                                        List<TestItem> item2 = new List<TestItem>();
                                        bool bResult = false;
                                        if (strings[2] == "1")
                                        {
                                            Task task = new Task(() => { str1 = testEngine.m_mcu1.Test(GlobalValue.testCommand); });
                                            task.Start();
                                            Task.WaitAll(task);
                                            item1 = testEngine.AnalysisMcuResult(str1, out bResult);
                                            ShowTestDataList(Station.stationA1, item1);
                                        }
                                        else if (strings[2] == "2")
                                        {
                                            Task task = new Task(() => { str2 = testEngine.m_mcu2.Test(GlobalValue.testCommand); });
                                            task.Start();
                                            Task.WaitAll(task);
                                            item2 = testEngine.AnalysisMcuResult(str2, out bResult);
                                            ShowTestDataList(Station.stationA2, item2);
                                        }
                                        else if (strings[2] == "3")
                                        {
                                            Task task1 = new Task(() => { str1 = testEngine.m_mcu1.Test(GlobalValue.testCommand); });
                                            Task task2 = new Task(() => { str2 = testEngine.m_mcu2.Test(GlobalValue.testCommand); });
                                            task1.Start();
                                            task2.Start();
                                            Task.WaitAll(task1, task2);
                                            item1 = testEngine.AnalysisMcuResult(str1, out bResult);
                                            ShowTestDataList(Station.stationA1, item1);
                                            item2 = testEngine.AnalysisMcuResult(str2, out bResult);
                                            ShowTestDataList(Station.stationA2, item2);
                                        }
                                    }

                                }
                            }
                        }));
                        
                    }
                }
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        private void TbABarcode1_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            try {
                if (e.KeyCode == Keys.Return)
                {
                    if (tbABarcode1.Text.Length > 0)
                    {
                        showLog(tbABarcode1.Text);
                    }
                    if (tbABarcode1.Text.Contains("pass,"))
                    {
                        string[] strings = tbABarcode1.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationA1, int.Parse(strings[1]), 0);
                        }
                    }
                    else if (tbABarcode1.Text.Contains("fail,"))
                    {
                        string[] strings = tbABarcode1.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            UpdateYield(Station.stationA1, 0, int.Parse(strings[1]));
                        }
                    }
                    else if (tbABarcode1.Text == "clear")
                    {
                        rtbLog.Clear();
                    }
                    else if (tbABarcode1.Text.Contains("test,"))
                    {
                        string[] strings = tbABarcode1.Text.Split(',');
                        if (strings.Length > 1)
                        {
                            if (strings[1] == "start")
                            {
                                testEngine.m_bStartTest = true;
                                if (strings.Length >= 2)
                                {
                                    testEngine.m_iType = int.Parse(strings[2]);
                                }
                                else
                                {
                                    testEngine.m_iType = 3;
                                }

                                if (strings.Length >=3)
                                {
                                    testEngine.m_iTurnTable = int.Parse(strings[3]);
                                }
                                else
                                {
                                    testEngine.m_iTurnTable = 1;
                                }
                                showLog("机械手上料完成");
                            }
                            else if (strings[1] == "end")
                            {
                                testEngine.m_bTestEnd = true;
                                showLog("机械手下料完成");
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                showLog(ex.Message, Color.Red);
            }
        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem adminToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem adminLoginToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem adminExitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem modifyToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem settleConfigToolStripMenuItem;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel MCULabel1;
        private System.Windows.Forms.ToolStripStatusLabel MCULabel2;
        private System.Windows.Forms.ToolStripStatusLabel PlcLabel1;
        private System.Windows.Forms.ToolStripStatusLabel PlcLabel2;
        private System.Windows.Forms.Label lbProgram;
        private System.Windows.Forms.Label A_AllStatus;
        private System.Windows.Forms.Label B_AllStatus;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label lbATestTime;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label lbAYield1;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label lbATotal1;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox tbABarcode1;
        private System.Windows.Forms.Label lbAYield2;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label lbATotal2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox tbABarcode2;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label lbBYield2;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label lbBTotal2;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.TextBox tbBBarcode2;
        private System.Windows.Forms.Label lbBTestTime;
        private System.Windows.Forms.Label label20;
        private System.Windows.Forms.Label lbBYield1;
        private System.Windows.Forms.Label label22;
        private System.Windows.Forms.Label lbBTotal1;
        private System.Windows.Forms.Label label24;
        private System.Windows.Forms.TextBox tbBBarcode1;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.Label label35;
        private System.Windows.Forms.Label lbTPass;
        private System.Windows.Forms.Label label37;
        private System.Windows.Forms.Label lbTFail;
        private System.Windows.Forms.Label label39;
        private System.Windows.Forms.Label lbTTotal;
        private System.Windows.Forms.Label label41;
        private System.Windows.Forms.Label lbTYield;
        private System.Windows.Forms.FlowLayoutPanel flowLayoutPanel1;
        private System.Windows.Forms.RichTextBox rtbLog;
        private System.Windows.Forms.TabControl tabResult;
        private System.Windows.Forms.TabPage A1TabResult;
        private System.Windows.Forms.TabPage B1TabResult;
        private System.Windows.Forms.Label runTime;
        private System.Windows.Forms.DataGridView tableA1Result;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableItem;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableValue;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableResult;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableLimitL;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableLimitH;
        private System.Windows.Forms.DataGridViewTextBoxColumn A_tableUnit;
        private System.Windows.Forms.DataGridView tableB1Result;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableItem;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableValue;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableResult;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableLimitL;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableLimitH;
        private System.Windows.Forms.DataGridViewTextBoxColumn B_tableUnit;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.Label lbAStatus1;
        private System.Windows.Forms.Label lbAStatus2;
        private System.Windows.Forms.Label lbBStatus1;
        private System.Windows.Forms.Label lbBStatus2;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.Label label25;
        private System.Windows.Forms.Label lbOperator;
        private System.Windows.Forms.Label label27;
        private System.Windows.Forms.Label lbLineId;
        private System.Windows.Forms.Label label29;
        private System.Windows.Forms.Label lbToolNum;
        private System.Windows.Forms.Label label31;
        private System.Windows.Forms.Label lbFixtureId;
        private System.Windows.Forms.Label label33;
        private System.Windows.Forms.Label lbWorkArea;
        private System.Windows.Forms.ToolStripMenuItem clearYieldToolStripMenuItem;
        private TabPage A2TabResult;
        private TabPage B2TabResult;
        private DataGridView tableA2Result;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn1;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn2;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn3;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn4;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn5;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn6;
        private DataGridView tableB2Result;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn7;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn8;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn9;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn10;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn11;
        private DataGridViewTextBoxColumn dataGridViewTextBoxColumn12;
        private ToolStripMenuItem debugToolStripMenuItem;
        private ToolStripMenuItem fixtureDebug;
        private Button btReset;
        private ToolStripMenuItem commmandTool;
        private ToolStripMenuItem testModeToolStripMenuItem;
        private ToolStripMenuItem oAndOTool;
        private ToolStripMenuItem reTestTool;
        private ToolStripMenuItem sampleTool;
        private Button button1;
        private Button button2;
        private Button button3;
        private Button button4;
        private Button button5;
        private Button button6;
        private Button button7;
        private Button button8;
        private ToolStripMenuItem opmodeToolStripMenuItem;
        private ToolStripMenuItem humenToolStripMenuItem;
        private ToolStripMenuItem autoToolStripMenuItem;
        private TabPage Sample;
        private ListView lvSample;
        private ColumnHeader columnHeader1;
        private ColumnHeader columnHeader2;
        private ColumnHeader columnHeader3;
        private ColumnHeader columnHeader4;
        private ColumnHeader columnHeader5;
    }
}

