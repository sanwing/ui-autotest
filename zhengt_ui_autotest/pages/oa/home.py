from common.driver_api import DriverApi as api

class Home(api):

    home_link = ('首页链接', 'link_text', '首页')
    group_news_link = ('新闻中心链接', 'link_text', '新闻中心')
    notices_link = ('通知公告链接', 'link_text', '通知公告')
    workflow_center_link = ('流程中心链接', 'link_text', '流程中心')
    username = ('导航栏右侧用户姓名', 'id', 'head-userName')

    def home_link_text(self, expect_value):
        """
        获取首页链接文本
        :return:
        """
        if api.wait_text_equal(self.home_link, expect_value):
            return True
        else:
            api.save_page_img('首页链接文本显示错误')
            return False

    def username_text(self, expect_value):
        """
        获取导航栏右侧的用户姓名
        :return:
        """
        if api.wait_text_equal(self.username, expect_value):
            return True
        else:
            api.save_page_img('首页用户名显示错误')
            return False

    def click_group_news_link(self):
        api.click_element(self.group_news_link)

    def click_notices_link(self):
        api.click_element(self.notices_link)

    def click_workflow_center_link(self):
        api.click_element(self.workflow_center_link)




