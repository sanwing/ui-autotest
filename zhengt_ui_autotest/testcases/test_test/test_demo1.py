import unittest
from common.decorators import deco_test_method_comment
from common.driver_init import DriverInit
from common.driver_api import DriverApi as api
from log.globallog import log

from HTMLReport import logger


class Demo1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        :return:
        """
        driver_init = DriverInit(is_headless=False)
        cls.driver = driver_init.driver
        api.driver = driver_init.driver


    @classmethod
    def tearDownClass(cls):
        """
        测试结束后的操作，这里基本上都是关闭浏览器
        :return:
        """
        cls.driver.quit()

    # @deco_test_method_comment
    # def test_add(self):
    #     api.get('https://baidu.com')
    #     self.fail()

    def test_OA首页显示正常(self):
        '''查看首页是否显示正常'''
        api.get('https://baidu.com')
        # Common.get_url_pagehome()
        # home = Home()
        # self.assertTrue(home.home_link_text('首页'), '首\页链接显示错误')
        # self.assertTrue(home.username_text(username), '导航栏右侧用户姓名显示错误')
        # api.save_page_img('首页截图')
        # api.close_window_retain_one()


if __name__ == '__main__':
    unittest.main()
