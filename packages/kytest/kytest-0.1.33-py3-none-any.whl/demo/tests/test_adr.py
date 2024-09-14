import kytest
from kytest.core.adr import TC
from page.adr_page import AdrPage


# ===========================用例内容============================================================
@kytest.story('测试demo')
class TestAdrDemo(TC):
    def start(self):
        self.dp = AdrPage(self.dr)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        self.start_app()
        if self.dp.adBtn.exists():
            self.dp.adBtn.click()
        self.dp.myTab.click()
        self.dp.setBtn.click()
        self.shot("设置页", delay=3)
        self.stop_app()
# ======可以用这种po模式，也可以直接使用self.elem(rid='xxx').click的方式调用=============================



