using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MFLEX_Compass.ConfigDir;

namespace MFLEX_Compass.UI
{
    public partial class SettleConfig : Form
    {
        public static Configure configure = new Configure();
        public showLog updataLog;
        public SettleConfig()
        {
            InitializeComponent();
        }

        private void btSave_Click(object sender, EventArgs e)
        {
            try 
            {
                DataGridViewRowCollection rowCollection = dgvSettleConfig.Rows;
                for (int i = 0;  i < rowCollection.Count - 1; i++) {
                    //if (rowCollection[i].Cells[1].Value != null)
                    {
                        string strSec = rowCollection[i].Cells[0].Value.ToString();
                        string strKey = rowCollection[i].Cells[1].Value.ToString();
                        string strValue = rowCollection[i].Cells[2].Value.ToString();
                        configure.SaveConfigure(strSec, strKey, strValue);
                    }
                }
                MessageBox.Show("保存成功","程序配置保存提示");
            }
            catch (Exception ex)
            {
                MessageBox.Show(string.Format("保存失败：{0}", ex.Message), "程序配置保存提示");
            }
        }

        private void SettleConfig_Load(object sender, EventArgs e)
        {
            foreach (string strSec in configure.configData.Keys) 
            {
                foreach (string strKey in configure.configData[strSec].Keys)
                {
                    string[] strTemp = { strSec, strKey, configure.configData[strSec][strKey] };
                    dgvSettleConfig.Rows.Add(strTemp);
                }
            }
        }
    }
}
