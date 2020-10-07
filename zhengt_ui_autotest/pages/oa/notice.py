from common.driver_api import DriverApi as api
from log.globallog import log
from HTMLReport import logger

class Notice(api):
    notice_list_first_title = ('通知列表选项第一个标题', 'css', '#demoContent > li:nth-child(1) > a')
    notice_list_title = ('通知列表选项标题', 'css', '#demoContent > li > a')
    notice_list_publisher = ('通知列表选项发布者', 'css', '#demoContent > li > span:nth-child(3)')
    notice_list_publish_time = ('通知列表选项发布时间', 'css', '#demoContent > li > span:nth-child(2)')

    def wait_notice_list_first_title_exist(self):
        """
        通知列表选项标题
        :return:
        """
        return api.el_is_display(self.notice_list_first_title)

    def notice_list_title_els(self):
        """
        通知列表选项标题
        :return:
        """
        return api.wait_find_elements(self.notice_list_title)

    def notice_list_publisher_els(self):
        """
        通知列表选项标题
        :return:
        """
        return api.wait_find_elements(self.notice_list_publisher)

    def notice_list_publish_time_els(self):
        """
        通知列表选项标题
        :return:
        """
        return api.wait_find_elements(self.notice_list_publish_time)


    def notice_list_item_title_len_gt_0(self):
        """
        判断通知列表选项标题长度是否大于0
        :return:
        """
        self.wait_notice_list_first_title_exist()
        elements = self.notice_list_title_els()
        if len(elements) == 0:
            api.save_page_img('通知列表标题长度等于0')
            return False
        for el in elements:
            el_text = el.text
            logger().info('通知列表选项标题：%s' % el_text)
            if el_text is None or len(el_text) == 0:
                api.save_page_img('通知列表标题长度等于0')
                return False
        return True

    def notice_list_item_publisher_len_gt_0(self):
        """
        判断新闻列表页选项简介长度是否大于0
        :return:
        """
        self.wait_notice_list_first_title_exist()
        elements = self.notice_list_publisher_els()
        if len(elements) == 0:
            api.save_page_img('通知列表简介长度等于0')
            return False
        for el in elements:
            el_text = el.text
            logger().info('通知列表选项简介：%s' % el_text)
            if el_text is None or len(el_text) == 0:
                api.save_page_img('通知列表简介长度等于0')
                return False
        return True

    def notice_list_item_publish_time_len_gt_0(self):
        """
        判断新闻列表页选项简介长度是否大于0
        :return:
        """
        self.wait_notice_list_first_title_exist()
        elements = self.notice_list_publish_time_els()
        if len(elements) == 0:
            api.save_page_img('通知列表发布人长度等于0')
            return False
        for el in elements:
            el_text = el.text
            logger().info('通知列表选项发布者：%s' % el_text)
            if el_text is None or len(el_text) == 0:
                api.save_page_img('通知列表发布人长度等于0')
                return False
        return True





