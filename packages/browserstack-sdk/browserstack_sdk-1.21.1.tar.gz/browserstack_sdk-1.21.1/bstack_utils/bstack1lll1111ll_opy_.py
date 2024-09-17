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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l1111lll_opy_, bstack11l11ll1l1_opy_, bstack1l11ll1ll_opy_, bstack11ll111l11_opy_, bstack111l111ll1_opy_, bstack111l1l1lll_opy_, bstack111l1l11ll_opy_, bstack11ll111l_opy_
from bstack_utils.bstack1lll111l1l1_opy_ import bstack1lll111l11l_opy_
import bstack_utils.bstack1ll111ll1l_opy_ as bstack1l111ll11_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from bstack_utils.bstack1l1ll1l1l1_opy_ import bstack1l1ll1l1l1_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11l1lll111_opy_
bstack1ll1ll11111_opy_ = bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᙎ")
logger = logging.getLogger(__name__)
class bstack1ll11l11l_opy_:
    bstack1lll111l1l1_opy_ = None
    bs_config = None
    bstack111lll1l_opy_ = None
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def launch(cls, bs_config, bstack111lll1l_opy_):
        cls.bs_config = bs_config
        cls.bstack111lll1l_opy_ = bstack111lll1l_opy_
        try:
            cls.bstack1ll1ll1l111_opy_()
            bstack11l11ll111_opy_ = bstack11l1111lll_opy_(bs_config)
            bstack11l11l111l_opy_ = bstack11l11ll1l1_opy_(bs_config)
            data = bstack1l111ll11_opy_.bstack1ll1l11ll11_opy_(bs_config, bstack111lll1l_opy_)
            config = {
                bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᙏ"): (bstack11l11ll111_opy_, bstack11l11l111l_opy_),
                bstack1ll1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᙐ"): cls.default_headers()
            }
            response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᙑ"), cls.request_url(bstack1ll1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩᙒ")), data, config)
            if response.status_code != 200:
                bstack1ll1ll111ll_opy_ = response.json()
                if bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᙓ")] == False:
                    cls.bstack1ll1ll11l11_opy_(bstack1ll1ll111ll_opy_)
                    return
                cls.bstack1ll1l1l1l11_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᙔ")])
                cls.bstack1ll1l1ll1ll_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙕ")])
                return None
            bstack1ll1l11lll1_opy_ = cls.bstack1ll1l1ll111_opy_(response)
            return bstack1ll1l11lll1_opy_
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦᙖ").format(str(error)))
            return None
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def stop(cls, bstack1ll1ll11ll1_opy_=None):
        if not bstack11ll1ll1l_opy_.on() and not bstack1l1ll111l_opy_.on():
            return
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᙗ")) == bstack1ll1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨᙘ") or os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᙙ")) == bstack1ll1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᙚ"):
            logger.error(bstack1ll1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᙛ"))
            return {
                bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᙜ"): bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᙝ"),
                bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᙞ"): bstack1ll1l11_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭ᙟ")
            }
        try:
            cls.bstack1lll111l1l1_opy_.shutdown()
            data = {
                bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᙠ"): bstack11ll111l_opy_()
            }
            if not bstack1ll1ll11ll1_opy_ is None:
                data[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧᙡ")] = [{
                    bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᙢ"): bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪᙣ"),
                    bstack1ll1l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ᙤ"): bstack1ll1ll11ll1_opy_
                }]
            config = {
                bstack1ll1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᙥ"): cls.default_headers()
            }
            bstack11111l111l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᙦ").format(os.environ[bstack1ll1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢᙧ")])
            bstack1ll1l1llll1_opy_ = cls.request_url(bstack11111l111l_opy_)
            response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠪࡔ࡚࡚ࠧᙨ"), bstack1ll1l1llll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1l11_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᙩ"))
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤᙪ") + str(error))
            return {
                bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙫ"): bstack1ll1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᙬ"),
                bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᙭"): str(error)
            }
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack1ll1l1ll111_opy_(cls, response):
        bstack1ll1ll111ll_opy_ = response.json()
        bstack1ll1l11lll1_opy_ = {}
        if bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠩ࡭ࡻࡹ࠭᙮")) is None:
            os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᙯ")] = bstack1ll1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᙰ")
        else:
            os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᙱ")] = bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡪࡸࡶࠪᙲ"), bstack1ll1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᙳ"))
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᙴ")] = bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᙵ"), bstack1ll1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᙶ"))
        if bstack11ll1ll1l_opy_.bstack1ll1l1lllll_opy_(cls.bs_config, cls.bstack111lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᙷ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᙸ"))) is True:
            bstack1ll1l1l1lll_opy_, bstack1ll1l11ll1l_opy_, bstack1ll1l1l11l1_opy_ = cls.bstack1ll1ll1111l_opy_(bstack1ll1ll111ll_opy_)
            if bstack1ll1l1l1lll_opy_ != None and bstack1ll1l11ll1l_opy_ != None:
                bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᙹ")] = {
                    bstack1ll1l11_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪᙺ"): bstack1ll1l1l1lll_opy_,
                    bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᙻ"): bstack1ll1l11ll1l_opy_,
                    bstack1ll1l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᙼ"): bstack1ll1l1l11l1_opy_
                }
            else:
                bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᙽ")] = {}
        else:
            bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᙾ")] = {}
        if bstack1l1ll111l_opy_.bstack11l111llll_opy_(cls.bs_config) is True:
            bstack1ll1l1ll11l_opy_, bstack1ll1l11ll1l_opy_ = cls.bstack1ll1l1lll11_opy_(bstack1ll1ll111ll_opy_)
            if bstack1ll1l1ll11l_opy_ != None and bstack1ll1l11ll1l_opy_ != None:
                bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙿ")] = {
                    bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪ "): bstack1ll1l1ll11l_opy_,
                    bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚁ"): bstack1ll1l11ll1l_opy_,
                }
            else:
                bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚂ")] = {}
        else:
            bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚃ")] = {}
        if bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚄ")].get(bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚅ")) != None or bstack1ll1l11lll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚆ")].get(bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚇ")) != None:
            cls.bstack1ll1ll1l1l1_opy_(bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡫ࡹࡷࠫᚈ")), bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚉ")))
        return bstack1ll1l11lll1_opy_
    @classmethod
    def bstack1ll1ll1111l_opy_(cls, bstack1ll1ll111ll_opy_):
        if bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚊ")) == None:
            cls.bstack1ll1l1l1l11_opy_()
            return [None, None, None]
        if bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚋ")][bstack1ll1l11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᚌ")] != True:
            cls.bstack1ll1l1l1l11_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚍ")])
            return [None, None, None]
        logger.debug(bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᚎ"))
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᚏ")] = bstack1ll1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᚐ")
        if bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠩ࡭ࡻࡹ࠭ᚑ")):
            os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᚒ")] = bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡯ࡽࡴࠨᚓ")]
            os.environ[bstack1ll1l11_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᚔ")] = json.dumps({
                bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᚕ"): bstack11l1111lll_opy_(cls.bs_config),
                bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᚖ"): bstack11l11ll1l1_opy_(cls.bs_config)
            })
        if bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚗ")):
            os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᚘ")] = bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᚙ")]
        if bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚚ")].get(bstack1ll1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᚛"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ᚜")):
            os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ᚝")] = str(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᚞")][bstack1ll1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ᚟")][bstack1ll1l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᚠ")])
        return [bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡯ࡽࡴࠨᚡ")], bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚢ")], os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᚣ")]]
    @classmethod
    def bstack1ll1l1lll11_opy_(cls, bstack1ll1ll111ll_opy_):
        if bstack1ll1ll111ll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚤ")) == None:
            cls.bstack1ll1l1ll1ll_opy_()
            return [None, None]
        if bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚥ")][bstack1ll1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᚦ")] != True:
            cls.bstack1ll1l1ll1ll_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚧ")])
            return [None, None]
        if bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚨ")].get(bstack1ll1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚩ")):
            logger.debug(bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᚪ"))
            parsed = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᚫ"), bstack1ll1l11_opy_ (u"ࠨࡽࢀࠫᚬ")))
            capabilities = bstack1l111ll11_opy_.bstack1ll1l1l1111_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚭ")][bstack1ll1l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚮ")][bstack1ll1l11_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚯ")], bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᚰ"), bstack1ll1l11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᚱ"))
            bstack1ll1l1ll11l_opy_ = capabilities[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᚲ")]
            os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᚳ")] = bstack1ll1l1ll11l_opy_
            parsed[bstack1ll1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᚴ")] = capabilities[bstack1ll1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚵ")]
            os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᚶ")] = json.dumps(parsed)
            scripts = bstack1l111ll11_opy_.bstack1ll1l1l1111_opy_(bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚷ")][bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚸ")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᚹ")], bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚺ"), bstack1ll1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪᚻ"))
            bstack1l1ll1l1l1_opy_.bstack11l111l11l_opy_(scripts)
            commands = bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚼ")][bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᚽ")][bstack1ll1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭ᚾ")].get(bstack1ll1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᚿ"))
            bstack1l1ll1l1l1_opy_.bstack11l11l1l11_opy_(commands)
            bstack1l1ll1l1l1_opy_.store()
        return [bstack1ll1l1ll11l_opy_, bstack1ll1ll111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᛀ")]]
    @classmethod
    def bstack1ll1l1l1l11_opy_(cls, response=None):
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛁ")] = bstack1ll1l11_opy_ (u"ࠩࡱࡹࡱࡲࠧᛂ")
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᛃ")] = bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᛄ")
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛅ")] = bstack1ll1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛆ")
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᛇ")] = bstack1ll1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᛈ")
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᛉ")] = bstack1ll1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᛊ")
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᛋ")] = bstack1ll1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᛌ")
        cls.bstack1ll1ll11l11_opy_(response, bstack1ll1l11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᛍ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1ll1ll_opy_(cls, response=None):
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᛎ")] = bstack1ll1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᛏ")
        os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᛐ")] = bstack1ll1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛑ")
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᛒ")] = bstack1ll1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᛓ")
        cls.bstack1ll1ll11l11_opy_(response, bstack1ll1l11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᛔ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1ll1l1l1_opy_(cls, bstack1ll1ll11lll_opy_, bstack1ll1l11ll1l_opy_):
        os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᛕ")] = bstack1ll1ll11lll_opy_
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛖ")] = bstack1ll1l11ll1l_opy_
    @classmethod
    def bstack1ll1ll11l11_opy_(cls, response=None, product=bstack1ll1l11_opy_ (u"ࠤࠥᛗ")):
        if response == None:
            logger.error(product + bstack1ll1l11_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧᛘ"))
        for error in response[bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᛙ")]:
            bstack111l11111l_opy_ = error[bstack1ll1l11_opy_ (u"ࠬࡱࡥࡺࠩᛚ")]
            error_message = error[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᛛ")]
            if error_message:
                if bstack111l11111l_opy_ == bstack1ll1l11_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨᛜ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1l11_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤᛝ") + product + bstack1ll1l11_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᛞ"))
    @classmethod
    def bstack1ll1ll1l111_opy_(cls):
        if cls.bstack1lll111l1l1_opy_ is not None:
            return
        cls.bstack1lll111l1l1_opy_ = bstack1lll111l11l_opy_(cls.bstack1ll1ll1l11l_opy_)
        cls.bstack1lll111l1l1_opy_.start()
    @classmethod
    def bstack11l1lllll1_opy_(cls):
        if cls.bstack1lll111l1l1_opy_ is None:
            return
        cls.bstack1lll111l1l1_opy_.shutdown()
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack1ll1ll1l11l_opy_(cls, bstack11ll111ll1_opy_, bstack1ll1l11llll_opy_=bstack1ll1l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᛟ")):
        config = {
            bstack1ll1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᛠ"): cls.default_headers()
        }
        response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪᛡ"), cls.request_url(bstack1ll1l11llll_opy_), bstack11ll111ll1_opy_, config)
        bstack11l111ll1l_opy_ = response.json()
    @classmethod
    def bstack11ll11l11l_opy_(cls, bstack11ll111ll1_opy_, bstack1ll1l11llll_opy_=bstack1ll1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᛢ")):
        if not bstack1l111ll11_opy_.bstack1ll1ll11l1l_opy_(bstack11ll111ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᛣ")]):
            return
        bstack11lll1ll1_opy_ = bstack1l111ll11_opy_.bstack1ll1l1l111l_opy_(bstack11ll111ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᛤ")], bstack11ll111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᛥ")))
        if bstack11lll1ll1_opy_ != None:
            bstack11ll111ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨᛦ")] = bstack11lll1ll1_opy_
        if bstack1ll1l11llll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᛧ"):
            cls.bstack1ll1ll1l111_opy_()
            cls.bstack1lll111l1l1_opy_.add(bstack11ll111ll1_opy_)
        elif bstack1ll1l11llll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᛨ"):
            cls.bstack1ll1ll1l11l_opy_([bstack11ll111ll1_opy_], bstack1ll1l11llll_opy_)
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack11llll11l_opy_(cls, bstack11ll111l1l_opy_):
        bstack1ll1l1l11ll_opy_ = []
        for log in bstack11ll111l1l_opy_:
            bstack1ll1l1lll1l_opy_ = {
                bstack1ll1l11_opy_ (u"࠭࡫ࡪࡰࡧࠫᛩ"): bstack1ll1l11_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᛪ"),
                bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᛫"): log[bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᛬")],
                bstack1ll1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᛭"): log[bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᛮ")],
                bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᛯ"): {},
                bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᛰ"): log[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛱ")],
            }
            if bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛲ") in log:
                bstack1ll1l1lll1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᛳ")] = log[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᛴ")]
            elif bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᛵ") in log:
                bstack1ll1l1lll1l_opy_[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᛶ")] = log[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᛷ")]
            bstack1ll1l1l11ll_opy_.append(bstack1ll1l1lll1l_opy_)
        cls.bstack11ll11l11l_opy_({
            bstack1ll1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᛸ"): bstack1ll1l11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ᛹"),
            bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ᛺"): bstack1ll1l1l11ll_opy_
        })
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack1ll1l1ll1l1_opy_(cls, steps):
        bstack1ll1ll111l1_opy_ = []
        for step in steps:
            bstack1ll1l1l1l1l_opy_ = {
                bstack1ll1l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ᛻"): bstack1ll1l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ᛼"),
                bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᛽"): step[bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᛾")],
                bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᛿"): step[bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᜀ")],
                bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᜁ"): step[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᜂ")],
                bstack1ll1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᜃ"): step[bstack1ll1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᜄ")]
            }
            if bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜅ") in step:
                bstack1ll1l1l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜆ")] = step[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜇ")]
            elif bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜈ") in step:
                bstack1ll1l1l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜉ")] = step[bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜊ")]
            bstack1ll1ll111l1_opy_.append(bstack1ll1l1l1l1l_opy_)
        cls.bstack11ll11l11l_opy_({
            bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᜋ"): bstack1ll1l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᜌ"),
            bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᜍ"): bstack1ll1ll111l1_opy_
        })
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack1lll111111_opy_(cls, screenshot):
        cls.bstack11ll11l11l_opy_({
            bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜎ"): bstack1ll1l11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᜏ"),
            bstack1ll1l11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᜐ"): [{
                bstack1ll1l11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᜑ"): bstack1ll1l11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᜒ"),
                bstack1ll1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᜓ"): datetime.datetime.utcnow().isoformat() + bstack1ll1l11_opy_ (u"᜔࡛ࠧࠩ"),
                bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ᜕ࠩ"): screenshot[bstack1ll1l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ᜖")],
                bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᜗"): screenshot[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᜘")]
            }]
        }, bstack1ll1l11llll_opy_=bstack1ll1l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ᜙"))
    @classmethod
    @bstack11ll111l11_opy_(class_method=True)
    def bstack1l1llll1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll11l11l_opy_({
            bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ᜚"): bstack1ll1l11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ᜛"),
            bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ᜜"): {
                bstack1ll1l11_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ᜝"): cls.current_test_uuid(),
                bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ᜞"): cls.bstack11ll11ll1l_opy_(driver)
            }
        })
    @classmethod
    def bstack11lll1l11l_opy_(cls, event: str, bstack11ll111ll1_opy_: bstack11l1lll111_opy_):
        bstack11l1ll1l1l_opy_ = {
            bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜟ"): event,
            bstack11ll111ll1_opy_.bstack11ll1ll11l_opy_(): bstack11ll111ll1_opy_.bstack11lll111l1_opy_(event)
        }
        cls.bstack11ll11l11l_opy_(bstack11l1ll1l1l_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᜠ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᜡ")] == bstack1ll1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᜢ")) and (os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᜣ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᜤ")] == bstack1ll1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᜥ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11l11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᜦ"): bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᜧ"),
            bstack1ll1l11_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᜨ"): bstack1ll1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᜩ")
        }
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᜪ"), None):
            headers[bstack1ll1l11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᜫ")] = bstack1ll1l11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᜬ").format(os.environ[bstack1ll1l11_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧᜭ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll1l11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᜮ").format(bstack1ll1ll11111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᜯ"), None)
    @staticmethod
    def bstack11ll11ll1l_opy_(driver):
        return {
            bstack111l111ll1_opy_(): bstack111l1l1lll_opy_(driver)
        }
    @staticmethod
    def bstack1ll1ll1l1ll_opy_(exception_info, report):
        return [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᜰ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l1l11111_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᜱ") in typename:
            return bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᜲ")
        return bstack1ll1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᜳ")