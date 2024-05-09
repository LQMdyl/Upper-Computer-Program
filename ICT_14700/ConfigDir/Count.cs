using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;
using CommonHelper.FileParser;
using MFLEX_Compass.UI;
using Newtonsoft.Json.Linq;
//using System.Collections.Specialized.BitVector32;

namespace MFLEX_Compass.ConfigDir
{
    public class Count
    {
        public static Count _instance;
        private readonly object locker = new object();
        private readonly object clearLock = new object();
        private readonly string path = @"D:/Configure/Counter.ini";
        private readonly IniParser iniParser = new IniParser();
        public readonly Dictionary<string, Dictionary<string, string>> counterData = new Dictionary<string, Dictionary<string, string>>();
        public showLog updateLog;
        public static Count Instance()
        {
            return _instance ?? (_instance = new Count());
        }

        public Count()
        {
            LoadCounter();
        }

        public bool LoadCounter()
        {
            if (!File.Exists(path))
            {
                MessageBox.Show(string.Format(@"配置文件{0}不存在。\n", path), "配置文件错误", MessageBoxButtons.OK, MessageBoxIcon.Error, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                return false;
            }

            counterData.Clear();
            List<string> configSections = iniParser.ReadSections(path);
            foreach (string section in configSections)
            {
                Dictionary<string, string> tmpSectionData = iniParser.ReadSection(path, section);
                if (tmpSectionData == null)
                    continue;

                counterData.Add(section, tmpSectionData);
            }

            return true;
        }

        public bool SaveCounter(string section, string node, string value)
        {
            lock (locker)
            {
                if (string.IsNullOrEmpty(section) || string.IsNullOrEmpty(node) || string.IsNullOrEmpty(value)) return false;

                value = value ?? "";

                if (!counterData.ContainsKey(section))
                {
                    counterData.Add(section, new Dictionary<string, string> { { node, value } });
                }
                else
                {
                    if (counterData[section].ContainsKey(node))
                    {
                        counterData[section][node] = value;
                    }
                    else
                    {
                        counterData[section].Add(node, value);
                    }
                }
                return iniParser.Write(path, section, node, value);
            }
        }

        public bool ClearCounter()
        {
            try
            {
                lock (clearLock)
                {
                    string strValue = "100";
                    foreach (string strSec in counterData.Keys)
                    {
                        foreach (string strKey in counterData[strSec].Keys)
                        {
                            if (strKey == "yield")
                            {
                                strValue = "100";
                            }
                            else
                            {
                                strValue = "0";
                            }
                            iniParser.Write(path, strSec, strKey, strValue);
                        }
                    }
                    return true;
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
                return false;
            }
        }
    }
}
