from common.driver_api import DriverApi as api
from HTMLReport import logger
import time, requests
from config.prd import *

class WorkflowCenter(api):
    unfinish_workflow_list_no_data = ('待办任务列表', 'css', '#tabUnfinishWorkitem > tbody > tr > td')
    unfinish_workflow_list_has_data = ('待办任务列表', 'css', '#tabUnfinishWorkitem > tbody > tr:nth-child(1) > '
                                                        'td:nth-child(2) > a')
    add_workflow_link = ('新建流程链接', 'css', 'ul.navleft.nav.ng-scope > li:nth-child(6) > a')
    my_initiate_link = ('我拟办的链接', 'css', 'ul.navleft.nav.ng-scope > li:nth-child(4) > a')
    my_initiate_list_first_item = ('我拟办的列表第一条记录', 'css', '#tabMyInstance > tbody > tr:nth-child(1)')
    my_initiate_count = ('我拟办的总数量', 'id', 'tabMyInstance_info')
    add_workflow_list = ('流程列表', 'css', '#MyWorkflowTable > tbody > tr > td:nth-child(1) > a')
    test_workflow_link = ('test链接', 'link_text', 'test')
    speed_test_workflow_link = ('生产环境速度测试专用链接', 'link_text', '生产环境速度测试专用')
    speed_test_form_title = ('生产环境速度测试表单-标题', 'id', 'lblTitle')
    speed_test_form_name_input = ('生产环境速度测试表单-姓名', 'id', 'Control11')
    speed_test_form_mobile_select = ('生产环境速度测试表单-手机', 'css', '#control2 > select >option:nth-child(2)')
    speed_test_form_save_btn = ('生产环境速度测试表单-保存按钮', 'css', '#divTopBars > li:nth-child(1) > a > span')
    speed_test_form_liushuihao_no = ('生产环境速度测试表单-流水号', 'css', '#lblSequenceNo')
    speed_test_form_submit_btn = ('生产环境速度测试表单-提交按钮', 'css', '#divTopBars > li:nth-child(3) > a')


    def list_text(self):
        if api.el_is_display(self.unfinish_workflow_list_has_data):
            text = api.get_text(self.unfinish_workflow_list_has_data)
            logger().info('待办任务列表选项标题：%s'%text)
            if len(text) > 0:
                return True
            else:
                return False
        elif api.get_text(self.unfinish_workflow_list_no_data) == '您的待办已经全部处理完成':
            return True
        else:
            api.save_page_img('待办列表显示错误')
            return False

    def click_test_workflow_link(self):
        api.click_element(self.test_workflow_link)

    def click_speed_test_workflow_link(self):
        api.click_element(self.speed_test_workflow_link)

    def wait_speed_test_form_title_display(self):
        api.el_is_display(self.speed_test_form_title)

    def click_speed_test_form_save_btn(self):
        api.click_element(self.speed_test_form_save_btn)

    def click_speed_test_form_submit_btn(self):
        api.click_element(self.speed_test_form_submit_btn)

    def send_text_speed_test_form_name_input(self, name):
        api.send_text(self.speed_test_form_name_input, name)

    def select_mobile_speed_test_form_mobile_select(self):
        api.click_element(self.speed_test_form_mobile_select)


    def click_add_workflow_link(self):
        """
        点击新建流程链接
        :return:
        """
        js = '$("ul.navleft >li:eq(5) > a").click()'
        for i in range(10):
            try:
                api.execute_script(js)
                if api.get_current_url().find('/app/Workflow/MyWorkflow') != -1 and api.el_is_display(self.test_workflow_link):
                    logger().info('页面跳转成功')
                    break
            except:
                pass
            time.sleep(2)

    def click_my_initiate_link(self):
        """
        点击我拟办的链接
        :return:
        """
        js = '$("ul.navleft >li:eq(3) > a").click()'
        for i in range(10):
            try:
                api.execute_script(js)
                if api.get_current_url().find('/app/Workflow/MyInstance') != -1:
                    logger().info('页面跳转成功')
                    break
            except:
                pass
            time.sleep(2)

    def get_count_of_my_initiate(self):
        """通过接口获取我拟办的总数量"""
        headers = {'Cookie': api.cookie, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        data = my_initiate_api_data
        res = requests.get(my_initiate_api_url, data=data, headers=headers)
        logger().info(res.text)
        total = res.json()['Total']
        return total

    def workflow_list_items(self):
        return api.wait_find_elements(self.add_workflow_list)

    def workflow_list_item_len_gt_0(self):
        elements = self.workflow_list_items()
        if len(elements) == 0:
            logger().info('元素列表长度为0')
            return False
        for el in self.workflow_list_items():
            el_text = el.text
            print(el_text)
            if el_text is None or len(el_text) == 0:
                return False
        return True


    def workflow_form_liushihao_text_valide(self):
        """
        验证流程新建成功后，生成一个流水号
        :return:
        """
        return api.wait_text_contains(self.speed_test_form_liushuihao_no, time.strftime("%Y%m"))






