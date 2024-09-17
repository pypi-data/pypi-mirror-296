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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l11111l1_opy_ as bstack11l11l1l1l_opy_
from bstack_utils.bstack1l1ll1l1l1_opy_ import bstack1l1ll1l1l1_opy_
from bstack_utils.helper import bstack11ll111l_opy_, bstack11ll1l1l11_opy_, bstack111l1111_opy_, bstack11l1111lll_opy_, bstack11l11ll1l1_opy_, bstack11lll111_opy_, get_host_info, bstack111lllll1l_opy_, bstack1l11ll1ll_opy_, bstack11ll111l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11ll111l11_opy_(class_method=False)
def _11l111l1ll_opy_(driver, bstack11l1l11lll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1l11_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬ໹"): caps.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ໺"), None),
        bstack1ll1l11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ໻"): bstack11l1l11lll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ໼"), None),
        bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ໽"): caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ໾"), None),
        bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໿"): caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬༀ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ༁") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ༂"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ༃")] == bstack1ll1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ༄"):
        return False
    return True
def bstack11l111llll_opy_(config):
  return config.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ༅"), False) or any([p.get(bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ༆"), False) == True for p in config.get(bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ༇"), [])])
def bstack1lllllll11_opy_(config, bstack1l1ll111l1_opy_):
  try:
    if not bstack111l1111_opy_(config):
      return False
    bstack11l11ll11l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ༈"), False)
    if int(bstack1l1ll111l1_opy_) < len(config.get(bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༉"), [])) and config[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ༊")][bstack1l1ll111l1_opy_]:
      bstack11l1111l1l_opy_ = config[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ་")][bstack1l1ll111l1_opy_].get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ༌"), None)
    else:
      bstack11l1111l1l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ།"), None)
    if bstack11l1111l1l_opy_ != None:
      bstack11l11ll11l_opy_ = bstack11l1111l1l_opy_
    bstack11l111111l_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ༎")) is not None and len(os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ༏"))) > 0 and os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ༐")) != bstack1ll1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ༑")
    return bstack11l11ll11l_opy_ and bstack11l111111l_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ༒") + str(error))
  return False
def bstack1l11111111_opy_(test_tags):
  bstack11l111l111_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ༓"))
  if bstack11l111l111_opy_ is None:
    return True
  bstack11l111l111_opy_ = json.loads(bstack11l111l111_opy_)
  try:
    include_tags = bstack11l111l111_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ༔")] if bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ༕") in bstack11l111l111_opy_ and isinstance(bstack11l111l111_opy_[bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ༖")], list) else []
    exclude_tags = bstack11l111l111_opy_[bstack1ll1l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ༗")] if bstack1ll1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩ༘ࠬ") in bstack11l111l111_opy_ and isinstance(bstack11l111l111_opy_[bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ༙࠭")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤ༚") + str(error))
  return False
def bstack11l111lll1_opy_(config, bstack11l11l1ll1_opy_, bstack11l11l1111_opy_, bstack11l1111111_opy_):
  bstack11l11ll111_opy_ = bstack11l1111lll_opy_(config)
  bstack11l11l111l_opy_ = bstack11l11ll1l1_opy_(config)
  if bstack11l11ll111_opy_ is None or bstack11l11l111l_opy_ is None:
    logger.error(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ༛"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ༜"), bstack1ll1l11_opy_ (u"ࠬࢁࡽࠨ༝")))
    data = {
        bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ༞"): config[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ༟")],
        bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ༠"): config.get(bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ༡"), os.path.basename(os.getcwd())),
        bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭༢"): bstack11ll111l_opy_(),
        bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ༣"): config.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ༤"), bstack1ll1l11_opy_ (u"࠭ࠧ༥")),
        bstack1ll1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༦"): {
            bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ༧"): bstack11l11l1ll1_opy_,
            bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ༨"): bstack11l11l1111_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ༩"): __version__,
            bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭༪"): bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ༫"),
            bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭༬"): bstack1ll1l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ༭"),
            bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ༮"): bstack11l1111111_opy_
        },
        bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ༯"): settings,
        bstack1ll1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫ༰"): bstack111lllll1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫ༱"): bstack11lll111_opy_(),
        bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧ༲"): get_host_info(),
        bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ༳"): bstack111l1111_opy_(config)
    }
    headers = {
        bstack1ll1l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭༴"): bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱ༵ࠫ"),
    }
    config = {
        bstack1ll1l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ༶"): (bstack11l11ll111_opy_, bstack11l11l111l_opy_),
        bstack1ll1l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶ༷ࠫ"): headers
    }
    response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠫࡕࡕࡓࡕࠩ༸"), bstack11l11l1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ༹ࠬ"), data, config)
    bstack11l111ll1l_opy_ = response.json()
    if bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ༺")]:
      parsed = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ༻"), bstack1ll1l11_opy_ (u"ࠨࡽࢀࠫ༼")))
      parsed[bstack1ll1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ༽")] = bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ༾")][bstack1ll1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ༿")]
      os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ཀ")] = json.dumps(parsed)
      bstack1l1ll1l1l1_opy_.bstack11l111l11l_opy_(bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫཁ")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨག")])
      bstack1l1ll1l1l1_opy_.bstack11l11l1l11_opy_(bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭གྷ")][bstack1ll1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫང")])
      bstack1l1ll1l1l1_opy_.store()
      return bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨཅ")][bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩཆ")], bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪཇ")][bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩ཈")]
    else:
      logger.error(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨཉ") + bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩཊ")])
      if bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཋ")] == bstack1ll1l11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬཌ"):
        for bstack11l111l1l1_opy_ in bstack11l111ll1l_opy_[bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫཌྷ")]:
          logger.error(bstack11l111l1l1_opy_[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཎ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢཏ") +  str(error))
    return None, None
def bstack111llllll1_opy_():
  if os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬཐ")) is None:
    return {
        bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨད"): bstack1ll1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨདྷ"),
        bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན"): bstack1ll1l11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪཔ")
    }
  data = {bstack1ll1l11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ཕ"): bstack11ll111l_opy_()}
  headers = {
      bstack1ll1l11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭བ"): bstack1ll1l11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨབྷ") + os.getenv(bstack1ll1l11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨམ")),
      bstack1ll1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨཙ"): bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ཚ")
  }
  response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠫࡕ࡛ࡔࠨཛ"), bstack11l11l1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧཛྷ"), data, { bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧཝ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1l11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣཞ") + bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪཟ"))
      return {bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩའ"): bstack1ll1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫཡ"), bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬར"): bstack1ll1l11_opy_ (u"ࠬ࠭ལ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤཤ") + str(error))
    return {
        bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧཥ"): bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧས"),
        bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཧ"): str(error)
    }
