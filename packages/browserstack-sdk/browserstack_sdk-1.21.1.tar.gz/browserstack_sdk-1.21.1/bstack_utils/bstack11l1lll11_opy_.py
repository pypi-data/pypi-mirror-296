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
import re
from bstack_utils.bstack111llllll_opy_ import bstack1lll11llll1_opy_
def bstack1lll11l11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖦ")):
        return bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᖧ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖨ")):
        return bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᖩ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖪ")):
        return bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᖫ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᖬ")):
        return bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᖭ")
def bstack1lll11ll1l1_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᖮ"), fixture_name))
def bstack1lll11l1l11_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᖯ"), fixture_name))
def bstack1lll11l1l1l_opy_(fixture_name):
    return bool(re.match(bstack1ll1l11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᖰ"), fixture_name))
def bstack1lll11ll111_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᖱ")):
        return bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᖲ"), bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᖳ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖴ")):
        return bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᖵ"), bstack1ll1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᖶ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᖷ")):
        return bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᖸ"), bstack1ll1l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᖹ")
    elif fixture_name.startswith(bstack1ll1l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖺ")):
        return bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᖻ"), bstack1ll1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᖼ")
    return None, None
def bstack1lll1l11111_opy_(hook_name):
    if hook_name in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᖽ"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᖾ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11lll11_opy_(hook_name):
    if hook_name in [bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᖿ"), bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᗀ")]:
        return bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᗁ")
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᗂ"), bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᗃ")]:
        return bstack1ll1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᗄ")
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᗅ"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᗆ")]:
        return bstack1ll1l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᗇ")
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᗈ"), bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᗉ")]:
        return bstack1ll1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᗊ")
    return hook_name
def bstack1lll11ll11l_opy_(node, scenario):
    if hasattr(node, bstack1ll1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᗋ")):
        parts = node.nodeid.rsplit(bstack1ll1l11_opy_ (u"ࠣ࡝ࠥᗌ"))
        params = parts[-1]
        return bstack1ll1l11_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᗍ").format(scenario.name, params)
    return scenario.name
def bstack1lll11lll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᗎ")):
            examples = list(node.callspec.params[bstack1ll1l11_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᗏ")].values())
        return examples
    except:
        return []
def bstack1lll11ll1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11l1ll1_opy_(report):
    try:
        status = bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗐ")
        if report.passed or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᗑ"))):
            status = bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗒ")
        elif report.skipped:
            status = bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᗓ")
        bstack1lll11llll1_opy_(status)
    except:
        pass
def bstack1l11ll111l_opy_(status):
    try:
        bstack1lll11lllll_opy_ = bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗔ")
        if status == bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᗕ"):
            bstack1lll11lllll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᗖ")
        elif status == bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᗗ"):
            bstack1lll11lllll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᗘ")
        bstack1lll11llll1_opy_(bstack1lll11lllll_opy_)
    except:
        pass
def bstack1lll11l1lll_opy_(item=None, report=None, summary=None, extra=None):
    return