"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest
from kytest.core.web import TC
from page.web_page import CommonPage


# ===========================用例内容============================================================
@kytest.story('登录模块')
class TestWebDemo(TC):
    def start(self):
        self.cp = CommonPage(self.dr)

    @kytest.title("登录")
    def test_login(self):
        self.cp.login()
        self.assert_url()
        self.shot('首页', delay=3)
# ======可以用这种po模式，也可以直接使用self.elem(xpath='xxx').click的方式调用=============================



