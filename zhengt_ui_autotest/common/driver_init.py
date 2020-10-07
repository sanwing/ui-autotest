from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os,time, platform
from config.prd import chrome_user_data_for_linux, chrome_user_data_for_windows

from log.globallog import log

class DriverInit(object):

    def __init__(self, is_headless=True, page_load_timeout=60):
        self.is_headless = is_headless
        self.page_load_timeout = page_load_timeout
        self.driver = self.init_driver(is_headless, page_load_timeout)

    def init_driver(self, is_headless, page_load_timeout):
        """
        初始化浏览器
        :param is_headless:
        :return:
        """
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-browser-side-navigation')
        # 禁止加载图片
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--start-maximized')
        if is_headless:
            chrome_options.add_argument('--headless')
        if platform.system() == 'Windows':
            executable_path = os.path.join(os.getcwd(), 'static/driver/chromedriver.exe')
            print(executable_path)
            chrome_options.add_argument('--user-data-dir=%s'%chrome_user_data_for_windows)
            chrome_options.add_argument('--disk-cache-dir=%s'%chrome_user_data_for_windows)
            driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
            # if is_headless:
            #     driver.set_window_size(1600, 1200)
        else:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--user-data-dir=%s' % chrome_user_data_for_linux)
            chrome_options.add_argument('--disk-cache-dir=%s' % chrome_user_data_for_linux)
            driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
            driver.set_window_size(1600, 1200)
        driver.set_page_load_timeout(page_load_timeout)
        driver.set_script_timeout(page_load_timeout)
        return driver

    def restart_drvier(self):
        """
        浏览器关闭重新开启
        :param self:
        :return:
        """
        self.quit_driver()
        driver = self.init_driver(self.is_headless, self.page_load_timeout)
        self.driver = driver
        return driver

    def quit_driver(self):
        """
        将drvier退出
        :return:
        """
        if self.driver is None:
            return
        self.driver.quit()