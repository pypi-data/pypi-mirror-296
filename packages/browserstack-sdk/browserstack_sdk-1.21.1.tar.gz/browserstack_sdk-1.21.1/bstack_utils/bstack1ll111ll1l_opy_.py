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
import datetime
import threading
from bstack_utils.helper import bstack111lllll1l_opy_, bstack11lll111_opy_, get_host_info, bstack111l1lll1l_opy_, \
 bstack111l1111_opy_, bstack1ll1l1l1_opy_, bstack11ll111l11_opy_, bstack111l1l11ll_opy_, bstack11ll111l_opy_
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.percy import bstack1111llll1_opy_
from bstack_utils.config import Config
bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1111llll1_opy_()
@bstack11ll111l11_opy_(class_method=False)
def bstack1ll1l11ll11_opy_(bs_config, bstack111lll1l_opy_):
  try:
    data = {
        bstack1ll1l11_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷ᜴ࠫ"): bstack1ll1l11_opy_ (u"ࠬࡰࡳࡰࡰࠪ᜵"),
        bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬ᜶"): bs_config.get(bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ᜷"), bstack1ll1l11_opy_ (u"ࠨࠩ᜸")),
        bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᜹"): bs_config.get(bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᜺"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᜻"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ᜼")),
        bstack1ll1l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᜽"): bs_config.get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᜾"), bstack1ll1l11_opy_ (u"ࠨࠩ᜿")),
        bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᝀ"): bstack11ll111l_opy_(),
        bstack1ll1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᝁ"): bstack111l1lll1l_opy_(bs_config),
        bstack1ll1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧᝂ"): get_host_info(),
        bstack1ll1l11_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ᝃ"): bstack11lll111_opy_(),
        bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᝄ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᝅ")),
        bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ᝆ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧᝇ"), False),
        bstack1ll1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬᝈ"): bstack111lllll1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᝉ"): bstack1ll1l111l1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩᝊ"): bstack1ll1l1111ll_opy_(bstack111lll1l_opy_),
        bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᝋ"): bstack1ll1lll1l_opy_(bs_config, bstack111lll1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᝌ"), bstack1ll1l11_opy_ (u"ࠨࠩᝍ"))),
        bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᝎ"): bstack111l1111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦᝏ").format(str(error)))
    return None
def bstack1ll1l1111ll_opy_(framework):
  return {
    bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᝐ"): framework.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᝑ"), bstack1ll1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᝒ")),
    bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᝓ"): framework.get(bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᝔")),
    bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᝕"): framework.get(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᝖")),
    bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭᝗"): bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᝘"),
    bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭᝙"): framework.get(bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ᝚"))
  }
def bstack1ll1lll1l_opy_(bs_config, framework):
  bstack1l1l11l111_opy_ = False
  bstack11l111lll_opy_ = False
  if bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࠬ᝛") in bs_config:
    bstack1l1l11l111_opy_ = True
  else:
    bstack11l111lll_opy_ = True
  bstack11lll1ll1_opy_ = {
    bstack1ll1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᝜"): bstack11ll1ll1l_opy_.bstack1ll1l111l11_opy_(bs_config, framework),
    bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᝝"): bstack1l1ll111l_opy_.bstack11l111llll_opy_(bs_config),
    bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ᝞"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᝟"), False),
    bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᝠ"): bstack11l111lll_opy_,
    bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᝡ"): bstack1l1l11l111_opy_
  }
  return bstack11lll1ll1_opy_
@bstack11ll111l11_opy_(class_method=False)
def bstack1ll1l111l1l_opy_():
  try:
    bstack1ll1l11l1ll_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᝢ"), bstack1ll1l11_opy_ (u"ࠩࡾࢁࠬᝣ")))
    return {
        bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᝤ"): bstack1ll1l11l1ll_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥᝥ").format(str(error)))
    return {}
def bstack1ll1l1l1111_opy_(array, bstack1ll1l111lll_opy_, bstack1ll1l1111l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l111lll_opy_]
    result[key] = o[bstack1ll1l1111l1_opy_]
  return result
def bstack1ll1ll11l1l_opy_(bstack1lll1l111l_opy_=bstack1ll1l11_opy_ (u"ࠬ࠭ᝦ")):
  bstack1ll1l111ll1_opy_ = bstack1l1ll111l_opy_.on()
  bstack1ll1l11l1l1_opy_ = bstack11ll1ll1l_opy_.on()
  bstack1ll1l11l111_opy_ = percy.bstack1llll1l1lll_opy_()
  if bstack1ll1l11l111_opy_ and not bstack1ll1l11l1l1_opy_ and not bstack1ll1l111ll1_opy_:
    return bstack1lll1l111l_opy_ not in [bstack1ll1l11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᝧ"), bstack1ll1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᝨ")]
  elif bstack1ll1l111ll1_opy_ and not bstack1ll1l11l1l1_opy_:
    return bstack1lll1l111l_opy_ not in [bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᝩ"), bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᝪ"), bstack1ll1l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᝫ")]
  return bstack1ll1l111ll1_opy_ or bstack1ll1l11l1l1_opy_ or bstack1ll1l11l111_opy_
@bstack11ll111l11_opy_(class_method=False)
def bstack1ll1l1l111l_opy_(bstack1lll1l111l_opy_, test=None):
  bstack1ll1l11l11l_opy_ = bstack1l1ll111l_opy_.on()
  if not bstack1ll1l11l11l_opy_ or bstack1lll1l111l_opy_ not in [bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᝬ")] or test == None:
    return None
  return {
    bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᝭"): bstack1ll1l11l11l_opy_ and bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᝮ"), None) == True and bstack1l1ll111l_opy_.bstack1l11111111_opy_(test[bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᝯ")])
  }