def bstack11ll11l1_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l11l1lll_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫཨ"), {}).get(bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨཀྵ"), caps.get(bstack1ll1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬཪ"), bstack1ll1l11_opy_ (u"࠭ࠧཫ")))
    if bstack11l11l1lll_opy_:
      logger.warn(bstack1ll1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦཬ"))
      return False
    if options:
      bstack111lllllll_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111lllllll_opy_ = desired_capabilities
    else:
      bstack111lllllll_opy_ = {}
    browser = caps.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭཭"), bstack1ll1l11_opy_ (u"ࠩࠪ཮")).lower() or bstack111lllllll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ཯"), bstack1ll1l11_opy_ (u"ࠫࠬ཰")).lower()
    if browser != bstack1ll1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩཱࠬ"):
      logger.warn(bstack1ll1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤི"))
      return False
    browser_version = caps.get(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨཱི")) or caps.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰུࠪ")) or bstack111lllllll_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰཱུࠪ")) or bstack111lllllll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫྲྀ"), {}).get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬཷ")) or bstack111lllllll_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ླྀ"), {}).get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨཹ"))
    if browser_version and browser_version != bstack1ll1l11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺེࠧ") and int(browser_version.split(bstack1ll1l11_opy_ (u"ࠨ࠰ཻࠪ"))[0]) <= 98:
      logger.warn(bstack1ll1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠽࠴ོࠢ"))
      return False
    if not options:
      bstack11l11lll11_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨཽ")) or bstack111lllllll_opy_.get(bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩཾ"), {})
      if bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩཿ") in bstack11l11lll11_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶྀࠫ"), []):
        logger.warn(bstack1ll1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤཱྀ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥྂ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l11111ll_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩྃ"), {})
    bstack11l11111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ྄࠭")] = os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ྅"))
    bstack11l11l11ll_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭྆"), bstack1ll1l11_opy_ (u"࠭ࡻࡾࠩ྇"))).get(bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྈ"))
    caps[bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨྉ")] = True
    if bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪྊ") in caps:
      caps[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫྋ")][bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫྌ")] = bstack11l11111ll_opy_
      caps[bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ྍ")][bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ྎ")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྏ")] = bstack11l11l11ll_opy_
    else:
      caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧྐ")] = bstack11l11111ll_opy_
      caps[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨྑ")][bstack1ll1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫྒ")] = bstack11l11l11ll_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧྒྷ") +  str(error))
def bstack1l11l1lll_opy_(driver, bstack11l11ll1ll_opy_):
  try:
    setattr(driver, bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬྔ"), True)
    session = driver.session_id
    if session:
      bstack11l1111ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1111ll1_opy_ = False
      bstack11l1111ll1_opy_ = url.scheme in [bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳࠦྕ"), bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨྖ")]
      if bstack11l1111ll1_opy_:
        if bstack11l11ll1ll_opy_:
          logger.info(bstack1ll1l11_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣྗ"))
      return bstack11l11ll1ll_opy_
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ྘") + str(e))
    return False
def bstack1l11ll11ll_opy_(driver, name, path):
  try:
    bstack11l1111l11_opy_ = {
        bstack1ll1l11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪྙ"): threading.current_thread().current_test_uuid,
        bstack1ll1l11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩྚ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪྛ"), bstack1ll1l11_opy_ (u"࠭ࠧྜ")),
        bstack1ll1l11_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫྜྷ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩྞ"), bstack1ll1l11_opy_ (u"ࠩࠪྟ"))
    }
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ྠ"))
    logger.debug(driver.execute_async_script(bstack1l1ll1l1l1_opy_.perform_scan, {bstack1ll1l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦྡ"): name}))
    logger.debug(driver.execute_async_script(bstack1l1ll1l1l1_opy_.bstack11l111ll11_opy_, bstack11l1111l11_opy_))
    logger.info(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣྡྷ"))
  except Exception as bstack11l11l11l1_opy_:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣྣ") + str(path) + bstack1ll1l11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤྤ") + str(bstack11l11l11l1_opy_))