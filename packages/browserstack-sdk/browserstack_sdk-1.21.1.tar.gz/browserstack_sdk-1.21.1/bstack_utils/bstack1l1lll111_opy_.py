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
import logging
import os
import threading
from bstack_utils.helper import bstack1llll111_opy_
from bstack_utils.constants import bstack111ll1lll1_opy_
logger = logging.getLogger(__name__)
class bstack11ll1ll1l_opy_:
    bstack1lll111l1l1_opy_ = None
    @classmethod
    def bstack1l1l11lll1_opy_(cls):
        if cls.on():
            logger.info(
                bstack1ll1l11_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫᝰ").format(os.environ[bstack1ll1l11_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣ᝱")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᝲ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᝳ")] == bstack1ll1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᝴"):
            return False
        return True
    @classmethod
    def bstack1ll1l111l11_opy_(cls, bs_config, framework=bstack1ll1l11_opy_ (u"ࠨࠢ᝵")):
        if framework == bstack1ll1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ᝶"):
            return bstack1llll111_opy_(bs_config.get(bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᝷")))
        bstack1ll11llll11_opy_ = framework in bstack111ll1lll1_opy_
        return bstack1llll111_opy_(bs_config.get(bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᝸"), bstack1ll11llll11_opy_))
    @classmethod
    def bstack1ll11lllll1_opy_(cls, framework):
        return framework in bstack111ll1lll1_opy_
    @classmethod
    def bstack1ll1l1lllll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l111l11_opy_(bs_config, framework) is True and cls.bstack1ll11lllll1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ᝹"), None)
    @staticmethod
    def bstack11lll11l1l_opy_():
        if getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ᝺"), None):
            return {
                bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ᝻"): bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࠫ᝼"),
                bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝽"): getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ᝾"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭᝿"), None):
            return {
                bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨក"): bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩខ"),
                bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬគ"): getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪឃ"), None)
            }
        return None
    @staticmethod
    def bstack1ll11llllll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll1ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1ll1ll1_opy_(test, hook_name=None):
        bstack1ll1l11111l_opy_ = test.parent
        if hook_name in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬង"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩច"), bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨឆ"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬជ")]:
            bstack1ll1l11111l_opy_ = test
        scope = []
        while bstack1ll1l11111l_opy_ is not None:
            scope.append(bstack1ll1l11111l_opy_.name)
            bstack1ll1l11111l_opy_ = bstack1ll1l11111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l111111_opy_(hook_type):
        if hook_type == bstack1ll1l11_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤឈ"):
            return bstack1ll1l11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤញ")
        elif hook_type == bstack1ll1l11_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥដ"):
            return bstack1ll1l11_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢឋ")
    @staticmethod
    def bstack1ll11llll1l_opy_(bstack1lll111ll_opy_):
        try:
            if not bstack11ll1ll1l_opy_.on():
                return bstack1lll111ll_opy_
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨឌ"), None) == bstack1ll1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢឍ"):
                tests = os.environ.get(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢណ"), None)
                if tests is None or tests == bstack1ll1l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤត"):
                    return bstack1lll111ll_opy_
                bstack1lll111ll_opy_ = tests.split(bstack1ll1l11_opy_ (u"ࠬ࠲ࠧថ"))
                return bstack1lll111ll_opy_
        except Exception as exc:
            print(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢទ"), str(exc))
        return bstack1lll111ll_opy_