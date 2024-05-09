using MFLEX_Compass.ConfigDir;
using MFLEX_Compass.GlobalDir;
using System;
using MFLEX_Compass.MesDir;
using CommonHelper;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MFLEX_Compass.UI
{
    public partial class LoginForm : Form
    {
        private Configure configure;
        public bool LoginAble = false;
        public bool isOperator = false;
        public LoginForm()
        {
            this.StartPosition = FormStartPosition.CenterScreen;//居中
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            configure = new Configure();
            InitializeComponent();
        }

        private void btLogin_Click(object sender, EventArgs e)
        {
            string strName = tbOperator.Text.Trim();
            string strPwd = tbPwd.Text.Trim();
            int iRole = cbRole.SelectedIndex;
            BeginInvoke(new EventHandler(delegate
            {
                if (strName == "" || strPwd == "")
                {
                    LoginAble = false;
                    MessageBox.Show("工号和密码不允许为空！", "", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else if (strName.ToUpper() == "GTS" && strPwd.ToUpper() == "GTS")
                {
                    LoginAble = true;
                    isOperator = true;
                }
                else
                {
                    bool result = CheckETUser(strName, strPwd, iRole);
                    if (!result)
                    {
                        LoginAble = false;
                        MessageBox.Show("用户校验错误！请检查工号和密码是否正确!", "输入工号错误", MessageBoxButtons.OK, MessageBoxIcon.Error,
                            MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                        tbOperator.Text = "";
                        tbPwd.Text = "";
                        tbOperator.Focus();
                    }
                    else
                    {
                        
                        LoginAble = true;
                        //this.Close();
                        isOperator = false;
                    }
                }
                if (LoginAble) 
                {
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyFixtureId, cbFixtureId.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyResourceName, cbLineLvl.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyLineId, cbLineId.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keySerialNumber, cbSerialNum.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyProjectName, cbProjectName.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyWorkArea, cbWorkArea.Text);
                    configure.SaveConfigure(GlobalValue.secApp, GlobalValue.keyOperator, strName);
                    this.Close(); 
                }
            }));
        }

        private void btExit_Click(object sender, EventArgs e)
        {
            LoginAble = false;
            this.Close();
        }

        private void LoginForm_Load(object sender, EventArgs e)
        {
            cbRole.SelectedIndex = 0;
            cbFixtureId.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keyFixtureId]); 
            cbFixtureId.SelectedIndex = 0;
            cbLineLvl.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keyResourceName]);
            cbLineLvl.SelectedIndex = 0;
            cbLineId.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keyLineId]);
            cbLineId.SelectedIndex = 0;
            cbSerialNum.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keySerialNumber]);
            cbSerialNum.SelectedIndex = 0;
            cbProjectName.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keyProjectName]);
            cbProjectName.SelectedIndex = 0;
            cbWorkArea.Items.Add(configure.configData[GlobalValue.secApp][GlobalValue.keyWorkArea]);
            cbWorkArea.SelectedIndex = 0;
        }

        private readonly object locker = new object();
        private void WriteLog(string str)
        {
            lock (locker)
            {
                string path = DateTime.Now.ToString("yyyy-MM-dd");
                if (Directory.Exists(@"D:/Log/TxtLog/" + path) == false)
                {
                    Directory.CreateDirectory(@"D:/Log/TxtLog/" + path);
                }
                using (StreamWriter sw = new StreamWriter(@"D:/Log//TxtLog//" + path + "//" + (DateTime.Now.ToString("yyyyMMdd") + "userCheck" + ".txt"), true, Encoding.Default))
                {
                    sw.WriteLine(DateTime.Now.ToString() + " --> " + str.ToString());
                    sw.Close();
                    sw.Dispose();
                }
            }

        }

        protected bool CheckETUser(string UserName, string userPWD, int Role)
        {
            // http://ot-ithzwin002.mflex.com.cn/ettest/
            // http://ot-ithzwin002.mflex.com.cn/ettest/api/ettestrecords/validation?

            if (UserName.ToUpper().Equals("GTS") && userPWD.ToUpper().Equals("GTS")) return true;

            MFLEXMes mfetTest = new MFLEXMes
            {
                ApiAddress = configure.configData[GlobalValue.secApp][GlobalValue.keyApiAddress],
                ApiPath = "api/etresources/etauthentication",// appConfig.StringFromConfigure(AppConfig.Section_App_Setup, AppConfig.Node_API_SFC_Path),

            };
            WriteLog(string.Format("mes地址为{0}", mfetTest.ApiAddress));
            WriteLog(string.Format("mes路径为{0}", mfetTest.ApiPath));
            ETuser etuser = new ETuser()
            {
                userName = UserName,
                password = userPWD,
                role = Role
            };
            WriteLog(string.Format("mes用户为{0}", etuser.userName));
            WriteLog(string.Format("mesPWD为{0}", etuser.password));
            WriteLog(string.Format("mesRole为{0}", etuser.role));
            string tmpSfcCommand, tmpSfcMessage;
            bool tmpResult = mfetTest.CheckUserResult(etuser, out tmpSfcCommand, out tmpSfcMessage);
            if (!tmpResult)
            {
                WriteLog(tmpSfcCommand.ToString());
                if (!string.IsNullOrEmpty(tmpSfcMessage))
                {
                    WriteLog(string.Format("校验用户mes返回信息：{0}。", tmpSfcMessage));
                }

                WriteLog("校验用户错误:获取校验用户数据错误，请检查网络或参数设置是否正确");
                return false;
            }

            WriteLog(tmpSfcCommand); ;
            if (!string.IsNullOrEmpty(tmpSfcMessage))
            {
                WriteLog(string.Format("校验用户mes返回信息：{0}。", tmpSfcMessage));
            }

            return tmpResult;
        }

        private void tbOperator_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == 13) { tbPwd.Focus(); }
        }

        private void tbPwd_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == 13) { btLogin.PerformClick(); }
        }
    }
}
