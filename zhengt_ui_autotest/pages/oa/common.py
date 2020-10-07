import requests, time
from config.prd import *
from HTMLReport import logger
from pages.oa.custom_exception import LoginError
from  common.driver_api import DriverApi

class Common(object):

    @staticmethod
    def oa_api_login(cookie):
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie
        }
        data = {
            'userCode': user_code,
            'password': user_password,
            'rendom': int(time.time())
        }
        res_raw = requests.post(login_api, json=data, headers=headers, verify=False)
        res = res_raw.json()
        if res['Success'] and res['User']['Code'] == user_code:
            # res_headers = res_raw.headers
            # if 'Set-Cookie' in res_headers:
            #     new_cookie = res_headers['Set-Cookie'].split('; ')[0]
            # print(res_headers)
            logger().info('接口登录成功')
        else:
            logger().info('接口登录失败,返回信息：\n%s'%res)
            error_msg = '接口URL：%s;\n 接口请求参数：%s;\n 接口请求头信息：%s;\n 接口返回数据：%s'%(
                login_api, data, headers, res_raw.text
            )
            raise LoginError('接口登录失败,返回信息：%s'%error_msg)


    @staticmethod
    def get_url_pagehome():
        """判断当前页面地址是否为首页，非首页则跳转到首页"""
        if DriverApi.get_current_url() == index_url:
            return
        else:
            DriverApi.get(index_url)