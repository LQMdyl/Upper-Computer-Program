import configparser
import os
from glob import glob
from pathlib import Path

from GlobalDir.GlobalGui import global_Gui


class cLimit():
    ConfigureDic: glob = {}

    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.ConfigurePath = os.getcwd() + '/config/Limit.ini'
            if not os.path.exists(self.ConfigurePath):
                self.ConfigurePath = '/vault/Configure/Limit.ini'
                if not os.path.exists(self.ConfigurePath):
                    global_Gui.tbvwLogEmit('Limit配置文件不存在', 'red', False)
                    return
            if len(self.ConfigureDic) <= 0:
                self.LoadConfiogure()
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red', False)


    def LoadConfiogure(self):
        try:
            myfile = Path(self.ConfigurePath)
            if not myfile.is_file(): return False

            self.config.read(self.ConfigurePath)
            for num in self.config:
                Tmp: dict = dict()
                for Key in self.config[num]:
                    Tmp[Key] = self.config[num][Key]
                self.ConfigureDic[num] = Tmp
            return True
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red')
            return False


    def SaveConfigure(self, section, Key, Value):
        try:
            self.config.set(section, Key, Value)
            self.config.write( open(self.ConfigurePath, "w"))
            self.LoadConfiogure()
        except Exception as e:
            global_Gui.tbvwLogEmit('保存配置文件失败 - ' + str(e), 'red', False)

    def ReadValue(self,section,key):
        try:
            if section not in self.ConfigureDic.keys():
                return ""
            if key not in self.ConfigureDic[section].keys():
                return ""

            return self.ConfigureDic[section][key]
        except Exception as e:
            global_Gui.tbvwLogEmit( '读取配置文件失败 - ' + str( e), 'red', False)