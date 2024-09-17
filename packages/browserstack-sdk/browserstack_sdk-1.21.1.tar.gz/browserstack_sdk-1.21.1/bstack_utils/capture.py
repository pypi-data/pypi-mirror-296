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
import sys
class bstack11llll1l1l_opy_:
    def __init__(self, handler):
        self._111lll1l1l_opy_ = sys.stdout.write
        self._111lll1ll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111lll1l11_opy_
        sys.stdout.error = self.bstack111lll11ll_opy_
    def bstack111lll1l11_opy_(self, _str):
        self._111lll1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿃"): bstack1ll1l11_opy_ (u"ࠫࡎࡔࡆࡐࠩ࿄"), bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿅"): _str})
    def bstack111lll11ll_opy_(self, _str):
        self._111lll1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰ࿆ࠬ"): bstack1ll1l11_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭࿇"), bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿈"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111lll1l1l_opy_
        sys.stderr.write = self._111lll1ll1_opy_