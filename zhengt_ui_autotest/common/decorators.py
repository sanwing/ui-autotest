from log.globallog import log
from common.driver_api import DriverApi

def deco_test_method_comment(f):
    def wrapper(self):
        log.info('*'*30 + f.__name__ + '*'*30)
        log.info('开始执行用例[%s]'%f.__name__)
        try:
            f(self)
        except Exception as e:
            DriverApi.save_page_img(f.__name__)
            log.exception(e)
            self.fail()
            raise e
        finally:
            log.info('执行用例[%s]完成' % f.__name__)
            log.info('*'*30 + f.__name__ + '*'*30)
            log.info('\n\n')
    return wrapper