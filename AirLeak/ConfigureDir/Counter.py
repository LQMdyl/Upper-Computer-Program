import configparser
import os


class cCounter():
    def __init__(self):
        try:
            self.filePath = os.getcwd() + '/config'
            # if not os.path.exists(self.filePath):
            #     os.mkdir(self.filePath)
            if not os.path.exists( self.filePath ):
                self.filePath='/vault/Configure'

            self.fileName = 'Counter.ini'
            self.configFile = os.path.join(self.filePath, self.fileName)
            self.config = configparser.ConfigParser()
            self.config.read(self.configFile)
        except Exception as e:
            print(e)
            raise e

    def ReadSecs(self):
        secs = self.config.sections()
        return secs

    def ReadKey(self, sec):
        keys = self.config.options(sec)
        return keys

    def ReadItem(self, sec):
        item = self.config.items(sec)
        return item

    def ReadValue(self, sec, key):
        value = self.config.get(sec, key)
        return value

    def WriteSec(self, sec, key, value):
        try:
            if not self.config.has_section(sec):
                self.config.add_section(sec)
                self.config.write(open(self.configFile, 'w'))
                return True
            return False
        except Exception as e:
            print(e)
            raise e


    def WriteValue(self, sec, key, value):
        try:
            if self.config.has_section(sec):
                if self.config.has_option(sec, key):
                    self.config.set(sec, key, value)
                    self.config.write(open(self.configFile, "w"))
                    return  True
            return False
        except Exception as e:
            print(e)
            raise e