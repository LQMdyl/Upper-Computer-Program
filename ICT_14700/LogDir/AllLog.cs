using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Forms.VisualStyles;
using CommonHelper;

namespace MFLEX_Compass.LogDir
{
    public class AllLog : FileBase
    {
        public string path { set; get; }
        private readonly object obj;
        public AllLog()
        {
            obj = new object();
        }

        public bool writeTxtLog(string strContent)
        {
            try 
            {
                lock (obj)
                {
                    FileName = path;
                    if (!DirectoryExist()) { CreateDirectory(); }
                    if (!FileExist()) {CreateFile(""); }
                    string data = string.Format("[{0:yyyy-MM-dd HH:mm:ss.fff}] {1}", DateTime.Now, strContent ?? "");
                    return WriteFile(data, true);
                }
            } 
            catch 
            { 
                return false;
            }
        }

        public bool writeCsvLog(string strContent, string strTitle)
        {
            try
            {
                lock (obj)
                {
                    FileName = path;
                    if (FileExist())
                    {
                        return WriteFile(strContent, true);
                    }
                    else
                    {
                        return WriteFile(strTitle + "\n" + strContent, true);
                    }
                }
            }
            catch
            {
                return false;
            }
        }

        public void setDir(string dir) 
        {
            DirPath = string.IsNullOrEmpty(dir) ? Application.StartupPath + "/csvLog" : dir;
            CreateDirectory();
        }
    }
}
