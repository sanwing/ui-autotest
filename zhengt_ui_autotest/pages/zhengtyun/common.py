import requests
from config.zhengt_yun import *
from log.globallog import log

class Common(object):

    @staticmethod
    def zhengt_yun_login():
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'userLoginName': username,
            'password': password
        }
        res = requests.post(login_url, json=data, headers=headers, verify=False)
        token = res.json()['data']
        log.info('token:%s'%token)
        return token

