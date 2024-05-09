using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using MFLEX_Compass.UI;

namespace MFLEX_Compass
{
    public static class Program
    {
        /// <summary>
        /// 应用程序的主入口点。
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            LoginForm form = new LoginForm();
            form.ShowDialog();
            if (form.LoginAble)
            {
                Application.Run(new MainWindow(form.isOperator));
            }
            //Application.Run(new MainWindow());
        }
    }
}
