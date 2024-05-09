import os
import logging
import datetime
import shutil

class cTxtLog():
    def __init__(self, name):
        self.name = name
        self.path = 'D:/Log/txtLog/'
        if not os.path.exists('D:/'):
            self.path = '/vault/Log/testLog'

        if not os.path.exists("D:/Log/txtLog"):
            os.makedirs("D:/Log/txtLog")

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.DEBUG)
        dtPath = self.path + str(datetime.date.today())
        if not os.path.exists(dtPath):
            os.makedirs(dtPath)
        fileName = dtPath + '/' + self.name
        handler = logging.FileHandler(fileName + '.txt')
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def writeError(self, text):
        self.logger.error(text)

    def writeWarning(self, text):
        self.logger.warning(text)

    def writeInfo(self, text):
        self.logger.info(text)

    def writeDebug(self, text):
        self.logger.debug(text)

    def OverdueLog(self, Days=int):
        TmpPath=self.path+'/'
        files = os.listdir(TmpPath)
        dirlist = []
        for file in files:
            if os.path.isdir(TmpPath+ file):
                dirlist.append(file)
        Curdt = datetime.date.today()
        if len(dirlist) > 0:
            for dirResult in dirlist:
                if (Curdt - (datetime.datetime.strptime(dirResult, '%Y-%m-%d')).date()).days >= Days:
                    shutil.rmtree(TmpPath + dirResult)

