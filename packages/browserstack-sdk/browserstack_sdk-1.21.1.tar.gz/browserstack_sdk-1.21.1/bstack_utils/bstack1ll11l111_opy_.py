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
import threading
import logging
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from bstack_utils.helper import bstack1ll1l1l1_opy_
logger = logging.getLogger(__name__)
def bstack1ll1l1llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1l1llll1l_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ྺ"), [])
    bstack11lllll11_opy_ = bstack1l1ll111l_opy_.bstack1l11111111_opy_(tags)
    threading.current_thread().isA11yTest = bstack11lllll11_opy_
    try:
      bstack1l1l1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1llll_opy_(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨྻ")) else context.browser
      if bstack1l1l1111l1_opy_ and bstack1l1l1111l1_opy_.session_id and bstack11lllll11_opy_ and bstack1ll1l1l1_opy_(
              threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩྼ"), None):
          threading.current_thread().isA11yTest = bstack1l1ll111l_opy_.bstack1l11l1lll_opy_(bstack1l1l1111l1_opy_, bstack11lllll11_opy_)
    except Exception as e:
       logger.debug(bstack1ll1l11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫ྽").format(str(e)))
def bstack1ll1ll1l11_opy_(bstack1l1l1111l1_opy_):
    if bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ྾"), None) and bstack1ll1l1l1_opy_(
      threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ྿"), None) and not bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪ࿀"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1ll111l_opy_.bstack1l11ll11ll_opy_(bstack1l1l1111l1_opy_, name=bstack1ll1l11_opy_ (u"ࠣࠤ࿁"), path=bstack1ll1l11_opy_ (u"ࠤࠥ࿂"))