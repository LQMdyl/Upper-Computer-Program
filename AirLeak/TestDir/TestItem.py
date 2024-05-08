class cTestItem():
    TestName = str
    TestDisplayName = str
    TestPDCAPriority = str
    TestUpLimit = str
    TestLowLimit = str
    TestUnit = str
    TestValue = str
    TestResult = bool
    TestFailItem = str

    def __init__(self):
        self.TestName = ''
        self.TestDisplayName = 'N/A'
        self.TestPDCAPriority = 'N/A'
        self.TestUpLimit = ''
        self.TestLowLimit = ''
        self.TestValue = ''
        self.TestUnit = ''
        self.TestResult = False
        self.TestFailItem = ''

    def Clone(self):
        testItem = cTestItem()
        testItem.TestName = self.TestName
        testItem.TestDisplayName = self.TestDisplayName
        testItem.TestPDCAPriority = self.TestPDCAPriority
        testItem.TestValue = self.TestValue
        testItem.TestUnit = self.TestUnit
        testItem.TestUpLimit = self.TestUpLimit
        testItem.TestLowLimit = self.TestLowLimit
        testItem.TestResult = self.TestResult
        testItem.TestFailItem = self.TestFailItem
        return testItem

    def Clear(self):
        self.TestName = ''
        self.TestDisplayName = 'N/A'
        self.TestPDCAPriority = 'N/A'
        self.TestUpLimit = ''
        self.TestLowLimit = ''
        self.TestValue = ''
        self.TestUnit = ''
        self.TestResult = False
        self.TestFailItem = ''
    # <editor-fold desc="属性">

    # </editor-fold>

class cUploadItem():
    def __init__(self):
        self.ApiAddress = ''
        self.ApiPath = ''
        self.Barcode = ''
        self.OperatorID = ''
        self.ToolNumber = ''
        self.PreviousTestType = ''
        self.TestType = ''
        self.ProductName = ''
        self.WorkArea = ''
        self.Site = ''
        self.slotName = ''
        self.subslotName = ''
        self.Program = ''
        self.Lot = ''
        self.IpAddress = ''
        self.StationTime = ''
        self.TestTime = ''
        self.TestResult = ''
        self.ResourceName = ''
        self.ErrorCode = ''

    def Clone(self):
        uploadItem = cUploadItem()
        uploadItem.ApiAddress = self.ApiAddress
        uploadItem.ApiPath = self.ApiPath
        uploadItem.Barcode = self.Barcode
        uploadItem.OperatorID = self.OperatorID
        uploadItem.ToolNumber = self.ToolNumber
        uploadItem.PreviousTestType = self.PreviousTestType
        uploadItem.TestType = self.TestType
        uploadItem.ProductName = self.ProductName
        uploadItem.WorkArea = self.WorkArea
        uploadItem.Site = self.Site
        uploadItem.slotName = self.slotName
        uploadItem.subslotName = self.subslotName
        uploadItem.Program = self.Program
        uploadItem.Lot = self.Lot
        uploadItem.IpAddress = self.IpAddress
        uploadItem.StationTime = self.StationTime
        uploadItem.TestTime = self.TestTime
        uploadItem.TestResult = self.TestResult
        uploadItem.ResourceName = self.ResourceName
        uploadItem.ErrorCode = self.ErrorCode
        return uploadItem

    def Clear(self):
        self.ApiAddress = ''
        self.ApiPath = ''
        self.Barcode = ''
        self.OperatorID = ''
        self.ToolNumber = ''
        self.PreviousTestType = ''
        self.TestType = ''
        self.ProductName = ''
        self.WorkArea = ''
        self.Site = ''
        self.slotName = ''
        self.subslotName = ''
        self.Program = ''
        self.Lot = ''
        self.IpAddress = ''
        self.StationTime = ''
        self.TestTime = ''
        self.TestResult = ''
        self.ResourceName = ''
        self.ErrorCode = ''

class cItem():
    def __init__(self):
        self.barcode = ''
        self.testType = ''
        self.testTime = ''
        self.testResult = ''
        self.Operator = ''
        self.workArea = ''
        self.resourceName = ''
        self.ipAddress = ''
        self.toolNumber = ''
        self.errorCode = ''
        self.errorValue = ''
        self.productName = ''
        self.program = ''
        self.slotName = ''
        self.subslotName = ''
        self.socketInfo = ''
        self.rosalineInfo = ''
        self.testDetailId = ''
        self.attribute1 = ''
        self.attribute2 = ''
        self.dartfishInfo = ''
        self.extendInfo = ''
        self.testDetails = cTestDetails()

    def Clone(self):
        item = cItem()
        item.barcode = self.barcode
        item.testType = self.testType
        item.testTime = self.testTime
        item.testResult = self.testResult
        item.Operator = self.Operator
        item.workArea = self.workArea
        item.resourceName = self.resourceName
        item.ipAddress = self.ipAddress
        item.toolNumber = self.toolNumber
        item.errorCode = self.errorCode
        item.errorValue = self.errorValue
        item.productName = self.productName
        item.program = self.program
        item.slotName = self.slotName
        item.subslotName = self.subslotName
        item.socketInfo = self.socketInfo
        item.rosalineInfo = self.rosalineInfo
        item.testDetailId = self.testDetailId
        item.attribute1 = self.attribute1
        item.attribute2 = self.attribute2
        item.dartfishInfo = self.dartfishInfo
        item.extendInfo = self.extendInfo
        item.testDetails = self.testDetails.Clone()
        return item

    def Clear(self):
        self.barcode = ''
        self.testType = ''
        self.testTime = ''
        self.testResult = ''
        self.Operator = ''
        self.workArea = ''
        self.resourceName = ''
        self.ipAddress = ''
        self.toolNumber = ''
        self.errorCode = ''
        self.errorValue = ''
        self.productName = ''
        self.program = ''
        self.slotName = ''
        self.subslotName = ''
        self.socketInfo = ''
        self.rosalineInfo = ''
        self.testDetailId = ''
        self.attribute1 = ''
        self.attribute2 = ''
        self.dartfishInfo = ''
        self.extendInfo = ''
        self.testDetails.Clear()

class cTestDetails():
    def __init__(self, header = '', value = '', measureUnit = '', upperLimit = '', lowerLimit = ''):
        self.header = header
        self.upperLimit = upperLimit
        self.lowerLimit = lowerLimit
        self.measureUnit = measureUnit
        self.value = value

    def Clone(self):
        testDetails = cTestDetails()
        testDetails.header = self.header
        testDetails.upperLimit = self.upperLimit
        testDetails.lowerLimit = self.lowerLimit
        testDetails.measureUnit = self.measureUnit
        testDetails.value = self.value
        return testDetails

    def Clear(self):
        self.header = ''
        self.upperLimit = ''
        self.lowerLimit = ''
        self.measureUnit = ''
        self.value = ''

class cTestResult():
    def __init__(self):
        self.isSuccess = False
        self.message = ''
        self.currentTime = ''
        self.extensionCode = '0'
        self.extensionMessages = cExtensionMessages()
        self.targetTestType = ''

class cExtensionMessages():
    def __init__(self):
        self.barcodeFamily = ''
        self.testedCount = ''

class cUser():
    def __init__(self):
        self.user = ''
        self.pwd = ''
        self.role = 0

class cReturnMessage():
    def __init__(self):
        self.isOk = False
        self.message = ''