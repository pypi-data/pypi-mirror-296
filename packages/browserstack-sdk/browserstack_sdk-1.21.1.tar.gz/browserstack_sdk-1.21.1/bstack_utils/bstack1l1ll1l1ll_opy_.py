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
from browserstack_sdk.bstack1ll11ll1_opy_ import bstack1l1ll1l1l_opy_
from browserstack_sdk.bstack11l1llllll_opy_ import RobotHandler
def bstack1l11lllll_opy_(framework):
    if framework.lower() == bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬኲ"):
        return bstack1l1ll1l1l_opy_.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬኳ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧኴ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll1l11_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩኵ")