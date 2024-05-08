import re
import guid
from GlobalDir.GlobalGui import global_Gui
from GlobalDir import GlobalConf
from LogDir.AllLog import cAllLog, cFileLog
import requests
import json
from datetime import datetime
from ConfigureDir.Configure import cConfigure
from ConfigureDir import ConfigureKey
from TestDir.TestItem import cTestItem, cTestResult


class cMes():
    def __init__(self):
        self.log = cAllLog('upload')
        self.conf = cConfigure()
        self.Configurekey = ConfigureKey
        self.ApiAddress = ''
        self.ApiPath = ''
        self.Barcode = ''
        self.OperatorID = ''
        self.ToolNumber = ''
        self.TestType = ''
        self.PreviousTestType = ''
        self.ProductName = ''
        self.WorkArea = ''
        self.Site = ''
        self.Program = ''
        self.Lot = ''
        self.IpAddress = ''
        self.StationTime = ''
        self.slotName = ''
        self.subslotName = ''
        self.Result = cTestResult()

    def Clone(self):
        mes = cMes()
        mes.log = self.log
        mes.conf = self.conf
        mes.ApiAddress = self.ApiAddress
        mes.ApiPath = self.ApiPath
        mes.Barcode = self.Barcode
        mes.OperatorID = self.OperatorID
        mes.ToolNumber = self.ToolNumber
        mes.TestType = self.TestType
        mes.PreviousTestType = self.PreviousTestType
        mes.ProductName = self.ProductName
        mes.WorkArea = self.WorkArea
        mes.Site = self.Site
        mes.Program = self.Program
        mes.Lot = self.Lot
        mes.IpAddress = self.IpAddress
        mes.StationTime = self.StationTime
        mes.slotName = self.slotName
        mes.subslotName = self.subslotName
        return mes


    def SnCheck(self, sn: str):
        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = ''
        if self.Barcode == '':
            responsebody.erroMessage = '条码为空'
            return responsebody
        if self.ApiAddress == '':
            responsebody.erroMessage = 'ET接口地址或是路径为空'
            return responsebody
        if self.OperatorID == '':
            responsebody.erroMessage = '操作员工号为空'
            return responsebody
        if self.IpAddress == '':
            responsebody.erroMessage = '机台IP地址为空'
            return responsebody
        try:
            self.ApiAddress = self.ApiAddress.endswith('/') and self.ApiAddress[0:len(self.ApiAddress) - 1] or self.ApiAddress
            self.StationTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            tmpJson = {}
            tmpJson['barcode'] = str(self.Barcode)
            tmpJson['operator'] = str(self.OperatorID)
            tmpJson['toolNumber'] = str(self.ToolNumber)
            tmpJson['testType'] = str(self.TestType)
            tmpJson['prevTestType'] = str(self.PreviousTestType)
            tmpJson['productName'] = str(self.ProductName)
            tmpJson['workArea'] = str(self.WorkArea)
            tmpJson['site'] = str(self.Site)
            tmpJson['program'] = str(self.Program)
            tmpJson['lot'] = str(self.Lot)
            tmpJson['ipAddress'] = str(self.IpAddress)
            tmpJson['stationTime'] = str(self.StationTime)
            tmpJson['slotName'] = '1'
            tmpJson['subslotName'] = '1'

            # url = '{0}/{1}?barcode={2}&operator={3}&toolNumber={4}&testType=\
            # {5}&prevTestType={6}&productName={7}&workArea={8}&site={9}&program=\
            # {10}&lot={11}&ipAddress={12}&stationTime={13}&slotName=\
            # {14}&subslotName={15}'.format(self.ApiAddress, self.ApiPath, self.Barcode, self.OperatorID,
            #                               self.ToolNumber, self.TestType, self.PreviousTestType, self.ProductName, self.WorkArea,
            #                               self.Site, self.Program, self.Lot, self.IpAddress, self.StationTime, self.slotName, self.subslotName)
            url = f'{self.ApiAddress}/{self.ApiPath}'
            global_Gui.tbvwLogEmit(f'URL:{url}', GlobalConf.colorGreen)
            self.log.writelog('MES卡控开始')
            tmpstr = self.HttpGet(url, params=tmpJson)
            if tmpstr == None:
                responsebody.erroMessage = "接收接口返回信息超时 error"
                self.log.writelog( "接收卡控接口返回信息超时 error" )
                return responsebody
            tmpjson = json.loads(tmpstr)
            self.analyseResult(tmpjson)
            responsebody.erroMessage = str(tmpjson["message"])
            self.log.writelog("卡控条码结果：" + str(responsebody.isOk) + "返回信息" + responsebody.erroMessage)
            responsebody.isOk = self.Result.isSuccess
            return responsebody
        except Exception as e:
            responsebody.erroMessage = str(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            return responsebody

    def uploadMes(self, barcode: str, testItems: list, startTime: datetime, endTime: datetime, testResult: bool):
        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = ''
        try:
            tmpProductName = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PRODUCT_NAME])
            tmpExtendBarcode = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_EXTENDED_BARCODE])
            tmpWorkArea = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_WORK_AREA])
            tmpProgram = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROGRAM])
            tmpPartNumber = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PART_NUMBER])
            tmpProjectName = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROJECT_NAME])
            testType = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TEST_TYPE])
            tmpResourceName = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_RESOURCE_NAME])
            tmpOperatorID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_OPERATOR])
            tmpLineID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_LINE_ID])
            tmpFixtureID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_FIXTURE_ID])
            tmpToolNumber = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TOOL_NUMBER])

            tmpProgramComponents = tmpProgram.split('-')
            if barcode == '':
                responsebody.erroMessage = '条码为空!'
                return responsebody
            if testItems == None:
                responsebody.erroMessage = '测试数据为空!'
                return responsebody

            failItems = ''
            failValue = ''

            tmpGuid = guid.guid.GUID().upper()
            tmptype = (testType.__contains__('-ABB') or testType.__contains__('-INLINE')) and testType.replace('-ABB', '').replace('-INLINE', '') or testType
            localIP = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_HOST_IP])
            tmpSWVersion = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_VERSION])

            tmpResult, failValue, failItems = self.GenerateErrorInformation(testItems)
            tmpTimeStamp = str(int(datetime.now().timestamp() * 1000))
            tmpTestTimeStamp = str(int((endTime - startTime).total_seconds()))

            tmpTestDetails = []
            tmpTestDetails.append(self.cls2dict("serialNumber", barcode))
            tmpTestDetails.append(self.cls2dict("Test Pass/Fail Status", testResult and "PASS" or "FAIL"))
            tmpTestDetails.append(self.cls2dict("errCode", failItems))
            tmpTestDetails.append(self.cls2dict("errStr", None))
            tmpTestDetails.append(self.cls2dict("TesterID", tmpFixtureID))
            tmpTestDetails.append(self.cls2dict("config", tmpProjectName))
            tmpTestDetails.append(self.cls2dict("timeStamp", tmpTimeStamp))
            tmpTestDetails.append(self.cls2dict("startTime", startTime.strftime("%Y-%m-%dT%H:%M:%S")))
            tmpTestDetails.append(self.cls2dict("EndTime", endTime.strftime("%Y-%m-%dT%H:%M:%S")))
            tmpTestDetails.append(self.cls2dict("TestTime", tmpTestTimeStamp,"sec"))
            tmpTestDetails.append(self.cls2dict("Failing items", failItems))
            tmpTestDetails.append(self.cls2dict("errValue", failValue))
            tmpTestDetails.append(self.cls2dict("holder", None))
            tmpTestDetails.append(self.cls2dict("slot", None))
            tmpTestDetails.append(self.cls2dict("testModel", testType))
            tmpTestDetails.append(self.cls2dict("swversion", tmpSWVersion))
            tmpTestDetails.append(self.cls2dict("attribute1", tmpGuid))
            tmpTestDetails.append(self.cls2dict("attribute2", tmpOperatorID))
            tmpTestDetails.append(self.cls2dict("attribute3", None))
            tmpTestDetails.append(self.cls2dict("attribute4", None))

            for num in testItems:
                tmpItem:cTestItem = num
                tmpTestDetails.append(self.cls2dict(tmpItem.TestName, tmpItem.TestValue))

            testjson = {}
            testjson['barcode'] = barcode
            testjson['testType'] = testType
            testjson['testTime'] = endTime.strftime('%Y-%m-%dT%H:%M:%S')
            testjson['testResult'] = testResult and 'PASS' or 'FAIL'
            testjson['operator'] = tmpOperatorID
            testjson['workArea'] = tmpWorkArea
            testjson['resourceName'] = tmpResourceName
            testjson['ipAddress'] = localIP
            testjson['toolNumber'] = tmpToolNumber
            testjson['slotName'] = '1'
            #应现场要求，subslotName设置为1
            testjson['subslotName'] = '1'
            testjson['errorCode'] = failItems
            testjson['errorValue'] = None
            testjson['productName'] = tmpPartNumber
            testjson['program'] = tmpProgram
            testjson['testDetailId'] = tmpGuid
            testjson['extendInfo'] = 'A:GTS;B:RCR'
            testjson['socketInfo'] = '1'
            testjson['rosalineInfo'] = '1'
            testjson['attribute1'] = None
            testjson['attribute2'] = None
            testjson['dartfishInfo'] = None
            testjson['testDetails'] = tmpTestDetails

            self.ApiAddress = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_ADDRESS])
            self.ApiPath = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_UPLOAD_PATH])
            tmpUrl = f'{self.ApiAddress}/{self.ApiPath}'
            result = False
            tmpCsvFlag1 = True
            uploadEnable = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_MES_UPLOAD]) == 'Y'
            if uploadEnable:
                self.log.writelog('开始上传数据 URL：' + tmpUrl)
                self.log.writelog("上传的数据为：" + json.dumps(testjson, indent=4, ensure_ascii=False))
                result, tmpstr = self.HttpPost(tmpUrl, json.dumps(testjson))

                responsebody.isOk = result
                responsebody.erroMessage = tmpstr
                if result:
                    tmpMesUpload = str(self.conf.ConfigureDic[self.Configurekey.SEC_MES][self.Configurekey.KEY_MESURL])
                    if not tmpMesUpload.endswith('\\'):
                        tmpMesUpload += '\\'
                    tmpDayDir = tmpMesUpload + tmpPartNumber[0:5]
                    # tmpDayDir = r'E:/data/'
                    tmpDayCsvLog = cFileLog(tmpDayDir)
                    tmpCsvFlag1 = tmpDayCsvLog.writeMFLEXTestCsv(False, tmpGuid, barcode, testResult, 'A',
                                                                 startTime, endTime, testType, tmpPartNumber, localIP,
                                                                 testItems, tmpFixtureID,
                                                                 tmpProjectName, tmpProgram, tmpSWVersion,
                                                                 tmpOperatorID, '1', tmpProductName, tmpExtendBarcode,
                                                                 self.Lot)

            if (uploadEnable and result) or tmpCsvFlag1:
                tmpDayDir = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_DATA_PATH])
                tmpDayCsvLog = cFileLog(tmpDayDir)
                tmpCsvFlag2 = tmpDayCsvLog.writeMFLEXTestCsv(False, tmpGuid, barcode, testResult, 'A',
                                                           startTime, endTime, testType, tmpPartNumber, localIP,
                                                           testItems, tmpFixtureID,
                                                           tmpProjectName, tmpProgram, tmpSWVersion, tmpOperatorID, '1',
                                                           tmpProductName, tmpExtendBarcode, self.Lot)
                #tmpDayCsvLog.writeTxtLog(startTime.strftime('%Y-%m-%d'), barcode, endTime, testItems)
                if not tmpCsvFlag1 or not tmpCsvFlag2:
                    responsebody.isOk = False
                    responsebody.erroMessage = 'csv写入错误，请检查.csv文件路径是否存在，是否有写入权限'

            self.log.writelog("上传数据 结果：" + str(responsebody.isOk) + "  返回信息：" + responsebody.erroMessage)
            return responsebody

        except Exception as e:
            responsebody.erroMessage = str(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            print(e)
            return  responsebody

    # def uploadMes(self, barcode: str, testItems: list, startTime: datetime, endTime: datetime, testResult: bool):
    #     responsebody = Responsebody()
    #     responsebody.isOk = False
    #     responsebody.erroMessage = ''
    #     try:
    #         tmpWorkArea = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_WORK_AREA])
    #         tmpResourceName = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_RESOURCE_NAME])
    #         tmpProgram = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROGRAM])
    #         tmpOperatorID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_OPERATOR])
    #         tmpPartNumber = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PART_NUMBER])
    #         tmpLineID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_LINE_ID])
    #         tmpFixtureID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_FIXTURE_ID])
    #         tmpProjectName = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PROJECT_NAME])
    #         testType = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TEST_TYPE])
    #
    #         tmpProgramComponents = tmpProgram.split('-')
    #         if len(tmpProgramComponents) != 4:
    #             responsebody.erroMessage = '参数测试程序设置错误，请重新配置！配置规则为:内部料号-站位-阶段-版本'
    #             return responsebody
    #         if tmpPartNumber == '':
    #             responsebody.erroMessage = '料号不能为空，请先设置料号!'
    #             return responsebody
    #         if barcode == '':
    #             responsebody.erroMessage = '条码为空!'
    #             return responsebody
    #         if testItems == None or testItems.count() <= 0:
    #             responsebody.erroMessage = '测试数据为空!'
    #             return responsebody
    #
    #         failItems = ''
    #         failValue = ''
    #         for num in testItems:
    #             item: cTestItem = num
    #             if not item.TestResult:
    #                 failItems += item.TestName + ';'
    #                 failValue += item.TestValue + ';'
    #         tmpProgramComponents[1] += testType.upper().__contains__('SEAL') and '_1' or (testType.upper().__contains__('ICT') and '_2' or '' )
    #         tmpSWVersion = '-'.join(tmpProgramComponents)
    #         tmpGuid = guid.guid.GUID().upper()
    #         tmptype = (testType.__contains__('-ABB') or testType.__contains__('-INLINE')) and testType.replace('-ABB', '').replace('-INLINE', '') or testType
    #         localIP = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_IP_ADDRESS])
    #         tmp = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_LOG])
    #         localPath = (tmp.endswith('/') or tmp.endswith('\\')) and tmp or tmp + '/'
    #         localLog = cFileLog(localPath)
    #         localLog.writeTestCsv(False, tmpGuid, barcode, testResult, 'A', startTime, endTime,
    #                               tmptype, tmpPartNumber, localIP, testItems, tmpFixtureID, tmpProjectName, tmpProgram,
    #                               tmpSWVersion, tmpOperatorID, '1')
    #
    #         # mfetTest = cUploadItem()
    #         # mfetTest.ApiAddress = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_ADDRESS])
    #         # mfetTest.ApiPath = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_PATH])
    #         # mfetTest.Barcode = barcode
    #         # mfetTest.OperatorID = tmpOperatorID
    #         # mfetTest.ToolNumber = tmpFixtureID
    #         # mfetTest.ProductName = tmpPartNumber
    #         # mfetTest.WorkArea = tmpWorkArea
    #         # mfetTest.slotName = '1'
    #         # mfetTest.subslotName = '1'
    #         # mfetTest.Program = tmpProgram
    #         # mfetTest.IpAddress = localIP
    #         # mfetTest.TestTime = endTime
    #         # mfetTest.ResourceName = tmpResourceName
    #
    #         tmpErrorCode, tmpErrorValue = self.GenerateErrorInformation(testItems)
    #         tmpTimeStamp = str(int(datetime.now().timestamp() * 1000))
    #         tmpTestTimeStamp = str(int((endTime - startTime).total_seconds()))
    #
    #         tmpTestDetails = []
    #         tmpTestDetails.append(cTestDetails("serialNumber", barcode))
    #         tmpTestDetails.append(cTestDetails("Test Pass/Fail Status", testResult and "PASS" or "FAIL"))
    #         tmpTestDetails.append(cTestDetails("errCode", failItems))
    #         tmpTestDetails.append(cTestDetails("errStr", None))
    #         tmpTestDetails.append(cTestDetails("TesterID", tmpFixtureID))
    #         tmpTestDetails.append(cTestDetails("config", tmpProjectName))
    #         tmpTestDetails.append(cTestDetails("timeStamp", tmpTimeStamp))
    #         tmpTestDetails.append(cTestDetails("startTime", startTime.strftime("%Y/%m%d %H:%M:%S")))
    #         tmpTestDetails.append(cTestDetails("EndTime", endTime.strftime("%Y/%m%d %H:%M:%S")))
    #         tmpTestDetails.append(cTestDetails("TestTime", tmpTestTimeStamp,"sec"))
    #         tmpTestDetails.append(cTestDetails("Failing items", failItems))
    #         tmpTestDetails.append(cTestDetails("errValue", failValue))
    #         tmpTestDetails.append(cTestDetails("holder", None))
    #         tmpTestDetails.append(cTestDetails("slot", None))
    #         tmpTestDetails.append(cTestDetails("testModel", testType))
    #         tmpTestDetails.append(cTestDetails("swversion", tmpSWVersion))
    #         tmpTestDetails.append(cTestDetails("attribute1", tmpGuid))
    #         tmpTestDetails.append(cTestDetails("attribute2", tmpOperatorID))
    #         tmpTestDetails.append(cTestDetails("attribute3", None))
    #         tmpTestDetails.append(cTestDetails("attribute4", None))
    #
    #         for numI in testItems:
    #             tmpItem: cTestItem = numI
    #             tmpTestDetails.append(cTestDetails(tmpItem.TestName, tmpItem.TestValue, tmpItem.TestUnit, tmpItem.TestUpLimit, tmpItem.TestLowLimit))
    #
    #         self.log.writelog('开始上传数据 URL：' + url)
    #
    #
    #         testjson = {}
    #         testjson['barcode'] = barcode
    #         testjson['testType'] = testType
    #         testjson['testTime'] = endTime.strftime('%Y-%m-%d %H:%M:%S')
    #         testjson['testResult'] = testResult and 'PASS' or 'FAIL'
    #         testjson['operator'] = tmpOperatorID
    #         testjson['workArea'] = tmpWorkArea
    #         testjson['resourceName'] = tmpResourceName
    #         testjson['ipAddress'] = localIP
    #         testjson['toolNumber'] = tmpFixtureID
    #         testjson['slotName'] = '1'
    #         testjson['subslotName'] = '1'
    #         testjson['errorCode'] = failItems
    #         testjson['errorValue'] = None
    #         testjson['productName'] = tmpPartNumber
    #         testjson['program'] = tmpProgram
    #         testjson['testDetailId'] = tmpGuid
    #         testjson['extendInfo'] = 'A:GTS;B:RCR'
    #         testjson['testDetails'] = tmpTestDetails
    #
    #         self.ApiAddress = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_ADDRESS])
    #         self.ApiPath = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_PATH])
    #         tmpUrl = f'{self.ApiAddress}/{self.ApiPath}'
    #         self.log.writelog("上传的数据为：" + json.dumps(testjson, indent=4, ensure_ascii=False))
    #         result, tmpstr = self.HttpPost(tmpUrl, json.dumps(testjson))
    #
    #         responsebody.isOk = result
    #         responsebody.erroMessage = tmpstr
    #
    #         if result:
    #             tmpDayDir = r'\\ot-mfcisilon02.mflex.com.cn\OneFS\ETLocalbackup2021\day_Data' + '\\' + tmpPartNumber[0:5]
    #             tmpDayCsvLog = cFileLog(tmpDayDir)
    #             tmpCsvFlag = tmpDayCsvLog.writeTestCsv(False, tmpGuid, barcode, testResult, 'A',
    #                                                    startTime, endTime, testType, tmpPartNumber, localIP, testItems, tmpFixtureID,
    #                                                    tmpProjectName, tmpProgram, tmpSWVersion, tmpOperatorID, '1')
    #             if not tmpCsvFlag:
    #                 responsebody.isOk = tmpCsvFlag
    #                 responsebody.erroMessage = 'csv写入错误，请检查day csv路径是否存在，是否有写入权限'
    #
    #         self.log.writelog("上传数据 结果：" + str(responsebody.isOk) + "  返回信息：" + responsebody.erroMessage)
    #         return responsebody
    #
    #     except Exception as e:
    #         responsebody.erroMessage = str(e)
    #         global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
    #         return  responsebody

    def uploadFLEXIUM(self, OpNumber, ProductType, WorkOrder,barcode:str, stratTime:datetime, testItems:list, testResult:bool, localIp:str):
        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = '写入失败，请检查上传路径和本地路径'
        try:
            #tmpUploadDir = str(self.conf.ConfigureDic[self.Configurekey.SEC_MES][self.Configurekey.KEY_MESURL])
            tmpLocalDir = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_DATA_PATH])
            tickets = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TICKETS])
            result1 = True
            #if str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_MES_UPLOAD]) == 'Y':
            #    tmpUploadDir = str(self.conf.ConfigureDic[self.Configurekey.SEC_MES][self.Configurekey.KEY_MESURL])
            #    tmpUploadLog = cFileLog(tmpUploadDir)
            #    result1 = tmpUploadLog.uploadFLEXIUMTestCsv(tickets, barcode, testResult, stratTime, testItems, localIp)
            tmpLocalLog = cFileLog(tmpLocalDir)
            result2 = tmpLocalLog.localFLEXIUMTestCsv(OpNumber, ProductType,WorkOrder, barcode, testResult, stratTime, testItems)
            responsebody.isOk = result1&result2
            return responsebody
        except Exception as e:
            responsebody.erroMessage = str(e)
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            print(e)
            return responsebody
    def GenerateErrorInformation(self, testItems: list):
        try:
            errCode = ''
            errValue = ''
            tmpErrCodeList = []
            for tmp in testItems:
                item: cTestItem = tmp
                if item.TestResult:
                    continue
                tmpName = item.TestName.upper()
                tmpErrCodeList.append(
                    tmpName.__contains__('OPEN') and 70 or (tmpName.__contains__('SHORT') and 90 or 100))
                errValue += item.TestValue
            errCode = self.GenrateError(tmpErrCodeList)
            return True, errCode, errValue
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            return False,'', ''


    def GenrateError(self, errList: list):
        errCode = ''
        if errList == None or len(errList) == 0:
            return errCode
        for err in errList:
            if errCode.__contains__(str(err)):
                continue
            errCode += str(err)
        return errCode

    def CheckBarcodeThreeNG(self, API, sn, key, NeedTestcount = 3):
        try:
            if API == "-" or key == "-":
                return True, "屏蔽捞取 NA NA"
            if sn == '':
                return False, '条码为空'
            url = API + sn
            tmpstr = self.HttpGet(url)
            if tmpstr == None:
                return False, '查询失败'

            tmpjson = json.loads(tmpstr)
            Pass = str(tmpjson["success"]).lower() == "true"
            if Pass == False:
                return False, "数据查询失败"
            Message = str(tmpjson["message"])
            NGCount = int(tmpjson["extensionMessages"]['TESTED_COUNT'])
            if NGCount < 3:
                return True, Message
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)
            return False, str(e)

    def HttpGet(self, url, timeout = 10, params:dict = {}):
        try:
            headers = { 'Accept-Language': 'zh-Hans,zh;q=0.9'}
            response = requests.get(url,timeout=timeout, headers=headers, params=params)
            print('url:',response.url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            global_Gui.tbvwLogEmit( 'HTTP GET ERROR' + str(e), GlobalConf.colorRed)
            return None

    def HttpPost(self, url, data, timeout = 10):
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            response = requests.post(url, data,timeout = timeout, headers=headers)
            return response.status_code==200,response.text
        except Exception as e:
            global_Gui.tbvwLogEmit('HTTP POST ERROR' + str(e), GlobalConf.colorRed)
            return False,e

    def analyseResult(self, tmpjson):
        try:
            self.Result.isSuccess = str(tmpjson["isSuccess"]).lower() == "true"
            self.Result.extensionCode = str(tmpjson["extensionCode"])
            self.Result.message = str(tmpjson["message"])
            self.Result.extensionMessages.barcodeFamily = str(tmpjson['extensionMessages']['BARCODE_FAMILY'])
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)


    def SampleCompare(self, sn, failItems, testResult, endTime: datetime):
        try:
            tmpPartNumber = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_PART_NUMBER])
            tmpFixtureID = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_FIXTURE_ID])
            testType = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TEST_TYPE])
            tmpSamples = self.GetShiftSamples()
            if tmpSamples == None:
                return
            isMatched = False
            for sample in tmpSamples:
                tmp: dict = sample
                #此处有修改， 用==无法实现
                if sn in tmp.values():
                    isMatched = str(tmpSamples['isResultMatched']).lower() == 'true'

            tmpTargetFailItem = str(tmpSamples['defectCode'])
            tmpSampleUpload = str(self.conf.ConfigureDic[self.Configurekey.SEC_MES][self.Configurekey.KEY_GOLDEN_PATH])
            if not tmpSampleUpload.endswith('\\'):
                tmpSampleUpload += '\\'
            samplePath = tmpSampleUpload
            sampleCSV = cFileLog(samplePath)
            sampleCSV.sampleCsv(sn, 'A', '1', testResult, failItems, isMatched, endTime, tmpPartNumber, tmpFixtureID,
                                testType)
            tmpPath = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_DATA_PATH])
            if not (tmpPath.endswith('\\') or tmpPath.endswith('/')):
                tmpPath += '/'
            localSamplePath = tmpPath + 'SampleCsvLog/'
            localSampleCSV = cFileLog(localSamplePath)
            localSampleCSV.sampleCsv(sn, 'A', '1', testResult, failItems, isMatched, endTime, tmpPartNumber,
                                     tmpFixtureID, testType)
            if not isMatched:
                msg = f'样本{sn}比对结果FAIL\n不良问题点：{tmpTargetFailItem}\n当前测试问题点：{failItems}'
                global_Gui.tbvwLogEmit(msg, GlobalConf.colorRed)
                global_Gui.showMsgBox('警告', msg)
        except Exception as e:
            global_Gui.tbvwLogEmit(str(e), GlobalConf.colorRed)



    def GetShiftSamples(self):
        try:
            ApiAddress = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_ADDRESS])
            ApiPath = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_API_SAMPLE_PATH])
            ToolNumber = str(self.conf.ConfigureDic[self.Configurekey.SEC_APP][self.Configurekey.KEY_TOOL_NUMBER])
            tmpjson = {}
            tmpjson['resourcename'] = ToolNumber
            if ApiAddress.endswith('/'):
                ApiAddress = ApiAddress[0:len(ApiAddress) - 1]
            tmpUrl = '{0}/{1}'.format(ApiAddress, ApiPath)
            tmpStr = self.HttpGet(tmpUrl, params=tmpjson)
            tmpJson = json.loads(tmpStr)
            return tmpJson
        except Exception as e:
            print(e)
            return None

    def cls2dict(self, header = '', value = '', measureUnit = '', upperLimit = '', lowerLimit = ''):
        tmpDict = {}
        tmpDict['header'] = header
        tmpDict['upperLimit'] = upperLimit
        tmpDict['lowerLimit'] = lowerLimit
        tmpDict['value'] = value
        tmpDict['measureUnit'] = measureUnit
        return tmpDict

class Responsebody:

    #initialization
    def __init__(self):
        self.isOk = False
        self.erroMessage = ''