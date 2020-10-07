import time
import unittest

from common.driver_init import DriverInit
from common.driver_api import DriverApi as api
from config.zhengt_yun import *
from log.globallog import log
from common.decorators import deco_test_method_comment
from pages.zhengtyun.as_work_order import ASWorkOrder
from pages.zhengtyun.common import Common


class TestASCommon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        :return:
        """
        driver_init = DriverInit(is_headless=False)
        cls.driver = driver_init.driver
        api.driver = driver_init.driver
        api.get(as_work_order_list)

        token = Common.zhengt_yun_login()
        log.info('正通云平台token的值为[%s]'%token)
        api.driver.add_cookie({'name': 'token', 'value': token})



    @classmethod
    def tearDownClass(cls):
        """
        测试结束后的操作，这里基本上都是关闭浏览器
        :return:
        """
        cls.driver.quit()


    # def test_add(self):
    #     print('aaaa')
    #     self.fail()

    @deco_test_method_comment
    def test_as_addworkorder(self):
        '''查看首页是否显示正常'''
        try:
            api.get(as_work_order_list)
            as_workorder = ASWorkOrder()
            as_workorder.add_work_order(cpno)
            time.sleep(10)
        except:
            log.exception()




if __name__ == '__main__':
    unittest.main()