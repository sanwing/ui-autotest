import time
import unittest

from common.driver_init import DriverInit
from common.driver_api import DriverApi as api
from pages.oa.home import Home
from pages.oa.common import Common
from pages.oa.group_news import GroupNews
from pages.oa.notice import Notice
from pages.oa.workflow_center import WorkflowCenter
from config.prd import *
from log.globallog import log
from common.decorators import deco_test_method_comment


class TestOACommon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        :return:
        """

        driver_init = DriverInit(is_headless=False)
        cls.driver = driver_init.driver
        api.driver = driver_init.driver

        # try:
        #     driver_init = DriverInit(is_headless=False)
        #     cls.driver = driver_init.driver
        #     api.driver = driver_init.driver
        #     api.get(login_url)
        #     res = api.driver.get_cookies()
        #     cookie = res[0]['name'] + '=' + res[0]['value']
        #     api.cookie = cookie
        #     Common.oa_api_login(cookie)
        #     api.driver.add_cookie({'name': 'h3bpmportal', 'value': res[0]['value']})
        # except Exception as e:
        #     log.info('OA初始化失败，失败原因：%s'%str(e))
        #     cls.driver.quit()
        #     raise e


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

    def test_OA0_登录_期望接口登录成功(self):
        api.get(login_url)
        res = api.driver.get_cookies()
        cookie = res[0]['name'] + '=' + res[0]['value']
        api.cookie = cookie
        Common.oa_api_login(cookie)
        api.driver.add_cookie({'name': 'h3bpmportal', 'value': res[0]['value']})

    def test_OA首页显示是否正常_期望显示当前登录用户名(self):

        Common.get_url_pagehome()
        home = Home()
        self.assertTrue(home.home_link_text('首页'), '首\页链接显示错误')
        self.assertTrue(home.username_text(username), '导航栏右侧用户姓名显示错误')
        api.save_page_img_2_report('首页截图')
        api.close_window_retain_one()

    def test_OA新闻中心显示是否正常_期望新闻列表数据标题简介长度大于0(self):

        Common.get_url_pagehome()
        home = Home()
        home.click_group_news_link()
        api.switch_new_window()
        news = GroupNews()
        self.assertTrue(news.news_list_item_name_len_gt_0(), '新闻列表选项标题长度等于0')
        self.assertTrue(news.news_list_item_article_len_gt_0(), '新闻列表选项简介长度等于0')
        api.save_page_img_2_report('新闻中心截图')
        api.close_window_retain_one()

    def test_OA通知页面显示是否正常_期望列表数据标题发布者长度大于0(self):
        Common.get_url_pagehome()
        home = Home()
        home.click_notices_link()
        api.switch_new_window()
        notice = Notice()
        self.assertTrue(notice.notice_list_item_title_len_gt_0(), '通知列表选项标题长度等于0')
        self.assertTrue(notice.notice_list_item_publish_time_len_gt_0(), '通知列表选项标题长度等于0')
        self.assertTrue(notice.notice_list_item_publisher_len_gt_0(), '通知列表选项标题长度等于0')
        api.save_page_img_2_report('通知页面截图')
        api.close_window_retain_one()

    def test_OA流程中心我的代办是否显示正常_期望列表数据大于等于0(self):
        """查看流程中心是否显示正常"""
        Common.get_url_pagehome()
        home = Home()
        home.click_workflow_center_link()
        api.switch_new_window()
        workflow = WorkflowCenter()
        self.assertTrue(workflow.list_text(),'列表数据显示错误')
        api.save_page_img_2_report('我的代办页面截图')
        api.close_window_retain_one()

    def test_OA流程中心发起审批任务是否正常_期望新建审批任务成功(self):
        Common.get_url_pagehome()
        home = Home()
        home.click_workflow_center_link()
        api.switch_new_window()
        workflow = WorkflowCenter()
        total_start = workflow.get_count_of_my_initiate()
        log.info('未添加流程之前，我拟办的总数量个数：%d'%total_start)
        workflow.click_add_workflow_link()
        self.assertTrue(workflow.workflow_list_item_len_gt_0(), '流程列表数据显示错误')
        workflow.click_test_workflow_link()
        workflow.click_speed_test_workflow_link()
        api.switch_new_window()
        workflow.wait_speed_test_form_title_display()
        workflow.send_text_speed_test_form_name_input('王志山')
        workflow.select_mobile_speed_test_form_mobile_select()
        api.save_page_img_2_report('新增审批流程页面截图')
        workflow.click_speed_test_form_submit_btn()
        time.sleep(1)
        workflow.accept_alert()
        time.sleep(1)
        workflow.accept_alert()
        total_end = workflow.get_count_of_my_initiate()
        log.info('添加流程之后，我拟办的总数量个数：%d' % total_end)
        self.assertTrue((total_end-total_start == 1), '新增失败')
        api.close_window_retain_one()


if __name__ == '__main__':
    unittest.main()