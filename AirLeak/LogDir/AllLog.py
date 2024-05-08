import os
import shutil
from datetime import datetime, timedelta
from GlobalDir import GlobalConf
from GlobalDir.GlobalGui import global_Gui
from ConfigureDir import ConfigureKey
from ConfigureDir.Configure import cConfigure
from TestDir.TestItem import cTestItem
import csv
import  pathlib
import logging


class cAllLog():
    def __init__(self, filename):
        try:
            self.conf = cConfigure()
            print('run into log init')
            self.dataPath = self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_DATA_PATH]
            if not os.path.exists(self.dataPath):
                os.mkdir(self.dataPath)
            self.logpath = self.conf.ConfigureDic[ConfigureKey.SEC_APP][ConfigureKey.KEY_LOG]
            if not os.path.exists(self.logpath):
                os.mkdir(self.logpath)
            dtPath = self.logpath + '/' + str(datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(dtPath):
                os.mkdir(dtPath)
            self.filename = filename
            self.logname = dtPath + '/' + self.filename + '.txt'
        except Exception as e:
            print(str(e)+'func:log init')


    def writelog(self, content: str = '', msglvl: str = 'INFO'):
        try:
            if self.logpath == '':
                global_Gui.tbvwLogEmit('文件路径不存在!', GlobalConf.colorRed)
                return
            else:
                with open(self.logname, 'a+') as fg:
                    #writeContent = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + content + '\n'
                    writeContent = '[{0}] - {1} - {2}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msglvl, content)
                    fg.write(writeContent)
        except Exception as e:
            global_Gui.tbvwLogEmit('写log失败' + str(e), GlobalConf.colorRed, False)

    def clearlog(self):
        if os.path.exists(self.logname):
            with open(self.logname, 'a+') as fg:
                fg.truncate(0)

    def writeAllLog(self, text = str, txtlog = bool, color = str, txtMode = bool, filelog = bool, msglvl: str = 'INFO'):
        if txtlog:
            global_Gui.tbvwLogEmit(text, color, txtMode)
        if filelog:
            self.writelog(text, msglvl)

class cFileLog():
    def __init__(self, name: str):
        if name == '':
            self.path = '/vault/data/'
        else:
            if not name.endswith('/') or name.endswith('\\'):
                self.path = name + '/'
            else:
                self.path = name
    def writeMFLEXTestCsv(self, isPcs: bool, guid: str, sn: str, result: bool, module: str,
                     startTime: datetime, endTime: datetime, testType: str, partNumber: str,
                     localIP: str, testItems: list, fixtureID: str, projectName: str, program: str,
                     version: str, user: str, plateID: str, product: str, entendedSeriaNumber: str,
                    lotNumber: str):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)

            failList = ''
            tmpTimeStamp = str(int(datetime.now().timestamp() * 1000))
            tmpTestResult = result and 'PASS' or 'FAIL'
            date = int(datetime.now().strftime('%H'))
            DorN = (date >= 7 and date < 19) and 'D' or 'N'
            testd = DorN == 'D' and endTime.strftime('%Y%m%d') or (endTime + timedelta(days=-1)).strftime('%Y%m%d')
            tmpLocalName = isPcs and '{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}{8}_{9}.csv'.format(partNumber,
                                                                                         sn, guid, localIP, testType, fixtureID,
                                                                                         tmpTestResult, projectName,
                                                                                         testType, DorN) or  ('{0}'
                                                                                                              '_{1}_{2}_{3}_{4}_{5}_{6}_{7}.csv').format(projectName,
                                                                                                                                                                  fixtureID, program.replace("-", "_"),
                                                                                                                                                                  testd, localIP, "GTS", testType, DorN)
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            filename = self.path + tmpLocalName
            fileapp = pathlib.Path(filename)
            writeTitle = not fileapp.is_file()
            firstLine = ['Test']
            title = ['Product','SerialNumber','ExtendedSerialNumber',
                     'Special Build Name','Special Build Description',
                     'Unit Number','Lot Number','Test Name',
                     'Subtest Name','Station ID',
                     'Test Pass/Fail Status','StartTime','EndTime',
                     'List Of Failing Tests','Version']
            displayName = ['Display Name ----->','','','','','','','','','','','','','','']
            PDCAPriority = ['PDCA Priority ----->','','','','','','','','','','','','','','']
            lowLimit = ['Lower Limit----->','','','','','','','','','','','','','','']
            upperLimit = ['Upper Limit----->','','','','','','','','','','','','','','']
            unit = ['Measurement Unit----->','','','','','','','','','','','','','','']
            testValue = []

            for num in testItems:
                tmpTestItem:cTestItem = num
                title.append(tmpTestItem.TestName)
                displayName.append(tmpTestItem.TestDisplayName)
                PDCAPriority.append(tmpTestItem.TestPDCAPriority)
                upperLimit.append(tmpTestItem.TestUpLimit)
                lowLimit.append(tmpTestItem.TestLowLimit)
                unit.append(tmpTestItem.TestUnit)
                if not tmpTestItem.TestResult:
                    failList += tmpTestItem.TestName
                testValue.append(tmpTestItem.TestValue)

            value = [product, sn, entendedSeriaNumber, '', '', '', lotNumber, 'MIC_TEST', '', fixtureID,
                         result and 'PASS' or 'FAIL', startTime.strftime('%Y/%m/%d %H:%M:%S'),
                         endTime.strftime('%Y/%m/%d %H:%M:%S'), failList, version]

            with open(filename, 'a', newline='') as fr:
                write = csv.writer(fr)
                if writeTitle:
                    write.writerow(firstLine)
                    write.writerow(title)
                    write.writerow(displayName)
                    write.writerow(PDCAPriority)
                    write.writerow(upperLimit)
                    write.writerow(lowLimit)
                    write.writerow(unit)

                for tmp in testValue:
                    tmplist = value
                    tmplist.append(tmp)
                    write.writerow(tmplist)
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit('保存数据文件失败!' + str(e), GlobalConf.colorRed)
            return False

    def uploadFLEXIUMTestCsv(self, tickets:str,barcode:str, testResult: bool, testTime:datetime, testItems:list, localIp:str):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '\\'

            startTime = testTime.strftime('%Y/%m/%d %H:%M:%S')
            testDay = testTime.strftime('%Y-%m-%d')
            tmpResult = testResult and 'PASS' or 'FAIL'
            content = [tickets, barcode, tmpResult, startTime]
            filename = f'{self.path}{tickets}_{testDay}.csv'

            with open(filename, 'a', newline='') as fr:
                write = csv.writer(fr)
                for tmp in testItems:
                    item:cTestItem = tmp
                    tmpContent = content
                    tmpContent.append(f'{localIp};TestValue:{item.TestValue}')
                    write.writerow(tmpContent)
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit('保存数据文件失败!' + str(e), GlobalConf.colorRed)
            return False

    def localFLEXIUMTestCsv(self, operator: str, productType: str, workOrder:str,barcode:str, testResult:bool, startTime:datetime, testItems:list):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            title = ['OpNumber', 'ProductType', 'WorkOrder', 'Barcode', 'TestResult', 'StartTime', 'TestValve', 'Bay', 'CT']
            displayName = ['USL', '', '', '', '', '']
            PDCAPriority = ['LSL', '', '', '', '', '']
            testValue = []
            for num in testItems:
                tmpTestItem:cTestItem = num
                testValue.append(tmpTestItem.TestValue)
                displayName.append(tmpTestItem.TestUpLimit)
                PDCAPriority.append(tmpTestItem.TestLowLimit)
            tmpResult = testResult and 'PASS' or 'FAIL'
            tmpStartTime = startTime.strftime('%Y/%m/%d %H:%M:%S')
            tmpDate = startTime.strftime('%Y-%m-%d')
            value = [operator, productType, workOrder, barcode, tmpResult,tmpStartTime]
            filename = f'{self.path}{tmpDate}.csv'
            fileapp = pathlib.Path(filename)
            writeTitle = not fileapp.is_file()
            with open(filename, 'a', newline='') as fr:
                write = csv.writer(fr)
                if writeTitle:
                    write.writerow(title)
                    write.writerow(displayName)
                    write.writerow(PDCAPriority)

                for tmp in testValue:
                    tmplist = value
                    tmplist.append(tmp)
                    tmplist.append('Bay:1')
                    tmplist.append('55')
                    write.writerow(tmplist)
            return True
        except Exception as e:
            global_Gui.tbvwLogEmit('保存本地数据文件失败', GlobalConf.colorRed)

    def writeAVARYTestCsv(self, isPcs: bool, guid: str, sn: str, result: bool, module: str,
                     startTime: datetime, endTime: datetime, testType: str, partNumber: str,
                     localIP: str, testItems: list, fixtureID: str, projectName: str, program: str,
                     version: str, user: str, plateID: str, product: str, entendedSeriaNumber: str,
                    lotNumber: str):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)

            failList = ''
            tmpTimeStamp = str(int(datetime.now().timestamp() * 1000))
            tmpTestResult = result and 'PASS' or 'FAIL'
            date = int(datetime.now().strftime('%H'))
            DorN = (date >= 7 and date < 19) and 'D' or 'N'
            testd = DorN == 'D' and endTime.strftime('%Y%m%d') or (endTime + timedelta(days=-1)).strftime('%Y%m%d')
            tmpLocalName = '{0}.csv'.format(startTime.strftime('%Y-%m-%d'))
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            filename = self.path + tmpLocalName
            fileapp = pathlib.Path(filename)
            writeTitle = not fileapp.is_file()
            firstLine = ['Test']
            title = ['Product', 'SerialNumber', 'ExtendedSerialNumber',
                     'Special Build Name', 'Special Build Description',
                     'Unit Number', 'Lot Number', 'Test Name',
                     'Subtest Name', 'Station ID',
                     'Test Pass/Fail Status', 'StartTime', 'EndTime',
                     'List Of Failing Tests', 'Version']
            displayName = ['Display Name ----->', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            PDCAPriority = ['PDCA Priority ----->', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            lowLimit = ['Lower Limit----->', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            upperLimit = ['Upper Limit----->', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            unit = ['Measurement Unit----->', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            testValue = []

            for num in testItems:
                tmpTestItem: cTestItem = num
                title.append(tmpTestItem.TestName)
                displayName.append(tmpTestItem.TestDisplayName)
                PDCAPriority.append(tmpTestItem.TestPDCAPriority)
                upperLimit.append(tmpTestItem.TestUpLimit)
                lowLimit.append(tmpTestItem.TestLowLimit)
                unit.append(tmpTestItem.TestUnit)
                if not tmpTestItem.TestResult:
                    failList += tmpTestItem.TestName
                testValue.append(tmpTestItem.TestValue)

            value = [product, sn, entendedSeriaNumber, '', '', '', lotNumber, 'MIC_TEST', '', fixtureID,
                     result and 'PASS' or 'FAIL', startTime.strftime('%Y/%m/%d %H:%M:%S'),
                     endTime.strftime('%Y/%m/%d %H:%M:%S'), failList, version]

            with open(filename, 'a', newline='') as fr:
                write = csv.writer(fr)
                if writeTitle:
                    write.writerow(firstLine)
                    write.writerow(title)
                    write.writerow(displayName)
                    write.writerow(PDCAPriority)
                    write.writerow(upperLimit)
                    write.writerow(lowLimit)
                    write.writerow(unit)

                for tmp in testValue:
                    tmplist = value
                    tmplist.append(tmp)
                    write.writerow(tmplist)
            return True
        except Exception as e:
            print(e)
            global_Gui.tbvwLogEmit('保存数据文件失败!' + str(e), GlobalConf.colorRed)
            return False
    # def writeTestCsv(self, isPcs: bool, guid: str, sn: str, result: bool, module: str,
    #                  startTime: datetime, endTime: datetime, testType: str, partNumber: str,
    #                  localIP: str, items: list, fixtureID: str, projectName: str, program: str,
    #                  version: str, user: str, plateID: str):
    #     try:
    #         if not os.path.exists(self.path):
    #             os.mkdir(self.path)
    #         tmpTimeStamp = str(int(datetime.now().timestamp() * 1000))
    #         tmpTestResult = result and 'PASS' or 'FAIL'
    #         date = int(datetime.now().strftime('%H'))
    #         DorN = (date >= 7 and date < 19) and 'D' or 'N'
    #         testd = DorN == 'D' and endTime.strftime('%Y%m%d') or (endTime + timedelta(days=-1)).strftime('%Y%m%d')
    #         tmpLocalName = isPcs and '{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}{8}_{9}.csv'.format(partNumber,
    #                                                                                      sn, guid, localIP, testType, fixtureID,
    #                                                                                      tmpTestResult, projectName,
    #                                                                                      testType, DorN) or  ('{0}'
    #                                                                                                           '_{1}_{2}_{3}_{4}_{5}_{6}_{7}.csv').format(projectName,
    #                                                                                                                                                               fixtureID, program.Replace("-", "_"),
    #                                                                                                                                                               testd, localIP, "GTS", testType, DorN)
    #         if not (self.path.endswith('/') or self.path.endswith('\\')):
    #             self.path += '/'
    #         filename = self.path + tmpLocalName
    #         fileapp = pathlib.Path(filename)
    #         writeTitle = not fileapp.is_file()
    #         title = ['SerialNumber','Test Pass/Fail Status','errCode',
    #                  'errStr','TesterID','config','timeStamp','StartTime',
    #                  'EndTime','TestTime','Failing items','errValue',
    #                  'holder','slot','testModel','swversion','attribute1',
    #                  'attribute2','attribute3','attribute4']
    #         lowLimit = ['Lower Limit----->','','','','','','','','','','','','','','','','','','','']
    #         upperLimit = ['Upper Limit----->','','','','','','','','','','','','','','','','','','','']
    #         unit = ['Measurement Unit----->','','','','','','','','','Sec','','','','','','','','','','']
    #         failItems = ''
    #         failValue = ''
    #         errorCode = []
    #         errorStr = []
    #         value = []
    #
    #         for num in items:
    #             Tmp: cTestItem = num
    #             title.append(Tmp.TestName)
    #             lowLimit.append(Tmp.TestLowLimit)
    #             upperLimit.append(Tmp.TestUpLimit)
    #             unit.append(Tmp.TestUnit)
    #             value.append(Tmp.TestValue)
    #             if not Tmp.TestResult:
    #                 failValue += Tmp.TestValue
    #                 failItems += Tmp.TestName
    #                 if Tmp.TestName.upper().__contains__('SHORT'):
    #                     if not errorCode.__contains__('90'):
    #                         errorCode.append('90')
    #                     if not errorStr.__contains__('Short'):
    #                         errorStr.append('Short')
    #                 elif Tmp.TestName.upper().__contains__('OPEN'):
    #                     if not errorCode.__contains__('70'):
    #                         errorCode.append('70')
    #                     if not errorStr.__contains__('Open'):
    #                         errorStr.append('Open')
    #                 else:
    #                     if not errorCode.__contains__('100'):
    #                         errorCode.append('100')
    #                     if not errorStr.__contains__('Components'):
    #                         errorStr.append('Components')
    #
    #
    #         testTime = str(int((endTime - startTime).total_seconds()))
    #         tmpValue = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},'.format(sn, tmpTestResult, failItems, "", fixtureID, partNumber, tmpTimeStamp, startTime, endTime, testTime, failItems, failValue, module, plateID, testType, version, guid, user)
    #         testValue = tmpValue.split(',') + value
    #         with open(file, 'a', newline='') as fr:
    #             write = csv.writer(fr)
    #             if writeTitle:
    #                 write.writerow(title)
    #                 write.writerow(lowLimit)
    #                 write.writerow(upperLimit)
    #                 write.writerow(unit)
    #             write.writerow(testValue)
    #         return True
    #     except Exception as e:
    #         global_Gui.tbvwLogEmit('保存数据文件失败!' + str(e), GlobalConf.colorRed)
    #         return False

    def writeTxtLog(self, tickets:str,barcode:str, testTime: datetime, testItems: list):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            tmpTestTime = int(testTime.strftime('%Y')) % 100
            tmpfileName = '{0}{1} {2}-{3}.txt'.format(self.path, tickets, tmpTestTime, testTime.strftime('%-m-%-d'))
            tmpDateTime = '{0}/{1}'.format(tmpTestTime, testTime.strftime('%-m/%-d %H:%M:%S'))
            with open(tmpfileName, 'a+') as fw:
                for num in testItems:
                    tmpItem:cTestItem = num
                    writecontent = '{0},{1},{2},{3},{4},{5},{6},{7}\r\n'.format(barcode,
                                                                            tmpDateTime,
                                                                            tmpItem.TestName,
                                                                            tmpItem.TestValue,
                                                                            tmpItem.TestUnit,
                                                                            tmpItem.TestResult and 'PASS' or 'FAIL',
                                                                            (tmpItem.TestUpLimit != '' and tmpItem.TestLowLimit != '') and 'MAX/MIN' or 'Tolerance curves',
                                                                            (tmpItem.TestUpLimit != '' and tmpItem.TestLowLimit != '') and f'{tmpItem.TestLowLimit}/{tmpItem.TestUpLimit}' or 'Absolute Limits')
                    fw.write(writecontent)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red')
            return False
    def mesCsvLog(self, barcode, ms, result, extensionCode, reason, projectName, fixtureID, localIP, testType, program = str, startTime = datetime, endTime = datetime):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            csvTitle = ['Barcode', 'StartTime', 'EndTime', 'ElapsedTime(ms)', 'CheckResult', 'ExtensionCode', 'Reason']
            value = [barcode, startTime.strftime('%Y-%m-%d %H:%M:%S'), endTime.strftime('%Y-%m-%d %H:%M:%S'), ms, result, extensionCode, reason]
            date = int(datetime.now().strftime('%H'))
            DorN = (date >= 7 and date < 19) and 'D' or 'N'
            testd = DorN == 'D' and endTime.strftime('%Y%m%d') or (endTime + timedelta(days=-1)).strftime('%Y%m%d')
            filename = self.path + '{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}.csv'.format(projectName, fixtureID, program.replace('-', '_'), testd, localIP, 'GTS', testType, DorN)
            if not os.path.isfile(filename):
                with open(filename, 'a', newline='') as fr:
                    csv.writer(fr).writerow(csvTitle)
            with open(filename, 'a', newline='') as fr:
                csv.writer(fr).writerow(value)
            return True
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), 'red')
            return False

    def sampleCsv(self, sn, module, plateID, testResult, failItems, compareResult, testTime:datetime, partNumber, fixtureID, testType):
        try:
            if not (self.path.endswith('/') or self.path.endswith('\\')):
                self.path += '/'
            date = int(datetime.now().strftime('%H'))
            DorN = (date >= 7 and date < 19) and 'D' or 'N'
            csvTitle = ['Barcode','Module','PlateID','TestResult','FailItems','CompareResult','Date','DorN','TestTime']
            value = [sn, module, plateID, testResult, failItems, compareResult, datetime.now().strftime('%Y%m%d'), DorN, testTime.strftime('%Y%m%d %H%M%S')]
            localIP = cConfigure().getLocalIP()
            dateM = datetime.now().strftime('%Y%m')
            tmpLocalName = self.path + f'{partNumber}_{fixtureID}_{testType}_{localIP}_GTS_{dateM}.csv'
            if not os.path.isfile(tmpLocalName):
                with open(tmpLocalName, 'a', newline='') as fr:
                    csv.writer(fr).writerow(csvTitle)
            with open(tmpLocalName, 'a', newline='') as fr:
                csv.writer(fr).writerow(value)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            return False


if __name__ == '__main__':
    day1 = datetime(2023,9,6,8,7,1)
    data = '{0}{1} {2}-{3}.txt'.format('self.path', 'tickets', 'tmpTestTime', datetime.now().strftime('%#m-%#d'))
    print(data)
    daystr = day1.strftime('%-m-%-d %-H:%-M:%-S')
    a= '%#m/%#d %H:%M:%S'
    b = '%#m-%#d'
    print(daystr)
# class cTxtLog():
#     def __init__(self, name):
#         self.name = name
#         self.path = cConfigure().getConfigure(ConfigureKey.SEC_APP, ConfigureKey.KEY_LOG)
#
#         if not os.path.exists(self.path):
#             os.mkdir(self.path)
#
#         logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(level=logging.DEBUG)
#         dtPath = self.path + '/' + str(datetime.now().strftime('%Y-%m-%d'))
#         if not os.path.exists(dtPath):
#             os.mkdir(dtPath)
#         fileName = dtPath + '/' + self.name
#         handler = logging.FileHandler(fileName + '.txt')
#         handler.setLevel(logging.DEBUG)
#
#         formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)
#         self.logger.addHandler(handler)
#
#     def writeError(self, text):
#         self.logger.error(text)
#
#     def writeWarning(self, text):
#         self.logger.warning(text)
#
#     def writeInfo(self, text):
#         self.logger.info(text)
#
#     def writeDebug(self, text):
#         self.logger.debug(text)
#
#     def OverdueLog(self, Days=int):
#         TmpPath=self.path+'/'
#         files = os.listdir(TmpPath)
#         dirlist = []
#         for file in files:
#             if os.path.isdir(TmpPath+ file):
#                 dirlist.append(file)
#         Curdt = datetime.date.today()
#         if len(dirlist) > 0:
#             for dirResult in dirlist:
#                 if (Curdt - (datetime.strptime(dirResult, '%Y-%m-%d')).date()).days >= Days:
#                     shutil.rmtree(TmpPath + dirResult)

