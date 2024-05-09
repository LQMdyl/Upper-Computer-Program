import csv
import os
import time
import pathlib

from TestDir.TestItem import cTestItem


class cCsv():
    def __init__(self):
        self.Path= "D:/Log/CSVLog"

        if not os.path.exists("D:/"):
            self.Path="/vault/Log/CSVLog"

        if not os.path.exists(self.Path):
            os.mkdir(self.Path)

    def SaveCSVLog(self, dirName, fileName, project, Items, SN, StartTime, HSGVendor, CoilSn, CoilVendor, CoilFerrite,CT):
        try:
            self.SavePath = "{0}/{1}/{2}".format(self.Path, dirName, time.strftime("%Y-%m-%d", time.localtime()))

            if not os.path.exists(self.SavePath):
                os.makedirs(self.SavePath)
            if fileName == "": return "ERROR:文件名错误-CSVLog"
            File = "{0}/{1}".format(self.SavePath, fileName)
            PathFile = pathlib.Path(File)
            Bt = ["Project", "HSG Vender", "HSG SN", " Coil SN", "Coil Cfg", "Ferrite Cfg", "Test Start", "TestResult", "ErrorItem", "Test Ct", "HSG Config", "AIM Status"]
            Low = ["", "", "LSL", "", "", "", "", "", "", "", "", ""]
            High = ["", "", "USL", "", "", "", "", "", "", "", "", ""]
            Unit = ["", "", "Unit", "", "", "", "", "", "", "", "", ""]
            Value = [project, HSGVendor, SN, CoilSn,CoilVendor,CoilFerrite,StartTime,"","",CT,"",""]
            Result = True
            ErrorName = ""
            for num in Items:
                Tmp: cTestItem = num
                Bt.append(Tmp.TestName)
                Low.append(Tmp.TestLowLimit)
                High.append(Tmp.TestUpLimit)
                Unit.append(Tmp.TestUnit)
                Value.append(Tmp.TestValue)
                Result &= Tmp.TestResult
                if not Tmp.TestResult:
                    ErrorName += Tmp.TestName + ";"

            Value[7] = 'PASS' if Result else 'FAIL'
            Value[8] = ErrorName

            writeBT = not PathFile.is_file()

            with open(File, "a",newline='') as f:
                writer = csv.writer(f)
                if writeBT:
                    writer.writerow(Bt)
                    writer.writerow(High)
                    writer.writerow(Low)
                    writer.writerow(Unit)
                writer.writerow(Value)

            return "保存CSV文件成功"
        except Exception as e:
            return "ERROR:保存csv 失败"
            sigOutSignal.sig.sinOutAddLog.emit("ERROR:" + str(e))

    def SaveDOECSVLog(self, project,fileName, Items, SN, StartTime,HSGVendor,CoilSn,CoilVendor,CoilFerrite,CT):
        try:
            path= "D:/Log/DOE"
            self.SavePath = "{0}/{1}".format(path, time.strftime("%Y-%m-%d", time.localtime()))

            if not os.path.exists(self.SavePath):
                os.makedirs(self.SavePath)
            if fileName == "": return "ERROR:文件名错误-CSVLog"
            File = "{0}/{1}".format(self.SavePath, fileName)
            PathFile = pathlib.Path(File)
            Bt = ["Project", "HSG Vender", "HSG SN", " Coil SN", "Coil Cfg", "Ferrite Cfg", "Test Start", "TestResult",
                  "ErrorItem", "Test Ct", "HSG Config", "AIM Status"]
            Low = ["", "", "LSL", "", "", "", "", "", "", "", "", ""]
            High = ["", "", "LSL", "", "", "", "", "", "", "", "", ""]
            Unit = ["", "", "Unit", "", "", "", "", "", "", "", "", ""]
            Value = [project, HSGVendor, SN, CoilSn, CoilVendor, CoilFerrite, StartTime, "", "", CT, "", ""]
            Result = True
            ErrorName = ""
            for num in Items:
                Tmp: cTestItem = num
                Bt.append(Tmp.TestName)
                Low.append(Tmp.TestLowLimit)
                High.append(Tmp.TestUpLimit)
                Unit.append(Tmp.TestUnit)
                Value.append(Tmp.TestValue)
                Result &= Tmp.TestResult
                if not Tmp.TestResult:
                    ErrorName += Tmp.TestName + ";"

            Value[7] = 'PASS' if Result else 'FAIL'
            Value[8] = ErrorName

            writeBT = not PathFile.is_file()

            with open(File, "a",newline='') as f:
                writer = csv.writer(f)
                if writeBT:
                    writer.writerow(Bt)
                    writer.writerow(High)
                    writer.writerow(Low)
                    writer.writerow(Unit)
                writer.writerow(Value)

            return "保存CSV文件成功"
        except Exception as e:
            return "ERROR:保存csv 失败"
            sigOutSignal.sig.sinOutAddLog.emit("ERROR:" + str(e))

    def SaveUploadCSVLog(self, fileName, Items, SN, StartTime):
        try:
            UploadSavePath = "{0}".format("/vault/UPDCA/read")
            if not os.path.exists(UploadSavePath):
                os.makedirs(UploadSavePath)

            if fileName == "": return "ERROR:文件名错误-CSVLog"
            File = "{0}/{1}".format(UploadSavePath, fileName)
            PathFile = pathlib.Path(File)
            Bt = ["StartTime", "Barcode", "TestResult", "ErrorItem"]
            Low = ["Lower Limit---->", "", "", ""]
            High = ["Upper Limit---->", "", "", ""]
            Unit = ["Unit ---->", "", "", ""]
            Value = [StartTime, SN, "", ""]
            Result = False
            ErrorName = ""
            for num in Items:
                Tmp: cTestItem = num
                Bt.append(Tmp.TestName)
                Low.append(Tmp.TestLowLimit)
                High.append(Tmp.TestUpLimit)
                Unit.append(Tmp.TestUnit)
                Value.append(Tmp.TestValue)
                Result &= Tmp.TestResult
                if not Tmp.TestResult:
                    ErrorName += Tmp.TestName + ";"

            Value[2] = 'PASS' if Result else 'FAIL'
            Value[3] = ErrorName

            writeBT = not PathFile.is_file()

            with open(File, "a",newline='') as f:
                writer = csv.writer(f)
                if writeBT:
                    writer.writerow(Bt)
                    writer.writerow(High)
                    writer.writerow(Low)
                    writer.writerow(Unit)
                writer.writerow(Value)

            return "保存CSV文件成功"
        except Exception as e:
            return "ERROR:保存csv 失败"
            sigOutSignal.sig.sinOutAddLog.emit("ERROR:" + str(e))

    def RKSaveCSVLog(self,path,fileName, Items, SN, StartTime,product,source,line,station,shift,equipment,result,process):
        try:
            SavePath =path
            if not os.path.exists(SavePath):
                os.makedirs(SavePath)
            if fileName == "": return "ERROR:文件名错误-CSVLog"
            File = "{0}/{1}".format(SavePath, fileName)
            PathFile = pathlib.Path(File)
            Bt = ["site", "product", "source", "line", "station", "shift", "time","serial_number", "equipment_ID", "OK_NG",
                  "text1","text2","text3","text4","text5","text6","text7","text8","text9","process"]
            Value = ["RK", product, source, line, station, shift, StartTime,SN,equipment, result,
                     None,None,None,None,None,None,None,None,None,process]
            for num in Items:
                Tmp: cTestItem = num
                if Tmp.TestUpLimit== "NA" or Tmp.TestLowLimit== "NA" or Tmp.TestUpLimit== "-" or Tmp.TestLowLimit== "-":
                    continue
                Bt.append(str.format("{0}({1} {2}~{3} {4}_{5})",Tmp.TestName,Tmp.TestLowLimit,Tmp.TestUnit,
                                     Tmp.TestUpLimit,Tmp.TestUnit,Tmp.TestResult and "Pass" or "Fail"))
                Value.append(Tmp.TestValue)

            writeBT = not PathFile.is_file()
            with open(File, "a",newline='') as f:
                writer = csv.writer(f)
                if writeBT:
                    writer.writerow(Bt)
                writer.writerow(Value)

            return "保存CSV文件成功"
        except Exception as e:
            return "ERROR:保存csv 失败"
            sigOutSignal.sig.sinOutAddLog.emit("ERROR:" + str(e))