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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1111llll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll1lll1_opy_ import bstack1llll1l1ll_opy_
import time
import requests
def bstack1l111l1111_opy_():
  global CONFIG
  headers = {
        bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lllllll1_opy_(CONFIG, bstack1lll1l11_opy_)
  try:
    response = requests.get(bstack1lll1l11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111l1l_opy_ = response.json()[bstack1ll1l11_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1lll1ll1l1_opy_.format(response.json()))
      return bstack1l111l1l_opy_
    else:
      logger.debug(bstack1lll1111l_opy_.format(bstack1ll1l11_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1lll1111l_opy_.format(e))
def bstack11111l1l1_opy_(hub_url):
  global CONFIG
  url = bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll1l11_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lllllll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1ll1lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1111111_opy_.format(hub_url, e))
def bstack111lll1l1_opy_():
  try:
    global bstack1111l111_opy_
    bstack1l111l1l_opy_ = bstack1l111l1111_opy_()
    bstack111l1llll_opy_ = []
    results = []
    for bstack111ll11l_opy_ in bstack1l111l1l_opy_:
      bstack111l1llll_opy_.append(bstack1lll111l1_opy_(target=bstack11111l1l1_opy_,args=(bstack111ll11l_opy_,)))
    for t in bstack111l1llll_opy_:
      t.start()
    for t in bstack111l1llll_opy_:
      results.append(t.join())
    bstack1l1lll1l_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1l11_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll1l11_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1lll1l_opy_[hub_url] = latency
    bstack1111ll11l_opy_ = min(bstack1l1lll1l_opy_, key= lambda x: bstack1l1lll1l_opy_[x])
    bstack1111l111_opy_ = bstack1111ll11l_opy_
    logger.debug(bstack1lllllll1l_opy_.format(bstack1111ll11l_opy_))
  except Exception as e:
    logger.debug(bstack1l1111ll1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1l11ll_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l1l1l1l_opy_, bstack1l11ll1ll_opy_, bstack11ll1l1l1_opy_, bstack1ll1l1l1_opy_, bstack111l1111_opy_, \
  Notset, bstack1ll1ll1ll_opy_, \
  bstack11ll11lll_opy_, bstack1lll1ll111_opy_, bstack11l111111_opy_, bstack11lll111_opy_, bstack1111l1111_opy_, bstack1lll1lllll_opy_, \
  bstack1ll11lll_opy_, \
  bstack1lll1llll1_opy_, bstack1llll1111l_opy_, bstack1l1111l1ll_opy_, bstack111ll1111_opy_, \
  bstack1l111l111l_opy_, bstack1ll11l1111_opy_, bstack1llll111_opy_, bstack11l1l1ll_opy_
from bstack_utils.bstack1l1ll1l1ll_opy_ import bstack1l11lllll_opy_
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack1l1lll11_opy_
from bstack_utils.bstack111llllll_opy_ import bstack1lll1ll11l_opy_, bstack111l1ll1_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack1ll11l11l_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.bstack1l1ll1l1l1_opy_ import bstack1l1ll1l1l1_opy_
from bstack_utils.proxy import bstack111111111_opy_, bstack1lllllll1_opy_, bstack111111l11_opy_, bstack1l1lllll1_opy_
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from browserstack_sdk.bstack1ll11ll1_opy_ import *
from browserstack_sdk.bstack1l11l11l11_opy_ import *
from bstack_utils.bstack11l1lll11_opy_ import bstack1l11ll111l_opy_
from browserstack_sdk.bstack11lll11ll_opy_ import *
import bstack_utils.bstack1ll111ll1l_opy_ as bstack1l111ll11_opy_
import bstack_utils.bstack1ll11l111_opy_ as bstack1ll1l11l1l_opy_
bstack11111l111_opy_ = bstack1ll1l11_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1ll111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack111l111l1_opy_ = None
CONFIG = {}
bstack1l1ll1111l_opy_ = {}
bstack1l11l111l1_opy_ = {}
bstack1l1l1l1l_opy_ = None
bstack1ll11ll111_opy_ = None
bstack1l1ll11l11_opy_ = None
bstack1ll1l1l1l_opy_ = -1
bstack1l11ll11_opy_ = 0
bstack11l1l1lll_opy_ = bstack1llll11lll_opy_
bstack1l1ll1llll_opy_ = 1
bstack1l1lll11l1_opy_ = False
bstack1l1111l11_opy_ = False
bstack1lll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩࢂ")
bstack1l1lll111l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪࢃ")
bstack11l1l1111_opy_ = False
bstack1l11l1111l_opy_ = True
bstack1111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫࢄ")
bstack1l1ll111_opy_ = []
bstack1111l111_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬࢅ")
bstack1l11l1ll11_opy_ = False
bstack1l1ll1ll_opy_ = None
bstack1ll1l111l1_opy_ = None
bstack1l1ll111ll_opy_ = None
bstack1l11ll1l1l_opy_ = -1
bstack1ll1l111l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠬࢄࠧࢆ")), bstack1ll1l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1ll1l11_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack11ll111l1_opy_ = 0
bstack111l1ll11_opy_ = 0
bstack1llll1l111_opy_ = []
bstack1lllll11l_opy_ = []
bstack1lllll11l1_opy_ = []
bstack11lllll1l_opy_ = []
bstack1ll1l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩࢉ")
bstack111l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪࢊ")
bstack1ll1l1111_opy_ = False
bstack11l1lll1_opy_ = False
bstack11lllll1_opy_ = {}
bstack1l1l1l11_opy_ = None
bstack1111l11ll_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1l11ll1l1_opy_ = None
bstack1lll1l1l1l_opy_ = None
bstack1l1l111111_opy_ = None
bstack11lll1111_opy_ = None
bstack11ll11ll1_opy_ = None
bstack1llll1l11_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1111ll1l1_opy_ = None
bstack1l1llll11_opy_ = None
bstack1ll11lll1l_opy_ = None
bstack111ll111_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack11lll11l1_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1ll111lll_opy_ = None
bstack1111l1ll1_opy_ = None
bstack1lllll111l_opy_ = None
bstack1l11l1l11l_opy_ = None
bstack1ll11111l_opy_ = False
bstack1l1l1l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠥࠦࢋ")
logger = bstack1l1l11ll_opy_.get_logger(__name__, bstack11l1l1lll_opy_)
bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
percy = bstack1111llll1_opy_()
bstack11l1l1l11_opy_ = bstack1llll1l1ll_opy_()
bstack1ll11l1l_opy_ = bstack11lll11ll_opy_()
def bstack1l111ll1l1_opy_():
  global CONFIG
  global bstack1ll1l1111_opy_
  global bstack1lll11ll_opy_
  bstack11l11lll_opy_ = bstack11l1l111_opy_(CONFIG)
  if bstack111l1111_opy_(CONFIG):
    if (bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack11l11lll_opy_ and str(bstack11l11lll_opy_[bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack1ll1l1111_opy_ = True
    bstack1lll11ll_opy_.bstack1ll111llll_opy_(bstack11l11lll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack1ll1l1111_opy_ = True
    bstack1lll11ll_opy_.bstack1ll111llll_opy_(True)
def bstack1l11111l11_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1ll11111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1l11_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1ll1l11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1111l11l_opy_
      bstack1111l11l_opy_ += bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1l11ll1ll1_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll1ll1ll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11ll1ll1_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll1l11_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1ll1l11_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1l1l1lll1_opy_():
  bstack11ll11ll_opy_ = bstack1l1l1l1111_opy_()
  if bstack11ll11ll_opy_ and os.path.exists(os.path.abspath(bstack11ll11ll_opy_)):
    fileName = bstack11ll11ll_opy_
  if bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1lllll1_opy_ = os.path.abspath(fileName)
  else:
    bstack1lllll1_opy_ = bstack1ll1l11_opy_ (u"࢛ࠬ࠭")
  bstack111llll11_opy_ = os.getcwd()
  bstack1ll111l1ll_opy_ = bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l11l111ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1lllll1_opy_)) and bstack111llll11_opy_ != bstack1ll1l11_opy_ (u"ࠣࠤ࢞"):
    bstack1lllll1_opy_ = os.path.join(bstack111llll11_opy_, bstack1ll111l1ll_opy_)
    if not os.path.exists(bstack1lllll1_opy_):
      bstack1lllll1_opy_ = os.path.join(bstack111llll11_opy_, bstack1l11l111ll_opy_)
    if bstack111llll11_opy_ != os.path.dirname(bstack111llll11_opy_):
      bstack111llll11_opy_ = os.path.dirname(bstack111llll11_opy_)
    else:
      bstack111llll11_opy_ = bstack1ll1l11_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1lllll1_opy_):
    bstack111111lll_opy_(
      bstack111l1l1l_opy_.format(os.getcwd()))
  try:
    with open(bstack1lllll1_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1ll1l11_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1l11ll1ll1_opy_)
      yaml.add_constructor(bstack1ll1l11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll1ll1ll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lllll1_opy_, bstack1ll1l11_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack111111lll_opy_(bstack1l1ll11l1_opy_.format(str(exc)))
def bstack1llll1l11l_opy_(config):
  bstack1l1111ll_opy_ = bstack1l11l1111_opy_(config)
  for option in list(bstack1l1111ll_opy_):
    if option.lower() in bstack111111ll1_opy_ and option != bstack111111ll1_opy_[option.lower()]:
      bstack1l1111ll_opy_[bstack111111ll1_opy_[option.lower()]] = bstack1l1111ll_opy_[option]
      del bstack1l1111ll_opy_[option]
  return config
def bstack1l11llllll_opy_():
  global bstack1l11l111l1_opy_
  for key, bstack1ll11l1lll_opy_ in bstack1lll1l111_opy_.items():
    if isinstance(bstack1ll11l1lll_opy_, list):
      for var in bstack1ll11l1lll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l111l1_opy_[key] = os.environ[var]
          break
    elif bstack1ll11l1lll_opy_ in os.environ and os.environ[bstack1ll11l1lll_opy_] and str(os.environ[bstack1ll11l1lll_opy_]).strip():
      bstack1l11l111l1_opy_[key] = os.environ[bstack1ll11l1lll_opy_]
  if bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1l11l111l1_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1l11l111l1_opy_[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1l1l1l1ll_opy_():
  global bstack1l1ll1111l_opy_
  global bstack1111l11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l1ll1111l_opy_[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l1ll1111l_opy_[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l111lll_opy_ in bstack111l1lll1_opy_.items():
    if isinstance(bstack1l111lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l111lll_opy_:
          if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l1ll1111l_opy_:
            bstack1l1ll1111l_opy_[key] = sys.argv[idx + 1]
            bstack1111l11l_opy_ += bstack1ll1l11_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1ll1l11_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l111lll_opy_.lower() == val.lower() and not key in bstack1l1ll1111l_opy_:
          bstack1l1ll1111l_opy_[key] = sys.argv[idx + 1]
          bstack1111l11l_opy_ += bstack1ll1l11_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l111lll_opy_ + bstack1ll1l11_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l11ll111_opy_(config):
  bstack11111l1l_opy_ = config.keys()
  for bstack1l11ll11l1_opy_, bstack1l1llll111_opy_ in bstack1l11ll1l11_opy_.items():
    if bstack1l1llll111_opy_ in bstack11111l1l_opy_:
      config[bstack1l11ll11l1_opy_] = config[bstack1l1llll111_opy_]
      del config[bstack1l1llll111_opy_]
  for bstack1l11ll11l1_opy_, bstack1l1llll111_opy_ in bstack1111ll1ll_opy_.items():
    if isinstance(bstack1l1llll111_opy_, list):
      for bstack11l1111l_opy_ in bstack1l1llll111_opy_:
        if bstack11l1111l_opy_ in bstack11111l1l_opy_:
          config[bstack1l11ll11l1_opy_] = config[bstack11l1111l_opy_]
          del config[bstack11l1111l_opy_]
          break
    elif bstack1l1llll111_opy_ in bstack11111l1l_opy_:
      config[bstack1l11ll11l1_opy_] = config[bstack1l1llll111_opy_]
      del config[bstack1l1llll111_opy_]
  for bstack11l1111l_opy_ in list(config):
    for bstack1l111l1ll_opy_ in bstack11llll11_opy_:
      if bstack11l1111l_opy_.lower() == bstack1l111l1ll_opy_.lower() and bstack11l1111l_opy_ != bstack1l111l1ll_opy_:
        config[bstack1l111l1ll_opy_] = config[bstack11l1111l_opy_]
        del config[bstack11l1111l_opy_]
  bstack1l1l1l111l_opy_ = [{}]
  if not config.get(bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack1l1l1l111l_opy_ = config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack1l1l1l111l_opy_:
    for bstack11l1111l_opy_ in list(platform):
      for bstack1l111l1ll_opy_ in bstack11llll11_opy_:
        if bstack11l1111l_opy_.lower() == bstack1l111l1ll_opy_.lower() and bstack11l1111l_opy_ != bstack1l111l1ll_opy_:
          platform[bstack1l111l1ll_opy_] = platform[bstack11l1111l_opy_]
          del platform[bstack11l1111l_opy_]
  for bstack1l11ll11l1_opy_, bstack1l1llll111_opy_ in bstack1111ll1ll_opy_.items():
    for platform in bstack1l1l1l111l_opy_:
      if isinstance(bstack1l1llll111_opy_, list):
        for bstack11l1111l_opy_ in bstack1l1llll111_opy_:
          if bstack11l1111l_opy_ in platform:
            platform[bstack1l11ll11l1_opy_] = platform[bstack11l1111l_opy_]
            del platform[bstack11l1111l_opy_]
            break
      elif bstack1l1llll111_opy_ in platform:
        platform[bstack1l11ll11l1_opy_] = platform[bstack1l1llll111_opy_]
        del platform[bstack1l1llll111_opy_]
  for bstack1l1l1ll1l_opy_ in bstack1l1lllll1l_opy_:
    if bstack1l1l1ll1l_opy_ in config:
      if not bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_] in config:
        config[bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_]] = {}
      config[bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_]].update(config[bstack1l1l1ll1l_opy_])
      del config[bstack1l1l1ll1l_opy_]
  for platform in bstack1l1l1l111l_opy_:
    for bstack1l1l1ll1l_opy_ in bstack1l1lllll1l_opy_:
      if bstack1l1l1ll1l_opy_ in list(platform):
        if not bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_] in platform:
          platform[bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_]] = {}
        platform[bstack1l1lllll1l_opy_[bstack1l1l1ll1l_opy_]].update(platform[bstack1l1l1ll1l_opy_])
        del platform[bstack1l1l1ll1l_opy_]
  config = bstack1llll1l11l_opy_(config)
  return config
def bstack111111l1l_opy_(config):
  global bstack1l1lll111l_opy_
  if bstack111l1111_opy_(config) and bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack1ll1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack11ll111l_opy_ = datetime.datetime.now()
      bstack1l1ll1l1_opy_ = bstack11ll111l_opy_.strftime(bstack1ll1l11_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack11l1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1l11_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1l1ll1l1_opy_, hostname, bstack11l1ll111_opy_)
      config[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1l1lll111l_opy_ = config[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack1lll1l1111_opy_():
  bstack1lll11l11_opy_ =  bstack11lll111_opy_()[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack1lll11l11_opy_ if bstack1lll11l11_opy_ else -1
def bstack1l11ll1lll_opy_(bstack1lll11l11_opy_):
  global CONFIG
  if not bstack1ll1l11_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack1ll1l11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack1lll11l11_opy_)
  )
def bstack1ll1l111_opy_():
  global CONFIG
  if not bstack1ll1l11_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack11ll111l_opy_ = datetime.datetime.now()
  bstack1l1ll1l1_opy_ = bstack11ll111l_opy_.strftime(bstack1ll1l11_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack1ll1l11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1l1ll1l1_opy_
  )
def bstack1ll1111111_opy_():
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack1ll1l11_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack1ll1l11_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1ll1l111_opy_()
    os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack1ll1l11_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack1lll11l11_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪࣞ")
  bstack1l11l111_opy_ = bstack1lll1l1111_opy_()
  if bstack1l11l111_opy_ != -1:
    bstack1lll11l11_opy_ = bstack1ll1l11_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1l11l111_opy_)
  if bstack1lll11l11_opy_ == bstack1ll1l11_opy_ (u"ࠫࠬ࣠"):
    bstack11ll1lll_opy_ = bstack1llll11ll1_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack11ll1lll_opy_ != -1:
      bstack1lll11l11_opy_ = str(bstack11ll1lll_opy_)
  if bstack1lll11l11_opy_:
    bstack1l11ll1lll_opy_(bstack1lll11l11_opy_)
    os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1l1ll11lll_opy_(bstack111lllll_opy_, bstack1l1llllll1_opy_, path):
  bstack1l1l1111_opy_ = {
    bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1l1llllll1_opy_
  }
  if os.path.exists(path):
    bstack1l1lllll11_opy_ = json.load(open(path, bstack1ll1l11_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1l1lllll11_opy_ = {}
  bstack1l1lllll11_opy_[bstack111lllll_opy_] = bstack1l1l1111_opy_
  with open(path, bstack1ll1l11_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1l1lllll11_opy_, outfile)
def bstack1llll11ll1_opy_(bstack111lllll_opy_):
  bstack111lllll_opy_ = str(bstack111lllll_opy_)
  bstack1l1ll11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠫࢃ࠭ࣧ")), bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1l1ll11l_opy_):
      os.makedirs(bstack1l1ll11l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"࠭ࡾࠨࣩ")), bstack1ll1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1l11_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack1ll1l11_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1l11_opy_ (u"ࠫࡷ࣮࠭")) as bstack111l11ll1_opy_:
      bstack11111ll11_opy_ = json.load(bstack111l11ll1_opy_)
    if bstack111lllll_opy_ in bstack11111ll11_opy_:
      bstack11l1111l1_opy_ = bstack11111ll11_opy_[bstack111lllll_opy_][bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1l111l1l1_opy_ = int(bstack11l1111l1_opy_) + 1
      bstack1l1ll11lll_opy_(bstack111lllll_opy_, bstack1l111l1l1_opy_, file_path)
      return bstack1l111l1l1_opy_
    else:
      bstack1l1ll11lll_opy_(bstack111lllll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l11lllll1_opy_.format(str(e)))
    return -1
def bstack1l1l1l11l_opy_(config):
  if not config[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack1l1l11ll1l_opy_(config, index=0):
  global bstack11l1l1111_opy_
  bstack1l111l1l1l_opy_ = {}
  caps = bstack1ll1111l1_opy_ + bstack111ll1ll_opy_
  if bstack11l1l1111_opy_:
    caps += bstack1l1l11ll1_opy_
  for key in config:
    if key in caps + [bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack1l111l1l1l_opy_[key] = config[key]
  if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack1ll111l111_opy_ in config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack1ll111l111_opy_ in caps:
        continue
      bstack1l111l1l1l_opy_[bstack1ll111l111_opy_] = config[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack1ll111l111_opy_]
  bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack1ll1l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack1l111l1l1l_opy_:
    del (bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack1l111l1l1l_opy_
def bstack11llllllll_opy_(config):
  global bstack11l1l1111_opy_
  bstack1l11llll1l_opy_ = {}
  caps = bstack111ll1ll_opy_
  if bstack11l1l1111_opy_:
    caps += bstack1l1l11ll1_opy_
  for key in caps:
    if key in config:
      bstack1l11llll1l_opy_[key] = config[key]
  return bstack1l11llll1l_opy_
def bstack1l111lll11_opy_(bstack1l111l1l1l_opy_, bstack1l11llll1l_opy_):
  bstack11lll11l_opy_ = {}
  for key in bstack1l111l1l1l_opy_.keys():
    if key in bstack1l11ll1l11_opy_:
      bstack11lll11l_opy_[bstack1l11ll1l11_opy_[key]] = bstack1l111l1l1l_opy_[key]
    else:
      bstack11lll11l_opy_[key] = bstack1l111l1l1l_opy_[key]
  for key in bstack1l11llll1l_opy_:
    if key in bstack1l11ll1l11_opy_:
      bstack11lll11l_opy_[bstack1l11ll1l11_opy_[key]] = bstack1l11llll1l_opy_[key]
    else:
      bstack11lll11l_opy_[key] = bstack1l11llll1l_opy_[key]
  return bstack11lll11l_opy_
def bstack1llll111l1_opy_(config, index=0):
  global bstack11l1l1111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1ll1lllll1_opy_ = bstack1l1l1l1l1l_opy_(bstack1llllll1ll_opy_, config, logger)
  bstack1l11llll1l_opy_ = bstack11llllllll_opy_(config)
  bstack1ll11lllll_opy_ = bstack111ll1ll_opy_
  bstack1ll11lllll_opy_ += bstack1ll1111l11_opy_
  bstack1l11llll1l_opy_ = update(bstack1l11llll1l_opy_, bstack1ll1lllll1_opy_)
  if bstack11l1l1111_opy_:
    bstack1ll11lllll_opy_ += bstack1l1l11ll1_opy_
  if bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack1ll11ll1l_opy_ = bstack1l1l1l1l1l_opy_(bstack1llllll1ll_opy_, config[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack1ll11lllll_opy_ += list(bstack1ll11ll1l_opy_.keys())
    for bstack1lll11lll1_opy_ in bstack1ll11lllll_opy_:
      if bstack1lll11lll1_opy_ in config[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1lll11lll1_opy_ == bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll11ll1l_opy_[bstack1lll11lll1_opy_] = str(config[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1lll11lll1_opy_] * 1.0)
          except:
            bstack1ll11ll1l_opy_[bstack1lll11lll1_opy_] = str(config[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1lll11lll1_opy_])
        else:
          bstack1ll11ll1l_opy_[bstack1lll11lll1_opy_] = config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1lll11lll1_opy_]
        del (config[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1lll11lll1_opy_])
    bstack1l11llll1l_opy_ = update(bstack1l11llll1l_opy_, bstack1ll11ll1l_opy_)
  bstack1l111l1l1l_opy_ = bstack1l1l11ll1l_opy_(config, index)
  for bstack11l1111l_opy_ in bstack111ll1ll_opy_ + list(bstack1ll1lllll1_opy_.keys()):
    if bstack11l1111l_opy_ in bstack1l111l1l1l_opy_:
      bstack1l11llll1l_opy_[bstack11l1111l_opy_] = bstack1l111l1l1l_opy_[bstack11l1111l_opy_]
      del (bstack1l111l1l1l_opy_[bstack11l1111l_opy_])
  if bstack1ll1ll1ll_opy_(config):
    bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1l11llll1l_opy_)
    caps[bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1l111l1l1l_opy_
  else:
    bstack1l111l1l1l_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1l111lll11_opy_(bstack1l111l1l1l_opy_, bstack1l11llll1l_opy_))
    if bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack11111llll_opy_():
  global bstack1111l111_opy_
  if bstack1l1ll11111_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1111l111_opy_ != bstack1ll1l11_opy_ (u"ࠪࠫग"):
      return bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1l11l1l1_opy_
  if bstack1111l111_opy_ != bstack1ll1l11_opy_ (u"࠭ࠧच"):
    return bstack1ll1l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l1111l1l1_opy_
def bstack1l11111l1l_opy_(options):
  return hasattr(options, bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l11l1l_opy_(options, bstack11ll1ll1_opy_):
  for bstack111lll1ll_opy_ in bstack11ll1ll1_opy_:
    if bstack111lll1ll_opy_ in [bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1ll1l11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack111lll1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack111lll1ll_opy_] = update(options._experimental_options[bstack111lll1ll_opy_],
                                                         bstack11ll1ll1_opy_[bstack111lll1ll_opy_])
    else:
      options.add_experimental_option(bstack111lll1ll_opy_, bstack11ll1ll1_opy_[bstack111lll1ll_opy_])
  if bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack11ll1ll1_opy_:
    for arg in bstack11ll1ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack11ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1ll1l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack11ll1ll1_opy_:
    for ext in bstack11ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack11ll1ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1ll11l1ll_opy_(options, bstack1ll1l1l1ll_opy_):
  if bstack1ll1l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1ll1l1l1ll_opy_:
    for bstack1l1lll11l_opy_ in bstack1ll1l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1l1lll11l_opy_ in options._preferences:
        options._preferences[bstack1l1lll11l_opy_] = update(options._preferences[bstack1l1lll11l_opy_], bstack1ll1l1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1l1lll11l_opy_])
      else:
        options.set_preference(bstack1l1lll11l_opy_, bstack1ll1l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l1lll11l_opy_])
  if bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1ll1l1l1ll_opy_:
    for arg in bstack1ll1l1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1l1111l11l_opy_(options, bstack1l1lll1lll_opy_):
  if bstack1ll1l11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1l1lll1lll_opy_:
    options.use_webview(bool(bstack1l1lll1lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack111l11l1l_opy_(options, bstack1l1lll1lll_opy_)
def bstack1ll11l1l11_opy_(options, bstack1lll1111_opy_):
  for bstack1l11ll1l_opy_ in bstack1lll1111_opy_:
    if bstack1l11ll1l_opy_ in [bstack1ll1l11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1l11ll1l_opy_, bstack1lll1111_opy_[bstack1l11ll1l_opy_])
  if bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1lll1111_opy_:
    for arg in bstack1lll1111_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1ll1l11_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1lll1111_opy_:
    options.bstack11l1ll1l_opy_(bool(bstack1lll1111_opy_[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack11l11l1l1_opy_(options, bstack1ll1l111ll_opy_):
  for bstack11lll1lll_opy_ in bstack1ll1l111ll_opy_:
    if bstack11lll1lll_opy_ in [bstack1ll1l11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack11lll1lll_opy_] = bstack1ll1l111ll_opy_[bstack11lll1lll_opy_]
  if bstack1ll1l11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1ll1l111ll_opy_:
    for bstack1ll1lll11l_opy_ in bstack1ll1l111ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1lll1l1l1_opy_(
        bstack1ll1lll11l_opy_, bstack1ll1l111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1ll1lll11l_opy_])
  if bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1ll1l111ll_opy_:
    for arg in bstack1ll1l111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1llll1lll1_opy_(options, caps):
  if not hasattr(options, bstack1ll1l11_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1ll1l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack111l11l1l_opy_(options, caps[bstack1ll1l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1ll11l1ll_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1ll11l1l11_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1ll1l11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1l1111l11l_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1ll1l11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack11l11l1l1_opy_(options, caps[bstack1ll1l11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1l1l1111l_opy_(caps):
  global bstack11l1l1111_opy_
  if isinstance(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack11l1l1111_opy_ = eval(os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack11l1l1111_opy_:
    if bstack1l11111l11_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1ll1l11_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1ll1l11_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1ll1l11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1ll1l11_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1ll1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1ll1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1ll1l11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1ll1l11_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1ll1l11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1ll1l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1ll1l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1ll1l11_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11111l1l_opy_(options):
        return None
      for bstack11l1111l_opy_ in caps.keys():
        options.set_capability(bstack11l1111l_opy_, caps[bstack11l1111l_opy_])
      bstack1llll1lll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll11lll_opy_(options, bstack1ll111l1_opy_):
  if not bstack1l11111l1l_opy_(options):
    return
  for bstack11l1111l_opy_ in bstack1ll111l1_opy_.keys():
    if bstack11l1111l_opy_ in bstack1ll1111l11_opy_:
      continue
    if bstack11l1111l_opy_ in options._caps and type(options._caps[bstack11l1111l_opy_]) in [dict, list]:
      options._caps[bstack11l1111l_opy_] = update(options._caps[bstack11l1111l_opy_], bstack1ll111l1_opy_[bstack11l1111l_opy_])
    else:
      options.set_capability(bstack11l1111l_opy_, bstack1ll111l1_opy_[bstack11l1111l_opy_])
  bstack1llll1lll1_opy_(options, bstack1ll111l1_opy_)
  if bstack1ll1l11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1ll1l11_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1l1111l1_opy_(proxy_config):
  if bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1ll1l11_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1ll1l11_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1ll1l11_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1ll1l11_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack11l1ll1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1l1111l1_opy_(config[bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack11lll1l1l_opy_(self):
  global CONFIG
  global bstack1l1llll11_opy_
  try:
    proxy = bstack111111l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1l11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack111111111_opy_(proxy, bstack11111llll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll1l11ll_opy_ = proxies.popitem()
          if bstack1ll1l11_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1lll1l11ll_opy_:
            return bstack1lll1l11ll_opy_
          else:
            return bstack1ll1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1lll1l11ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l1llll11_opy_(self)
def bstack1ll11llll_opy_():
  global CONFIG
  return bstack1l1lllll1_opy_(CONFIG) and bstack1lll1lllll_opy_() and bstack1l1ll11111_opy_() >= version.parse(bstack111l11l1_opy_)
def bstack1111l1l1l_opy_():
  global CONFIG
  return (bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1ll1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1ll11lll_opy_()
def bstack1l11l1111_opy_(config):
  bstack1l1111ll_opy_ = {}
  if bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1l1111ll_opy_ = config[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1ll1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1l1111ll_opy_ = config[bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack111111l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1l11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1l1111ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1l11_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1lllllll1_opy_(config, bstack11111llll_opy_())
        if len(proxies) > 0:
          protocol, bstack1lll1l11ll_opy_ = proxies.popitem()
          if bstack1ll1l11_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1lll1l11ll_opy_:
            parsed_url = urlparse(bstack1lll1l11ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1l11_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1lll1l11ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1111ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1111ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1111ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1111ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1l1111ll_opy_
def bstack11l1l111_opy_(config):
  if bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack11ll1l1l_opy_(caps):
  global bstack1l1lll111l_opy_
  if bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1l1lll111l_opy_:
      caps[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1ll1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1l1lll111l_opy_
  else:
    caps[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1l1lll111l_opy_:
      caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1l1lll111l_opy_
def bstack1ll1l11ll1_opy_():
  global CONFIG
  if not bstack111l1111_opy_(CONFIG):
    return
  if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1llll111_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1llll111_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack1ll1l11_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1l1111ll_opy_ = bstack1l11l1111_opy_(CONFIG)
    bstack1l1111111l_opy_(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1l1111ll_opy_)
def bstack1l1111111l_opy_(key, bstack1l1111ll_opy_):
  global bstack111l111l1_opy_
  logger.info(bstack1l1l1llll_opy_)
  try:
    bstack111l111l1_opy_ = Local()
    bstack1l11lll111_opy_ = {bstack1ll1l11_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1l11lll111_opy_.update(bstack1l1111ll_opy_)
    logger.debug(bstack11ll1llll_opy_.format(str(bstack1l11lll111_opy_)))
    bstack111l111l1_opy_.start(**bstack1l11lll111_opy_)
    if bstack111l111l1_opy_.isRunning():
      logger.info(bstack1l11l1l1ll_opy_)
  except Exception as e:
    bstack111111lll_opy_(bstack1ll1llll1_opy_.format(str(e)))
def bstack1ll1lllll_opy_():
  global bstack111l111l1_opy_
  if bstack111l111l1_opy_.isRunning():
    logger.info(bstack1l1ll11ll1_opy_)
    bstack111l111l1_opy_.stop()
  bstack111l111l1_opy_ = None
def bstack1llll1llll_opy_(bstack1l1lll1l1l_opy_=[]):
  global CONFIG
  bstack1lll1111l1_opy_ = []
  bstack1l111111l1_opy_ = [bstack1ll1l11_opy_ (u"ࠨࡱࡶࠫও"), bstack1ll1l11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1ll1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1l1lll1l1l_opy_:
      bstack11l1ll1ll_opy_ = {}
      for k in bstack1l111111l1_opy_:
        val = CONFIG[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1ll1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack11l1ll1ll_opy_[k] = val
      if(err[bstack1ll1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1ll1l11_opy_ (u"ࠪࠫজ")):
        bstack11l1ll1ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1lll1111l1_opy_.append(bstack11l1ll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1lll1111l1_opy_
def bstack1ll11l11_opy_(file_name):
  bstack11ll11111_opy_ = []
  try:
    bstack1ll11111_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll11111_opy_):
      with open(bstack1ll11111_opy_) as f:
        bstack1l1111lll_opy_ = json.load(f)
        bstack11ll11111_opy_ = bstack1l1111lll_opy_
      os.remove(bstack1ll11111_opy_)
    return bstack11ll11111_opy_
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack11ll11111_opy_
def bstack1l1l111l11_opy_():
  global bstack1l1l1l1l1_opy_
  global bstack1l1ll111_opy_
  global bstack1llll1l111_opy_
  global bstack1lllll11l_opy_
  global bstack1lllll11l1_opy_
  global bstack111l11ll_opy_
  global CONFIG
  bstack1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l111l11l_opy_ in [bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1ll1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack11ll1l111_opy_()
  percy.shutdown()
  if bstack1l1l1l1l1_opy_:
    logger.warning(bstack1l1l1l11l1_opy_.format(str(bstack1l1l1l1l1_opy_)))
  else:
    try:
      bstack1l1lllll11_opy_ = bstack11ll11lll_opy_(bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1lllll11_opy_.get(bstack1ll1l11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1lllll11_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1ll1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l1l1l11l1_opy_.format(str(bstack1l1lllll11_opy_[bstack1ll1l11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11ll1l11_opy_)
  global bstack111l111l1_opy_
  if bstack111l111l1_opy_:
    bstack1ll1lllll_opy_()
  try:
    for driver in bstack1l1ll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11ll11_opy_)
  if bstack111l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1lllll11l1_opy_ = bstack1ll11l11_opy_(bstack1ll1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack111l11ll_opy_ == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1lllll11l_opy_) == 0:
    bstack1lllll11l_opy_ = bstack1ll11l11_opy_(bstack1ll1l11_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1lllll11l_opy_) == 0:
      bstack1lllll11l_opy_ = bstack1ll11l11_opy_(bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1ll11ll11l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪর")
  if len(bstack1llll1l111_opy_) > 0:
    bstack1ll11ll11l_opy_ = bstack1llll1llll_opy_(bstack1llll1l111_opy_)
  elif len(bstack1lllll11l_opy_) > 0:
    bstack1ll11ll11l_opy_ = bstack1llll1llll_opy_(bstack1lllll11l_opy_)
  elif len(bstack1lllll11l1_opy_) > 0:
    bstack1ll11ll11l_opy_ = bstack1llll1llll_opy_(bstack1lllll11l1_opy_)
  elif len(bstack11lllll1l_opy_) > 0:
    bstack1ll11ll11l_opy_ = bstack1llll1llll_opy_(bstack11lllll1l_opy_)
  if bool(bstack1ll11ll11l_opy_):
    bstack1l1ll1ll1_opy_(bstack1ll11ll11l_opy_)
  else:
    bstack1l1ll1ll1_opy_()
  bstack1lll1ll111_opy_(bstack11l111l11_opy_, logger)
  bstack1l1l11ll_opy_.bstack11llll11l_opy_(CONFIG)
  if len(bstack1lllll11l1_opy_) > 0:
    sys.exit(len(bstack1lllll11l1_opy_))
def bstack1111l1ll_opy_(bstack1lll1ll11_opy_, frame):
  global bstack1lll11ll_opy_
  logger.error(bstack1lllll1111_opy_)
  bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1lll1ll11_opy_)
  if hasattr(signal, bstack1ll1l11_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1lll1ll11_opy_).name)
  else:
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack1ll1l11_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1ll11l11l_opy_.stop(bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack1l1l111l11_opy_()
  sys.exit(1)
def bstack111111lll_opy_(err):
  logger.critical(bstack1ll111ll_opy_.format(str(err)))
  bstack1l1ll1ll1_opy_(bstack1ll111ll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1l111l11_opy_)
  bstack11ll1l111_opy_()
  sys.exit(1)
def bstack1ll111l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1ll1ll1_opy_(message, True)
  atexit.unregister(bstack1l1l111l11_opy_)
  bstack11ll1l111_opy_()
  sys.exit(1)
def bstack1lll1ll1_opy_():
  global CONFIG
  global bstack1l1ll1111l_opy_
  global bstack1l11l111l1_opy_
  global bstack1l11l1111l_opy_
  CONFIG = bstack1l1l1lll1_opy_()
  load_dotenv(CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack1l11llllll_opy_()
  bstack1l1l1l1ll_opy_()
  CONFIG = bstack1l11ll111_opy_(CONFIG)
  update(CONFIG, bstack1l11l111l1_opy_)
  update(CONFIG, bstack1l1ll1111l_opy_)
  CONFIG = bstack111111l1l_opy_(CONFIG)
  bstack1l11l1111l_opy_ = bstack111l1111_opy_(CONFIG)
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack1l11l1111l_opy_.__str__()
  bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack1l11l1111l_opy_)
  if (bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack1l1ll1111l_opy_) or (
          bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack1l11l111l1_opy_):
    if os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack1ll1111111_opy_()
  elif (bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack1l11l111l1_opy_ and bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack1l1ll1111l_opy_):
    del (CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack1l1l1l11l_opy_(CONFIG):
    bstack111111lll_opy_(bstack1l11111ll1_opy_)
  bstack1ll1l11lll_opy_()
  bstack1lll1l1lll_opy_()
  if bstack11l1l1111_opy_:
    CONFIG[bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack11l111ll_opy_(CONFIG)
    logger.info(bstack1111lllll_opy_.format(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack1l11l1111l_opy_:
    CONFIG[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack11111ll1l_opy_(config, bstack11111lll1_opy_):
  global CONFIG
  global bstack11l1l1111_opy_
  CONFIG = config
  bstack11l1l1111_opy_ = bstack11111lll1_opy_
def bstack1lll1l1lll_opy_():
  global CONFIG
  global bstack11l1l1111_opy_
  if bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l1l11l_opy_)
    bstack11l1l1111_opy_ = True
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack11l111ll_opy_(config):
  bstack1ll1llll11_opy_ = bstack1ll1l11_opy_ (u"্ࠪࠫ")
  app = config[bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11llll111_opy_:
      if os.path.exists(app):
        bstack1ll1llll11_opy_ = bstack1lll11l1l_opy_(config, app)
      elif bstack111l111ll_opy_(app):
        bstack1ll1llll11_opy_ = app
      else:
        bstack111111lll_opy_(bstack1l11l11l1l_opy_.format(app))
    else:
      if bstack111l111ll_opy_(app):
        bstack1ll1llll11_opy_ = app
      elif os.path.exists(app):
        bstack1ll1llll11_opy_ = bstack1lll11l1l_opy_(app)
      else:
        bstack111111lll_opy_(bstack111llll1_opy_)
  else:
    if len(app) > 2:
      bstack111111lll_opy_(bstack1ll11lll11_opy_)
    elif len(app) == 2:
      if bstack1ll1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack1ll1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack1ll1l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack1ll1llll11_opy_ = bstack1lll11l1l_opy_(config, app[bstack1ll1l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack111111lll_opy_(bstack1l11l11l1l_opy_.format(app))
      else:
        bstack111111lll_opy_(bstack1ll11lll11_opy_)
    else:
      for key in app:
        if key in bstack1lllll1l11_opy_:
          if key == bstack1ll1l11_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack1ll1llll11_opy_ = bstack1lll11l1l_opy_(config, app[key])
            else:
              bstack111111lll_opy_(bstack1l11l11l1l_opy_.format(app))
          else:
            bstack1ll1llll11_opy_ = app[key]
        else:
          bstack111111lll_opy_(bstack1l1l111ll_opy_)
  return bstack1ll1llll11_opy_
def bstack111l111ll_opy_(bstack1ll1llll11_opy_):
  import re
  bstack1111l1l11_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack1l11l11lll_opy_ = re.compile(bstack1ll1l11_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack1ll1l11_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack1ll1llll11_opy_ or re.fullmatch(bstack1111l1l11_opy_, bstack1ll1llll11_opy_) or re.fullmatch(bstack1l11l11lll_opy_, bstack1ll1llll11_opy_):
    return True
  else:
    return False
def bstack1lll11l1l_opy_(config, path, bstack1ll1ll111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1l11_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack1l111l11_opy_ = bstack1l111l11ll_opy_(md5_hash)
  bstack1ll1llll11_opy_ = None
  if bstack1l111l11_opy_:
    logger.info(bstack1lll11l111_opy_.format(bstack1l111l11_opy_, md5_hash))
    return bstack1l111l11_opy_
  bstack1l11l111l_opy_ = MultipartEncoder(
    fields={
      bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1l11_opy_ (u"ࠩࡵࡦࠬ৚")), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack1ll1l11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack1ll1ll111l_opy_
    }
  )
  response = requests.post(bstack1ll1l1ll1l_opy_, data=bstack1l11l111l_opy_,
                           headers={bstack1ll1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1l11l111l_opy_.content_type},
                           auth=(config[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack1ll1llll11_opy_ = res[bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack1llll11111_opy_.format(bstack1ll1llll11_opy_))
    bstack1ll1llllll_opy_(md5_hash, bstack1ll1llll11_opy_)
  except ValueError as err:
    bstack111111lll_opy_(bstack1l1111l1l_opy_.format(str(err)))
  return bstack1ll1llll11_opy_
def bstack1ll1l11lll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1ll1llll_opy_
  bstack1llll1lll_opy_ = 1
  bstack1l1l1ll1l1_opy_ = 1
  if bstack1ll1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack1l1l1ll1l1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack1l1l1ll1l1_opy_ = bstack1ll1l11l11_opy_(framework_name, args) or 1
  if bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack1llll1lll_opy_ = len(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack1l1ll1llll_opy_ = int(bstack1l1l1ll1l1_opy_) * int(bstack1llll1lll_opy_)
def bstack1ll1l11l11_opy_(framework_name, args):
  if framework_name == bstack111l1lll_opy_ and args and bstack1ll1l11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack1l11l11111_opy_ = args.index(bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack1l11l11111_opy_ + 1]) or 1
  return 1
def bstack1l111l11ll_opy_(md5_hash):
  bstack1ll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠨࢀࠪ১")), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1ll1llll_opy_):
    bstack1lllll1ll1_opy_ = json.load(open(bstack1ll1llll_opy_, bstack1ll1l11_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1lllll1ll1_opy_:
      bstack11llll1l1_opy_ = bstack1lllll1ll1_opy_[md5_hash]
      bstack11l11l11l_opy_ = datetime.datetime.now()
      bstack1llll1l1l1_opy_ = datetime.datetime.strptime(bstack11llll1l1_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack1ll1l11_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack11l11l11l_opy_ - bstack1llll1l1l1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11llll1l1_opy_[bstack1ll1l11_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack11llll1l1_opy_[bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack1ll1llllll_opy_(md5_hash, bstack1ll1llll11_opy_):
  bstack1l1ll11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠩࢁࠫ৯")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack1l1ll11l_opy_):
    os.makedirs(bstack1l1ll11l_opy_)
  bstack1ll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠫࢃ࠭ৱ")), bstack1ll1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack1l11l11l_opy_ = {
    bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪ৴"): bstack1ll1llll11_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1l11_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1ll1llll_opy_):
    bstack1lllll1ll1_opy_ = json.load(open(bstack1ll1llll_opy_, bstack1ll1l11_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1lllll1ll1_opy_ = {}
  bstack1lllll1ll1_opy_[md5_hash] = bstack1l11l11l_opy_
  with open(bstack1ll1llll_opy_, bstack1ll1l11_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1lllll1ll1_opy_, outfile)
def bstack1llll1ll1_opy_(self):
  return
def bstack111llll1l_opy_(self):
  return
def bstack1l111ll1_opy_(self):
  global bstack1ll11lll1l_opy_
  bstack1ll11lll1l_opy_(self)
def bstack11lll1l11_opy_():
  global bstack1l1ll111ll_opy_
  bstack1l1ll111ll_opy_ = True
def bstack1l1ll1lll1_opy_(self):
  global bstack1lll11ll11_opy_
  global bstack1l1l1l1l_opy_
  global bstack1111l11ll_opy_
  try:
    if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack1lll11ll11_opy_ and self.session_id != None and bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack1ll1l11_opy_ (u"ࠨࠩৼ")) != bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack111ll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack111ll1l1_opy_ == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1l111l111l_opy_(logger)
      if self != None:
        bstack1lll1ll11l_opy_(self, bstack111ll1l1_opy_, bstack1ll1l11_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠧࠨਂ")
    if bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack1lll11ll11_opy_ and getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack1l1ll1l1l_opy_.bstack1lll11ll1l_opy_(self, bstack11lllll1_opy_, logger, wait=True)
    if bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack1lll11ll11_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1lll1ll11l_opy_(self, bstack1ll1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack1ll1l11l1l_opy_.bstack1ll1ll1l11_opy_(self)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack1111l11ll_opy_(self)
  self.session_id = None
def bstack11111l11l_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack111l11l11_opy_
    global bstack1lll11ll11_opy_
    command_executor = kwargs.get(bstack1ll1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack1ll1l11_opy_ (u"ࠧࠨਉ"))
    bstack1l11l1l1l_opy_ = False
    if type(command_executor) == str and bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack1l11l1l1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack1ll1l11_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack1ll1l11_opy_ (u"ࠫࠬ਍"))):
      bstack1l11l1l1l_opy_ = True
    else:
      return bstack1l1l1l11_opy_(self, *args, **kwargs)
    if bstack1l11l1l1l_opy_:
      if kwargs.get(bstack1ll1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack1ll1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack111l11l11_opy_(kwargs[bstack1ll1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack1lll11ll11_opy_)
      elif kwargs.get(bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack1ll1l11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack111l11l11_opy_(kwargs[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack1lll11ll11_opy_)
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack1l1l1l11_opy_(self, *args, **kwargs)
def bstack1lll11llll_opy_(self, command_executor=bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack1l11lll1ll_opy_ = bstack11111l11l_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack11ll1ll1l_opy_.on():
    return bstack1l11lll1ll_opy_
  try:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll11l11l_opy_.bstack1l1llll1ll_opy_(self)
  return bstack1l11lll1ll_opy_
def bstack1l11l1l11_opy_(args):
  return bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1111ll1l_opy_(self, driver_command, *args, **kwargs):
  global bstack1111l1ll1_opy_
  global bstack1ll11111l_opy_
  bstack1l1l11l1l_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack1ll1l1l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack1l1ll1ll11_opy_ = getattr(self, bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack1ll11111l_opy_ and bstack1l11l1111l_opy_ and bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1l1ll1l1l1_opy_.bstack1ll1lll1_opy_(driver_command) and (bstack1l1ll1ll11_opy_ or bstack1l1l11l1l_opy_) and not bstack1l11l1l11_opy_(args):
    try:
      bstack1ll11111l_opy_ = True
      logger.debug(bstack1ll1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack1ll11111l_opy_ = False
  response = bstack1111l1ll1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack1lll11ll11_opy_).lower() or bstack1ll1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack1lll11ll11_opy_).lower()) and bstack11ll1ll1l_opy_.on():
    try:
      if driver_command == bstack1ll1l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack1ll11l11l_opy_.bstack1lll111111_opy_({
            bstack1ll1l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack1ll1l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack1ll11l11l_opy_.current_test_uuid() if bstack1ll11l11l_opy_.current_test_uuid() else bstack11ll1ll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lll1lll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1l1l1l_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1ll11l11_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l1111l11_opy_
  global bstack1lll11ll11_opy_
  global bstack1l1l1l11_opy_
  global bstack1l1ll111_opy_
  global bstack1l11ll1l1l_opy_
  global bstack11lllll1_opy_
  CONFIG[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1lll11ll11_opy_) + str(__version__)
  command_executor = bstack11111llll_opy_()
  logger.debug(bstack11111l1ll_opy_.format(command_executor))
  proxy = bstack11l1ll1l1_opy_(CONFIG, proxy)
  bstack1l1ll111l1_opy_ = 0 if bstack1ll1l1l1l_opy_ < 0 else bstack1ll1l1l1l_opy_
  try:
    if bstack1l1lll11l1_opy_ is True:
      bstack1l1ll111l1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1111l11_opy_ is True:
      bstack1l1ll111l1_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1ll111l1_opy_ = 0
  bstack1ll111l1_opy_ = bstack1llll111l1_opy_(CONFIG, bstack1l1ll111l1_opy_)
  logger.debug(bstack1l1l1l1ll1_opy_.format(str(bstack1ll111l1_opy_)))
  if bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack1llll111_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack11ll1l1l_opy_(bstack1ll111l1_opy_)
  if bstack1l1ll111l_opy_.bstack1lllllll11_opy_(CONFIG, bstack1l1ll111l1_opy_) and bstack1l1ll111l_opy_.bstack11ll11l1_opy_(bstack1ll111l1_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1l1ll111l_opy_.set_capabilities(bstack1ll111l1_opy_, CONFIG)
  if desired_capabilities:
    bstack1lll1l11l_opy_ = bstack1l11ll111_opy_(desired_capabilities)
    bstack1lll1l11l_opy_[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack1ll1ll1ll_opy_(CONFIG)
    bstack1l111l111_opy_ = bstack1llll111l1_opy_(bstack1lll1l11l_opy_)
    if bstack1l111l111_opy_:
      bstack1ll111l1_opy_ = update(bstack1l111l111_opy_, bstack1ll111l1_opy_)
    desired_capabilities = None
  if options:
    bstack1lll11lll_opy_(options, bstack1ll111l1_opy_)
  if not options:
    options = bstack1l1l1111l_opy_(bstack1ll111l1_opy_)
  bstack11lllll1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack1l1ll111l1_opy_]
  if proxy and bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1ll11111_opy_() < version.parse(bstack1ll1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll111l1_opy_)
  logger.info(bstack1l11lll1_opy_)
  if bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1l1l11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1l1llllll_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫਸ਼")
    if bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1l1llllll_opy_ = self.caps.get(bstack1ll1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1l1llllll_opy_ = self.capabilities.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1l1llllll_opy_:
      bstack1l1111l1ll_opy_(bstack1l1llllll_opy_)
      if bstack1l1ll11111_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1l1llllll_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack1ll1ll1l_opy_.format(bstack1l1llllll_opy_))
    else:
      logger.debug(bstack1l1l1llll1_opy_.format(bstack1ll1l11_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1l1l1llll1_opy_.format(e))
  if bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack1lll11ll11_opy_:
    bstack1ll1lll111_opy_(bstack1ll1l1l1l_opy_, bstack1l11ll1l1l_opy_)
  bstack1l1l1l1l_opy_ = self.session_id
  if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack1lll11ll11_opy_ or bstack1ll1l11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack1lll11ll11_opy_ or bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack1lll11ll11_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1ll11l11l_opy_.bstack1l1llll1ll_opy_(self)
  bstack1l1ll111_opy_.append(self)
  if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack1l1ll111l1_opy_]:
    bstack1l1ll11l11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack1l1ll111l1_opy_][bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack1ll11l111l_opy_.format(bstack1l1l1l1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1111111l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l11l1ll11_opy_
      if(bstack1ll1l11_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠩࢁࠫ੊")), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack1ll1l11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack1ll1l11_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack1ll1l11_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack1ll1l11_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1l11_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11111l111_opy_)
            lines.insert(1, bstack1ll111l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack1ll1l11_opy_ (u"ࠫࡼ࠭੓")) as bstack1lll11l1_opy_:
              bstack1lll11l1_opy_.writelines(lines)
        CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack1lll11ll11_opy_) + str(__version__)
        bstack1l1ll111l1_opy_ = 0 if bstack1ll1l1l1l_opy_ < 0 else bstack1ll1l1l1l_opy_
        try:
          if bstack1l1lll11l1_opy_ is True:
            bstack1l1ll111l1_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1111l11_opy_ is True:
            bstack1l1ll111l1_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1ll111l1_opy_ = 0
        CONFIG[bstack1ll1l11_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack1ll1l11_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack1ll111l1_opy_ = bstack1llll111l1_opy_(CONFIG, bstack1l1ll111l1_opy_)
        logger.debug(bstack1l1l1l1ll1_opy_.format(str(bstack1ll111l1_opy_)))
        if CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack11ll1l1l_opy_(bstack1ll111l1_opy_)
        if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack1ll1l11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack1l1ll111l1_opy_]:
          bstack1l1ll11l11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack1l1ll111l1_opy_][bstack1ll1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠧࡿࠩ੝")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1ll1l11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll111l1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1l11_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1l11l1ll11_opy_ = True
      return bstack1l1lll1l11_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack111l1ll1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1ll1l1l1l_opy_
    global bstack1l1ll11l11_opy_
    global bstack1l1lll11l1_opy_
    global bstack1l1111l11_opy_
    global bstack1lll11ll11_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack1lll11ll11_opy_) + str(__version__)
    bstack1l1ll111l1_opy_ = 0 if bstack1ll1l1l1l_opy_ < 0 else bstack1ll1l1l1l_opy_
    try:
      if bstack1l1lll11l1_opy_ is True:
        bstack1l1ll111l1_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1111l11_opy_ is True:
        bstack1l1ll111l1_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1ll111l1_opy_ = 0
    CONFIG[bstack1ll1l11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack1ll111l1_opy_ = bstack1llll111l1_opy_(CONFIG, bstack1l1ll111l1_opy_)
    logger.debug(bstack1l1l1l1ll1_opy_.format(str(bstack1ll111l1_opy_)))
    if CONFIG.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack11ll1l1l_opy_(bstack1ll111l1_opy_)
    if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack1ll1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack1l1ll111l1_opy_]:
      bstack1l1ll11l11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack1l1ll111l1_opy_][bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack1l1lll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack1ll111l1_opy_))
    browser = self.connect(bstack1l1lll11ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1lllll_opy_():
    global bstack1l11l1ll11_opy_
    global bstack1lll11ll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll1l1l11_opy_
        if not bstack1l11l1111l_opy_:
          global bstack1l11l1l11l_opy_
          if not bstack1l11l1l11l_opy_:
            from bstack_utils.helper import bstack11l1l1l1_opy_, bstack1ll11ll11_opy_
            bstack1l11l1l11l_opy_ = bstack11l1l1l1_opy_()
            bstack1ll11ll11_opy_(bstack1lll11ll11_opy_)
          BrowserType.connect = bstack1lll1l1l11_opy_
          return
        BrowserType.launch = bstack111l1ll1l_opy_
        bstack1l11l1ll11_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1111111l_opy_
      bstack1l11l1ll11_opy_ = True
    except Exception as e:
      pass
def bstack1l1l11lll_opy_(context, bstack1ll1l1111l_opy_):
  try:
    context.page.evaluate(bstack1ll1l11_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1111lll1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack1ll1l11_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack1ll1l11_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack1l111111_opy_(self, url):
  global bstack111ll111_opy_
  try:
    bstack1lll111ll1_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll1l11l1_opy_.format(str(err)))
  try:
    bstack111ll111_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1l11l1ll_opy_ = str(e)
      if any(err_msg in bstack1l1l11l1ll_opy_ for err_msg in bstack1llll11l1l_opy_):
        bstack1lll111ll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll1l11l1_opy_.format(str(err)))
    raise e
def bstack1lllll1l1_opy_(self):
  global bstack1ll1l111l1_opy_
  bstack1ll1l111l1_opy_ = self
  return
def bstack1l11111lll_opy_(self):
  global bstack1l1ll1ll_opy_
  bstack1l1ll1ll_opy_ = self
  return
def bstack1l1l1ll11l_opy_(test_name, bstack1l1lll1ll_opy_):
  global CONFIG
  if CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧੳ"), False):
    bstack11l11ll11_opy_ = os.path.relpath(bstack1l1lll1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11l11ll11_opy_)
    bstack1lll111l1l_opy_ = suite_name + bstack1ll1l11_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1lll111l1l_opy_
def bstack11l11llll_opy_(self, test, *args, **kwargs):
  global bstack1l111lll1l_opy_
  test_name = None
  bstack1l1lll1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1lll1ll_opy_ = str(test.source)
  bstack1l1l1ll11l_opy_(test_name, bstack1l1lll1ll_opy_)
  bstack1l111lll1l_opy_(self, test, *args, **kwargs)
def bstack1lll11ll1_opy_(driver, bstack1lll111l1l_opy_):
  if not bstack1ll1l1111_opy_ and bstack1lll111l1l_opy_:
      bstack1111l1lll_opy_ = {
          bstack1ll1l11_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1lll111l1l_opy_
          }
      }
      bstack1111l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack1111l1lll_opy_))
      driver.execute_script(bstack1111l1l1_opy_)
  if bstack1ll11ll111_opy_:
      bstack1lll1ll1l_opy_ = {
          bstack1ll1l11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack1ll1l11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack1ll1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1lll111l1l_opy_ + bstack1ll1l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack1ll1l11_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack1ll11ll111_opy_.status == bstack1ll1l11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1ll111lll1_opy_ = bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack1lll1ll1l_opy_))
          driver.execute_script(bstack1ll111lll1_opy_)
          bstack1lll1ll11l_opy_(driver, bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack1ll11ll111_opy_.status == bstack1ll1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack1ll1l11_opy_ (u"ࠧࠨઅ")
          bstack1lllll1l1l_opy_ = bstack1lll111l1l_opy_ + bstack1ll1l11_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack1ll11ll111_opy_.message:
              reason = str(bstack1ll11ll111_opy_.message)
              bstack1lllll1l1l_opy_ = bstack1lllll1l1l_opy_ + bstack1ll1l11_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack1lll1ll1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack1ll1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack1lllll1l1l_opy_
          }
          bstack1ll111lll1_opy_ = bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack1lll1ll1l_opy_))
          driver.execute_script(bstack1ll111lll1_opy_)
          bstack1lll1ll11l_opy_(driver, bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack1ll11l1111_opy_(reason, str(bstack1ll11ll111_opy_), str(bstack1ll1l1l1l_opy_), logger)
def bstack1ll1lll1l1_opy_(driver, test):
  if CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭઎"), False) and CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫએ"), bstack1ll1l11_opy_ (u"ࠤࡤࡹࡹࡵࠢઐ")) == bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧઑ"):
      bstack1lll11l1ll_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ઒"), None)
      bstack11l1lllll_opy_(driver, bstack1lll11l1ll_opy_, test)
  if bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩઓ"), None) and bstack1ll1l1l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬઔ"), None):
      logger.info(bstack1ll1l11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢક"))
      bstack1l1ll111l_opy_.bstack1l11ll11ll_opy_(driver, name=test.name, path=test.source)
def bstack1l11111l1_opy_(test, bstack1lll111l1l_opy_):
    try:
      data = {}
      if test:
        data[bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ખ")] = bstack1lll111l1l_opy_
      if bstack1ll11ll111_opy_:
        if bstack1ll11ll111_opy_.status == bstack1ll1l11_opy_ (u"ࠩࡓࡅࡘ࡙ࠧગ"):
          data[bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪઘ")] = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫઙ")
        elif bstack1ll11ll111_opy_.status == bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪચ"):
          data[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭છ")] = bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧજ")
          if bstack1ll11ll111_opy_.message:
            data[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨઝ")] = str(bstack1ll11ll111_opy_.message)
      user = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫઞ")]
      key = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ટ")]
      url = bstack1ll1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩઠ").format(user, key, bstack1l1l1l1l_opy_)
      headers = {
        bstack1ll1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫડ"): bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩઢ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll11111l_opy_.format(str(e)))
def bstack1ll1ll11l_opy_(test, bstack1lll111l1l_opy_):
  global CONFIG
  global bstack1l1ll1ll_opy_
  global bstack1ll1l111l1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1ll11ll111_opy_
  global bstack1l1ll11l11_opy_
  global bstack1l11ll1l1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1l111111_opy_
  global bstack1lllll111l_opy_
  global bstack1l1ll111_opy_
  global bstack11lllll1_opy_
  try:
    if not bstack1l1l1l1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠧࡿࠩણ")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨત"), bstack1ll1l11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫથ"))) as f:
        bstack1l1111lll1_opy_ = json.loads(bstack1ll1l11_opy_ (u"ࠥࡿࠧદ") + f.read().strip() + bstack1ll1l11_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭ધ") + bstack1ll1l11_opy_ (u"ࠧࢃࠢન"))
        bstack1l1l1l1l_opy_ = bstack1l1111lll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1ll111_opy_:
    for driver in bstack1l1ll111_opy_:
      if bstack1l1l1l1l_opy_ == driver.session_id:
        if test:
          bstack1ll1lll1l1_opy_(driver, test)
        bstack1lll11ll1_opy_(driver, bstack1lll111l1l_opy_)
  elif bstack1l1l1l1l_opy_:
    bstack1l11111l1_opy_(test, bstack1lll111l1l_opy_)
  if bstack1l1ll1ll_opy_:
    bstack1lll1l1l1l_opy_(bstack1l1ll1ll_opy_)
  if bstack1ll1l111l1_opy_:
    bstack1l1l111111_opy_(bstack1ll1l111l1_opy_)
  if bstack1l1ll111ll_opy_:
    bstack1lllll111l_opy_()
def bstack1lll1lll11_opy_(self, test, *args, **kwargs):
  bstack1lll111l1l_opy_ = None
  if test:
    bstack1lll111l1l_opy_ = str(test.name)
  bstack1ll1ll11l_opy_(test, bstack1lll111l1l_opy_)
  bstack1l11ll1l1_opy_(self, test, *args, **kwargs)
def bstack11l1llll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11lll1111_opy_
  global CONFIG
  global bstack1l1ll111_opy_
  global bstack1l1l1l1l_opy_
  bstack1l1l1111l1_opy_ = None
  try:
    if bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ઩"), None):
      try:
        if not bstack1l1l1l1l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠧࡿࠩપ")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨફ"), bstack1ll1l11_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫબ"))) as f:
            bstack1l1111lll1_opy_ = json.loads(bstack1ll1l11_opy_ (u"ࠥࡿࠧભ") + f.read().strip() + bstack1ll1l11_opy_ (u"ࠫࠧࡾࠢ࠻ࠢࠥࡽࠧ࠭મ") + bstack1ll1l11_opy_ (u"ࠧࢃࠢય"))
            bstack1l1l1l1l_opy_ = bstack1l1111lll1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1ll111_opy_:
        for driver in bstack1l1ll111_opy_:
          if bstack1l1l1l1l_opy_ == driver.session_id:
            bstack1l1l1111l1_opy_ = driver
    bstack11lllll11_opy_ = bstack1l1ll111l_opy_.bstack1l11111111_opy_(test.tags)
    if bstack1l1l1111l1_opy_:
      threading.current_thread().isA11yTest = bstack1l1ll111l_opy_.bstack1l11l1lll_opy_(bstack1l1l1111l1_opy_, bstack11lllll11_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11lllll11_opy_
  except:
    pass
  bstack11lll1111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll11ll111_opy_
  bstack1ll11ll111_opy_ = self._test
def bstack11l1l11ll_opy_():
  global bstack1ll1l111l_opy_
  try:
    if os.path.exists(bstack1ll1l111l_opy_):
      os.remove(bstack1ll1l111l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩર") + str(e))
def bstack11l11111_opy_():
  global bstack1ll1l111l_opy_
  bstack1l1lllll11_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll1l111l_opy_):
      with open(bstack1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠧࡸࠩ઱")):
        pass
      with open(bstack1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠣࡹ࠮ࠦલ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll1l111l_opy_):
      bstack1l1lllll11_opy_ = json.load(open(bstack1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠩࡵࡦࠬળ")))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ઴") + str(e))
  finally:
    return bstack1l1lllll11_opy_
def bstack1ll1lll111_opy_(platform_index, item_index):
  global bstack1ll1l111l_opy_
  try:
    bstack1l1lllll11_opy_ = bstack11l11111_opy_()
    bstack1l1lllll11_opy_[item_index] = platform_index
    with open(bstack1ll1l111l_opy_, bstack1ll1l11_opy_ (u"ࠦࡼ࠱ࠢવ")) as outfile:
      json.dump(bstack1l1lllll11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪશ") + str(e))
def bstack111ll1l1l_opy_(bstack1l111111l_opy_):
  global CONFIG
  bstack1111111l1_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧષ")
  if not bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ") in CONFIG:
    logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬહ"))
  try:
    platform = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")][bstack1l111111l_opy_]
    if bstack1ll1l11_opy_ (u"ࠪࡳࡸ࠭઻") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠫࡴࡹ઼ࠧ")]) + bstack1ll1l11_opy_ (u"ࠬ࠲ࠠࠨઽ")
    if bstack1ll1l11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩા") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪિ")]) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠣࠫી")
    if bstack1ll1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ુ") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧૂ")]) + bstack1ll1l11_opy_ (u"ࠫ࠱ࠦࠧૃ")
    if bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧૄ") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨૅ")]) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠢࠪ૆")
    if bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ે") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧૈ")]) + bstack1ll1l11_opy_ (u"ࠪ࠰ࠥ࠭ૉ")
    if bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૊") in platform:
      bstack1111111l1_opy_ += str(platform[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ો")]) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠩૌ")
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴ્ࠧ") + str(e))
  finally:
    if bstack1111111l1_opy_[len(bstack1111111l1_opy_) - 2:] == bstack1ll1l11_opy_ (u"ࠨ࠮ࠣࠫ૎"):
      bstack1111111l1_opy_ = bstack1111111l1_opy_[:-2]
    return bstack1111111l1_opy_
def bstack1ll111111_opy_(path, bstack1111111l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111l1l1ll_opy_ = ET.parse(path)
    bstack1111ll11_opy_ = bstack111l1l1ll_opy_.getroot()
    bstack1l1ll1lll_opy_ = None
    for suite in bstack1111ll11_opy_.iter(bstack1ll1l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ૏")):
      if bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪૐ") in suite.attrib:
        suite.attrib[bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ૑")] += bstack1ll1l11_opy_ (u"ࠬࠦࠧ૒") + bstack1111111l1_opy_
        bstack1l1ll1lll_opy_ = suite
    bstack1l11l1l1l1_opy_ = None
    for robot in bstack1111ll11_opy_.iter(bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૓")):
      bstack1l11l1l1l1_opy_ = robot
    bstack111l111l_opy_ = len(bstack1l11l1l1l1_opy_.findall(bstack1ll1l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔")))
    if bstack111l111l_opy_ == 1:
      bstack1l11l1l1l1_opy_.remove(bstack1l11l1l1l1_opy_.findall(bstack1ll1l11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ૕"))[0])
      bstack1ll111ll1_opy_ = ET.Element(bstack1ll1l11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ૖"), attrib={bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ૗"): bstack1ll1l11_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ૘"), bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ૙"): bstack1ll1l11_opy_ (u"࠭ࡳ࠱ࠩ૚")})
      bstack1l11l1l1l1_opy_.insert(1, bstack1ll111ll1_opy_)
      bstack1l1l1lll1l_opy_ = None
      for suite in bstack1l11l1l1l1_opy_.iter(bstack1ll1l11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૛")):
        bstack1l1l1lll1l_opy_ = suite
      bstack1l1l1lll1l_opy_.append(bstack1l1ll1lll_opy_)
      bstack1l11l11l1_opy_ = None
      for status in bstack1l1ll1lll_opy_.iter(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ૜")):
        bstack1l11l11l1_opy_ = status
      bstack1l1l1lll1l_opy_.append(bstack1l11l11l1_opy_)
    bstack111l1l1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ૝") + str(e))
def bstack1ll11l1l1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1l11l1_opy_
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ૞") in options:
    del options[bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ૟")]
  bstack1l1l1111_opy_ = bstack11l11111_opy_()
  for bstack11111111l_opy_ in bstack1l1l1111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬૠ"), str(bstack11111111l_opy_), bstack1ll1l11_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪૡ"))
    bstack1ll111111_opy_(path, bstack111ll1l1l_opy_(bstack1l1l1111_opy_[bstack11111111l_opy_]))
  bstack11l1l11ll_opy_()
  return bstack11l1l11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l111llll1_opy_(self, ff_profile_dir):
  global bstack11ll11ll1_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11ll1_opy_(self, ff_profile_dir)
def bstack11l11111l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1lll111l_opy_
  bstack111111l1_opy_ = []
  if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪૢ") in CONFIG:
    bstack111111l1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫૣ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ૤")],
      pabot_args[bstack1ll1l11_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ૥")],
      argfile,
      pabot_args.get(bstack1ll1l11_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ૦")),
      pabot_args[bstack1ll1l11_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ૧")],
      platform[0],
      bstack1l1lll111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1l11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ૨")] or [(bstack1ll1l11_opy_ (u"ࠢࠣ૩"), None)]
    for platform in enumerate(bstack111111l1_opy_)
  ]
def bstack1llll11ll_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1ll1111_opy_=bstack1ll1l11_opy_ (u"ࠨࠩ૪")):
  global bstack1lll1l1ll_opy_
  self.platform_index = platform_index
  self.bstack1111l11l1_opy_ = bstack1ll1ll1111_opy_
  bstack1lll1l1ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1lllllll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1111ll1l1_opy_
  global bstack1111l11l_opy_
  bstack1ll11111ll_opy_ = copy.deepcopy(item)
  if not bstack1ll1l11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫") in item.options:
    bstack1ll11111ll_opy_.options[bstack1ll1l11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")] = []
  bstack1l1l111l1_opy_ = bstack1ll11111ll_opy_.options[bstack1ll1l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૭")].copy()
  for v in bstack1ll11111ll_opy_.options[bstack1ll1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ૮")]:
    if bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ૯") in v:
      bstack1l1l111l1_opy_.remove(v)
    if bstack1ll1l11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ૰") in v:
      bstack1l1l111l1_opy_.remove(v)
    if bstack1ll1l11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ૱") in v:
      bstack1l1l111l1_opy_.remove(v)
  bstack1l1l111l1_opy_.insert(0, bstack1ll1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫ૲").format(bstack1ll11111ll_opy_.platform_index))
  bstack1l1l111l1_opy_.insert(0, bstack1ll1l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ૳").format(bstack1ll11111ll_opy_.bstack1111l11l1_opy_))
  bstack1ll11111ll_opy_.options[bstack1ll1l11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૴")] = bstack1l1l111l1_opy_
  if bstack1111l11l_opy_:
    bstack1ll11111ll_opy_.options[bstack1ll1l11_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ૵")].insert(0, bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩ૶").format(bstack1111l11l_opy_))
  return bstack1111ll1l1_opy_(caller_id, datasources, is_last, bstack1ll11111ll_opy_, outs_dir)
def bstack1llllll111_opy_(command, item_index):
  if bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ૷")):
    os.environ[bstack1ll1l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩ૸")] = json.dumps(CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬૹ")][item_index % bstack1l11ll11_opy_])
  global bstack1111l11l_opy_
  if bstack1111l11l_opy_:
    command[0] = command[0].replace(bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૺ"), bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨૻ") + str(
      item_index) + bstack1ll1l11_opy_ (u"ࠬࠦࠧૼ") + bstack1111l11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૽"),
                                    bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ૾") + str(item_index), 1)
def bstack1l1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1llll1l11_opy_
  bstack1llllll111_opy_(command, item_index)
  return bstack1llll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111lllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1llll1l11_opy_
  bstack1llllll111_opy_(command, item_index)
  return bstack1llll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11lll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1llll1l11_opy_
  bstack1llllll111_opy_(command, item_index)
  return bstack1llll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1lllll1ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1llllll1l_opy_
  bstack1ll1lll11_opy_ = bstack1llllll1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨ૿")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1l11_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭଀")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1lll11_opy_
def bstack11l11ll1l_opy_(runner, hook_name, context, element, bstack11111l11_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll11l1l_opy_.bstack11l11l111_opy_(hook_name, element)
    bstack11111l11_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll11l1l_opy_.bstack1l111l1l11_opy_(element)
      if hook_name not in [bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧଁ"), bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧଂ")] and args and hasattr(args[0], bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬଃ")):
        args[0].error_message = bstack1ll1l11_opy_ (u"࠭ࠧ଄")
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡬ࡦࡴࡤ࡭ࡧࠣ࡬ࡴࡵ࡫ࡴࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩଅ").format(str(e)))
def bstack1l1l1lll11_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack11l11ll1l_opy_(runner, name, context, runner, bstack11111l11_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1ll1l1llll_opy_(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଆ")) else context.browser
      runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨଇ")
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧଈ").format(str(e)))
def bstack11llll1l_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack11l11ll1l_opy_(runner, name, context, context.feature, bstack11111l11_opy_, *args)
    try:
      if not bstack1ll1l1111_opy_:
        bstack1l1l1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1llll_opy_(bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଉ")) else context.browser
        if is_driver_active(bstack1l1l1111l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨଊ")
          bstack1ll1l1111l_opy_ = str(runner.feature.name)
          bstack1l1l11lll_opy_(context, bstack1ll1l1111l_opy_)
          bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଋ") + json.dumps(bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠧࡾࡿࠪଌ"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ଍").format(str(e)))
def bstack1l1llll1l1_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack11l11ll1l_opy_(runner, name, context, context.scenario, bstack11111l11_opy_, *args)
def bstack1lll1l1l_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack1ll11l1l_opy_.start_test(args[0].name, args[0])
    bstack11l11ll1l_opy_(runner, name, context, context.scenario, bstack11111l11_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1l11l1l_opy_.bstack1l1llll1l_opy_(context, *args)
    try:
      bstack1l1l1111l1_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଎"), context.browser)
      if is_driver_active(bstack1l1l1111l1_opy_):
        bstack1ll11l11l_opy_.bstack1l1llll1ll_opy_(bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଏ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨଐ")
        if (not bstack1ll1l1111_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1l1111l_opy_ = str(runner.feature.name)
          bstack1ll1l1111l_opy_ = feature_name + bstack1ll1l11_opy_ (u"ࠬࠦ࠭ࠡࠩ଑") + scenario_name
          if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ଒"):
            bstack1l1l11lll_opy_(context, bstack1ll1l1111l_opy_)
            bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଓ") + json.dumps(bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠨࡿࢀࠫଔ"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪକ").format(str(e)))
def bstack111ll111l_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack11l11ll1l_opy_(runner, name, context, args[0], bstack11111l11_opy_, *args)
    try:
      bstack1l1l1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1llll_opy_(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଖ")) else context.browser
      if is_driver_active(bstack1l1l1111l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤଗ")
        bstack1ll11l1l_opy_.bstack1ll1ll1l1_opy_(args[0])
        if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥଘ"):
          feature_name = bstack1ll1l1111l_opy_ = str(runner.feature.name)
          bstack1ll1l1111l_opy_ = feature_name + bstack1ll1l11_opy_ (u"࠭ࠠ࠮ࠢࠪଙ") + context.scenario.name
          bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଚ") + json.dumps(bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠨࡿࢀࠫଛ"))
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ଜ").format(str(e)))
def bstack1l1llll11l_opy_(runner, name, context, bstack11111l11_opy_, *args):
  bstack1ll11l1l_opy_.bstack1l1111llll_opy_(args[0])
  try:
    bstack11ll1111l_opy_ = args[0].status.name
    bstack1l1l1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଝ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1l1111l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫଞ")
        feature_name = bstack1ll1l1111l_opy_ = str(runner.feature.name)
        bstack1ll1l1111l_opy_ = feature_name + bstack1ll1l11_opy_ (u"ࠬࠦ࠭ࠡࠩଟ") + context.scenario.name
        bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଠ") + json.dumps(bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠧࡾࡿࠪଡ"))
    if str(bstack11ll1111l_opy_).lower() == bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଢ"):
      bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪଣ")
      bstack1lll11l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫତ")
      bstack1ll1l11111_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬଥ")
      try:
        import traceback
        bstack1l1l111l1l_opy_ = runner.exception.__class__.__name__
        bstack11ll11l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll11l11l_opy_ = bstack1ll1l11_opy_ (u"ࠬࠦࠧଦ").join(bstack11ll11l11_opy_)
        bstack1ll1l11111_opy_ = bstack11ll11l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lll11l_opy_.format(str(e)))
      bstack1l1l111l1l_opy_ += bstack1ll1l11111_opy_
      bstack1111lll1_opy_(context, json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧଧ") + str(bstack1lll11l11l_opy_)),
                          bstack1ll1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨନ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ଩"):
        bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧପ"), None), bstack1ll1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଫ"), bstack1l1l111l1l_opy_)
        bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩବ") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦଭ") + str(bstack1lll11l11l_opy_)) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ମ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଯ"):
        bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨର"), bstack1ll1l11_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ଱") + str(bstack1l1l111l1l_opy_))
    else:
      bstack1111lll1_opy_(context, bstack1ll1l11_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦଲ"), bstack1ll1l11_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଳ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ଴"):
        bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"࠭ࡰࡢࡩࡨࠫଵ"), None), bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଶ"))
      bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଷ") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨସ")) + bstack1ll1l11_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩହ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ଺"):
        bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଻"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁ଼ࠬ").format(str(e)))
  bstack11l11ll1l_opy_(runner, name, context, args[0], bstack11111l11_opy_, *args)
def bstack1l11l11ll_opy_(runner, name, context, bstack11111l11_opy_, *args):
  bstack1ll11l1l_opy_.end_test(args[0])
  try:
    bstack1l11lll11l_opy_ = args[0].status.name
    bstack1l1l1111l1_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଽ"), context.browser)
    bstack1ll1l11l1l_opy_.bstack1ll1ll1l11_opy_(bstack1l1l1111l1_opy_)
    if str(bstack1l11lll11l_opy_).lower() == bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା"):
      bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪି")
      bstack1lll11l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫୀ")
      bstack1ll1l11111_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬୁ")
      try:
        import traceback
        bstack1l1l111l1l_opy_ = runner.exception.__class__.__name__
        bstack11ll11l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1lll11l11l_opy_ = bstack1ll1l11_opy_ (u"ࠬࠦࠧୂ").join(bstack11ll11l11_opy_)
        bstack1ll1l11111_opy_ = bstack11ll11l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack111lll11l_opy_.format(str(e)))
      bstack1l1l111l1l_opy_ += bstack1ll1l11111_opy_
      bstack1111lll1_opy_(context, json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧୃ") + str(bstack1lll11l11l_opy_)),
                          bstack1ll1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨୄ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ୅") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ୆"):
        bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨେ"), None), bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦୈ"), bstack1l1l111l1l_opy_)
        bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୉") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ୊") + str(bstack1lll11l11l_opy_)) + bstack1ll1l11_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧୋ"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥୌ") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱ୍ࠩ"):
        bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ୎"), bstack1ll1l11_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ୏") + str(bstack1l1l111l1l_opy_))
    else:
      bstack1111lll1_opy_(context, bstack1ll1l11_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ୐"), bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ୑"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୒") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୓"):
        bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ୔"), None), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ୕"))
      bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩୖ") + json.dumps(str(args[0].name) + bstack1ll1l11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤୗ")) + bstack1ll1l11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ୘"))
      if runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୙") or runner.driver_initialised == bstack1ll1l11_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୚"):
        bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ୛"))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଡ଼").format(str(e)))
  bstack11l11ll1l_opy_(runner, name, context, context.scenario, bstack11111l11_opy_, *args)
  threading.current_thread().current_test_uuid = None
def bstack1llllll11_opy_(runner, name, context, bstack11111l11_opy_, *args):
    bstack11l11ll1l_opy_(runner, name, context, context.scenario, bstack11111l11_opy_, *args)
def bstack1llll1ll1l_opy_(runner, name, context, bstack11111l11_opy_, *args):
    try:
      bstack1l1l1111l1_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଢ଼"), context.browser)
      if context.failed is True:
        bstack111ll1lll_opy_ = []
        bstack1l1l1ll111_opy_ = []
        bstack1l1ll1111_opy_ = []
        bstack11llllll_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭୞")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack111ll1lll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11ll11l11_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll11l1l_opy_ = bstack1ll1l11_opy_ (u"࠭ࠠࠨୟ").join(bstack11ll11l11_opy_)
            bstack1l1l1ll111_opy_.append(bstack1l1ll11l1l_opy_)
            bstack1l1ll1111_opy_.append(bstack11ll11l11_opy_[-1])
        except Exception as e:
          logger.debug(bstack111lll11l_opy_.format(str(e)))
        bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨୠ")
        for i in range(len(bstack111ll1lll_opy_)):
          bstack1l1l111l1l_opy_ += bstack111ll1lll_opy_[i] + bstack1l1ll1111_opy_[i] + bstack1ll1l11_opy_ (u"ࠨ࡞ࡱࠫୡ")
        bstack11llllll_opy_ = bstack1ll1l11_opy_ (u"ࠩࠣࠫୢ").join(bstack1l1l1ll111_opy_)
        if runner.driver_initialised in [bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦୣ"), bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ୤")]:
          bstack1111lll1_opy_(context, bstack11llllll_opy_, bstack1ll1l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ୥"))
          bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"࠭ࡰࡢࡩࡨࠫ୦"), None), bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ୧"), bstack1l1l111l1l_opy_)
          bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୨") + json.dumps(bstack11llllll_opy_) + bstack1ll1l11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ୩"))
          bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ୪"), bstack1ll1l11_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ୫") + str(bstack1l1l111l1l_opy_))
          bstack1l1l1ll11_opy_ = bstack111ll1111_opy_(bstack11llllll_opy_, runner.feature.name, logger)
          if (bstack1l1l1ll11_opy_ != None):
            bstack11lllll1l_opy_.append(bstack1l1l1ll11_opy_)
      else:
        if runner.driver_initialised in [bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ୬"), bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ୭")]:
          bstack1111lll1_opy_(context, bstack1ll1l11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ୮") + str(runner.feature.name) + bstack1ll1l11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ୯"), bstack1ll1l11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ୰"))
          bstack111l1ll1_opy_(getattr(context, bstack1ll1l11_opy_ (u"ࠪࡴࡦ࡭ࡥࠨୱ"), None), bstack1ll1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ୲"))
          bstack1l1l1111l1_opy_.execute_script(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୳") + json.dumps(bstack1ll1l11_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ୴") + str(runner.feature.name) + bstack1ll1l11_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ୵")) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ୶"))
          bstack1lll1ll11l_opy_(bstack1l1l1111l1_opy_, bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୷"))
          bstack1l1l1ll11_opy_ = bstack111ll1111_opy_(bstack11llllll_opy_, runner.feature.name, logger)
          if (bstack1l1l1ll11_opy_ != None):
            bstack11lllll1l_opy_.append(bstack1l1l1ll11_opy_)
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ୸").format(str(e)))
    bstack11l11ll1l_opy_(runner, name, context, context.feature, bstack11111l11_opy_, *args)
def bstack11l1l111l_opy_(self, name, context, *args):
  if bstack1l11l1111l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l11ll11_opy_
    bstack111lll111_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")][platform_index]
    os.environ[bstack1ll1l11_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭୺")] = json.dumps(bstack111lll111_opy_)
  global bstack11111l11_opy_
  if not hasattr(self, bstack1ll1l11_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫ୻")):
    self.driver_initialised = None
  bstack1ll1111ll_opy_ = {
      bstack1ll1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ୼"): bstack1l1l1lll11_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ୽"): bstack11llll1l_opy_,
      bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭୾"): bstack1l1llll1l1_opy_,
      bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ୿"): bstack1lll1l1l_opy_,
      bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ஀"): bstack111ll111l_opy_,
      bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ஁"): bstack1l1llll11l_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧஂ"): bstack1l11l11ll_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪஃ"): bstack1llllll11_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ஄"): bstack1llll1ll1l_opy_,
      bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬஅ"): lambda *args: bstack11l11ll1l_opy_(*args, self)
  }
  handler = bstack1ll1111ll_opy_.get(name, bstack11111l11_opy_)
  handler(self, name, context, bstack11111l11_opy_, *args)
  if name in [bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪஆ"), bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஇ"), bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ")]:
    try:
      bstack1l1l1111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l1llll_opy_(bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬஉ")) else context.browser
      bstack11ll1111_opy_ = (
        (name == bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪஊ") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஋")) or
        (name == bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ஌") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ஍")) or
        (name == bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஎ") and self.driver_initialised in [bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஏ"), bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨஐ")]) or
        (name == bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ஑") and self.driver_initialised == bstack1ll1l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨஒ"))
      )
      if bstack11ll1111_opy_:
        self.driver_initialised = None
        bstack1l1l1111l1_opy_.quit()
    except Exception:
      pass
def bstack1lllll1lll_opy_(config, startdir):
  return bstack1ll1l11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢஓ").format(bstack1ll1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤஔ"))
notset = Notset()
def bstack1l1l1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l11l1ll1_opy_
  if str(name).lower() == bstack1ll1l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫக"):
    return bstack1ll1l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ஖")
  else:
    return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack11l1llll_opy_(item, when):
  global bstack11lll11l1_opy_
  try:
    bstack11lll11l1_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll1111ll1_opy_():
  return
def bstack1ll1ll1l1l_opy_(type, name, status, reason, bstack1ll11l1ll1_opy_, bstack1lllll111_opy_):
  bstack1111l1lll_opy_ = {
    bstack1ll1l11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭஗"): type,
    bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ஘"): {}
  }
  if type == bstack1ll1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪங"):
    bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬச")][bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ஛")] = bstack1ll11l1ll1_opy_
    bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧஜ")][bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪ஝")] = json.dumps(str(bstack1lllll111_opy_))
  if type == bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஞ"):
    bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪட")][bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭஠")] = name
  if type == bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ஡"):
    bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஢")][bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫண")] = status
    if status == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬத"):
      bstack1111l1lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ஥")][bstack1ll1l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ஦")] = json.dumps(str(reason))
  bstack1111l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭஧").format(json.dumps(bstack1111l1lll_opy_))
  return bstack1111l1l1_opy_
def bstack1l11llll11_opy_(driver_command, response):
    if driver_command == bstack1ll1l11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ந"):
        bstack1ll11l11l_opy_.bstack1lll111111_opy_({
            bstack1ll1l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩன"): response[bstack1ll1l11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪப")],
            bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ஫"): bstack1ll11l11l_opy_.current_test_uuid()
        })
def bstack1l1l11llll_opy_(item, call, rep):
  global bstack1ll111lll_opy_
  global bstack1l1ll111_opy_
  global bstack1ll1l1111_opy_
  name = bstack1ll1l11_opy_ (u"࠭ࠧ஬")
  try:
    if rep.when == bstack1ll1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ஭"):
      bstack1l1l1l1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1l1111_opy_:
          name = str(rep.nodeid)
          bstack1l1ll1l11_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩம"), name, bstack1ll1l11_opy_ (u"ࠩࠪய"), bstack1ll1l11_opy_ (u"ࠪࠫர"), bstack1ll1l11_opy_ (u"ࠫࠬற"), bstack1ll1l11_opy_ (u"ࠬ࠭ல"))
          threading.current_thread().bstack1ll1l1l1l1_opy_ = name
          for driver in bstack1l1ll111_opy_:
            if bstack1l1l1l1l_opy_ == driver.session_id:
              driver.execute_script(bstack1l1ll1l11_opy_)
      except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ள").format(str(e)))
      try:
        bstack1l11ll111l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨழ"):
          status = bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨவ") if rep.outcome.lower() == bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஶ") else bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪஷ")
          reason = bstack1ll1l11_opy_ (u"ࠫࠬஸ")
          if status == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஹ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ஺") if status == bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஻") else bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ஼")
          data = name + bstack1ll1l11_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ஽") if status == bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪா") else name + bstack1ll1l11_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧி") + reason
          bstack11l11l1l_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧீ"), bstack1ll1l11_opy_ (u"࠭ࠧு"), bstack1ll1l11_opy_ (u"ࠧࠨூ"), bstack1ll1l11_opy_ (u"ࠨࠩ௃"), level, data)
          for driver in bstack1l1ll111_opy_:
            if bstack1l1l1l1l_opy_ == driver.session_id:
              driver.execute_script(bstack11l11l1l_opy_)
      except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭௄").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ௅").format(str(e)))
  bstack1ll111lll_opy_(item, call, rep)
def bstack11l1lllll_opy_(driver, bstack1ll1l1l11_opy_, test=None):
  global bstack1ll1l1l1l_opy_
  if test != None:
    bstack11l1ll11_opy_ = test.get(bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩெ"), bstack1ll1l11_opy_ (u"ࠬ࠭ே"))
    bstack1l11llll_opy_ = test.get(bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫை"), bstack1ll1l11_opy_ (u"ࠧࠨ௉"))
    PercySDK.screenshot(driver, bstack1ll1l1l11_opy_, bstack11l1ll11_opy_=bstack11l1ll11_opy_, bstack1l11llll_opy_=bstack1l11llll_opy_, bstack1ll1l1lll1_opy_=bstack1ll1l1l1l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1ll1l1l11_opy_)
def bstack1l11l1lll1_opy_(driver):
  if bstack11l1l1l11_opy_.bstack1llll11l1_opy_() is True or bstack11l1l1l11_opy_.capturing() is True:
    return
  bstack11l1l1l11_opy_.bstack1l111ll1l_opy_()
  while not bstack11l1l1l11_opy_.bstack1llll11l1_opy_():
    bstack1l111lll1_opy_ = bstack11l1l1l11_opy_.bstack1llll1111_opy_()
    bstack11l1lllll_opy_(driver, bstack1l111lll1_opy_)
  bstack11l1l1l11_opy_.bstack11111111_opy_()
def bstack1l1l1ll1ll_opy_(sequence, driver_command, response = None, bstack11l1ll11l_opy_ = None, args = None):
    try:
      if sequence != bstack1ll1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨொ"):
        return
      if not CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨோ"), False):
        return
      bstack1l111lll1_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ௌ"), None)
      for command in bstack1l111111ll_opy_:
        if command == driver_command:
          for driver in bstack1l1ll111_opy_:
            bstack1l11l1lll1_opy_(driver)
      bstack1ll1l11l1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫்ࠧ"), bstack1ll1l11_opy_ (u"ࠧࡧࡵࡵࡱࠥ௎"))
      if driver_command in bstack1l1l1l111_opy_[bstack1ll1l11l1_opy_]:
        bstack11l1l1l11_opy_.bstack11ll1ll11_opy_(bstack1l111lll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack111lll11_opy_(framework_name):
  global bstack1lll11ll11_opy_
  global bstack1l11l1ll11_opy_
  global bstack11l1lll1_opy_
  bstack1lll11ll11_opy_ = framework_name
  logger.info(bstack11l1l1ll1_opy_.format(bstack1lll11ll11_opy_.split(bstack1ll1l11_opy_ (u"࠭࠭ࠨ௏"))[0]))
  bstack1l111ll1l1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l11l1111l_opy_:
      Service.start = bstack1llll1ll1_opy_
      Service.stop = bstack111llll1l_opy_
      webdriver.Remote.get = bstack1l111111_opy_
      WebDriver.close = bstack1l111ll1_opy_
      WebDriver.quit = bstack1l1ll1lll1_opy_
      webdriver.Remote.__init__ = bstack1lll1lll1l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l11l1111l_opy_:
        webdriver.Remote.__init__ = bstack1lll11llll_opy_
    WebDriver.execute = bstack1111ll1l_opy_
    bstack1l11l1ll11_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l11l1111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack11lll1l11_opy_
  except Exception as e:
    pass
  bstack1l1lllll_opy_()
  if not bstack1l11l1ll11_opy_:
    bstack1ll111l11_opy_(bstack1ll1l11_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤௐ"), bstack1l1l1ll1_opy_)
  if bstack1ll11llll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11lll1l1l_opy_
    except Exception as e:
      logger.error(bstack11l1111ll_opy_.format(str(e)))
  if bstack1111l1l1l_opy_():
    bstack1lll1llll1_opy_(CONFIG, logger)
  if (bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௑") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ௒"), False):
          bstack1l1lll11_opy_(bstack1l1l1ll1ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l111llll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l11111lll_opy_
      except Exception as e:
        logger.warn(bstack11l1lll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lllll1l1_opy_
      except Exception as e:
        logger.debug(bstack1lll111lll_opy_ + str(e))
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l1lll1l_opy_)
    Output.start_test = bstack11l11llll_opy_
    Output.end_test = bstack1lll1lll11_opy_
    TestStatus.__init__ = bstack11l1llll1_opy_
    QueueItem.__init__ = bstack1llll11ll_opy_
    pabot._create_items = bstack11l11111l_opy_
    try:
      from pabot import __version__ as bstack1llllll11l_opy_
      if version.parse(bstack1llllll11l_opy_) >= version.parse(bstack1ll1l11_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪ௓")):
        pabot._run = bstack11lll111l_opy_
      elif version.parse(bstack1llllll11l_opy_) >= version.parse(bstack1ll1l11_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫ௔")):
        pabot._run = bstack111lllll1_opy_
      else:
        pabot._run = bstack1l1l11l11_opy_
    except Exception as e:
      pabot._run = bstack1l1l11l11_opy_
    pabot._create_command_for_execution = bstack1l1lllllll_opy_
    pabot._report_results = bstack1ll11l1l1l_opy_
  if bstack1ll1l11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௕") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l111l1l_opy_)
    Runner.run_hook = bstack11l1l111l_opy_
    Step.run = bstack1lllll1ll_opy_
  if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௖") in str(framework_name).lower():
    if not bstack1l11l1111l_opy_:
      return
    try:
      if CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ௗ"), False):
          bstack1l1lll11_opy_(bstack1l1l1ll1ll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1lllll1lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll1111ll1_opy_
      Config.getoption = bstack1l1l1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1l11llll_opy_
    except Exception as e:
      pass
def bstack111111ll_opy_():
  global CONFIG
  if bstack1ll1l11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ௘") in CONFIG and int(CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ௙")]) > 1:
    logger.warn(bstack1ll1lll1ll_opy_)
def bstack111l1111l_opy_(arg, bstack1l11l1ll_opy_, bstack11ll11111_opy_=None):
  global CONFIG
  global bstack1111l111_opy_
  global bstack11l1l1111_opy_
  global bstack1l11l1111l_opy_
  global bstack1lll11ll_opy_
  bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௚")
  if bstack1l11l1ll_opy_ and isinstance(bstack1l11l1ll_opy_, str):
    bstack1l11l1ll_opy_ = eval(bstack1l11l1ll_opy_)
  CONFIG = bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫ௛")]
  bstack1111l111_opy_ = bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭௜")]
  bstack11l1l1111_opy_ = bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ௝")]
  bstack1l11l1111l_opy_ = bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ௞")]
  bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ௟"), bstack1l11l1111l_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௠")] = bstack1l111l11l_opy_
  os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ௡")] = json.dumps(CONFIG)
  os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ௢")] = bstack1111l111_opy_
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭௣")] = str(bstack11l1l1111_opy_)
  os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬ௤")] = str(True)
  if bstack11l111111_opy_(arg, [bstack1ll1l11_opy_ (u"ࠧ࠮ࡰࠪ௥"), bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ௦")]) != -1:
    os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪ௧")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111ll1ll1_opy_)
    return
  bstack1llll1l1_opy_()
  global bstack1l1ll1llll_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1lll111l_opy_
  global bstack1111l11l_opy_
  global bstack1lllll11l_opy_
  global bstack11l1lll1_opy_
  global bstack1l1lll11l1_opy_
  arg.append(bstack1ll1l11_opy_ (u"ࠥ࠱࡜ࠨ௨"))
  arg.append(bstack1ll1l11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ௩"))
  arg.append(bstack1ll1l11_opy_ (u"ࠧ࠳ࡗࠣ௪"))
  arg.append(bstack1ll1l11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧ௫"))
  global bstack1l1l1l11_opy_
  global bstack1111l11ll_opy_
  global bstack1111l1ll1_opy_
  global bstack11lll1111_opy_
  global bstack11ll11ll1_opy_
  global bstack1lll1l1ll_opy_
  global bstack1111ll1l1_opy_
  global bstack1ll11lll1l_opy_
  global bstack111ll111_opy_
  global bstack1l1llll11_opy_
  global bstack1l11l1ll1_opy_
  global bstack11lll11l1_opy_
  global bstack1ll111lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l11_opy_ = webdriver.Remote.__init__
    bstack1111l11ll_opy_ = WebDriver.quit
    bstack1ll11lll1l_opy_ = WebDriver.close
    bstack111ll111_opy_ = WebDriver.get
    bstack1111l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1lllll1_opy_(CONFIG) and bstack1lll1lllll_opy_():
    if bstack1l1ll11111_opy_() < version.parse(bstack111l11l1_opy_):
      logger.error(bstack1l1lll1ll1_opy_.format(bstack1l1ll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1llll11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1111ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l11l1ll1_opy_ = Config.getoption
    from _pytest import runner
    bstack11lll11l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1ll1llll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll111lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ௬"))
  bstack1l1lll111l_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ௭"), {}).get(bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௮"))
  bstack1l1lll11l1_opy_ = True
  bstack111lll11_opy_(bstack1l111ll1ll_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ௯")] = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭௰")]
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ௱")] = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௲")]
  os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ௳")] = bstack1l11l1111l_opy_.__str__()
  from _pytest.config import main as bstack1llll1ll_opy_
  bstack1lll1l1ll1_opy_ = []
  try:
    bstack1111ll111_opy_ = bstack1llll1ll_opy_(arg)
    if bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ௴") in multiprocessing.current_process().__dict__.keys():
      for bstack11l11l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1l1ll1_opy_.append(bstack11l11l11_opy_)
    try:
      bstack1ll11l11ll_opy_ = (bstack1lll1l1ll1_opy_, int(bstack1111ll111_opy_))
      bstack11ll11111_opy_.append(bstack1ll11l11ll_opy_)
    except:
      bstack11ll11111_opy_.append((bstack1lll1l1ll1_opy_, bstack1111ll111_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll1l1ll1_opy_.append({bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ௵"): bstack1ll1l11_opy_ (u"ࠪࡔࡷࡵࡣࡦࡵࡶࠤࠬ௶") + os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ௷")), bstack1ll1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௸"): traceback.format_exc(), bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ௹"): int(os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ௺")))})
    bstack11ll11111_opy_.append((bstack1lll1l1ll1_opy_, 1))
def bstack111ll11ll_opy_(arg):
  global bstack111l1ll11_opy_
  bstack111lll11_opy_(bstack1ll1ll11_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௻")] = str(bstack11l1l1111_opy_)
  from behave.__main__ import main as bstack1l1ll11ll_opy_
  status_code = bstack1l1ll11ll_opy_(arg)
  if status_code != 0:
    bstack111l1ll11_opy_ = status_code
def bstack1111111ll_opy_():
  logger.info(bstack1l1111ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ௼"), help=bstack1ll1l11_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ௽"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠫ࠲ࡻࠧ௾"), bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ௿"), help=bstack1ll1l11_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬఀ"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠧ࠮࡭ࠪఁ"), bstack1ll1l11_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧం"), help=bstack1ll1l11_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪః"))
  parser.add_argument(bstack1ll1l11_opy_ (u"ࠪ࠱࡫࠭ఄ"), bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩఅ"), help=bstack1ll1l11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫఆ"))
  bstack1ll111111l_opy_ = parser.parse_args()
  try:
    bstack1l11l1l111_opy_ = bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪఇ")
    if bstack1ll111111l_opy_.framework and bstack1ll111111l_opy_.framework not in (bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧఈ"), bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩఉ")):
      bstack1l11l1l111_opy_ = bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨఊ")
    bstack1l1lll1111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l11l1l111_opy_)
    bstack1l1111l111_opy_ = open(bstack1l1lll1111_opy_, bstack1ll1l11_opy_ (u"ࠪࡶࠬఋ"))
    bstack1llllllll_opy_ = bstack1l1111l111_opy_.read()
    bstack1l1111l111_opy_.close()
    if bstack1ll111111l_opy_.username:
      bstack1llllllll_opy_ = bstack1llllllll_opy_.replace(bstack1ll1l11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫఌ"), bstack1ll111111l_opy_.username)
    if bstack1ll111111l_opy_.key:
      bstack1llllllll_opy_ = bstack1llllllll_opy_.replace(bstack1ll1l11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ఍"), bstack1ll111111l_opy_.key)
    if bstack1ll111111l_opy_.framework:
      bstack1llllllll_opy_ = bstack1llllllll_opy_.replace(bstack1ll1l11_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧఎ"), bstack1ll111111l_opy_.framework)
    file_name = bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪఏ")
    file_path = os.path.abspath(file_name)
    bstack1ll11l1l1_opy_ = open(file_path, bstack1ll1l11_opy_ (u"ࠨࡹࠪఐ"))
    bstack1ll11l1l1_opy_.write(bstack1llllllll_opy_)
    bstack1ll11l1l1_opy_.close()
    logger.info(bstack1llllll1l1_opy_)
    try:
      os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ఑")] = bstack1ll111111l_opy_.framework if bstack1ll111111l_opy_.framework != None else bstack1ll1l11_opy_ (u"ࠥࠦఒ")
      config = yaml.safe_load(bstack1llllllll_opy_)
      config[bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫఓ")] = bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫఔ")
      bstack1lllll11_opy_(bstack1llll11l11_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll111l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llll11l_opy_.format(str(e)))
def bstack1lllll11_opy_(bstack1lll1l111l_opy_, config, bstack11ll11l1l_opy_={}):
  global bstack1l11l1111l_opy_
  global bstack111l11ll_opy_
  global bstack1lll11ll_opy_
  if not config:
    return
  bstack11lll1ll_opy_ = bstack1l1l1111ll_opy_ if not bstack1l11l1111l_opy_ else (
    bstack1ll1111l1l_opy_ if bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪక") in config else bstack1l1lll1l1_opy_)
  bstack1l1l11l111_opy_ = False
  bstack11l111lll_opy_ = False
  if bstack1l11l1111l_opy_ is True:
      if bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫఖ") in config:
          bstack1l1l11l111_opy_ = True
      else:
          bstack11l111lll_opy_ = True
  bstack11lll1ll1_opy_ = bstack1l111ll11_opy_.bstack1ll1lll1l_opy_(config, bstack111l11ll_opy_)
  data = {
    bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪగ"): config[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫఘ")],
    bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ఙ"): config[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧచ")],
    bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩఛ"): bstack1lll1l111l_opy_,
    bstack1ll1l11_opy_ (u"࠭ࡤࡦࡶࡨࡧࡹ࡫ࡤࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪజ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩఝ"), bstack111l11ll_opy_),
    bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪఞ"): bstack1ll1l1lll_opy_,
    bstack1ll1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫట"): bstack1llll1111l_opy_(),
    bstack1ll1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ఠ"): {
      bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩడ"): str(config[bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬఢ")]) if bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ణ") in config else bstack1ll1l11_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣత"),
      bstack1ll1l11_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧ࡙ࡩࡷࡹࡩࡰࡰࠪథ"): sys.version,
      bstack1ll1l11_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫద"): bstack1l111ll11l_opy_(os.getenv(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧధ"), bstack1ll1l11_opy_ (u"ࠦࠧన"))),
      bstack1ll1l11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ఩"): bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ప"),
      bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨఫ"): bstack11lll1ll_opy_,
      bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭బ"): bstack11lll1ll1_opy_,
      bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡹࡺ࡯ࡤࠨభ"): os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨమ")],
      bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧయ"): bstack1l11lllll_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧర"), bstack111l11ll_opy_)),
      bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩఱ"): config[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪల")] if config[bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫళ")] else bstack1ll1l11_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥఴ"),
      bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬవ"): str(config[bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭శ")]) if bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష") in config else bstack1ll1l11_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢస"),
      bstack1ll1l11_opy_ (u"ࠧࡰࡵࠪహ"): sys.platform,
      bstack1ll1l11_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪ఺"): socket.gethostname(),
      bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ఻"): bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨ఼ࠬ"))
    }
  }
  if not bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫఽ")) is None:
    data[bstack1ll1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨా")][bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡎࡧࡷࡥࡩࡧࡴࡢࠩి")] = {
      bstack1ll1l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧీ"): bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ు"),
      bstack1ll1l11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩూ"): bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪృ")),
      bstack1ll1l11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࡒࡺࡳࡢࡦࡴࠪౄ"): bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱࡔ࡯ࠨ౅"))
    }
  if bstack1lll1l111l_opy_ == bstack1ll11ll1ll_opy_:
    data[bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩె")][bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡉ࡯࡯ࡨ࡬࡫ࠬే")] = bstack11l1l1ll_opy_(config)
  update(data[bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫై")], bstack11ll11l1l_opy_)
  try:
    response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ౉"), bstack11ll1l1l1_opy_(bstack1l11llll1_opy_), data, {
      bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺࡨࠨొ"): (config[bstack1ll1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ో")], config[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨౌ")])
    })
    if response:
      logger.debug(bstack1l11lll1l1_opy_.format(bstack1lll1l111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1l1l111_opy_.format(str(e)))
def bstack1l111ll11l_opy_(framework):
  return bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿ్ࠥ").format(str(framework), __version__) if framework else bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ౎").format(
    __version__)
