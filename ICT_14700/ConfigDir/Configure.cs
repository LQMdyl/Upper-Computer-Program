using CommonHelper.FileParser;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MFLEX_Compass.ConfigDir
{
    public class Configure
    {
        private static Configure _instance;
        private readonly object locker = new object();
        private readonly string path = @"D:/Configure/config.ini";
        private readonly IniParser iniParser = new IniParser();
        public readonly Dictionary<string, Dictionary<string, string>> configData = new Dictionary<string, Dictionary<string, string>>();

        public static Configure Instance
        {
            get { return _instance ?? (_instance = new Configure()); }
        }
        public Configure() 
        {
            LoadAppConfigure();
        }

        public bool LoadAppConfigure()
        {
            if (!File.Exists(path))
            {
                MessageBox.Show(string.Format(@"配置文件{0}不存在。\n", path), "配置文件错误", MessageBoxButtons.OK, MessageBoxIcon.Error, MessageBoxDefaultButton.Button1, MessageBoxOptions.DefaultDesktopOnly);
                return false;
            }

            configData.Clear();
            List<string> configSections = iniParser.ReadSections(path);
            foreach (string section in configSections)
            {
                Dictionary<string, string> tmpSectionData = iniParser.ReadSection(path, section);
                if (tmpSectionData == null) continue;

                configData.Add(section, tmpSectionData);
            }

            return configData != null && configData.Count > 0;
        }

        public int IntFromConfigure(string section, string node)
        {
            try
            {
                if (!configData.Keys.Contains(section) || !configData[section].ContainsKey(node)) return -99999999;

                string tmpData = configData[section][node];
                int tmpIntValue = -99999999;

                if (!int.TryParse(tmpData, out tmpIntValue)) return -99999999;

                return tmpIntValue;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
                return -99999999;
            }
        }

        public double DoubleFromConfigure(string section, string node)
        {
            try
            {
                if (!configData.Keys.Contains(section) || !configData[section].ContainsKey(node)) return -99999999.0;

                string tmpData = configData[section][node];
                double tmpDoubleValue = -99999999.0;

                if (!double.TryParse(tmpData, out tmpDoubleValue)) return -99999999.0;

                return tmpDoubleValue;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
                return -99999999.0;
            }
        }

        public string StringFromConfigure(string section, string node)
        {
            try
            {
                if (!configData.Keys.Contains(section) || !configData[section].ContainsKey(node)) return "";

                string tmpData = configData[section][node];

                return tmpData ?? "";
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
                return "";
            }
        }

        public bool BoolFromConfigure(string section, string node)
        {
            try
            {
                if (!configData.Keys.Contains(section) || !configData[section].ContainsKey(node)) return false;

                string tmpData = configData[section][node];

                bool tmpBoolValue = false;
                if (!bool.TryParse(tmpData, out tmpBoolValue)) return false;

                return tmpBoolValue;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
                return false;
            }
        }

        public bool SaveConfigure(string section, string node, string value)
        {
            lock (locker)
            {
                if (string.IsNullOrEmpty(section) || string.IsNullOrEmpty(node)) return false;

                value = string.IsNullOrEmpty(value) ? "" : value;

                if (!configData.ContainsKey(section))
                {
                    configData.Add(section, new Dictionary<string, string>() { { node, value } });
                }
                else
                {
                    if (configData[section].ContainsKey(node))
                    {
                        configData[section][node] = value;
                    }
                    else
                    {
                        configData[section].Add(node, value);
                    }
                }

                return iniParser.Write(path, section, node, value);
            }
        }
    }
}
