

class LoginError(Exception):
    def __init__(self, ErrorInfo='登录接口异常'):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class PageLoadError(Exception):
    def __init__(self, ErrorInfo='页面加载异常'):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo