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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll1ll11_opy_
bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
def bstack1lll1l111l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l1111l_opy_(bstack1lll1l11ll1_opy_, bstack1lll1l11lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1l11ll1_opy_):
        with open(bstack1lll1l11ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1l111l1_opy_(bstack1lll1l11ll1_opy_):
        pac = get_pac(url=bstack1lll1l11ll1_opy_)
    else:
        raise Exception(bstack1ll1l11_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᖀ").format(bstack1lll1l11ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll1l11_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦᖁ"), 80))
        bstack1lll1l11l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1l11l11_opy_ = bstack1ll1l11_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬᖂ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l11lll_opy_, bstack1lll1l11l11_opy_)
    return proxy_url
def bstack1l1lllll1_opy_(config):
    return bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖃ") in config or bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖄ") in config
def bstack111111l11_opy_(config):
    if not bstack1l1lllll1_opy_(config):
        return
    if config.get(bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᖅ")):
        return config.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᖆ"))
    if config.get(bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᖇ")):
        return config.get(bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖈ"))
def bstack1lllllll1_opy_(config, bstack1lll1l11lll_opy_):
    proxy = bstack111111l11_opy_(config)
    proxies = {}
    if config.get(bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᖉ")) or config.get(bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᖊ")):
        if proxy.endswith(bstack1ll1l11_opy_ (u"࠭࠮ࡱࡣࡦࠫᖋ")):
            proxies = bstack111111111_opy_(proxy, bstack1lll1l11lll_opy_)
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᖌ"): proxy
            }
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᖍ"), proxies)
    return proxies
def bstack111111111_opy_(bstack1lll1l11ll1_opy_, bstack1lll1l11lll_opy_):
    proxies = {}
    global bstack1lll1l111ll_opy_
    if bstack1ll1l11_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᖎ") in globals():
        return bstack1lll1l111ll_opy_
    try:
        proxy = bstack1lll1l1111l_opy_(bstack1lll1l11ll1_opy_, bstack1lll1l11lll_opy_)
        if bstack1ll1l11_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᖏ") in proxy:
            proxies = {}
        elif bstack1ll1l11_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᖐ") in proxy or bstack1ll1l11_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᖑ") in proxy or bstack1ll1l11_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᖒ") in proxy:
            bstack1lll1l11l1l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠢࠡࠤᖓ"))
            if bstack1ll1l11_opy_ (u"ࠣ࠼࠲࠳ࠧᖔ") in bstack1ll1l11_opy_ (u"ࠤࠥᖕ").join(bstack1lll1l11l1l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖖ"): bstack1ll1l11_opy_ (u"ࠦࠧᖗ").join(bstack1lll1l11l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᖘ"): str(bstack1lll1l11l1l_opy_[0]).lower() + bstack1ll1l11_opy_ (u"ࠨ࠺࠰࠱ࠥᖙ") + bstack1ll1l11_opy_ (u"ࠢࠣᖚ").join(bstack1lll1l11l1l_opy_[1:])
                }
        elif bstack1ll1l11_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᖛ") in proxy:
            bstack1lll1l11l1l_opy_ = proxy.split(bstack1ll1l11_opy_ (u"ࠤࠣࠦᖜ"))
            if bstack1ll1l11_opy_ (u"ࠥ࠾࠴࠵ࠢᖝ") in bstack1ll1l11_opy_ (u"ࠦࠧᖞ").join(bstack1lll1l11l1l_opy_[1:]):
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᖟ"): bstack1ll1l11_opy_ (u"ࠨࠢᖠ").join(bstack1lll1l11l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᖡ"): bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᖢ") + bstack1ll1l11_opy_ (u"ࠤࠥᖣ").join(bstack1lll1l11l1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖤ"): proxy
            }
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᖥ"), bstack1lllll1ll11_opy_.format(bstack1lll1l11ll1_opy_, str(e)))
    bstack1lll1l111ll_opy_ = proxies
    return proxies