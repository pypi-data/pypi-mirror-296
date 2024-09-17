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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll11l11_opy_, bstack1ll1111l_opy_, bstack1l11l1l1_opy_, bstack1l1111l1l1_opy_,
                                    bstack111ll1l11l_opy_, bstack111ll1llll_opy_, bstack111ll1ll11_opy_, bstack111ll11l1l_opy_)
from bstack_utils.messages import bstack1l11lllll1_opy_, bstack11l1111ll_opy_
from bstack_utils.proxy import bstack1lllllll1_opy_, bstack111111l11_opy_
bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
logger = logging.getLogger(__name__)
def bstack11l1111lll_opy_(config):
    return config[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ኶")]
def bstack11l11ll1l1_opy_(config):
    return config[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭኷")]
def bstack1ll11lll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111l1l1ll1_opy_(obj):
    values = []
    bstack1111ll1l11_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣኸ"), re.I)
    for key in obj.keys():
        if bstack1111ll1l11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1lll1l_opy_(config):
    tags = []
    tags.extend(bstack111l1l1ll1_opy_(os.environ))
    tags.extend(bstack111l1l1ll1_opy_(config))
    return tags
def bstack111l1111ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l1l1111_opy_(bstack1111l111l1_opy_):
    if not bstack1111l111l1_opy_:
        return bstack1ll1l11_opy_ (u"ࠬ࠭ኹ")
    return bstack1ll1l11_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢኺ").format(bstack1111l111l1_opy_.name, bstack1111l111l1_opy_.email)
def bstack111lllll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l111l1l_opy_ = repo.common_dir
        info = {
            bstack1ll1l11_opy_ (u"ࠢࡴࡪࡤࠦኻ"): repo.head.commit.hexsha,
            bstack1ll1l11_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦኼ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll1l11_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤኽ"): repo.active_branch.name,
            bstack1ll1l11_opy_ (u"ࠥࡸࡦ࡭ࠢኾ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ኿"): bstack111l1l1111_opy_(repo.head.commit.committer),
            bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨዀ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ዁"): bstack111l1l1111_opy_(repo.head.commit.author),
            bstack1ll1l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧዂ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll1l11_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤዃ"): repo.head.commit.message,
            bstack1ll1l11_opy_ (u"ࠤࡵࡳࡴࡺࠢዄ"): repo.git.rev_parse(bstack1ll1l11_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧዅ")),
            bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ዆"): bstack111l111l1l_opy_,
            bstack1ll1l11_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ዇"): subprocess.check_output([bstack1ll1l11_opy_ (u"ࠨࡧࡪࡶࠥወ"), bstack1ll1l11_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥዉ"), bstack1ll1l11_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦዊ")]).strip().decode(
                bstack1ll1l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨዋ")),
            bstack1ll1l11_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧዌ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll1l11_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨው"): repo.git.rev_list(
                bstack1ll1l11_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧዎ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111ll1ll_opy_ = []
        for remote in remotes:
            bstack1111lllll1_opy_ = {
                bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦዏ"): remote.name,
                bstack1ll1l11_opy_ (u"ࠢࡶࡴ࡯ࠦዐ"): remote.url,
            }
            bstack11111ll1ll_opy_.append(bstack1111lllll1_opy_)
        bstack11111ll111_opy_ = {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨዑ"): bstack1ll1l11_opy_ (u"ࠤࡪ࡭ࡹࠨዒ"),
            **info,
            bstack1ll1l11_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦዓ"): bstack11111ll1ll_opy_
        }
        bstack11111ll111_opy_ = bstack111l11l1l1_opy_(bstack11111ll111_opy_)
        return bstack11111ll111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢዔ").format(err))
        return {}
def bstack111l11l1l1_opy_(bstack11111ll111_opy_):
    bstack1111ll1ll1_opy_ = bstack11111lll11_opy_(bstack11111ll111_opy_)
    if bstack1111ll1ll1_opy_ and bstack1111ll1ll1_opy_ > bstack111ll1l11l_opy_:
        bstack111111llll_opy_ = bstack1111ll1ll1_opy_ - bstack111ll1l11l_opy_
        bstack1111l111ll_opy_ = bstack111l11l1ll_opy_(bstack11111ll111_opy_[bstack1ll1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨዕ")], bstack111111llll_opy_)
        bstack11111ll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢዖ")] = bstack1111l111ll_opy_
        logger.info(bstack1ll1l11_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤ዗")
                    .format(bstack11111lll11_opy_(bstack11111ll111_opy_) / 1024))
    return bstack11111ll111_opy_
def bstack11111lll11_opy_(bstack1l1l1111_opy_):
    try:
        if bstack1l1l1111_opy_:
            bstack11111ll11l_opy_ = json.dumps(bstack1l1l1111_opy_)
            bstack1111llll1l_opy_ = sys.getsizeof(bstack11111ll11l_opy_)
            return bstack1111llll1l_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣዘ").format(e))
    return -1
def bstack111l11l1ll_opy_(field, bstack1111ll1111_opy_):
    try:
        bstack111l1l11l1_opy_ = len(bytes(bstack111ll1llll_opy_, bstack1ll1l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨዙ")))
        bstack111l111111_opy_ = bytes(field, bstack1ll1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩዚ"))
        bstack1111ll11ll_opy_ = len(bstack111l111111_opy_)
        bstack11111l11l1_opy_ = ceil(bstack1111ll11ll_opy_ - bstack1111ll1111_opy_ - bstack111l1l11l1_opy_)
        if bstack11111l11l1_opy_ > 0:
            bstack111l111l11_opy_ = bstack111l111111_opy_[:bstack11111l11l1_opy_].decode(bstack1ll1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪዛ"), errors=bstack1ll1l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬዜ")) + bstack111ll1llll_opy_
            return bstack111l111l11_opy_
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦዝ").format(e))
    return field
def bstack11lll111_opy_():
    env = os.environ
    if (bstack1ll1l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧዞ") in env and len(env[bstack1ll1l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨዟ")]) > 0) or (
            bstack1ll1l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣዠ") in env and len(env[bstack1ll1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤዡ")]) > 0):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤዢ"): bstack1ll1l11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨዣ"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤዤ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥዥ")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥዦ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦዧ")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤየ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥዩ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡉࠣዪ")) == bstack1ll1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦያ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤዬ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨይ"): bstack1ll1l11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦዮ"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዯ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢደ")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዱ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥዲ")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨዳ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦዴ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࠧድ")) == bstack1ll1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣዶ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦዷ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥዸ"): bstack1ll1l11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤዹ"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥዺ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣዻ")),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦዼ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧዽ")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥዾ"): env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦዿ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤጀ")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧጁ") and env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤጂ")) == bstack1ll1l11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦጃ"):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣጄ"): bstack1ll1l11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨጅ"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣጆ"): None,
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጇ"): None,
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨገ"): None
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦጉ")) and env.get(bstack1ll1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧጊ")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣጋ"): bstack1ll1l11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢጌ"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣግ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦጎ")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤጏ"): None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጐ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ጑"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨጒ")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤጓ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦጔ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጕ"): bstack1ll1l11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ጖"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ጗"): env.get(bstack1ll1l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧጘ")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጙ"): None,
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጚ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥጛ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࠤጜ")) == bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧጝ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦጞ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጟ"): bstack1ll1l11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨጠ"),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጡ"): env.get(bstack1ll1l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦጢ")),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጣ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧጤ")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጥ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧጦ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨጧ")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤጨ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣጩ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጪ"): bstack1ll1l11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢጫ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦጬ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨጭ")),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጮ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤጯ")),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦጰ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤጱ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡋࠥጲ")) == bstack1ll1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨጳ") and bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧጴ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣጵ"): bstack1ll1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢጶ"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣጷ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧጸ")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤጹ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥጺ")) or env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧጻ")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጼ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨጽ"))
        }
    if bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢጾ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦጿ"): bstack1ll1l11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢፀ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦፁ"): bstack1ll1l11_opy_ (u"ࠤࡾࢁࢀࢃࠢፂ").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ፃ")), env.get(bstack1ll1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫፄ"))),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢፅ"): env.get(bstack1ll1l11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧፆ")),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨፇ"): env.get(bstack1ll1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣፈ"))
        }
    if bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦፉ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣፊ"): bstack1ll1l11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨፋ"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣፌ"): bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧፍ").format(env.get(bstack1ll1l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ፎ")), env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩፏ")), env.get(bstack1ll1l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪፐ")), env.get(bstack1ll1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧፑ"))),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨፒ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤፓ")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧፔ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣፕ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤፖ")) and env.get(bstack1ll1l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦፗ")):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣፘ"): bstack1ll1l11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨፙ"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣፚ"): bstack1ll1l11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤ፛").format(env.get(bstack1ll1l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ፜")), env.get(bstack1ll1l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭፝")), env.get(bstack1ll1l11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩ፞"))),
            bstack1ll1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፟"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ፠")),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ፡"): env.get(bstack1ll1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ።"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ፣")), env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ፤")), env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ፥"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ፦"): bstack1ll1l11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ፧"),
            bstack1ll1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፨"): env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ፩")),
            bstack1ll1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፪"): env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ፫")),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ፬"): env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ፭"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ፮")):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ፯"): bstack1ll1l11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨ፰"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፱"): env.get(bstack1ll1l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥ፲")),
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ፳"): env.get(bstack1ll1l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤ፴")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ፵"): env.get(bstack1ll1l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥ፶"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢ፷")) or env.get(bstack1ll1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ፸")):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ፹"): bstack1ll1l11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥ፺"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ፻"): env.get(bstack1ll1l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ፼")),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ፽"): bstack1ll1l11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨ፾") if env.get(bstack1ll1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤ፿")) else None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎀ"): env.get(bstack1ll1l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᎁ"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᎂ")), env.get(bstack1ll1l11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᎃ")), env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᎄ"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎅ"): bstack1ll1l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᎆ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎇ"): None,
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎈ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᎉ")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎊ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᎋ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᎌ")):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎍ"): bstack1ll1l11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᎎ"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎏ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᎐")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᎑"): bstack1ll1l11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ᎒").format(env.get(bstack1ll1l11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩ᎓"))) if env.get(bstack1ll1l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᎔")) else None,
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᎕"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᎖"))
        }
    if bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ᎗"))):
        return {
            bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᎘"): bstack1ll1l11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ᎙"),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᎚"): env.get(bstack1ll1l11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ᎛")),
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᎜"): env.get(bstack1ll1l11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᎝")),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᎞"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᎟"))
        }
    if bstack1llll111_opy_(env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᎠ"))):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎡ"): bstack1ll1l11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᎢ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎣ"): bstack1ll1l11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᎤ").format(env.get(bstack1ll1l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᎥ")), env.get(bstack1ll1l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᎦ")), env.get(bstack1ll1l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᎧ"))),
            bstack1ll1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎨ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᎩ")),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎪ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᎫ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡎࠨᎬ")) == bstack1ll1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᎭ") and env.get(bstack1ll1l11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᎮ")) == bstack1ll1l11_opy_ (u"ࠨ࠱ࠣᎯ"):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎰ"): bstack1ll1l11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᎱ"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎲ"): bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᎳ").format(env.get(bstack1ll1l11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᎴ"))),
            bstack1ll1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᎵ"): None,
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎶ"): None,
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᎷ")):
        return {
            bstack1ll1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᎸ"): bstack1ll1l11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᎹ"),
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᎺ"): None,
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎻ"): env.get(bstack1ll1l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᎼ")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎽ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᎾ"))
        }
    if any([env.get(bstack1ll1l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᎿ")), env.get(bstack1ll1l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᏀ")), env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᏁ")), env.get(bstack1ll1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᏂ"))]):
        return {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏃ"): bstack1ll1l11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᏄ"),
            bstack1ll1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏅ"): None,
            bstack1ll1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᏆ"): env.get(bstack1ll1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᏇ")) or None,
            bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᏈ"): env.get(bstack1ll1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᏉ"), 0)
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᏊ")):
        return {
            bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᏋ"): bstack1ll1l11_opy_ (u"ࠢࡈࡱࡆࡈࠧᏌ"),
            bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᏍ"): None,
            bstack1ll1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏎ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᏏ")),
            bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏐ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᏑ"))
        }
    if env.get(bstack1ll1l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᏒ")):
        return {
            bstack1ll1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᏓ"): bstack1ll1l11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᏔ"),
            bstack1ll1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᏕ"): env.get(bstack1ll1l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᏖ")),
            bstack1ll1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᏗ"): env.get(bstack1ll1l11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᏘ")),
            bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏙ"): env.get(bstack1ll1l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᏚ"))
        }
    return {bstack1ll1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏛ"): None}
def get_host_info():
    return {
        bstack1ll1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᏜ"): platform.node(),
        bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᏝ"): platform.system(),
        bstack1ll1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤᏞ"): platform.machine(),
        bstack1ll1l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᏟ"): platform.version(),
        bstack1ll1l11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᏠ"): platform.architecture()[0]
    }
def bstack1lll1lllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l111ll1_opy_():
    if bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᏡ")):
        return bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᏢ")
    return bstack1ll1l11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᏣ")
def bstack111l1l1lll_opy_(driver):
    info = {
        bstack1ll1l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᏤ"): driver.capabilities,
        bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᏥ"): driver.session_id,
        bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭Ꮶ"): driver.capabilities.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᏧ"), None),
        bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᏨ"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᏩ"), None),
        bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᏪ"): driver.capabilities.get(bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᏫ"), None),
    }
    if bstack111l111ll1_opy_() == bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᏬ"):
        info[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭Ꮽ")] = bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᏮ") if bstack11111lll1_opy_() else bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᏯ")
    return info
def bstack11111lll1_opy_():
    if bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᏰ")):
        return True
    if bstack1llll111_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᏱ"), None)):
        return True
    return False
def bstack1l11ll1ll_opy_(bstack1111l1l1ll_opy_, url, data, config):
    headers = config.get(bstack1ll1l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᏲ"), None)
    proxies = bstack1lllllll1_opy_(config, url)
    auth = config.get(bstack1ll1l11_opy_ (u"ࠫࡦࡻࡴࡩࠩᏳ"), None)
    response = requests.request(
            bstack1111l1l1ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l111l1ll1_opy_(bstack1lll111l_opy_, size):
    bstack1llll1l1l_opy_ = []
    while len(bstack1lll111l_opy_) > size:
        bstack111ll11l1_opy_ = bstack1lll111l_opy_[:size]
        bstack1llll1l1l_opy_.append(bstack111ll11l1_opy_)
        bstack1lll111l_opy_ = bstack1lll111l_opy_[size:]
    bstack1llll1l1l_opy_.append(bstack1lll111l_opy_)
    return bstack1llll1l1l_opy_
def bstack111l1l11ll_opy_(message, bstack111l1ll1ll_opy_=False):
    os.write(1, bytes(message, bstack1ll1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᏴ")))
    os.write(1, bytes(bstack1ll1l11_opy_ (u"࠭࡜࡯ࠩᏵ"), bstack1ll1l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᏶")))
    if bstack111l1ll1ll_opy_:
        with open(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ᏷") + os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᏸ")] + bstack1ll1l11_opy_ (u"ࠪ࠲ࡱࡵࡧࠨᏹ"), bstack1ll1l11_opy_ (u"ࠫࡦ࠭ᏺ")) as f:
            f.write(message + bstack1ll1l11_opy_ (u"ࠬࡢ࡮ࠨᏻ"))
def bstack1111lll111_opy_():
    return os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᏼ")].lower() == bstack1ll1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬᏽ")
def bstack11ll1l1l1_opy_(bstack11111l111l_opy_):
    return bstack1ll1l11_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ᏾").format(bstack111ll11l11_opy_, bstack11111l111l_opy_)
def bstack11ll111l_opy_():
    return bstack11ll1l1l11_opy_().replace(tzinfo=None).isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫ᏿")
def bstack1111l1l111_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll1l11_opy_ (u"ࠪ࡞ࠬ᐀"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll1l11_opy_ (u"ࠫ࡟࠭ᐁ")))).total_seconds() * 1000
def bstack11111l1lll_opy_(timestamp):
    return bstack1111l11l1l_opy_(timestamp).isoformat() + bstack1ll1l11_opy_ (u"ࠬࡠࠧᐂ")
def bstack111l11lll1_opy_(bstack1111l1l11l_opy_):
    date_format = bstack1ll1l11_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫᐃ")
    bstack111l11l111_opy_ = datetime.datetime.strptime(bstack1111l1l11l_opy_, date_format)
    return bstack111l11l111_opy_.isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩᐄ")
def bstack1111ll11l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐅ")
    else:
        return bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᐆ")
def bstack1llll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨᐇ")
def bstack1111llll11_opy_(val):
    return val.__str__().lower() == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᐈ")
def bstack11ll111l11_opy_(bstack111l11111l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l11111l_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧᐉ").format(func.__name__, bstack111l11111l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l1111l1_opy_(bstack1111l11lll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111l11lll_opy_(cls, *args, **kwargs)
            except bstack111l11111l_opy_ as e:
                print(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᐊ").format(bstack1111l11lll_opy_.__name__, bstack111l11111l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l1111l1_opy_
    else:
        return decorator
def bstack111l1111_opy_(bstack11l1l1ll11_opy_):
    if bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᐋ") in bstack11l1l1ll11_opy_ and bstack1111llll11_opy_(bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᐌ")]):
        return False
    if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᐍ") in bstack11l1l1ll11_opy_ and bstack1111llll11_opy_(bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᐎ")]):
        return False
    return True
def bstack1111l1111_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack11111llll_opy_(hub_url):
    if bstack1l1ll11111_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᐏ")):
        if hub_url != bstack1ll1l11_opy_ (u"ࠬ࠭ᐐ"):
            return bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᐑ") + hub_url + bstack1ll1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᐒ")
        return bstack1l11l1l1_opy_
    if hub_url != bstack1ll1l11_opy_ (u"ࠨࠩᐓ"):
        return bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᐔ") + hub_url + bstack1ll1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᐕ")
    return bstack1l1111l1l1_opy_
def bstack1111ll1l1l_opy_():
    return isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᐖ")), str)
def bstack1llll1ll11_opy_(url):
    return urlparse(url).hostname
def bstack1ll11ll1l1_opy_(hostname):
    for bstack1l111l1lll_opy_ in bstack1ll1111l_opy_:
        regex = re.compile(bstack1l111l1lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1ll11l_opy_(bstack111l1l1l1l_opy_, file_name, logger):
    bstack1l1ll11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠬࢄࠧᐗ")), bstack111l1l1l1l_opy_)
    try:
        if not os.path.exists(bstack1l1ll11l_opy_):
            os.makedirs(bstack1l1ll11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"࠭ࡾࠨᐘ")), bstack111l1l1l1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll1l11_opy_ (u"ࠧࡸࠩᐙ")):
                pass
            with open(file_path, bstack1ll1l11_opy_ (u"ࠣࡹ࠮ࠦᐚ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l11lllll1_opy_.format(str(e)))
def bstack111l1l1l11_opy_(file_name, key, value, logger):
    file_path = bstack111l1ll11l_opy_(bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᐛ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lllll11_opy_ = json.load(open(file_path, bstack1ll1l11_opy_ (u"ࠪࡶࡧ࠭ᐜ")))
        else:
            bstack1l1lllll11_opy_ = {}
        bstack1l1lllll11_opy_[key] = value
        with open(file_path, bstack1ll1l11_opy_ (u"ࠦࡼ࠱ࠢᐝ")) as outfile:
            json.dump(bstack1l1lllll11_opy_, outfile)
def bstack11ll11lll_opy_(file_name, logger):
    file_path = bstack111l1ll11l_opy_(bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᐞ"), file_name, logger)
    bstack1l1lllll11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll1l11_opy_ (u"࠭ࡲࠨᐟ")) as bstack111l11ll1_opy_:
            bstack1l1lllll11_opy_ = json.load(bstack111l11ll1_opy_)
    return bstack1l1lllll11_opy_
def bstack1lll1ll111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᐠ") + file_path + bstack1ll1l11_opy_ (u"ࠨࠢࠪᐡ") + str(e))
def bstack1l1ll11111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll1l11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᐢ")
def bstack1ll1ll1ll_opy_(config):
    if bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᐣ") in config:
        del (config[bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᐤ")])
        return False
    if bstack1l1ll11111_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᐥ")):
        return False
    if bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᐦ")):
        return True
    if bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᐧ") in config and config[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᐨ")] is False:
        return False
    else:
        return True
def bstack11l111111_opy_(args_list, bstack111l11l11l_opy_):
    index = -1
    for value in bstack111l11l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll11lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll11lll_opy_ = bstack11lll11lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᐩ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᐪ"), exception=exception)
    def bstack11l1l11111_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐫ"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᐬ") in self.exception_type:
            return bstack1ll1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᐭ")
        return bstack1ll1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᐮ")
    def bstack11111ll1l1_opy_(self):
        if self.result != bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐯ"):
            return None
        if self.bstack11lll11lll_opy_:
            return self.bstack11lll11lll_opy_
        return bstack11111l1l1l_opy_(self.exception)
def bstack11111l1l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11111llll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1l1l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1lll1llll1_opy_(config, logger):
    try:
        import playwright
        bstack111l1llll1_opy_ = playwright.__file__
        bstack1111l1llll_opy_ = os.path.split(bstack111l1llll1_opy_)
        bstack1111lll1l1_opy_ = bstack1111l1llll_opy_[0] + bstack1ll1l11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬᐰ")
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ᐱ")] = bstack111111l11_opy_(config)
        with open(bstack1111lll1l1_opy_, bstack1ll1l11_opy_ (u"ࠫࡷ࠭ᐲ")) as f:
            bstack1ll1ll111_opy_ = f.read()
            bstack1111lll11l_opy_ = bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫᐳ")
            bstack111111ll1l_opy_ = bstack1ll1ll111_opy_.find(bstack1111lll11l_opy_)
            if bstack111111ll1l_opy_ == -1:
              process = subprocess.Popen(bstack1ll1l11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥᐴ"), shell=True, cwd=bstack1111l1llll_opy_[0])
              process.wait()
              bstack111l11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧᐵ")
              bstack1111ll1lll_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧᐶ")
              bstack111l1l111l_opy_ = bstack1ll1ll111_opy_.replace(bstack111l11ll11_opy_, bstack1111ll1lll_opy_)
              with open(bstack1111lll1l1_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫᐷ")) as f:
                f.write(bstack111l1l111l_opy_)
    except Exception as e:
        logger.error(bstack11l1111ll_opy_.format(str(e)))
def bstack1llll1111l_opy_():
  try:
    bstack11111l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᐸ"))
    bstack1111l1ll11_opy_ = []
    if os.path.exists(bstack11111l1l11_opy_):
      with open(bstack11111l1l11_opy_) as f:
        bstack1111l1ll11_opy_ = json.load(f)
      os.remove(bstack11111l1l11_opy_)
    return bstack1111l1ll11_opy_
  except:
    pass
  return []
def bstack1l1111l1ll_opy_(bstack1l1llllll_opy_):
  try:
    bstack1111l1ll11_opy_ = []
    bstack11111l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᐹ"))
    if os.path.exists(bstack11111l1l11_opy_):
      with open(bstack11111l1l11_opy_) as f:
        bstack1111l1ll11_opy_ = json.load(f)
    bstack1111l1ll11_opy_.append(bstack1l1llllll_opy_)
    with open(bstack11111l1l11_opy_, bstack1ll1l11_opy_ (u"ࠬࡽࠧᐺ")) as f:
        json.dump(bstack1111l1ll11_opy_, f)
  except:
    pass
def bstack1l111l111l_opy_(logger, bstack111ll11111_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᐻ"), bstack1ll1l11_opy_ (u"ࠧࠨᐼ"))
    if test_name == bstack1ll1l11_opy_ (u"ࠨࠩᐽ"):
        test_name = threading.current_thread().__dict__.get(bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨᐾ"), bstack1ll1l11_opy_ (u"ࠪࠫᐿ"))
    bstack11111l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠫ࠱ࠦࠧᑀ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111ll11111_opy_:
        bstack1l1ll111l1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᑁ"), bstack1ll1l11_opy_ (u"࠭࠰ࠨᑂ"))
        bstack1l1l1ll11_opy_ = {bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑃ"): test_name, bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᑄ"): bstack11111l1ll1_opy_, bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᑅ"): bstack1l1ll111l1_opy_}
        bstack1111l1lll1_opy_ = []
        bstack1111ll111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᑆ"))
        if os.path.exists(bstack1111ll111l_opy_):
            with open(bstack1111ll111l_opy_) as f:
                bstack1111l1lll1_opy_ = json.load(f)
        bstack1111l1lll1_opy_.append(bstack1l1l1ll11_opy_)
        with open(bstack1111ll111l_opy_, bstack1ll1l11_opy_ (u"ࠫࡼ࠭ᑇ")) as f:
            json.dump(bstack1111l1lll1_opy_, f)
    else:
        bstack1l1l1ll11_opy_ = {bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᑈ"): test_name, bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᑉ"): bstack11111l1ll1_opy_, bstack1ll1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᑊ"): str(multiprocessing.current_process().name)}
        if bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬᑋ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1ll11_opy_)
  except Exception as e:
      logger.warn(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᑌ").format(e))
def bstack1ll11l1111_opy_(error_message, test_name, index, logger):
  try:
    bstack111l1lll11_opy_ = []
    bstack1l1l1ll11_opy_ = {bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᑍ"): test_name, bstack1ll1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᑎ"): error_message, bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᑏ"): index}
    bstack11111l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᑐ"))
    if os.path.exists(bstack11111l1111_opy_):
        with open(bstack11111l1111_opy_) as f:
            bstack111l1lll11_opy_ = json.load(f)
    bstack111l1lll11_opy_.append(bstack1l1l1ll11_opy_)
    with open(bstack11111l1111_opy_, bstack1ll1l11_opy_ (u"ࠧࡸࠩᑑ")) as f:
        json.dump(bstack111l1lll11_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᑒ").format(e))
def bstack111ll1111_opy_(bstack11llllll_opy_, name, logger):
  try:
    bstack1l1l1ll11_opy_ = {bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑓ"): name, bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᑔ"): bstack11llllll_opy_, bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᑕ"): str(threading.current_thread()._name)}
    return bstack1l1l1ll11_opy_
  except Exception as e:
    logger.warn(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᑖ").format(e))
  return
def bstack111l1lllll_opy_():
    return platform.system() == bstack1ll1l11_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᑗ")
def bstack1l1l1l1l1l_opy_(bstack1111l1111l_opy_, config, logger):
    bstack1111llllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111l1111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᑘ").format(e))
    return bstack1111llllll_opy_
def bstack111l11ll1l_opy_(bstack1111l1l1l1_opy_, bstack111l1ll1l1_opy_):
    bstack1111l11ll1_opy_ = version.parse(bstack1111l1l1l1_opy_)
    bstack111l111lll_opy_ = version.parse(bstack111l1ll1l1_opy_)
    if bstack1111l11ll1_opy_ > bstack111l111lll_opy_:
        return 1
    elif bstack1111l11ll1_opy_ < bstack111l111lll_opy_:
        return -1
    else:
        return 0
def bstack11ll1l1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l11l1l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11111lll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111l11l11_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1ll1l11_opy_ (u"ࠨࡩࡨࡸࠬᑙ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l111l1l1l_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᑚ"))
    bstack1111l1ll1l_opy_ = True
    if bstack1111llll11_opy_(caps.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩᑛ"))) or bstack1111llll11_opy_(caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫᑜ"))):
        bstack1111l1ll1l_opy_ = False
    if bstack1ll1ll1ll_opy_({bstack1ll1l11_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧᑝ"): bstack1111l1ll1l_opy_}):
        bstack1l111l1l1l_opy_ = bstack1l111l1l1l_opy_ or {}
        bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᑞ")] = bstack11111lll1l_opy_(framework)
        bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑟ")] = bstack1111lll111_opy_()
        if getattr(options, bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᑠ"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᑡ"), bstack1l111l1l1l_opy_)
        else:
            options[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᑢ")] = bstack1l111l1l1l_opy_
    else:
        if getattr(options, bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᑣ"), None):
            options.set_capability(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑤ"), bstack11111lll1l_opy_(framework))
            options.set_capability(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑥ"), bstack1111lll111_opy_())
        else:
            options[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᑦ")] = bstack11111lll1l_opy_(framework)
            options[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑧ")] = bstack1111lll111_opy_()
    return options
def bstack111111lll1_opy_(bstack111l1ll111_opy_, framework):
    if bstack111l1ll111_opy_ and len(bstack111l1ll111_opy_.split(bstack1ll1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᑨ"))) > 1:
        ws_url = bstack111l1ll111_opy_.split(bstack1ll1l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᑩ"))[0]
        if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᑪ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11111l11ll_opy_ = json.loads(urllib.parse.unquote(bstack111l1ll111_opy_.split(bstack1ll1l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᑫ"))[1]))
            bstack11111l11ll_opy_ = bstack11111l11ll_opy_ or {}
            bstack11111l11ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᑬ")] = str(framework) + str(__version__)
            bstack11111l11ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᑭ")] = bstack1111lll111_opy_()
            bstack111l1ll111_opy_ = bstack111l1ll111_opy_.split(bstack1ll1l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑮ"))[0] + bstack1ll1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᑯ") + urllib.parse.quote(json.dumps(bstack11111l11ll_opy_))
    return bstack111l1ll111_opy_
def bstack11l1l1l1_opy_():
    global bstack1l11l1l11l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l11l1l11l_opy_ = BrowserType.connect
    return bstack1l11l1l11l_opy_
def bstack1ll11ll11_opy_(framework_name):
    global bstack1lll11ll11_opy_
    bstack1lll11ll11_opy_ = framework_name
    return framework_name
def bstack1lll1l1l11_opy_(self, *args, **kwargs):
    global bstack1l11l1l11l_opy_
    try:
        global bstack1lll11ll11_opy_
        if bstack1ll1l11_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᑰ") in kwargs:
            kwargs[bstack1ll1l11_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨᑱ")] = bstack111111lll1_opy_(
                kwargs.get(bstack1ll1l11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᑲ"), None),
                bstack1lll11ll11_opy_
            )
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨᑳ").format(str(e)))
    return bstack1l11l1l11l_opy_(self, *args, **kwargs)
def bstack111l11llll_opy_(bstack111ll1111l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lllllll1_opy_(bstack111ll1111l_opy_, bstack1ll1l11_opy_ (u"ࠢࠣᑴ"))
        if proxies and proxies.get(bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᑵ")):
            parsed_url = urlparse(proxies.get(bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᑶ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ᑷ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧᑸ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᑹ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᑺ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1ll_opy_(bstack111ll1111l_opy_):
    bstack1111l11l11_opy_ = {
        bstack111ll11l1l_opy_[bstack11111lllll_opy_]: bstack111ll1111l_opy_[bstack11111lllll_opy_]
        for bstack11111lllll_opy_ in bstack111ll1111l_opy_
        if bstack11111lllll_opy_ in bstack111ll11l1l_opy_
    }
    bstack1111l11l11_opy_[bstack1ll1l11_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢᑻ")] = bstack111l11llll_opy_(bstack111ll1111l_opy_, bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᑼ")))
    bstack1111l11111_opy_ = [element.lower() for element in bstack111ll1ll11_opy_]
    bstack1111lll1ll_opy_(bstack1111l11l11_opy_, bstack1111l11111_opy_)
    return bstack1111l11l11_opy_
def bstack1111lll1ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll1l11_opy_ (u"ࠤ࠭࠮࠯࠰ࠢᑽ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111lll1ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111lll1ll_opy_(item, keys)