def bstack1llll1l1_opy_():
  global CONFIG
  global bstack11l1l1lll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1lll1ll1_opy_()
    logger.debug(bstack1lll1llll_opy_.format(str(CONFIG)))
    bstack11l1l1lll_opy_ = bstack1l1l11ll_opy_.bstack1ll1l1ll_opy_(CONFIG, bstack11l1l1lll_opy_)
    bstack1l111ll1l1_opy_()
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧ౏") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l1l1l1l_opy_
  atexit.register(bstack1l1l111l11_opy_)
  signal.signal(signal.SIGINT, bstack1111l1ll_opy_)
  signal.signal(signal.SIGTERM, bstack1111l1ll_opy_)
def bstack11l1l1l1l_opy_(exctype, value, traceback):
  global bstack1l1ll111_opy_
  try:
    for driver in bstack1l1ll111_opy_:
      bstack1lll1ll11l_opy_(driver, bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ౐"), bstack1ll1l11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ౑") + str(value))
  except Exception:
    pass
  bstack1l1ll1ll1_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1ll1ll1_opy_(message=bstack1ll1l11_opy_ (u"ࠫࠬ౒"), bstack1l1l11l1l1_opy_ = False):
  global CONFIG
  bstack1llllllll1_opy_ = bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧ౓") if bstack1l1l11l1l1_opy_ else bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౔")
  try:
    if message:
      bstack11ll11l1l_opy_ = {
        bstack1llllllll1_opy_ : str(message)
      }
      bstack1lllll11_opy_(bstack1ll11ll1ll_opy_, CONFIG, bstack11ll11l1l_opy_)
    else:
      bstack1lllll11_opy_(bstack1ll11ll1ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll1ll1ll_opy_.format(str(e)))
