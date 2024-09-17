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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llll1lll_opy_ = {}
        bstack11lllllll1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫක"), bstack1ll1l11_opy_ (u"ࠫࠬඛ"))
        if not bstack11lllllll1_opy_:
            return bstack1llll1lll_opy_
        try:
            bstack11llllll1l_opy_ = json.loads(bstack11lllllll1_opy_)
            if bstack1ll1l11_opy_ (u"ࠧࡵࡳࠣග") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࠤඝ")] = bstack11llllll1l_opy_[bstack1ll1l11_opy_ (u"ࠢࡰࡵࠥඞ")]
            if bstack1ll1l11_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧඟ") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧච") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨඡ")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣජ"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣඣ")))
            if bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢඤ") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧඥ") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨඦ")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥට"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣඨ")))
            if bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨඩ") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨඪ") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢණ")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤඬ"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤත")))
            if bstack1ll1l11_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤථ") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢද") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣධ")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧන"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ඲")))
            if bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤඳ") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢප") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣඵ")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧබ"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥභ")))
            if bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣම") in bstack11llllll1l_opy_ or bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣඹ") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤය")] = bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦර"), bstack11llllll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ඼")))
            if bstack1ll1l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧල") in bstack11llllll1l_opy_:
                bstack1llll1lll_opy_[bstack1ll1l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨ඾")] = bstack11llllll1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ඿")]
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧව") +  str(error))
        return bstack1llll1lll_opy_