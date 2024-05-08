import configparser
import os
import socket

from GlobalDir.GlobalGui import global_Gui
from GlobalDir import GlobalConf
from ConfigureDir import ConfigureKey
from glob import glob
import re


class cConfigure():
    ConfigureDic: glob = {}
    def __init__(self):
        self.path = os.getcwd() + '/config/config.ini'
        if not os.path.exists(self.path):
            self.path = '/vault/Configure/config.ini'
            if not os.path.exists(self.path):
                global_Gui.tbvwLogEmit('配置文件不存在', GlobalConf.colorRed, False)
                return
        self.conf = configparser.ConfigParser()
        self.BarcodeRules = dict()
        if len(self.ConfigureDic) <= 0:
            self.loadConfigure()

    def saveConfigure(self, section, option, value):
        try:
            if not os.path.exists(self.path):
                global_Gui.tbvwLogEmit('文件路径不存在', GlobalConf.colorRed, False)
                return False
            self.conf.read(self.path, encoding='utf-8')
            if not self.conf.has_section(section):
                self.conf.add_section(section)
            self.conf.set(section, option, value)
            self.conf.write(open(self.path, 'w'))
            self.loadConfigure()
        except Exception as e:
            global_Gui.tbvwLogEmit(e, GlobalConf.colorRed, False)


    def getConfigure(self, section, option):
        try:
            if not os.path.exists(self.path):
                global_Gui.tbvwLogEmit('文件路径不存在', GlobalConf.colorRed, False)
                return ''
            self.conf.read(self.path, encoding='utf-8')
            if not self.conf.has_section(section):
                global_Gui.tbvwLogEmit('节点不存在', GlobalConf.colorRed, False)
                return ''
            if not self.conf.has_option(section, option):
                global_Gui.tbvwLogEmit('键不存在', GlobalConf.colorRed, False)
                return ''
            return self.conf.get(section, option)
        except Exception as e:
            global_Gui.tbvwLogEmit(e, GlobalConf.colorRed, False)

    def loadConfigure(self):
        try:
            if not os.path.exists(self.path):
                return False, '文件路径不存在'
            self.conf.read(self.path, encoding='utf-8')
            for sec in self.conf:
                temp: dict = dict()
                for opt in self.conf[sec]:
                    temp[opt] = self.conf[sec][opt]
                self.ConfigureDic[sec] = temp
        except Exception as e:
            return False, str(e)


    def loadBarcodeConfigure(self):
        try:
            self.barcodePath = os.getcwd() + '/config/BarcodeRuleConfig.ini'
            if not os.path.exists(self.barcodePath):
                self.barcodePath = '/vault/Configure/BarcodeRuleConfig.ini'
                if not os.path.exists(self.barcodePath):
                    global_Gui.tbvwLogEmit('条码规则文件不存在', GlobalConf.colorRed)
                    return
            conf = configparser.ConfigParser()
            conf.read(self.barcodePath, encoding='utf-8')
            for sec in conf:
                temp: dict = dict()
                for opt in conf[sec]:
                    temp[opt] = conf[sec][opt]
                self.BarcodeRules[sec] = temp
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed, False)

    def Equal(self, barcode):
        tmplist = [[],[],[]]
        equalResult = False
        if len(self.BarcodeRules) == 0 or barcode == '':
            return False,tmplist
        for sec in self.BarcodeRules:
            temp: dict = sec
            tmpBarcodeRule = str(temp[ConfigureKey.KEY_BARCODE_RULE])
            if len(tmpBarcodeRule) != len(barcode):
                return False, tmplist
            tmpStr = '^{0}$'.format(tmpBarcodeRule.replace('$', '.'))
            tmpgroup = re.match(tmpStr, barcode)
            if tmpgroup != None:
                tmplist[0].append(str(temp[ConfigureKey.KEY_VENDOR]))
                tmplist[1].append(str(temp[ConfigureKey.KEY_COMMAND]))
                tmplist[2].append(f'Vendor:{temp[ConfigureKey.KEY_VENDOR]}, Barcode Rule:{temp[ConfigureKey.KEY_BARCODE_RULE]}, Miccode Rule:{temp[ConfigureKey.KEY_MIC_RULE]}')
                equalResult = True
        return equalResult, tmplist

    def getLocalIP(self):
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            IP = st.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            st.close()
        return IP

class cUseCount():
    UseCountDic:glob = {}
    def __init__(self):
        self.path = os.getcwd() + '/config/UseCount.ini'
        if not os.path.exists(self.path):
            self.path = '/vault/Configure/UseCount.ini'
            if not os.path.exists(self.path):
                global_Gui.tbvwLogEmit('使用计数文件不存在', GlobalConf.colorRed, False)
                return
        self.conf = configparser.ConfigParser()
        if len(self.UseCountDic) <= 0:
            self.loadConfigure()

    def loadConfigure(self):
        try:
            if not os.path.exists(self.path):
                return False, '文件路径不存在'
            self.conf.read(self.path, encoding='utf-8')
            for sec in self.conf:
                temp: dict = dict()
                for opt in self.conf[sec]:
                    temp[opt] = self.conf[sec][opt]
                self.UseCountDic[sec] = temp
        except Exception as e:
            return False, str(e)

    def saveConfigure(self, section, option, value):
        try:
            if not os.path.exists(self.path):
                global_Gui.tbvwLogEmit('文件路径不存在', GlobalConf.colorRed, False)
                return False
            self.conf.read(self.path, encoding='utf-8')
            if not self.conf.has_section(section):
                self.conf.add_section(section)
            self.conf.set(section, option, value)
            self.conf.write(open(self.path, 'w'))
            self.loadConfigure()
        except Exception as e:
            global_Gui.tbvwLogEmit(e, GlobalConf.colorRed, False)