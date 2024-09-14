"""
@Author: kang.yang
@Date: 2024/9/14 09:44
"""
from kytest.core.adr import Page, Elem


# ===========================页面定义============================================================
class AdrPage(Page):
    adBtn = Elem(rid='com.qizhidao.clientapp:id/bottom_btn')
    myTab = Elem(xpath='//android.widget.FrameLayout[4]')
    spaceTab = Elem(text='科创空间')
    setBtn = Elem(rid='com.qizhidao.clientapp:id/me_top_bar_setting_iv')
    title = Elem(rid='com.qizhidao.clientapp:id/tv_actionbar_title')
    agreeText = Elem(rid='com.qizhidao.clientapp:id/agreement_tv_2')
    moreService = Elem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/layout_top_content"]'
                             '/android.view.ViewGroup[3]/android.view.View[10]')
# ============少的话就放用例中，多的话可以单独拆一个页面定义的模块========================================