def bstack1l111l1ll1_opy_(bstack1lll111l_opy_, size):
  bstack1llll1l1l_opy_ = []
  while len(bstack1lll111l_opy_) > size:
    bstack111ll11l1_opy_ = bstack1lll111l_opy_[:size]
    bstack1llll1l1l_opy_.append(bstack111ll11l1_opy_)
    bstack1lll111l_opy_ = bstack1lll111l_opy_[size:]
  bstack1llll1l1l_opy_.append(bstack1lll111l_opy_)
  return bstack1llll1l1l_opy_
def bstack1l1ll1l111_opy_(args):
  if bstack1ll1l11_opy_ (u"ࠧ࠮࡯ౕࠪ") in args and bstack1ll1l11_opy_ (u"ࠨࡲࡧࡦౖࠬ") in args:
    return True
  return False
def run_on_browserstack(bstack11ll1l1ll_opy_=None, bstack11ll11111_opy_=None, bstack1ll11llll1_opy_=False):
  global CONFIG
  global bstack1111l111_opy_
  global bstack11l1l1111_opy_
  global bstack111l11ll_opy_
  global bstack1lll11ll_opy_
  bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪ౗")
  bstack1lll1ll111_opy_(bstack11l111l11_opy_, logger)
  if bstack11ll1l1ll_opy_ and isinstance(bstack11ll1l1ll_opy_, str):
    bstack11ll1l1ll_opy_ = eval(bstack11ll1l1ll_opy_)
  if bstack11ll1l1ll_opy_:
    CONFIG = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪౘ")]
    bstack1111l111_opy_ = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬౙ")]
    bstack11l1l1111_opy_ = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧౚ")]
    bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ౛"), bstack11l1l1111_opy_)
    bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౜")
  bstack1lll11ll_opy_.bstack11l111ll1_opy_(bstack1ll1l11_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪౝ"), uuid4().__str__())
  logger.debug(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࡁࠬ౞") + bstack1lll11ll_opy_.get_property(bstack1ll1l11_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ౟")))
  if not bstack1ll11llll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111ll1ll1_opy_)
      return
    if sys.argv[1] == bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧౠ") or sys.argv[1] == bstack1ll1l11_opy_ (u"ࠬ࠳ࡶࠨౡ"):
      logger.info(bstack1ll1l11_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ౢ").format(__version__))
      return
    if sys.argv[1] == bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ౣ"):
      bstack1111111ll_opy_()
      return
  args = sys.argv
  bstack1llll1l1_opy_()
  global bstack1l1ll1llll_opy_
  global bstack1l11ll11_opy_
  global bstack1l1lll11l1_opy_
  global bstack1l1111l11_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1lll111l_opy_
  global bstack1111l11l_opy_
  global bstack1llll1l111_opy_
  global bstack1lllll11l_opy_
  global bstack11l1lll1_opy_
  global bstack11ll111l1_opy_
  bstack1l11ll11_opy_ = len(CONFIG.get(bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౤"), []))
  if not bstack1l111l11l_opy_:
    if args[1] == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౥") or args[1] == bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ౦"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ౧")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ౨"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ౩")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭౪"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ౫")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ౬"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ౭")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ౮"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ౯")
      args = args[2:]
    elif args[1] == bstack1ll1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭౰"):
      bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ౱")
      args = args[2:]
    else:
      if not bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౲") in CONFIG or str(CONFIG[bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ౳")]).lower() in [bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ౴"), bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ౵")]:
        bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ౶")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ౷")]).lower() == bstack1ll1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭౸"):
        bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ౹")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ౺")]).lower() == bstack1ll1l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ౻"):
        bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ౼")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ౽")]).lower() == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭౾"):
        bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౿")
        args = args[1:]
      elif str(CONFIG[bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫಀ")]).lower() == bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಁ"):
        bstack1l111l11l_opy_ = bstack1ll1l11_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪಂ")
        args = args[1:]
      else:
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ಃ")] = bstack1l111l11l_opy_
        bstack111111lll_opy_(bstack1l111ll111_opy_)
  os.environ[bstack1ll1l11_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭಄")] = bstack1l111l11l_opy_
  bstack111l11ll_opy_ = bstack1l111l11l_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l11l1l11l_opy_
  if bstack11ll1l1ll_opy_:
    try:
      os.environ[bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಅ")] = bstack1l111l11l_opy_
      bstack1lllll11_opy_(bstack1ll111ll11_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l111l11l1_opy_.format(str(e)))
  global bstack1l1l1l11_opy_
  global bstack1111l11ll_opy_
  global bstack1l111lll1l_opy_
  global bstack1l11ll1l1_opy_
  global bstack1l1l111111_opy_
  global bstack1lll1l1l1l_opy_
  global bstack11lll1111_opy_
  global bstack11ll11ll1_opy_
  global bstack1llll1l11_opy_
  global bstack1lll1l1ll_opy_
  global bstack1111ll1l1_opy_
  global bstack1ll11lll1l_opy_
  global bstack11111l11_opy_
  global bstack1llllll1l_opy_
  global bstack111ll111_opy_
  global bstack1l1llll11_opy_
  global bstack1l11l1ll1_opy_
  global bstack11lll11l1_opy_
  global bstack11l1l11l1_opy_
  global bstack1ll111lll_opy_
  global bstack1111l1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1l1l11_opy_ = webdriver.Remote.__init__
    bstack1111l11ll_opy_ = WebDriver.quit
    bstack1ll11lll1l_opy_ = WebDriver.close
    bstack111ll111_opy_ = WebDriver.get
    bstack1111l1ll1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1lll1l11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l1l1l1_opy_
    bstack1l11l1l11l_opy_ = bstack11l1l1l1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1lllll111l_opy_
    from QWeb.keywords import browser
    bstack1lllll111l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1lllll1_opy_(CONFIG) and bstack1lll1lllll_opy_():
    if bstack1l1ll11111_opy_() < version.parse(bstack111l11l1_opy_):
      logger.error(bstack1l1lll1ll1_opy_.format(bstack1l1ll11111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1llll11_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1111ll_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll1l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩಆ"), False) and not bstack11ll1l1ll_opy_:
    logger.info(bstack1lll111l11_opy_)
  if bstack1l111l11l_opy_ != bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨಇ") or (bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩಈ") and not bstack11ll1l1ll_opy_):
    bstack111lll1l1_opy_()
  if (bstack1l111l11l_opy_ in [bstack1ll1l11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩಉ"), bstack1ll1l11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಊ"), bstack1ll1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ಋ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l111llll1_opy_
        bstack1lll1l1l1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11l1lll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1l1l111111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll111lll_opy_ + str(e))
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l1lll1l_opy_)
    if bstack1l111l11l_opy_ != bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧಌ"):
      bstack11l1l11ll_opy_()
    bstack1l111lll1l_opy_ = Output.start_test
    bstack1l11ll1l1_opy_ = Output.end_test
    bstack11lll1111_opy_ = TestStatus.__init__
    bstack1llll1l11_opy_ = pabot._run
    bstack1lll1l1ll_opy_ = QueueItem.__init__
    bstack1111ll1l1_opy_ = pabot._create_command_for_execution
    bstack11l1l11l1_opy_ = pabot._report_results
  if bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ಍"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l111l1l_opy_)
    bstack11111l11_opy_ = Runner.run_hook
    bstack1llllll1l_opy_ = Step.run
  if bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨಎ"):
    try:
      from _pytest.config import Config
      bstack1l11l1ll1_opy_ = Config.getoption
      from _pytest import runner
      bstack11lll11l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1ll1llll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll111lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪಏ"))
  try:
    framework_name = bstack1ll1l11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಐ") if bstack1l111l11l_opy_ in [bstack1ll1l11_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ಑"), bstack1ll1l11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಒ"), bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧಓ")] else bstack111l11111_opy_(bstack1l111l11l_opy_)
    bstack111lll1l_opy_ = {
      bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨಔ"): bstack1ll1l11_opy_ (u"ࠨࡽ࠳ࢁ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧಕ").format(framework_name) if bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಖ") and bstack1111l1111_opy_() else framework_name,
      bstack1ll1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಗ"): bstack1l11lllll_opy_(framework_name),
      bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಘ"): __version__,
      bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ಙ"): bstack1l111l11l_opy_
    }
    if bstack1l111l11l_opy_ in bstack1lll11111_opy_:
      if bstack1l11l1111l_opy_ and bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ಚ") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧಛ")] == True:
        if bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨಜ") in CONFIG:
          os.environ[bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪಝ")] = os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫಞ"), json.dumps(CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫಟ")]))
          CONFIG[bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬಠ")].pop(bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫಡ"), None)
          CONFIG[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧಢ")].pop(bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ಣ"), None)
        bstack111lll1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩತ")] = {
          bstack1ll1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨಥ"): bstack1ll1l11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ದ"),
          bstack1ll1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ಧ"): str(bstack1l1ll11111_opy_())
        }
    if bstack1l111l11l_opy_ not in [bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧನ")]:
      bstack11l111l1_opy_ = bstack1ll11l11l_opy_.launch(CONFIG, bstack111lll1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l1ll1_opy_.format(bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡍࡻࡢࠨ಩"), str(e)))
  if bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨಪ"):
    bstack1l1lll11l1_opy_ = True
    if bstack11ll1l1ll_opy_ and bstack1ll11llll1_opy_:
      bstack1l1lll111l_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ಫ"), {}).get(bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಬ"))
      bstack111lll11_opy_(bstack11l11lll1_opy_)
    elif bstack11ll1l1ll_opy_:
      bstack1l1lll111l_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಭ"), {}).get(bstack1ll1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಮ"))
      global bstack1l1ll111_opy_
      try:
        if bstack1l1ll1l111_opy_(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩಯ")]) and multiprocessing.current_process().name == bstack1ll1l11_opy_ (u"ࠧ࠱ࠩರ"):
          bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಱ")].remove(bstack1ll1l11_opy_ (u"ࠩ࠰ࡱࠬಲ"))
          bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ಳ")].remove(bstack1ll1l11_opy_ (u"ࠫࡵࡪࡢࠨ಴"))
          bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨವ")] = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩಶ")][0]
          with open(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪಷ")], bstack1ll1l11_opy_ (u"ࠨࡴࠪಸ")) as f:
            bstack1ll1ll111_opy_ = f.read()
          bstack11111lll_opy_ = bstack1ll1l11_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡕࡪࡢࠩࠫ࠱ࡷࡪࡺ࡟ࡵࡴࡤࡧࡪ࠮ࠩ࡝ࡰࠥࠦࠧಹ").format(str(bstack11ll1l1ll_opy_))
          bstack11ll111ll_opy_ = bstack11111lll_opy_ + bstack1ll1ll111_opy_
          bstack1111lll11_opy_ = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭಺")] + bstack1ll1l11_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭಻")
          with open(bstack1111lll11_opy_, bstack1ll1l11_opy_ (u"ࠬࡽ಼ࠧ")):
            pass
          with open(bstack1111lll11_opy_, bstack1ll1l11_opy_ (u"ࠨࡷࠬࠤಽ")) as f:
            f.write(bstack11ll111ll_opy_)
          import subprocess
          bstack1l1ll1l11l_opy_ = subprocess.run([bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢಾ"), bstack1111lll11_opy_])
          if os.path.exists(bstack1111lll11_opy_):
            os.unlink(bstack1111lll11_opy_)
          os._exit(bstack1l1ll1l11l_opy_.returncode)
        else:
          if bstack1l1ll1l111_opy_(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಿ")]):
            bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೀ")].remove(bstack1ll1l11_opy_ (u"ࠪ࠱ࡲ࠭ು"))
            bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧೂ")].remove(bstack1ll1l11_opy_ (u"ࠬࡶࡤࡣࠩೃ"))
            bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")] = bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೅")][0]
          bstack111lll11_opy_(bstack11l11lll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫೆ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫೇ")] = bstack1ll1l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬೈ")
          mod_globals[bstack1ll1l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭೉")] = os.path.abspath(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨೊ")])
          exec(open(bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೋ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1l11_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧೌ").format(str(e)))
          for driver in bstack1l1ll111_opy_:
            bstack11ll11111_opy_.append({
              bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ್࠭"): bstack11ll1l1ll_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ೎")],
              bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ೏"): str(e),
              bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ೐"): multiprocessing.current_process().name
            })
            bstack1lll1ll11l_opy_(driver, bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ೑"), bstack1ll1l11_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ೒") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1ll111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l1l1111_opy_, CONFIG, logger)
      bstack1ll1l11ll1_opy_()
      bstack111111ll_opy_()
      bstack1l11l1ll_opy_ = {
        bstack1ll1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ೓"): args[0],
        bstack1ll1l11_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ೔"): CONFIG,
        bstack1ll1l11_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪೕ"): bstack1111l111_opy_,
        bstack1ll1l11_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬೖ"): bstack11l1l1111_opy_
      }
      percy.bstack111l1l1l1_opy_()
      if bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೗") in CONFIG:
        bstack1l111llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11llllll1_opy_ = manager.list()
        if bstack1l1ll1l111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೘")]):
            if index == 0:
              bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ೙")] = args
            bstack1l111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1ll_opy_, bstack11llllll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೚")]):
            bstack1l111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1ll_opy_, bstack11llllll1_opy_)))
        for t in bstack1l111llll_opy_:
          t.start()
        for t in bstack1l111llll_opy_:
          t.join()
        bstack1llll1l111_opy_ = list(bstack11llllll1_opy_)
      else:
        if bstack1l1ll1l111_opy_(args):
          bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ೛")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l1ll_opy_,))
          test.start()
          test.join()
        else:
          bstack111lll11_opy_(bstack11l11lll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1l11_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ೜")] = bstack1ll1l11_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬೝ")
          mod_globals[bstack1ll1l11_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ೞ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ೟") or bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬೠ"):
    percy.init(bstack11l1l1111_opy_, CONFIG, logger)
    percy.bstack111l1l1l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l1lll1l_opy_)
    bstack1ll1l11ll1_opy_()
    bstack111lll11_opy_(bstack111l1lll_opy_)
    if bstack1l11l1111l_opy_:
      bstack1ll1l11lll_opy_(bstack111l1lll_opy_, args)
      if bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬೡ") in args:
        i = args.index(bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ೢ"))
        args.pop(i)
        args.pop(i)
      if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೣ") not in CONFIG:
        CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭೤")] = [{}]
        bstack1l11ll11_opy_ = 1
      if bstack1l1ll1llll_opy_ == 0:
        bstack1l1ll1llll_opy_ = 1
      args.insert(0, str(bstack1l1ll1llll_opy_))
      args.insert(0, str(bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ೥")))
    if bstack1ll11l11l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11111ll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1l11l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll1l11_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧ೦"),
        ).parse_args(bstack11111ll1_opy_)
        bstack1l1l11111l_opy_ = args.index(bstack11111ll1_opy_[0]) if len(bstack11111ll1_opy_) > 0 else len(args)
        args.insert(bstack1l1l11111l_opy_, str(bstack1ll1l11_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ೧")))
        args.insert(bstack1l1l11111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫ೨"))))
        if bstack1llll111_opy_(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭೩"))) and str(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭೪"), bstack1ll1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ೫"))) != bstack1ll1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ೬"):
          for bstack1ll1l11l_opy_ in bstack1l1l11l1_opy_:
            args.remove(bstack1ll1l11l_opy_)
          bstack111ll1l11_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ೭")).split(bstack1ll1l11_opy_ (u"࠭ࠬࠨ೮"))
          for bstack1lll11l1l1_opy_ in bstack111ll1l11_opy_:
            args.append(bstack1lll11l1l1_opy_)
      except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥ೯").format(e))
    pabot.main(args)
  elif bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ೰"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l1lll1l_opy_)
    for a in args:
      if bstack1ll1l11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨೱ") in a:
        bstack1ll1l1l1l_opy_ = int(a.split(bstack1ll1l11_opy_ (u"ࠪ࠾ࠬೲ"))[1])
      if bstack1ll1l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨೳ") in a:
        bstack1l1lll111l_opy_ = str(a.split(bstack1ll1l11_opy_ (u"ࠬࡀࠧ೴"))[1])
      if bstack1ll1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭೵") in a:
        bstack1111l11l_opy_ = str(a.split(bstack1ll1l11_opy_ (u"ࠧ࠻ࠩ೶"))[1])
    bstack1l11ll1111_opy_ = None
    if bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧ೷") in args:
      i = args.index(bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ೸"))
      args.pop(i)
      bstack1l11ll1111_opy_ = args.pop(i)
    if bstack1l11ll1111_opy_ is not None:
      global bstack1l11ll1l1l_opy_
      bstack1l11ll1l1l_opy_ = bstack1l11ll1111_opy_
    bstack111lll11_opy_(bstack111l1lll_opy_)
    run_cli(args)
    if bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧ೹") in multiprocessing.current_process().__dict__.keys():
      for bstack11l11l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll11111_opy_.append(bstack11l11l11_opy_)
  elif bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ೺"):
    percy.init(bstack11l1l1111_opy_, CONFIG, logger)
    percy.bstack111l1l1l1_opy_()
    bstack1ll111l11l_opy_ = bstack1l1ll1l1l_opy_(args, logger, CONFIG, bstack1l11l1111l_opy_)
    bstack1ll111l11l_opy_.bstack1ll1111lll_opy_()
    bstack1ll1l11ll1_opy_()
    bstack1l1111l11_opy_ = True
    bstack11l1lll1_opy_ = bstack1ll111l11l_opy_.bstack1l1111ll11_opy_()
    bstack1ll111l11l_opy_.bstack1l11l1ll_opy_(bstack1ll1l1111_opy_)
    bstack1l1l1l11ll_opy_ = bstack1ll111l11l_opy_.bstack11lll1l1_opy_(bstack111l1111l_opy_, {
      bstack1ll1l11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭೻"): bstack1111l111_opy_,
      bstack1ll1l11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ೼"): bstack11l1l1111_opy_,
      bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ೽"): bstack1l11l1111l_opy_
    })
    try:
      bstack1lll1l1ll1_opy_, bstack111l1l11l_opy_ = map(list, zip(*bstack1l1l1l11ll_opy_))
      bstack1lllll11l_opy_ = bstack1lll1l1ll1_opy_[0]
      for status_code in bstack111l1l11l_opy_:
        if status_code != 0:
          bstack11ll111l1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨ೾").format(str(e)))
  elif bstack1l111l11l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ೿"):
    try:
      from behave.__main__ import main as bstack1l1ll11ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll111l11_opy_(e, bstack11l111l1l_opy_)
    bstack1ll1l11ll1_opy_()
    bstack1l1111l11_opy_ = True
    bstack1lll1lll1_opy_ = 1
    if bstack1ll1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഀ") in CONFIG:
      bstack1lll1lll1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫഁ")]
    if bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨം") in CONFIG:
      bstack111l1l11_opy_ = int(bstack1lll1lll1_opy_) * int(len(CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഃ")]))
    else:
      bstack111l1l11_opy_ = int(bstack1lll1lll1_opy_)
    config = Configuration(args)
    bstack1ll1l1l11l_opy_ = config.paths
    if len(bstack1ll1l1l11l_opy_) == 0:
      import glob
      pattern = bstack1ll1l11_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ഄ")
      bstack1lll1lll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll1lll_opy_)
      config = Configuration(args)
      bstack1ll1l1l11l_opy_ = config.paths
    bstack1lll111ll_opy_ = [os.path.normpath(item) for item in bstack1ll1l1l11l_opy_]
    bstack111l11lll_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1l111l_opy_ = [item for item in bstack111l11lll_opy_ if item not in bstack1lll111ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1l11_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩഅ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1lll111ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1l1l11_opy_)))
                    for bstack1l1l1l1l11_opy_ in bstack1lll111ll_opy_]
    bstack1ll11lll1_opy_ = []
    for spec in bstack1lll111ll_opy_:
      bstack1l11lll1l_opy_ = []
      bstack1l11lll1l_opy_ += bstack1l1l111l_opy_
      bstack1l11lll1l_opy_.append(spec)
      bstack1ll11lll1_opy_.append(bstack1l11lll1l_opy_)
    execution_items = []
    for bstack1l11lll1l_opy_ in bstack1ll11lll1_opy_:
      if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬആ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ഇ")]):
          item = {}
          item[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࠨഈ")] = bstack1ll1l11_opy_ (u"ࠬࠦࠧഉ").join(bstack1l11lll1l_opy_)
          item[bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬഊ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࠫഋ")] = bstack1ll1l11_opy_ (u"ࠨࠢࠪഌ").join(bstack1l11lll1l_opy_)
        item[bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ഍")] = 0
        execution_items.append(item)
    bstack1l1l111ll1_opy_ = bstack1l111l1ll1_opy_(execution_items, bstack111l1l11_opy_)
    for execution_item in bstack1l1l111ll1_opy_:
      bstack1l111llll_opy_ = []
      for item in execution_item:
        bstack1l111llll_opy_.append(bstack1lll111l1_opy_(name=str(item[bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩഎ")]),
                                             target=bstack111ll11ll_opy_,
                                             args=(item[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࠨഏ")],)))
      for t in bstack1l111llll_opy_:
        t.start()
      for t in bstack1l111llll_opy_:
        t.join()
  else:
    bstack111111lll_opy_(bstack1l111ll111_opy_)
  if not bstack11ll1l1ll_opy_:
    bstack11ll1l111_opy_()
  bstack1l1l11ll_opy_.bstack1ll11l11l1_opy_()
def browserstack_initialize(bstack1l1l111lll_opy_=None):
  run_on_browserstack(bstack1l1l111lll_opy_, None, True)
def bstack11ll1l111_opy_():
  global CONFIG
  global bstack111l11ll_opy_
  global bstack11ll111l1_opy_
  global bstack111l1ll11_opy_
  global bstack1lll11ll_opy_
  bstack1ll11l11l_opy_.stop()
  bstack11ll1ll1l_opy_.bstack1l1l11lll1_opy_()
  [bstack1l111lllll_opy_, bstack1l11111ll_opy_] = get_build_link()
  if bstack1l111lllll_opy_ is not None and bstack1lll1l1111_opy_() != -1:
    sessions = bstack1l1l11l11l_opy_(bstack1l111lllll_opy_)
    bstack11llll1ll_opy_(sessions, bstack1l11111ll_opy_)
  if bstack111l11ll_opy_ == bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬഐ") and bstack11ll111l1_opy_ != 0:
    sys.exit(bstack11ll111l1_opy_)
  if bstack111l11ll_opy_ == bstack1ll1l11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭഑") and bstack111l1ll11_opy_ != 0:
    sys.exit(bstack111l1ll11_opy_)
def bstack111l11111_opy_(bstack1l11l1ll1l_opy_):
  if bstack1l11l1ll1l_opy_:
    return bstack1l11l1ll1l_opy_.capitalize()
  else:
    return bstack1ll1l11_opy_ (u"ࠧࠨഒ")
def bstack1111l111l_opy_(bstack1l1llll1_opy_):
  if bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ഓ") in bstack1l1llll1_opy_ and bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഔ")] != bstack1ll1l11_opy_ (u"ࠪࠫക"):
    return bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഖ")]
  else:
    bstack1lll111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨഗ")
    if bstack1ll1l11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ഘ") in bstack1l1llll1_opy_ and bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧങ")] != None:
      bstack1lll111l1l_opy_ += bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨച")] + bstack1ll1l11_opy_ (u"ࠤ࠯ࠤࠧഛ")
      if bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡳࡸ࠭ജ")] == bstack1ll1l11_opy_ (u"ࠦ࡮ࡵࡳࠣഝ"):
        bstack1lll111l1l_opy_ += bstack1ll1l11_opy_ (u"ࠧ࡯ࡏࡔࠢࠥഞ")
      bstack1lll111l1l_opy_ += (bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪട")] or bstack1ll1l11_opy_ (u"ࠧࠨഠ"))
      return bstack1lll111l1l_opy_
    else:
      bstack1lll111l1l_opy_ += bstack111l11111_opy_(bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩഡ")]) + bstack1ll1l11_opy_ (u"ࠤࠣࠦഢ") + (
              bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬണ")] or bstack1ll1l11_opy_ (u"ࠫࠬത")) + bstack1ll1l11_opy_ (u"ࠧ࠲ࠠࠣഥ")
      if bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"࠭࡯ࡴࠩദ")] == bstack1ll1l11_opy_ (u"ࠢࡘ࡫ࡱࡨࡴࡽࡳࠣധ"):
        bstack1lll111l1l_opy_ += bstack1ll1l11_opy_ (u"࡙ࠣ࡬ࡲࠥࠨന")
      bstack1lll111l1l_opy_ += bstack1l1llll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ഩ")] or bstack1ll1l11_opy_ (u"ࠪࠫപ")
      return bstack1lll111l1l_opy_
def bstack1l11l1llll_opy_(bstack1ll1ll11l1_opy_):
  if bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠦࡩࡵ࡮ࡦࠤഫ"):
    return bstack1ll1l11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡄࡱࡰࡴࡱ࡫ࡴࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨബ")
  elif bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨഭ"):
    return bstack1ll1l11_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡌࡡࡪ࡮ࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪമ")
  elif bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣയ"):
    return bstack1ll1l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡕࡧࡳࡴࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩര")
  elif bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤറ"):
    return bstack1ll1l11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡈࡶࡷࡵࡲ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ല")
  elif bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠧࡺࡩ࡮ࡧࡲࡹࡹࠨള"):
    return bstack1ll1l11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࠥࡨࡩࡦ࠹࠲࠷࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࠧࡪ࡫ࡡ࠴࠴࠹ࠦࡃ࡚ࡩ࡮ࡧࡲࡹࡹࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫഴ")
  elif bstack1ll1ll11l1_opy_ == bstack1ll1l11_opy_ (u"ࠢࡳࡷࡱࡲ࡮ࡴࡧࠣവ"):
    return bstack1ll1l11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࡖࡺࡴ࡮ࡪࡰࡪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩശ")
  else:
    return bstack1ll1l11_opy_ (u"ࠩ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃ࠭ഷ") + bstack111l11111_opy_(
      bstack1ll1ll11l1_opy_) + bstack1ll1l11_opy_ (u"ࠪࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩസ")
def bstack1l1l11111_opy_(session):
  return bstack1ll1l11_opy_ (u"ࠫࡁࡺࡲࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡴࡲࡻࠧࡄ࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠡࡵࡨࡷࡸ࡯࡯࡯࠯ࡱࡥࡲ࡫ࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࡿࢂࠨࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡡࡥࡰࡦࡴ࡫ࠣࡀࡾࢁࡁ࠵ࡡ࠿࠾࠲ࡸࡩࡄࡻࡾࡽࢀࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂ࠯ࡵࡴࡁࠫഹ").format(
    session[bstack1ll1l11_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩഺ")], bstack1111l111l_opy_(session), bstack1l11l1llll_opy_(session[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷ഻ࠬ")]),
    bstack1l11l1llll_opy_(session[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹ഼ࠧ")]),
    bstack111l11111_opy_(session[bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩഽ")] or session[bstack1ll1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩാ")] or bstack1ll1l11_opy_ (u"ࠪࠫി")) + bstack1ll1l11_opy_ (u"ࠦࠥࠨീ") + (session[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧു")] or bstack1ll1l11_opy_ (u"࠭ࠧൂ")),
    session[bstack1ll1l11_opy_ (u"ࠧࡰࡵࠪൃ")] + bstack1ll1l11_opy_ (u"ࠣࠢࠥൄ") + session[bstack1ll1l11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭൅")], session[bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬെ")] or bstack1ll1l11_opy_ (u"ࠫࠬേ"),
    session[bstack1ll1l11_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩൈ")] if session[bstack1ll1l11_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ൉")] else bstack1ll1l11_opy_ (u"ࠧࠨൊ"))
def bstack11llll1ll_opy_(sessions, bstack1l11111ll_opy_):
  try:
    bstack11l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤോ")
    if not os.path.exists(bstack1l1l1l1lll_opy_):
      os.mkdir(bstack1l1l1l1lll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l11_opy_ (u"ࠩࡤࡷࡸ࡫ࡴࡴ࠱ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧൌ")), bstack1ll1l11_opy_ (u"ࠪࡶ്ࠬ")) as f:
      bstack11l11ll1_opy_ = f.read()
    bstack11l11ll1_opy_ = bstack11l11ll1_opy_.replace(bstack1ll1l11_opy_ (u"ࠫࢀࠫࡒࡆࡕࡘࡐ࡙࡙࡟ࡄࡑࡘࡒ࡙ࠫࡽࠨൎ"), str(len(sessions)))
    bstack11l11ll1_opy_ = bstack11l11ll1_opy_.replace(bstack1ll1l11_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡕࡓࡎࠨࢁࠬ൏"), bstack1l11111ll_opy_)
    bstack11l11ll1_opy_ = bstack11l11ll1_opy_.replace(bstack1ll1l11_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠪࢃࠧ൐"),
                                              sessions[0].get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡢ࡯ࡨࠫ൑")) if sessions[0] else bstack1ll1l11_opy_ (u"ࠨࠩ൒"))
    with open(os.path.join(bstack1l1l1l1lll_opy_, bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭൓")), bstack1ll1l11_opy_ (u"ࠪࡻࠬൔ")) as stream:
      stream.write(bstack11l11ll1_opy_.split(bstack1ll1l11_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨൕ"))[0])
      for session in sessions:
        stream.write(bstack1l1l11111_opy_(session))
      stream.write(bstack11l11ll1_opy_.split(bstack1ll1l11_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩൖ"))[1])
    logger.info(bstack1ll1l11_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡤࡸ࡭ࡱࡪࠠࡢࡴࡷ࡭࡫ࡧࡣࡵࡵࠣࡥࡹࠦࡻࡾࠩൗ").format(bstack1l1l1l1lll_opy_));
  except Exception as e:
    logger.debug(bstack1llll111ll_opy_.format(str(e)))
def bstack1l1l11l11l_opy_(bstack1l111lllll_opy_):
  global CONFIG
  try:
    host = bstack1ll1l11_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ൘") if bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࠬ൙") in CONFIG else bstack1ll1l11_opy_ (u"ࠩࡤࡴ࡮࠭൚")
    user = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ൛")]
    key = CONFIG[bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ൜")]
    bstack1lllllllll_opy_ = bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ൝") if bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࠪ൞") in CONFIG else bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩൟ")
    url = bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠯࡬ࡶࡳࡳ࠭ൠ").format(user, key, host, bstack1lllllllll_opy_,
                                                                                bstack1l111lllll_opy_)
    headers = {
      bstack1ll1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨൡ"): bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ൢ"),
    }
    proxies = bstack1lllllll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩൣ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l11111l_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1ll1l1lll_opy_
  try:
    if bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ൤") in CONFIG:
      host = bstack1ll1l11_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ൥") if bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫ൦") in CONFIG else bstack1ll1l11_opy_ (u"ࠨࡣࡳ࡭ࠬ൧")
      user = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ൨")]
      key = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭൩")]
      bstack1lllllllll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ൪") if bstack1ll1l11_opy_ (u"ࠬࡧࡰࡱࠩ൫") in CONFIG else bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ൬")
      url = bstack1ll1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧ൭").format(user, key, host, bstack1lllllllll_opy_)
      headers = {
        bstack1ll1l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ൮"): bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ൯"),
      }
      if bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ൰") in CONFIG:
        params = {bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ൱"): CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ൲")], bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൳"): CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൴")]}
      else:
        params = {bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭൵"): CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ൶")]}
      proxies = bstack1lllllll1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111l1l111_opy_ = response.json()[0][bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭൷")]
        if bstack111l1l111_opy_:
          bstack1l11111ll_opy_ = bstack111l1l111_opy_[bstack1ll1l11_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ൸")].split(bstack1ll1l11_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫ൹"))[0] + bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧൺ") + bstack111l1l111_opy_[
            bstack1ll1l11_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪൻ")]
          logger.info(bstack1l11lll11_opy_.format(bstack1l11111ll_opy_))
          bstack1ll1l1lll_opy_ = bstack111l1l111_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫർ")]
          bstack1ll111l1l1_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬൽ")]
          if bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬൾ") in CONFIG:
            bstack1ll111l1l1_opy_ += bstack1ll1l11_opy_ (u"ࠫࠥ࠭ൿ") + CONFIG[bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ඀")]
          if bstack1ll111l1l1_opy_ != bstack111l1l111_opy_[bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫඁ")]:
            logger.debug(bstack1ll11111l1_opy_.format(bstack111l1l111_opy_[bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬං")], bstack1ll111l1l1_opy_))
          return [bstack111l1l111_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫඃ")], bstack1l11111ll_opy_]
    else:
      logger.warn(bstack11ll1l11l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l11ll_opy_.format(str(e)))
  return [None, None]
def bstack1lll111ll1_opy_(url, bstack1l1l1lllll_opy_=False):
  global CONFIG
  global bstack1l1l1l1l1_opy_
  if not bstack1l1l1l1l1_opy_:
    hostname = bstack1llll1ll11_opy_(url)
    is_private = bstack1ll11ll1l1_opy_(hostname)
    if (bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭඄") in CONFIG and not bstack1llll111_opy_(CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧඅ")])) and (is_private or bstack1l1l1lllll_opy_):
      bstack1l1l1l1l1_opy_ = hostname
def bstack1llll1ll11_opy_(url):
  return urlparse(url).hostname
def bstack1ll11ll1l1_opy_(hostname):
  for bstack1l111l1lll_opy_ in bstack1ll1111l_opy_:
    regex = re.compile(bstack1l111l1lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1ll1l1llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1ll1l1l1l_opy_
  bstack11lllllll_opy_ = not (bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨආ"), None) and bstack1ll1l1l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫඇ"), None))
  bstack1lllll11ll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ඈ"), None) != True
  if not bstack1l1ll111l_opy_.bstack1lllllll11_opy_(CONFIG, bstack1ll1l1l1l_opy_) or (bstack1lllll11ll_opy_ and bstack11lllllll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥඉ"))
    return {}
  try:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬඊ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1ll1l1l1_opy_.bstack1111lll1l_opy_)
    return results
  except Exception:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦඋ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1ll1l1l1l_opy_
  bstack11lllllll_opy_ = not (bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧඌ"), None) and bstack1ll1l1l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪඍ"), None))
  bstack1lllll11ll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬඎ"), None) != True
  if not bstack1l1ll111l_opy_.bstack1lllllll11_opy_(CONFIG, bstack1ll1l1l1l_opy_) or (bstack1lllll11ll_opy_ and bstack11lllllll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥඏ"))
    return {}
  try:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬඐ"))
    logger.debug(perform_scan(driver))
    bstack11l11l1ll_opy_ = driver.execute_async_script(bstack1l1ll1l1l1_opy_.bstack1l11ll11l_opy_)
    return bstack11l11l1ll_opy_
  except Exception:
    logger.error(bstack1ll1l11_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤඑ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1ll1l1l1l_opy_
  bstack11lllllll_opy_ = not (bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ඒ"), None) and bstack1ll1l1l1_opy_(
          threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩඓ"), None))
  bstack1lllll11ll_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫඔ"), None) != True
  if not bstack1l1ll111l_opy_.bstack1lllllll11_opy_(CONFIG, bstack1ll1l1l1l_opy_) or (bstack1lllll11ll_opy_ and bstack11lllllll_opy_):
    logger.warning(bstack1ll1l11_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢඕ"))
    return {}
  try:
    bstack1l11l11ll1_opy_ = driver.execute_async_script(bstack1l1ll1l1l1_opy_.perform_scan, {bstack1ll1l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ඖ"): kwargs.get(bstack1ll1l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ඗"), None) or bstack1ll1l11_opy_ (u"ࠨࠩ඘")})
    return bstack1l11l11ll1_opy_
  except Exception:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣ඙"))
    return {}