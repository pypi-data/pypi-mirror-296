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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l1l1ll11_opy_, bstack11l1l11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1ll11_opy_ = bstack11l1l1ll11_opy_
        self.bstack11l1l11l11_opy_ = bstack11l1l11l11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1ll1ll1_opy_(bstack11l11lll1l_opy_):
        bstack11l11lllll_opy_ = []
        if bstack11l11lll1l_opy_:
            tokens = str(os.path.basename(bstack11l11lll1l_opy_)).split(bstack1ll1l11_opy_ (u"ࠨ࡟ࠣ໴"))
            camelcase_name = bstack1ll1l11_opy_ (u"ࠢࠡࠤ໵").join(t.title() for t in tokens)
            suite_name, bstack11l11llll1_opy_ = os.path.splitext(camelcase_name)
            bstack11l11lllll_opy_.append(suite_name)
        return bstack11l11lllll_opy_
    @staticmethod
    def bstack11l1l11111_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ໶") in typename:
            return bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ໷")
        return bstack1ll1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ໸")