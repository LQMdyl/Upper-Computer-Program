using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MFLEX_Compass.UI
{
    public delegate void AdminDelegate(string strUser, string strPwd);
    public partial class Admin : Form
    {
        public event AdminDelegate loginEvent;
        public Admin()
        {
            InitializeComponent();
        }

        private void btCancel_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btLogin_Click(object sender, EventArgs e)
        {
            if (tbUserId.Text.ToLower() == "gts" && tbPassword.Text.ToLower() == "gts")
            {
                MessageBox.Show("登录成功");
                loginEvent(tbUserId.Text, tbPassword.Text);
                this.Close();
            }
            else if (tbUserId.Text.ToLower() == "test" && tbPassword.Text.ToLower() == "abc123")
            {
                MessageBox.Show("启动指令调试模式");
                loginEvent(tbUserId.Text, tbPassword.Text);
                this.Close();
            }
            else
            {
                MessageBox.Show("登录失败");
            }
        }
    }
}
