# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l11l11_opy_ = 2048
bstack1ll111l_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l11l1_opy_):
    global bstack1lllll_opy_
    bstack1l111l_opy_ = ord (bstack11l11l1_opy_ [-1])
    bstack11111l1_opy_ = bstack11l11l1_opy_ [:-1]
    bstack1l1l1_opy_ = bstack1l111l_opy_ % len (bstack11111l1_opy_)
    bstack1lll11_opy_ = bstack11111l1_opy_ [:bstack1l1l1_opy_] + bstack11111l1_opy_ [bstack1l1l1_opy_:]
    if bstack11llll_opy_:
        bstack1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11l11_opy_ - (bstack111ll11_opy_ + bstack1l111l_opy_) % bstack1ll111l_opy_) for bstack111ll11_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1_opy_ = str () .join ([chr (ord (char) - bstack1l11l11_opy_ - (bstack111ll11_opy_ + bstack1l111l_opy_) % bstack1ll111l_opy_) for bstack111ll11_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1_opy_)
class bstack1l1lll11_opy_:
    def __init__(self, handler):
        self._1lll11111ll_opy_ = None
        self.handler = handler
        self._1lll1111l11_opy_ = self.bstack1lll1111ll1_opy_()
        self.patch()
    def patch(self):
        self._1lll11111ll_opy_ = self._1lll1111l11_opy_.execute
        self._1lll1111l11_opy_.execute = self.bstack1lll1111l1l_opy_()
    def bstack1lll1111l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᗙ"), driver_command, None, this, args)
            response = self._1lll11111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1l11_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᗚ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1111l11_opy_.execute = self._1lll11111ll_opy_
    @staticmethod
    def bstack1lll1111ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver