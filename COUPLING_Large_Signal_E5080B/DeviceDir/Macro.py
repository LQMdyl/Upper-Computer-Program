from enum import Enum


class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("这是const常量  (%s)" % key)
        self.__dict__[key] = value


const = _const()
MCU = "MCU"
SCAN = "SCAN"
CAMREA = "CAMREA"
ROBOT_2002 = "ROBOT_2002"
ROBOT_2001 = "ROBOT_2001"
LCR = "LCR"
VNA = "VNA"
HWAK = "HWAK"
TEMP = 'TEMP'
SUR_TEMP = 'SUR_TEMP'
OSC = 'OSC'

PASS="PASS"
FAIL="FAIL"
IDEL="IDEL"
TEST="TEST"

INFO=1
DEBUG=2
WARNING=3
ERROR=4

TYPE_4XX = "J4XX"
TYPE_5XX = "J5XX"
TYPE_6XX = "J6XX"
TYPE_7XX = "J7XX"
ADDRESS_CD_MCEG = "CD_MCEG"   # 成都MCEG
ADDRESS_CD_JP= "CD_JP"   # 成都JP
ADDRESS_YC_LIKAI= "YC_LIKAI"   # 盐城立凯

class cColor(Enum):
    red = 1
    orange = 2
    yellow = 3
    green = 4
    blue = 5
    indigo = 6
    puiple = 7

