import configparser
import os
from glob import glob
from pathlib import Path


import GlobalGui


class cTestItemName():
    ConfigureDic: glob = {}

    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.filePath = 'E:/Configure'
            # if not os.path.exists(self.filePath):
            #     os.mkdir(self.filePath)
            if not os.path.exists( self.filePath ):
                self.filePath = '/vault/Configure'
            self.fileName ="TestName.ini"
            self.configFile = os.path.join(self.filePath, self.fileName)
            self.ConfigurePath = "{0}/{1}".format( self.filePath, self.fileName )
        except Exception as e:
            print(e)
            raise e


    def LoadConfiogure(self):
        myfile = Path(self.ConfigurePath)
        if not myfile.is_file(): return "文件不存在！请检查配置文件是否存在"

        self.config.read(self.ConfigurePath)
        for num in self.config:
            Tmp: dict = dict()
            for Key in self.config[num]:
                Tmp[Key] = self.config[num][Key]
            self.ConfigureDic[num] = Tmp

        return "加载配置文件成功"

    def SaveConfigure(self, section, Key, Value):
        try:
            self.config.set(section, Key, Value)
            self.config.write( open(self.ConfigurePath, "w"))
            self.LoadConfiogure()
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit('保存配置文件失败 - ' + str(e), 'red', False)

    def ReadValue(self,section,key):
        try:
            if section not in self.ConfigureDic.keys():
                return ""
            if key not in self.ConfigureDic[section].keys():
                return ""

            return self.ConfigureDic[section][key]
            pass
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit('读取配置文件失败 - ' + str(e), 'red', False)