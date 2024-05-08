import requests
import json
from GlobalDir.GlobalGui import cGlobalGui
from LogDir.AllLog import cAllLog
from datetime import datetime


class cCheckRole():
    def __init__(self, role: int, userName: str, password: str):
        self.role = role
        self.userName = userName
        self.password = password
        self.logname = datetime.now().strftime('%Y-%m-%d') + '_log'
        self.log = cAllLog(self.logname)

    def login(self):
        try:
            tmpjson = {}
            tmpjson['userName'] = self.userName
            tmpjson['password'] = self.password
            tmpjson['role'] = self.role
            tmpUrl = 'http://mycsmtetwebapi.mflex.com.cn/api/etresources/etauthentication'
            result, tmpstr = self.HttpPost(tmpUrl, json.dumps(tmpjson))
            if not result:
                return False, str(tmpstr)
            self.log.writelog(str(tmpstr))
            tmpdic = json.loads(tmpstr)
            self.log.writelog(str(tmpdic))
            if str(tmpdic['isSuccess']).lower() == 'true':
                self.log.writelog('用户名和密码正确')
                return True, ''
            else:
                self.log.writelog('用户名或密码错误')
                return False, str(tmpdic['message'])
        except Exception as e:
            return False, str(e)

    def HttpGet(self, url, timeout=10, params: dict = {}):
        try:
            headers = {'Accept-Language': 'zh-Hans,zh;q=0.9'}
            response = requests.get(url, timeout=timeout, headers=headers, params=params)
            print('url:', response.url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            return None

    def HttpPost(self, url, data, timeout=10):
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            response = requests.post(url, data, timeout=timeout, headers=headers)
            return response.status_code == 200, response.text
        except Exception as e:
            return False, e
