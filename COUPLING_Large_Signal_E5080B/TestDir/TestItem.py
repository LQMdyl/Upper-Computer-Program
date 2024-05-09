class cTestItem():
    TestName: str = ""
    TestUpLimit: str = ""
    TestLowLimit: str = ""
    TestUnit: str = ""
    TestValue: str = ""
    TestResult: bool = False

    def __init__(self):
        self.TestName = ""
        self.TestUpLimit = ""
        self.TestLowLimit = ""
        self.TestValue = ""
        self.TestUnit = ""
        self.TestResult = False

    def Clone(self):
        testItem = cTestItem()
        testItem.TestName = self.TestName
        testItem.TestValue = self.TestValue
        testItem.TestUnit = self.TestUnit
        testItem.TestUpLimit = self.TestUpLimit
        testItem.TestLowLimit = self.TestLowLimit
        testItem.TestResult = self.TestResult

        return testItem

    def Clear(self):
        self.TestName = ""
        self.TestUpLimit = ""
        self.TestLowLimit = ""
        self.TestValue = ""
        self.TestUnit = ""
        self.TestResult = False

    # <editor-fold desc="属性">

    # </editor-fold>

