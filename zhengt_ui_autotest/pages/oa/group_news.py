from common.driver_api import DriverApi as api
from HTMLReport import logger

class GroupNews(api):
    news_list_first_item_name = ('新闻列表第一个选项标题', 'css', '.news-introduce > div:nth-child(2) > div.plate-content > div.plate-title > a')
    news_list_name = ('新闻列表选项标题', 'css', '.news-introduce > div.news-plate > div.plate-content > div.plate-title > a')
    news_list_article = ('新闻列表选项简介', 'css', '.news-introduce > div.news-plate > div.plate-content > div.plate-article > a')

    def news_list_first_item_name_exist(self):
        """
        新闻列表选项标题
        :return:
        """
        return api.wait_find_elements(self.news_list_first_item_name)

    def news_list_name_els(self):
        """
        新闻列表选项标题
        :return:
        """
        return api.wait_find_elements(self.news_list_name)

    def news_list_article_els(self):
        """
        新闻列表选项标题
        :return:
        """
        return api.wait_find_elements(self.news_list_article)

    def news_list_item_name_len_gt_0(self):
        """
        判断新闻列表选项标题长度是否大于0
        :return:
        """
        self.news_list_first_item_name_exist()
        elements = self.news_list_name_els()
        for el in elements:
            el_text = el.text
            logger().info('新闻列表选项标题：%s' % el_text)
            if el_text is None or len(el_text) == 0:
                api.save_page_img('新闻列表选项标题长度等于0')
                return False
        return True

    def news_list_item_article_len_gt_0(self):
        """
        判断新闻列表页选项简介长度是否大于0
        :return:
        """
        self.news_list_first_item_name_exist()
        elements = self.news_list_article_els()
        for el in elements:
            el_text = el.text
            logger().info('新闻列表选项简介：%s'%el_text)
            if el_text is None or len(el_text) == 0:
                api.save_page_img('新闻列表选项简介长度等于0')
                return False
        return True





