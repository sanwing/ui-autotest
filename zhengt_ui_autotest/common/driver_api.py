# coding=utf-8

import os, platform
import time
import random
import base64

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from common.custom_error import TypeError
from selenium.common.exceptions import NoSuchWindowException
from HTMLReport import logger, AddImage


# 项目根目录
base_dir = os.getcwd()

Loc_Type = {
    "xpath": By.XPATH,
    "id": By.ID,
    "name": By.NAME,
    "css_selector": By.CSS_SELECTOR,
    "class_name": By.CLASS_NAME,
    "tag_name": By.TAG_NAME,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT
}

LOCATED_TYPE = [
    'ID',
     'XPATH',
     'LINK_TEXT',
     'PARTIAL_LINK_TEXT',
     'NAME',
     'TAG_NAME',
     'CLASS_NAME',
     'CSS_SELECTOR'
]

ELE_TIMEOUT = 30
RETRY_TIMES = 2

class TimeoutException(WebDriverException):
    """
    Thrown when a command does not complete in enough time.
    """
    pass


class DriverApi():
    """
    selenium 常用方法封装
    """

    driver = None


    # def __init__(DriverApi, driver, timeout=15, retry_times=2):
    #     DriverApi.timeout = timeout
    #     DriverApi.retry_times = retry_times

    @staticmethod
    def get(url):
        try:
            DriverApi.driver.get(url)
            logger().info('访问[%s]成功!!!' % url)
        except:
            logger().info('页面加载超时，尝试获取页面url地址')
            current_url = DriverApi.driver.current_url
            logger().info(current_url)

    @staticmethod
    def refresh():
        """
        刷新页面，此处在刷新出现异常时，未抛出异常，主要考虑有些情况，页面已经显示出来，但是仍在加载中，此时如果加载
        时间超过页面默认加载时间，则会抛出异常，为了程序正常往下执行，故在只是捕获异常，并未抛出
        :return:
        """
        try:
            DriverApi.driver.refresh()
            logger().info('刷新页面成功，当前页面url为：[%s]'%DriverApi.driver.current_url)
        except:
            logger().info('刷新页面出现异常，程序继续往下执行')

    @staticmethod
    def get_current_url():
        try:
            url = DriverApi.driver.current_url
            logger().info('获取当前页面的URL地址成功，当前页面url为：[%s]'%url)
            return url
        except Exception as e:
            logger().info('获取当前页面的URL地址出现异常')
            raise e

    @staticmethod
    def _find_element(type, value):
        if type.upper() == 'ID':
            el = DriverApi.driver.find_element_by_id(value)
        elif type.upper() == 'XPATH':
            el = DriverApi.driver.find_element_by_xpath(value)
        elif type.upper() == 'CSS':
            el = DriverApi.driver.find_element_by_css_selector(value)
        elif type.upper() == 'TAG':
            el = DriverApi.driver.find_element_by_tag_name(value)
        elif type.upper() == 'PARTIAL_LINK_TEXT':
            el = DriverApi.driver.find_element_by_partial_link_text(value)
        elif type.upper() == 'CLASS_NAME':
            el = DriverApi.driver.find_element_by_class_name(value)
        elif type.upper() == 'LINK_TEXT':
            el = DriverApi.driver.find_element_by_link_text(value)
        else:
            logger().info('类型错误，请检查类型是否正确')
            raise TypeError('类型错误，请检查类型是否正确')
        return el

    @staticmethod
    def _find_elements(type, value):
        if type.upper() == 'XPATH':
            el = DriverApi.driver.find_elements_by_xpath(value)
        elif type.upper() == 'CSS':
            el = DriverApi.driver.find_elements_by_css_selector(value)
        elif type.upper() == 'TAG':
            el = DriverApi.driver.find_elements_by_tag_name(value)
        elif type.upper() == 'PARTIAL_LINK_TEXT':
            el = DriverApi.driver.find_elements_by_partial_link_text(value)
        elif type.upper() == 'CLASS_NAME':
            el = DriverApi.driver.find_elements_by_class_name(value)
        elif type.upper() == 'LINK_TEXT':
            el = DriverApi.driver.find_elements_by_link_text(value)
        else:
            logger().info('类型错误，请检查类型是否正确')
            raise TypeError('类型错误，请检查类型是否正确')
        return el


    @staticmethod
    def _wait_find_element(value, timeout):
        el_name, type, pattern = value[0], value[1], value[2]
        end_time = time.time() + timeout
        while True:
            try:
                el = DriverApi._find_element(type, pattern)
                logger().info('查找元素[%s]成功，查找方式[%s], 查找表达式[%s]' % (el_name, type, pattern))
                return el
            except TypeError as e:
                raise TypeError(e)
            except Exception as e:
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        logger().info('查找元素[%s]超时，元素不存在，查找方式[%a], 查找表达式[%s]' % (el_name, type, pattern))
        DriverApi._save_error_img()
        raise TimeoutException('查找元素超时')

    @staticmethod
    def wait_find_elements(value, timeout=ELE_TIMEOUT):
        el_name, type, pattern = value[0], value[1], value[2]
        end_time = time.time() + timeout
        while True:
            try:
                el = DriverApi._find_elements(type, pattern)
                logger().info('查找元素[%s]成功，查找方式[%s], 查找表达式[%s]' % (el_name, type, pattern))
                return el
            except TypeError as e:
                raise TypeError(e)
            except Exception as e:
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        logger().info('查找元素[%s]超时，元素不存在，查找方式[%a], 查找表达式[%s]' % (el_name, type, pattern))
        DriverApi._save_error_img()
        raise TimeoutException('查找元素超时')

    @staticmethod
    def el_is_exits(value, timeout=ELE_TIMEOUT):
        """
        查找元素是否存在，存在返回元素，否则返回False
        :param type:
        :param value:
        :param timeout:
        :return:
        """
        try:

            el = DriverApi._wait_find_element(value, timeout)
            logger().info('元素存在')
            return el
        except:
            logger().info('元素不存在')
            return False

    @staticmethod
    def el_is_display(value, timeout=ELE_TIMEOUT):
        """
        查找元素是否存在，存在返回元素，否则返回False
        :param type:
        :param value:
        :param timeout:
        :return:
        """
        try:
            el = DriverApi._wait_find_element( value, timeout)
            res = el.is_displayed()
            if res:
                logger().info('元素显示')
            else:
                logger().info('元素不显示')
            return res
        except:
            return False

    @staticmethod
    def click_element(value, timeout=ELE_TIMEOUT):
        """
        点击元素
        :param type:
        :param value:
        :param timeout:
        :return:
        """
        try:
            el = DriverApi._wait_find_element( value, timeout)
            el.click()
            logger().info('点击元素成功')
        except Exception as e:
            logger().info('点击元素出现异常')
            logger().exception(e)
            raise e

    @staticmethod
    def set_window_size_of_linux(x=1600, y=1200):
        if platform.system() != 'Windows':
            DriverApi.driver.set_window_size(x, y)

    @staticmethod
    def send_text(value, content, timeout=ELE_TIMEOUT):
        """
        文本框输入文本
        :param type:
        :param value:
        :param timeout:
        :return:
        """
        try:
            el = DriverApi._wait_find_element( value, timeout)
            el.clear()
            el.send_keys(content)
            logger().info('输入文本成功，输入的文本内容为：[%s]'%content)
        except Exception as e:
            logger().info('输入文本内容[%s]出现异常'%content)
            raise e

    @staticmethod
    def get_text(value, timeout=ELE_TIMEOUT):
        """
        获取元素文本内容
        :param type:
        :param value:
        :param time:
        :return:
        """
        try:
            el = DriverApi._wait_find_element(value, timeout)
            content = el.text
            logger().info('获取文本内容成功，文本内容为：[%s]' % content)
            return content
        except Exception as e:
            logger().info('获取文本内容出现异常')
            raise e

    @staticmethod
    def wait_text_equal(value, content, timeout=ELE_TIMEOUT):
        end_time = time.time() + timeout
        while True:
            try:
                el = DriverApi._wait_find_element(value, ELE_TIMEOUT)
                actual_value = el.text
                if content == actual_value:
                    logger().info('获取文本内容成功，文本内容为：[%s]' % actual_value)
                    return actual_value
                else:
                    logger().info('本次获取到的文本内容为：[%s]'%actual_value)
            except Exception as e:
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        return False


    @staticmethod
    def wait_text_contains(value, content, timeout=ELE_TIMEOUT):
        end_time = time.time() + timeout
        while True:
            try:
                el = DriverApi._wait_find_element(value, timeout)
                actual_value = el.text
                if actual_value.find(content) != -1:
                    logger().info('获取文本内容成功，文本内容为：[%s]' % actual_value)
                    return actual_value
            except Exception as e:
                pass
            time.sleep(1)
            if time.time() > end_time:
                break
        return False

    @staticmethod
    def switch_new_window():
        """
        切换到新窗口
        :return:
        """
        cur_window = DriverApi.driver.current_window_handle
        windows = DriverApi.driver.window_handles
        logger().info('当前窗口为[%s], 窗口总个数%d' % (cur_window, len(windows)))
        if len(windows) > 1:
            DriverApi.driver.switch_to.window(windows[len(windows)-1])
            active_window = DriverApi.driver.current_window_handle
            if active_window != cur_window:
                logger().info('窗口切换成功，当前窗口为[%s]'%active_window)
                DriverApi.set_window_size_of_linux()
        else:
            logger().info('窗口总个数小于2，无法进行切换')

    @staticmethod
    def close_window_retain_one():
        while True:
            windows = DriverApi.driver.window_handles
            window_length = len(windows)
            logger().info('当前窗口总个数%d'%window_length)
            if window_length > 1:
                try:
                    DriverApi.driver.switch_to.window(windows[-1])
                    DriverApi.driver.close()
                    if window_length == 2:
                        DriverApi.driver.switch_to.window(windows[0])
                    logger().info('窗口关闭成功')
                except NoSuchWindowException:
                    logger().info('目标窗口已经关闭')
                time.sleep(1)
            else:
                break

    @staticmethod
    def accept_alert():
        try:
            DriverApi.driver.switch_to.alert.accept()
        except Exception as e:
            logger().info('当前页面没有alert弹窗')

    @staticmethod
    def dismiss_alert():
        try:
            DriverApi.driver.switch_to.alert.dismiss()
        except Exception as e:
            logger().info('当前页面没有alert弹窗')

    @staticmethod
    def execute_script(js):
        DriverApi.driver.execute_script(js)
        logger().info('执行js成功')

    @staticmethod
    def get_locator(type, value):
        if type is None or value is None:
            return None
        if type.upper() not in LOCATED_TYPE:
            return None
        if type.upper() == 'ID':
            return By.ID, value
        elif type.upper() == 'XPATH':
            return By.XPATH, value
        elif type.upper() == 'LINK_TEXT':
            return By.LINK_TEXT, value
        elif type.upper() == 'PARTIAL_LINK_TEXT':
            return By.PARTIAL_LINK_TEXT, value
        elif type.upper() == 'NAME':
            return By.NAME, value
        elif type.upper() == 'TAG_NAME':
            return By.TAG_NAME, value
        elif type.upper() == 'CLASS_NAME':
            return By.CLASS_NAME, value
        elif type.upper() == 'CSS_SELECTOR':
            return By.CSS_SELECTOR, value

    @staticmethod
    def _save_error_img():
        try:
            img_name_temp = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '_element.png'
            img_path = os.path.join(base_dir, 'static/img')
            filepath = os.path.join(img_path, img_name_temp)
            if os.path.exists(filepath):
                img_name_temp = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(1, 1000000)) + '_element.png'
                filepath = os.path.join(img_path, img_name_temp)
            DriverApi.driver.get_screenshot_as_file(filepath)
            logger().info('页面截图保存路径[%s]'%filepath)
        except Exception as e:
            logger().info('保存图片失败%s'%str(e))
            raise e

    @staticmethod
    def _save_error_page_img():
        try:
            img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '_page.png'
            img_path = os.path.join(base_dir, 'static/img')
            filepath = os.path.join(img_path, img_name)
            if os.path.exists(filepath):
                img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(1, 1000000)) + '_page.png'
                filepath = os.path.join(img_path, img_name)
            DriverApi.driver.get_screenshot_as_file(filepath)
            logger().info('页面加载失败，错误页面截图保存路径[%s]' % filepath)
        except Exception as e:
            logger().info('保存图片失败')
            raise e

    @staticmethod
    def save_page_img(page_info=''):
        try:
            img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '_page.png'
            img_path = os.path.join(base_dir, 'static/img')
            filepath = os.path.join(img_path, img_name)
            if os.path.exists(filepath):
                img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(
                    random.randint(1, 1000000)) + '_page.png'
                filepath = os.path.join(img_path, img_name)
            DriverApi.driver.get_screenshot_as_file(filepath)
            logger().info('页面信息[%s]，页面截图保存路径[%s]' % (page_info, filepath))
        except Exception as e:
            logger().info('保存图片失败')
            raise e

    @staticmethod
    def save_page_img_2_report(page_info=''):
        try:
            img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '_page.png'
            img_path = os.path.join(base_dir, 'static/img')
            filepath = os.path.join(img_path, img_name)
            if os.path.exists(filepath):
                img_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(
                    random.randint(1, 1000000)) + '_page.png'
                filepath = os.path.join(img_path, img_name)
            DriverApi.driver.get_screenshot_as_file(filepath)
            with open(filepath, 'rb') as f:
                image = base64.b64encode(f.read())
                AddImage(image)
            logger().info('页面信息[%s]，页面截图保存路径[%s]' % (page_info, filepath))
        except Exception as e:
            logger().info('保存图片失败')
            raise e


if __name__ == '__main__':
    import  requests
    headers = {'Content-Type': 'application/json'}
    url = 'http://127.0.0.1:5000/spiderPorscheCfgData'
    data = {'code': 'PKD5U8J2'}
    res = requests.post(url, json=data, headers=headers)
    print(res.json())
    print(res.elapsed.total_seconds())


