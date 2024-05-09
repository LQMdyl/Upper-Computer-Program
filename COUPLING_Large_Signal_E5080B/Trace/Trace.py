import os
import time


import requests
import json

import GlobalGui
from TestDir.TestItem import cTestItem

class cTrace:

    #initializationq
    def __init__(self):
        print("Trace init")

    def __del__(self):
        print("Trace del")

    def SnCheck(self, sn):
        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = ""
        try:
            Tmp = "http://localhost:8765/v2"
            if sn == "":
                responsebody.erroMessage = "SN is empty"
                return responsebody

            Url = "{0}/process_control?serial={1}&serial_type=part_id".format( Tmp, sn )
            self.writeUploadLog( "开始卡控条码 URL：" + Url )
            tmpstr = self.HttpGet( Url )
            if tmpstr == None:
                responsebody.erroMessage = "接收接口返回信息超时 error"
                self.writeUploadLog( "接收卡控接口返回信息超时 error" )
                return responsebody

            tmpjson = json.loads( tmpstr )
            responsebody.isOk = str( tmpjson["pass"] ).lower() == "true"
            responsebody.erroMessage = str( tmpjson["processes"] )
            self.writeUploadLog( "卡控条码结果：" + str( responsebody.isOk ) + "返回信息" + responsebody.erroMessage )
            return responsebody
        except Exception as e:
            responsebody.erroM0essage = str( e )
            self.writeUploadLog( "卡控条码结果：" + str( responsebody.isOk ) + "返回信息" + responsebody.erroMessage )
            return responsebody

    def UploadJson_RK(self, Result:str, Barcode:str,startTime:str,endTime:str,cycle_time:str,op_id:str,shift:str,
                      LineID:str,stationID:str,softName:str,softVersion:str,fixtureID:str,
                      GoldenSampleSN:str,LastCheckTime:str,IsGolden:bool,testItems):

        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = ""

        try:
            Tmp = "http://localhost:8765/v2"
            Url = "{0}/logs".format( Tmp )
            self.writeUploadLog( "开始上传数据 URL：" + Url )

            Testlist = []

            if Result == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数Result为空"
                return responsebody
            if Barcode == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数Barcode为空"
                return responsebody
            if op_id == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数op_id为空"
                return responsebody
            if LineID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数LineID为空"
                return responsebody
            if stationID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数stationID为空"
                return responsebody
            if softName == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数softName为空"
                return responsebody
            if softVersion == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数softVersion为空"
                return responsebody
            if fixtureID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数fixtureID为空"
                return responsebody
            if GoldenSampleSN == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数GoldenSampleSN为空"
                return responsebody
            if LastCheckTime == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数LastCheckTime为空"
                return responsebody
            if len( testItems ) <= 0:
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数testItems为空"
                return responsebody

            for item in testItems:
                num: cTestItem = item
                if num.TestLowLimit=="-" or num.TestLowLimit=="NA":
                    continue
                Testlist.append(
                    {"result": num.TestResult and "pass" or "fail",
                     "units": num.TestUnit,
                     "test": num.TestName,
                     "value": str(num.TestValue),
                     "lower_limit": str(num.TestLowLimit),
                     "upper_limit": str(num.TestUpLimit)
                     })

            testjson = {}
            testjson["serials"] = {"part_id": Barcode}
            testjson["data"] = {
                "insight":
                    {
                        "test_attributes":
                            {
                                "test_result": Result,
                                "uut_start": startTime,
                                "uut_stop": endTime
                            },
                        "test_station_attributes":
                            {
                                "line_id": LineID,
                                "station_id": stationID,
                                "software_name": softName,
                                "software_version": softVersion,
                                #"fixture_id": fixtureID,
                                "last_calibration_hsg_no": GoldenSampleSN,
                                "calibration_hsg":IsGolden and "Y" or "N",
                                "last_calibration_time": LastCheckTime
                            },
                        "uut_attributes":
                            {
                                "cavity_id": fixtureID,
                                #"shift": shift,
                                #"op_id": op_id,
                                "station_vendor": "GTS",
                                #"cycle_time": cycle_time,
                            },
                        "results": Testlist
                    }
            }

            self.writeUploadLog( "上传的数据为：" + json.dumps( testjson, indent=4, ensure_ascii=False ) )
            result, tmpstr = self.HttpPost( Url, json.dumps( testjson ) )

            if result == False:
                self.writeUploadLog( "上传数据 结果：" + str( result ) + "  错误信息：" + tmpstr )
                responsebody.isOk = False
                responsebody.erroMessage = tmpstr
                return responsebody

            responsebody.isOk = True
            responsebody.erroMessage = tmpstr
            self.writeUploadLog( "上传数据 结果：" + str( result ) + "  返回信息：" + tmpstr )
            return responsebody
        except Exception as e:
            responsebody.isOk = False
            responsebody.erroMessage = str( e )
            self.writeUploadLog( "上传数据 结果：" + str( responsebody.isOk ) + "  返回信息：" + responsebody.erroMessage )
            return responsebody
            print(e)

    def UploadJson_MCEG(self, Result:str, Barcode:str,startTime:str,endTime:str,cycle_time:str,op_id:str,
                      LineID:str,stationID:str,softName:str,softVersion:str,fixtureID:str,
                      GoldenSampleSN:str,LastCheckTime:str,IsGolden:bool,testItems):

        responsebody = Responsebody()
        responsebody.isOk = False
        responsebody.erroMessage = ""

        try:
            Tmp = "http://localhost:8765/v2"
            Url = "{0}/logs".format( Tmp )
            self.writeUploadLog( "开始上传数据 URL：" + Url )

            Testlist = []

            if Result == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数Result为空"
                return responsebody
            if Barcode == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数Barcode为空"
                return responsebody
            if op_id == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数op_id为空"
                return responsebody
            if LineID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数LineID为空"
                return responsebody
            if stationID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数stationID为空"
                return responsebody
            if softName == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数softName为空"
                return responsebody
            if softVersion == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数softVersion为空"
                return responsebody
            if fixtureID == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数fixtureID为空"
                return responsebody
            if GoldenSampleSN == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数GoldenSampleSN为空"
                return responsebody
            if LastCheckTime == "":
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数LastCheckTime为空"
                return responsebody
            if len( testItems ) <= 0:
                responsebody.isOk = False
                responsebody.erroMessage = "传入的参数testItems为空"
                return responsebody

            for item in testItems:
                num: cTestItem = item
                if num.TestLowLimit=="-" or num.TestLowLimit=="NA":
                    continue
                Testlist.append(
                    {"result": num.TestResult and "pass" or "fail",
                     "units": num.TestUnit,
                     "test": num.TestName,
                     "value": str(num.TestValue),
                     "lower_limit": str(num.TestLowLimit),
                     "upper_limit": str(num.TestUpLimit)
                     })

            testjson = {}
            testjson["serials"] = {"part_id": Barcode}
            testjson["data"] = {
                "insight":
                    {
                        "test_attributes":
                            {
                                "test_result": Result,
                                "uut_start": startTime,
                                "uut_stop": endTime
                            },
                        "test_station_attributes":
                            {
                                "line_id": LineID,
                                "station_id": stationID,
                                "software_name": softName,
                                "software_version": softVersion,
                                #"fixture_id": fixtureID,
                                "last_calibration_hsg_no": GoldenSampleSN,
                                "calibration_hsg":IsGolden and "Y" or "N",
                                "last_calibration_time": LastCheckTime
                            },
                        "uut_attributes":
                            {
                                "cavity_id": fixtureID,
                                #"shift": shift,
                                "op_id": op_id,
                                "station_vendor": "GTS",
                                "cycle_time": cycle_time,
                            },
                        "results": Testlist
                    }
            }

            self.writeUploadLog( "上传的数据为：" + json.dumps( testjson, indent=4, ensure_ascii=False ) )
            result, tmpstr = self.HttpPost( Url, json.dumps( testjson ) )

            if result == False:
                self.writeUploadLog( "上传数据 结果：" + str( result ) + "  错误信息：" + tmpstr )
                responsebody.isOk = False
                responsebody.erroMessage = tmpstr
                return responsebody

            responsebody.isOk = True
            responsebody.erroMessage = tmpstr
            self.writeUploadLog( "上传数据 结果：" + str( result ) + "  返回信息：" + tmpstr )
            return responsebody
        except Exception as e:
            responsebody.isOk = False
            responsebody.erroMessage = str( e )
            self.writeUploadLog( "上传数据 结果：" + str( responsebody.isOk ) + "  返回信息：" + responsebody.erroMessage )
            return responsebody
            print(e)

    def writeUploadLog(self,Message):
        file="D:\\UploadLog\\"+time.strftime("%Y%m", time.localtime())
        if not os.path.exists(file):
            os.makedirs(file)
        fileName = file + "\\" + time.strftime("%Y%m%d", time.localtime()) + ".txt"
        with open(fileName, "a") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+",   "+Message+"\n")

    def McegGetCoilConfig(self, sn):
        try:
            Url = "http://17.239.117.210/api/v2/parts?serial_type=part_id&serial={0}&process_name=mahi-coil-link".format(
                sn)
            self.writeUploadLog("开始查询COIL 信息 URL：" + Url)
            Reback = self.HttpGetPassWord(Url)  # self.readFile(r"C:\Users\GTS\Desktop\coil.txt")#
            if Reback == None:
                return False, ""
            self.writeUploadLog("COIL信息 结果：" + Reback)

            tmpjson = json.loads(Reback)
            list: dict = tmpjson["history"][0]
            coilSN = list["data"]["insight"]["uut_attributes"]["scorpius_coil_id"]
            self.writeUploadLog("COIL SN：" + coilSN)
            return True, coilSN
            pass
        except Exception as e:
            self.writeUploadLog("GetCoil 异常：" + str(e))
            return False, "异常：" + str(e)

    def McegGetCoilConfig_5xx(self, sn):
        try:
            Url = "http://17.239.117.210/api/v2/parts?serial_type=part_id&serial={0}&process_name=mahi-coil-assy".format(
                sn)
            self.writeUploadLog("开始查询COIL 信息 URL：" + Url)
            Reback = self.HttpGetPassWord(Url)  # self.readFile(r"C:\Users\GTS\Desktop\coil.txt")#
            if Reback == None:
                return False, ""
            self.writeUploadLog("COIL信息 结果：" + Reback)

            tmpjson = json.loads(Reback)
            list: dict = tmpjson["history"][0]
            coilSN = list["data"]["insight"]["uut_attributes"]["mahi_coil_sn"]#["scorpius_coil_id")
            self.writeUploadLog("COIL SN：" + coilSN)
            return True, coilSN
            pass
        except Exception as e:
            self.writeUploadLog("GetCoil 异常：" + str(e))
            return False, "异常：" + str(e)


    def CheckBarcodeThreeNG_RK(self,sn,station):
        try:
            Url = "http://10.134.9.139/api/getEachStationInfo?serialNumber=" + sn + "&station=" + station + "&dbName=v2";
            Reback = self.HttpGet( Url )
            if Reback == None:
                return False, ""
            tmpjson = json.loads( Reback )
            Pass = str( tmpjson["success"] ).lower() == "true"
            if Pass == False:
                return False, "数据查询失败"
            Message = str( tmpjson["message"] )
            testdata = str( tmpjson["data"]["result"] )
            NGCount = self.findStrCount( testdata, "NG" )
            if NGCount < 3:
                return True, Message
            pass
        except Exception as e:
            GlobalGui.WriteLog("CheckBarcodeThreeNG_RK", "异常：" + str(e))
            return False, "异常：" + str(e)
    def CheckBarcodeThreeNG_JP(self,API,sn,key,Prestation,doekeys):
        try:
            if API == "-" or key == "-":
                return True, "屏蔽捞取", "NA", "NA", "NA", "NA"
            coilKey="/processes/4be987fc-480e-44ff-85e4-b7697d093ecc"
            ConfigKey="/processes/71c2973c-eecf-4deb-895c-d99b78618116"
            coilSn = "NA-NULL"
            HSGConfig = "NA-NULL"

            self.writeUploadLog("开始检查条码 API:"+API)
            Url = API + sn
            Reback = self.HttpGetPassWord( Url )#self.readFile(r"C:\Users\GTS\Desktop\3.txt")#self.HttpGetPassWord( Url )
            if Reback == None:
                return False, "捞取数据超时", "NA", "NA", "NA", "NA"
            self.writeUploadLog( "获取数据\n" + Reback )

            tmpjson: dict = json.loads( Reback )
            count = 0
            Color = "NA-NULL"
            Model = "NA-NULL"

            list: dict = tmpjson["data"][0]["history"]
            # colorAndModel: dict = tmpjson["data"][0]["properties"]

            for item in list:
                process = item["links"]["process"]
                if coilKey in process:
                    coilSn= item["data"]["results"]["coil"]


            for item in list:
                process = item["links"]["process"]
                if ConfigKey in process:
                    HSGConfig= item["data"]["results"]["Config"]
                    Color = item["data"]["results"]["color"]
                    Model = item["data"]["results"]["model"]
                # if "Color" == item:
                #     Color = colorAndModel["Color"]
                # if "Model" == item:
                #     Model = colorAndModel["Model"]

            for item in list:
                process = item["links"]["process"]
                testResult = item["links"]["event"]
                if "/events/rework" == testResult:
                    break
                if key in process:  # and "pass" not in testResult:
                    count = count + 1

            self.writeUploadLog( "检查结果:Model-{0}  Color-{1}  TestCount-{2} CoilSn-{3} Config-{4}".format( Model, Color, count, coilSn, HSGConfig ) )

            #管控DOE
            if doekeys != "":
                for item in list:
                    process = item["links"]["process"]
                    if process in doekeys:  # and "pass" not in testResult:
                        return True, "DOE物料", Color, Model, coilSn, HSGConfig


            PreStationBool = Prestation == "-"
            for item in list:
                process = item["links"]["process"]
                testResult = item["links"]["event"]
                if "/events/rework" == testResult:
                    break
                if Prestation in process and "pass" in testResult:
                    PreStationBool = True
                    break

            if PreStationBool == False:
                return False, "上站点未pass", Color, Model, coilSn, HSGConfig

            if count >= 3:
                return False, "测试次数超过3次，不允许测试", Color, Model, coilSn, HSGConfig

            return True, "测试次数为：" + str( count ) + "  颜色：" + Color + "  型号：" + Model, Color, Model, coilSn, HSGConfig
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit( '捞取失败' + str( e ), 'red', False )
            return False, "捞取失败", "NA", "NA", "NA", "NA"
    # def CheckBarcodeThreeNG_JP(self, API, sn, key, Prestation):
    #     try:
    #         if API == "-" or key == "-":
    #             return True, "屏蔽捞取", "NA", "NA"
    #
    #         self.writeUploadLog("开始检查条码 API:" + API)
    #         Url = API + sn
    #         Reback = self.HttpGetPassWord(Url)
    #         if Reback == None:
    #             return False, "捞取数据超时", "NA", "NA"
    #         self.writeUploadLog("获取数据\n" + Reback)
    #
    #         tmpjson: dict = json.loads(Reback)
    #         count = 0
    #         Color = "NA"
    #         Model = "NA"
    #
    #         list: dict = tmpjson["data"][0]["history"]
    #         colorAndModel: dict = tmpjson["data"][0]["properties"]
    #
    #         for item in colorAndModel:
    #             if "Color" == item:
    #                 Color = colorAndModel["Color"]
    #             if "Model" == item:
    #                 Model = colorAndModel["Model"]
    #
    #         for item in list:
    #             process = item["links"]["process"]
    #             testResult = item["links"]["event"]
    #             if "/events/rework" == testResult:
    #                 break
    #             if key in process:  # and "pass" not in testResult:
    #                 count = count + 1
    #
    #         self.writeUploadLog("检查结果:Model-{0}  Color-{1}  TestCount-{2}".format(Model, Color, count))
    #
    #         PreStationBool = Prestation == "-"
    #         for item in list:
    #             process = item["links"]["process"]
    #             testResult = item["links"]["event"]
    #             if "/events/rework" == testResult:
    #                 break
    #             if Prestation in process and "pass" in testResult:
    #                 PreStationBool = True
    #
    #         if PreStationBool == False:
    #             return False, "上站点未pass", Color, Model
    #
    #         if count >= 3:
    #             return False, "测试次数超过3次，不允许测试", Color, Model
    #
    #         return True, "测试次数为：" + str(count) + "  颜色：" + Color + "  型号：" + Model, Color, Model
    #     except Exception as e:
    #         GlobalGui.global_Gui.TextBrowserSignal.emit('捞取失败' + str(e), 'red', False)
    #         return False, "捞取失败", "NA", "NA"
    def CheckBarcodeRework_MCEG(self, API,  sn, process_id):
        try:
            if API == "-" or process_id == "-":
                return True, "屏蔽捞取"

            result =False

            #Url = API + sn+"&process_name="+processname
            Url="http://17.239.117.210/api/v2/parts?serial_type=part_id&serial={0}".format(sn)
            self.writeUploadLog( "开始reWork检查 URL：" + Url )
            self.writeUploadLog("process_id ：" + process_id)
            Reback =self.HttpGetPassWord( Url )#self.readFile(r"C:\Users\GTS\Desktop\1.txt") #self.HttpGetPassWord( Url )
            if Reback == None:
                self.writeUploadLog( "获取返回失败")
                return False, "捞取数据超时"
            self.writeUploadLog( "返回的数据：" + str(Reback) )


            tmpjson: dict = json.loads( Reback )
            list: dict = tmpjson["history"]

            if list==None or len(list) == 0:
                return False, "测试数据为：0"

            Rework = 'null'
            for item in list:
                if item['process_id'] == process_id:
                    Rework = item["event"]
                    self.writeUploadLog("Rework:"+str(Rework))
                    if "rework" == Rework:
                        self.writeUploadLog("符合 rework")
                        result = True
                        break


            self.writeUploadLog( "测试reWork检查为：" + str( Rework ) )

            return result, "测试reWork检查为：" + str( Rework )
        except Exception as e:
            self.writeUploadLog( "Error：" + str( e ) )
            GlobalGui.global_Gui.TextBrowserSignal.emit( '捞取失败' + str( e ), 'red', False )
            return False, "捞取失败"


    def CheckBarcodeThreeNG_MCEG(self,API,sn,processname,NeedTestcount):
        try:
            if API == "-" or processname == "-":
                return True, "屏蔽捞取"

            #Url = API + sn+"&process_name="+processname
            Url="http://17.239.117.210/api/v2/parts?serial_type=part_id&serial={0}&process_name={1}".format(sn,processname)
            self.writeUploadLog( "开始卡控条码 URL：" + Url )
            Reback =self.HttpGetPassWord( Url )#self.readFile(r"C:\Users\GTS\Desktop\1.txt") #self.HttpGetPassWord( Url )
            if Reback == None:
                self.writeUploadLog( "获取返回失败")
                return False, "捞取数据超时"
            self.writeUploadLog( "返回的数据：" + str(Reback) )

            tmpjson: dict = json.loads( Reback )
            count = 0

            list: dict = tmpjson["history"]

            if list==None or len(list) == 0:
                return True, "测试NG次数为：0"

            for item in list:
                # Rework =  item["data"]["event"]
                # if "rework" == Rework:
                #     break
                testResult = item["data"]["insight"]["test_attributes"]["test_result"]
                if "pass" not in testResult:
                    count = count + 1

            if count >= NeedTestcount:
                return False, "测试NG次数超过3次，不允许测试"

            self.writeUploadLog( "测试NG次数为：" + str( count ) )

            return True, "测试NG次数为：" + str( count )
        except Exception as e:
            self.writeUploadLog( "Error：" + str( e ) )
            GlobalGui.global_Gui.TextBrowserSignal.emit( '捞取失败' + str( e ), 'red', False )
            return False, "捞取失败"

    def RTGetCoilConfig(self, sn):
        try:
            Url = "http://10.134.9.139:80/api/getMahicoilLink?serialNumber={0}".format(sn)
            self.writeUploadLog( "开始查询COIL 信息 URL：" + Url )

            Reback = self.HttpGet( Url )  # self.readFile(r"C:\Users\GTS\Desktop\coil.txt")#
            if Reback == None:
                return False, "获取超时","",""
            self.writeUploadLog( "COIL信息 结果：" + Reback )

            tmpjson = json.loads( Reback )
            Pass = str( tmpjson["success"] ).lower() == "true"
            if Pass == False:
                self.writeUploadLog( "COIL信息 结果：失败" )
                return False,str(tmpjson["message"]),"",""

            coilSN = tmpjson["data"]["data1"]
            coil_cfg = tmpjson["data"]["coil_cfg"]
            ferrite_cfg = tmpjson["data"]["ferrite_cfg"]

            self.writeUploadLog( "COIL信息 结果：成功--" + str( coilSN ) + "  " + str( coil_cfg ) + "  " + str( ferrite_cfg ))
            return True, coilSN, coil_cfg, ferrite_cfg
            pass
        except Exception as e:
            self.writeUploadLog( "GetCoil 异常：" + str( e ) )
            return False, "NA","NA","NA"

    def RTSnCheck(self, sn,station):
        try:
            Url = "http://10.134.9.139/api/getEachStationInfo?" \
                  "serialNumber={0}&station={1}&dbName=v2&from_wecom=1".format(sn,station)
            self.writeUploadLog( "开始查询三次锁定 信息 URL：" + Url )

            Reback = self.HttpGet( Url )  # self.readFile(r"C:\Users\GTS\Desktop\coil.txt")#
            if Reback == None:
                return False, "获取超时"
            self.writeUploadLog( "三次锁定 结果：" + Reback )

            tmpjson = json.loads( Reback )
            Pass = str( tmpjson["success"] ).lower() == "true"
            if Pass == False:
                self.writeUploadLog( "三次锁定 结果：失败" )
                return False,str(tmpjson["message"])

            Message = str( tmpjson["message"] )
            testdata = str( tmpjson["data"]["result"] )
            NGCount = self.findStrCount( testdata, "NG" )

            if NGCount < 3:
                return True, Message
            else:
                return False,"测试NG次数 已到三次"

        except Exception as e:
            self.writeUploadLog( "三次锁定 异常：" + str( e ) )
            return False, str(e)
    # 读取文件内容
    def readFile(self, fileName):
        with open(fileName, 'r') as f:
            return f.read()

    # 寻找字符串指定字符串的个数
    def findStrCount(self, str, subStr):
        count = str.count(subStr)
        return count

    #http get 账号密码
    def HttpGetPassWord(self, url):
        try:
            s = requests.session()
            s.auth = ('cm', 'password')
            response = s.get(url,timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit('捞取失败'+str(e), 'red', 0, False)
            return None

    def HttpGet(self, url):
        try:
            response = requests.get(url,timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit( 'HTTP GET ERROR' + str( e ), 'red', 0, False )
            return None

    def HttpPost(self, url, data):
        try:
            response = requests.post(url, data,timeout=10)
            return response.status_code==200,response.text
        except Exception as e:
            GlobalGui.global_Gui.TextBrowserSignal.emit( 'HTTP POST ERROR' + str( e ), 'red', 0, False )
            return False,e

class Responsebody:

    #initialization
    def __init__(self):
        print("Responsebody init")
        self.isOk = False
        self.erroMessage = ""


if __name__ == '__main__':
    isAlarm = False
    if True:
        ProcessID = '123'
        ReworkProcessID ='123'
        result_r, Message_r = False, '测试reWork检查为：null'
        print(f'rework判定结果：' + str(result_r) + '，rework判定信息：' + Message_r)
        if result_r:
            print(f'当前为rework不判定3次')
        else:
            print(f'当前不为rework开始判定3次')
            result, Message = True, '测试NG次数为：0'
            print(f'判定结果：' + str(result) + '，判定信息：' + Message)

            if not result:
                TestResult = False
                BarcodeFail = True
                isAlarm = True

    if isAlarm:
        pass
    try:
        process_id = 'b8b1c859-4245-47ab-b426-e49cc7e58739'
        with open('D:/Config/111.json', encoding='utf-8') as a:
            # 读取文件
            result : dict = json.load(a)
            list: dict = result["history"]

            Rework = 'null'
            for item in list:
                if item['process_id'] == process_id:
                    print(str(123))
                if process_id in item:
                    Rework = item["event"]
                    if "rework" == Rework:

                        result = True
                        break
        pass
    except Exception as e:
        print(str(e))

    # trace = cTrace()
    # trace.CheckBarcodeRework_MCEG("", "", "b8b1c859-4245-47ab-b426-e49cc7e58739")
#     re,mess,color,model= trace.CheckBarcodeThreeNG_JP("123456","12345","/processes/6f6b5eee-9acb-458b-b06b-2bf112f994c2","-")
#     print(str(re)+"------"+mess)

    # repp=trace.SnCheck("234")
    # print(str(repp.isOk)+repp.erroMessage)
    # TestItem=cTestItem()
    # TestItem.TestResult="pass"
    # TestItem.TestUnit="mohm"
    # TestItem.TestName="DCR"
    # TestItem.TestValue="254.085333333333"
    # TestItem.TestLowLimit="200"
    # TestItem.TestUpLimit="315"
    # testitems=[]
    # testitems.append(TestItem)
    # rep=trace.UploadJson("PASS","1234567890","2020-01-01 00:00:00","2020-01-01 00:00:00","10","123456","A","LineID","stationID","softName","softVersion","fixtureID","GoldenSampleSN","LastCheckTime",testitems)
    # print(str(repp.isOk)+repp.erroMessage)
    # print(trace.findStrCount("1234A674A94A","4A"))




