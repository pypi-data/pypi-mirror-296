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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111l1ll11l_opy_, bstack1llll1ll11_opy_, bstack1ll1l1l1_opy_, bstack1ll11ll1l1_opy_, \
    bstack111l1l1l11_opy_
def bstack1l1l111l11_opy_(bstack1ll1lllllll_opy_):
    for driver in bstack1ll1lllllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1ll11l_opy_(driver, status, reason=bstack1ll1l11_opy_ (u"ࠩࠪᗛ")):
    bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
    if bstack1lll11ll_opy_.bstack11l1l111ll_opy_():
        return
    bstack1l1ll1l11_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᗜ"), bstack1ll1l11_opy_ (u"ࠫࠬᗝ"), status, reason, bstack1ll1l11_opy_ (u"ࠬ࠭ᗞ"), bstack1ll1l11_opy_ (u"࠭ࠧᗟ"))
    driver.execute_script(bstack1l1ll1l11_opy_)
def bstack111l1ll1_opy_(page, status, reason=bstack1ll1l11_opy_ (u"ࠧࠨᗠ")):
    try:
        if page is None:
            return
        bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
        if bstack1lll11ll_opy_.bstack11l1l111ll_opy_():
            return
        bstack1l1ll1l11_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᗡ"), bstack1ll1l11_opy_ (u"ࠩࠪᗢ"), status, reason, bstack1ll1l11_opy_ (u"ࠪࠫᗣ"), bstack1ll1l11_opy_ (u"ࠫࠬᗤ"))
        page.evaluate(bstack1ll1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᗥ"), bstack1l1ll1l11_opy_)
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᗦ"), e)
def bstack1ll1ll1l1l_opy_(type, name, status, reason, bstack1ll11l1ll1_opy_, bstack1lllll111_opy_):
    bstack1111l1lll_opy_ = {
        bstack1ll1l11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᗧ"): type,
        bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗨ"): {}
    }
    if type == bstack1ll1l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᗩ"):
        bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᗪ")][bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᗫ")] = bstack1ll11l1ll1_opy_
        bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᗬ")][bstack1ll1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᗭ")] = json.dumps(str(bstack1lllll111_opy_))
    if type == bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᗮ"):
        bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗯ")][bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᗰ")] = name
    if type == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᗱ"):
        bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᗳ")] = status
        if status == bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗴ") and str(reason) != bstack1ll1l11_opy_ (u"ࠢࠣᗵ"):
            bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗶ")][bstack1ll1l11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᗷ")] = json.dumps(str(reason))
    bstack1111l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᗸ").format(json.dumps(bstack1111l1lll_opy_))
    return bstack1111l1l1_opy_
def bstack1lll111ll1_opy_(url, config, logger, bstack1l1l1lllll_opy_=False):
    hostname = bstack1llll1ll11_opy_(url)
    is_private = bstack1ll11ll1l1_opy_(hostname)
    try:
        if is_private or bstack1l1l1lllll_opy_:
            file_path = bstack111l1ll11l_opy_(bstack1ll1l11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᗹ"), bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᗺ"), logger)
            if os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᗻ")) and eval(
                    os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᗼ"))):
                return
            if (bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᗽ") in config and not config[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᗾ")]):
                os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᗿ")] = str(True)
                bstack1lll11111l1_opy_ = {bstack1ll1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᘀ"): hostname}
                bstack111l1l1l11_opy_(bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᘁ"), bstack1ll1l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᘂ"), bstack1lll11111l1_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1l1l_opy_(caps, bstack1lll111111l_opy_):
    if bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘃ") in caps:
        caps[bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘄ")][bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᘅ")] = True
        if bstack1lll111111l_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᘆ")][bstack1ll1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᘇ")] = bstack1lll111111l_opy_
    else:
        caps[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᘈ")] = True
        if bstack1lll111111l_opy_:
            caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘉ")] = bstack1lll111111l_opy_
def bstack1lll11llll1_opy_(bstack11ll11l1ll_opy_):
    bstack1lll1111111_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᘊ"), bstack1ll1l11_opy_ (u"ࠨࠩᘋ"))
    if bstack1lll1111111_opy_ == bstack1ll1l11_opy_ (u"ࠩࠪᘌ") or bstack1lll1111111_opy_ == bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᘍ"):
        threading.current_thread().testStatus = bstack11ll11l1ll_opy_
    else:
        if bstack11ll11l1ll_opy_ == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘎ"):
            threading.current_thread().testStatus = bstack11ll11l1ll_opy_