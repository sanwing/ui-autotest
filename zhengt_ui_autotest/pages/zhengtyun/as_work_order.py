from common.driver_api import DriverApi as api
from log.globallog import log
import time, requests
from config.zhengt_yun import *

class ASWorkOrder(api):

    add_work_order_btn = ('新增工单按钮', 'xpath',
                          '//div[@class="page-content"]/div[2]/div/div[2]/div/div/button')
    select_cpno_btn = ('新增页面选择车牌按钮', 'xpath',
                       '//div[@id="workorder__scroll"]//div[@class="form-list"]/div[3]/div/div/div/button')
    select_cpno_window_cpno_input = ('选择车牌弹框中车牌输入框', 'xpath',
                                     '//div[@class="el-dialog__body"]/form/div[2]//input')
    select_cpno_window_search_btn = ('选择车牌弹框中搜索按钮', 'xpath',
                                     '//div[@class="el-dialog__body"]/div[1]/button')
    select_cpno_window_table_first_radio = ('选择车牌弹框中列表第一个单选按钮', 'xpath',
                                            '//div[@class="el-dialog__body"]/div[2]//tbody/tr/td/div/label/span')
    select_cpno_window_enter_btn = ('选择车牌弹框中确定按钮', 'xpath',
                                            '//div[@aria-label="车辆选择"]/div[@class="el-dialog__footer"]/div/button[2]/span')

    def click_add_work_order_btn(self):
        """点击新增工单按钮"""
        api.click_element(self.add_work_order_btn)

    def click_select_cpno_btn(self):
        """点击选择车牌按钮"""
        api.click_element(self.select_cpno_btn)

    def send_cpno_in_select_cpno_window(self, cpno):
        """在选择车牌弹出中输入车牌号"""
        api.send_text(self.select_cpno_window_cpno_input, cpno)

    def click_search_btn_in_select_cpno_window(self):
        """在选择车牌弹窗中点击搜索按钮"""
        api.click_element(self.select_cpno_window_search_btn)

    def click_table_first_in_select_cpno_window(self):
        """在选择车牌弹窗中点击第一个搜索结果"""
        api.click_element(self.select_cpno_window_table_first_radio)

    def click_enter_btn_in_select_cpno_window(self):
        """在选择车牌弹窗中点击确定按钮"""
        api.click_element(self.select_cpno_window_enter_btn)

    def add_work_order(self, cpno):
        """根据车牌号新增工单"""
        self.click_add_work_order_btn()
        self.click_select_cpno_btn()
        self.send_cpno_in_select_cpno_window(cpno)
        self.click_search_btn_in_select_cpno_window()
        time.sleep(4)
        self.click_table_first_in_select_cpno_window()
        time.sleep(5)
        self.click_enter_btn_in_select_cpno_window()










