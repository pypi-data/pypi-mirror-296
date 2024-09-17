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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11ll1l1l1_opy_, bstack1l11ll1ll_opy_
class bstack1111llll1_opy_:
  working_dir = os.getcwd()
  bstack11111lll1_opy_ = False
  config = {}
  binary_path = bstack1ll1l11_opy_ (u"ࠪࠫᔘ")
  bstack1llll111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠫࠬᔙ")
  bstack11l1l1l11_opy_ = False
  bstack1lll1lllll1_opy_ = None
  bstack1llll11ll11_opy_ = {}
  bstack1lll1llllll_opy_ = 300
  bstack1llll1l1l1l_opy_ = False
  logger = None
  bstack1lll1llll11_opy_ = False
  bstack1llll1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠬ࠭ᔚ")
  bstack1llll11l111_opy_ = {
    bstack1ll1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᔛ") : 1,
    bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᔜ") : 2,
    bstack1ll1l11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ᔝ") : 3,
    bstack1ll1l11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᔞ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lllll1l111_opy_(self):
    bstack1lllll11lll_opy_ = bstack1ll1l11_opy_ (u"ࠪࠫᔟ")
    bstack1llll11lll1_opy_ = sys.platform
    bstack1llll1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᔠ")
    if re.match(bstack1ll1l11_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᔡ"), bstack1llll11lll1_opy_) != None:
      bstack1lllll11lll_opy_ = bstack111ll1l1l1_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᔢ")
      self.bstack1llll1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠧ࡮ࡣࡦࠫᔣ")
    elif re.match(bstack1ll1l11_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᔤ"), bstack1llll11lll1_opy_) != None:
      bstack1lllll11lll_opy_ = bstack111ll1l1l1_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥᔥ")
      bstack1llll1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᔦ")
      self.bstack1llll1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠫࡼ࡯࡮ࠨᔧ")
    else:
      bstack1lllll11lll_opy_ = bstack111ll1l1l1_opy_ + bstack1ll1l11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᔨ")
      self.bstack1llll1ll111_opy_ = bstack1ll1l11_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᔩ")
    return bstack1lllll11lll_opy_, bstack1llll1llll1_opy_
  def bstack1lllll11l11_opy_(self):
    try:
      bstack1llll1ll11l_opy_ = [os.path.join(expanduser(bstack1ll1l11_opy_ (u"ࠢࡿࠤᔪ")), bstack1ll1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᔫ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll1ll11l_opy_:
        if(self.bstack1lllll1111l_opy_(path)):
          return path
      raise bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡲࡢࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᔬ")
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᔭ").format(e))
  def bstack1lllll1111l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll1111ll_opy_(self, bstack1lllll11lll_opy_, bstack1llll1llll1_opy_):
    try:
      bstack1llll11ll1l_opy_ = self.bstack1lllll11l11_opy_()
      bstack1llll11111l_opy_ = os.path.join(bstack1llll11ll1l_opy_, bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᔮ"))
      bstack1llll111l11_opy_ = os.path.join(bstack1llll11ll1l_opy_, bstack1llll1llll1_opy_)
      if os.path.exists(bstack1llll111l11_opy_):
        self.logger.info(bstack1ll1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᔯ").format(bstack1llll111l11_opy_))
        return bstack1llll111l11_opy_
      if os.path.exists(bstack1llll11111l_opy_):
        self.logger.info(bstack1ll1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦᔰ").format(bstack1llll11111l_opy_))
        return self.bstack1lllll1l1l1_opy_(bstack1llll11111l_opy_, bstack1llll1llll1_opy_)
      self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧᔱ").format(bstack1lllll11lll_opy_))
      response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠨࡉࡈࡘࠬᔲ"), bstack1lllll11lll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1llll11111l_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࡦࠬᔳ")) as file:
          file.write(response.content)
        self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᔴ").format(bstack1llll11111l_opy_))
        return self.bstack1lllll1l1l1_opy_(bstack1llll11111l_opy_, bstack1llll1llll1_opy_)
      else:
        raise(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᔵ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᔶ").format(e))
  def bstack1llll111l1l_opy_(self, bstack1lllll11lll_opy_, bstack1llll1llll1_opy_):
    try:
      retry = 2
      bstack1llll111l11_opy_ = None
      bstack1lllll111l1_opy_ = False
      while retry > 0:
        bstack1llll111l11_opy_ = self.bstack1llll1111ll_opy_(bstack1lllll11lll_opy_, bstack1llll1llll1_opy_)
        bstack1lllll111l1_opy_ = self.bstack1llll1l11l1_opy_(bstack1lllll11lll_opy_, bstack1llll1llll1_opy_, bstack1llll111l11_opy_)
        if bstack1lllll111l1_opy_:
          break
        retry -= 1
      return bstack1llll111l11_opy_, bstack1lllll111l1_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᔷ").format(e))
    return bstack1llll111l11_opy_, False
  def bstack1llll1l11l1_opy_(self, bstack1lllll11lll_opy_, bstack1llll1llll1_opy_, bstack1llll111l11_opy_, bstack1llll1l1l11_opy_ = 0):
    if bstack1llll1l1l11_opy_ > 1:
      return False
    if bstack1llll111l11_opy_ == None or os.path.exists(bstack1llll111l11_opy_) == False:
      self.logger.warn(bstack1ll1l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᔸ"))
      return False
    bstack1llll11llll_opy_ = bstack1ll1l11_opy_ (u"ࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼࡠ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠳ࡢࡤࠬ࠰࡟ࡨ࠰ࠨᔹ")
    command = bstack1ll1l11_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔺ").format(bstack1llll111l11_opy_)
    bstack1lllll11111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1llll11llll_opy_, bstack1lllll11111_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤᔻ"))
      return False
  def bstack1lllll1l1l1_opy_(self, bstack1llll11111l_opy_, bstack1llll1llll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll11111l_opy_)
      shutil.unpack_archive(bstack1llll11111l_opy_, working_dir)
      bstack1llll111l11_opy_ = os.path.join(working_dir, bstack1llll1llll1_opy_)
      os.chmod(bstack1llll111l11_opy_, 0o755)
      return bstack1llll111l11_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᔼ"))
  def bstack1llll1l1lll_opy_(self):
    try:
      percy = str(self.config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᔽ"), bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧᔾ"))).lower()
      if percy != bstack1ll1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᔿ"):
        return False
      self.bstack11l1l1l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕀ").format(e))
  def bstack1lllll1l11l_opy_(self):
    try:
      bstack1lllll1l11l_opy_ = str(self.config.get(bstack1ll1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬᕁ"), bstack1ll1l11_opy_ (u"ࠥࡥࡺࡺ࡯ࠣᕂ"))).lower()
      return bstack1lllll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᕃ").format(e))
  def init(self, bstack11111lll1_opy_, config, logger):
    self.bstack11111lll1_opy_ = bstack11111lll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1l1lll_opy_():
      return
    self.bstack1llll11ll11_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫᕄ"), {})
    self.bstack1llll1lll1l_opy_ = config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᕅ"), bstack1ll1l11_opy_ (u"ࠢࡢࡷࡷࡳࠧᕆ"))
    try:
      bstack1lllll11lll_opy_, bstack1llll1llll1_opy_ = self.bstack1lllll1l111_opy_()
      bstack1llll111l11_opy_, bstack1lllll111l1_opy_ = self.bstack1llll111l1l_opy_(bstack1lllll11lll_opy_, bstack1llll1llll1_opy_)
      if bstack1lllll111l1_opy_:
        self.binary_path = bstack1llll111l11_opy_
        thread = Thread(target=self.bstack1lll1llll1l_opy_)
        thread.start()
      else:
        self.bstack1lll1llll11_opy_ = True
        self.logger.error(bstack1ll1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦࡦࡰࡷࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤ࡚ࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡐࡦࡴࡦࡽࠧᕇ").format(bstack1llll111l11_opy_))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕈ").format(e))
  def bstack1llll1ll1ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll1l11_opy_ (u"ࠪࡰࡴ࡭ࠧᕉ"), bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡰࡴ࡭ࠧᕊ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡖࡵࡴࡪ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࡵࠣࡥࡹࠦࡻࡾࠤᕋ").format(logfile))
      self.bstack1llll111ll1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࠦࡰࡦࡴࡦࡽࠥࡲ࡯ࡨࠢࡳࡥࡹ࡮ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᕌ").format(e))
  def bstack1lll1llll1l_opy_(self):
    bstack1lllll111ll_opy_ = self.bstack1llll11l1ll_opy_()
    if bstack1lllll111ll_opy_ == None:
      self.bstack1lll1llll11_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠥᕍ"))
      return False
    command_args = [bstack1ll1l11_opy_ (u"ࠣࡣࡳࡴ࠿࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠤᕎ") if self.bstack11111lll1_opy_ else bstack1ll1l11_opy_ (u"ࠩࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹ࠭ᕏ")]
    bstack1lllll11ll1_opy_ = self.bstack1llll11l1l1_opy_()
    if bstack1lllll11ll1_opy_ != None:
      command_args.append(bstack1ll1l11_opy_ (u"ࠥ࠱ࡨࠦࡻࡾࠤᕐ").format(bstack1lllll11ll1_opy_))
    env = os.environ.copy()
    env[bstack1ll1l11_opy_ (u"ࠦࡕࡋࡒࡄ࡛ࡢࡘࡔࡑࡅࡏࠤᕑ")] = bstack1lllll111ll_opy_
    env[bstack1ll1l11_opy_ (u"࡚ࠧࡈࡠࡄࡘࡍࡑࡊ࡟ࡖࡗࡌࡈࠧᕒ")] = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᕓ"), bstack1ll1l11_opy_ (u"ࠧࠨᕔ"))
    bstack1llll1lll11_opy_ = [self.binary_path]
    self.bstack1llll1ll1ll_opy_()
    self.bstack1lll1lllll1_opy_ = self.bstack1llll11l11l_opy_(bstack1llll1lll11_opy_ + command_args, env)
    self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡕࡷࡥࡷࡺࡩ࡯ࡩࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠤᕕ"))
    bstack1llll1l1l11_opy_ = 0
    while self.bstack1lll1lllll1_opy_.poll() == None:
      bstack1llll111lll_opy_ = self.bstack1llll1ll1l1_opy_()
      if bstack1llll111lll_opy_:
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠧᕖ"))
        self.bstack1llll1l1l1l_opy_ = True
        return True
      bstack1llll1l1l11_opy_ += 1
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡕࡩࡹࡸࡹࠡ࠯ࠣࡿࢂࠨᕗ").format(bstack1llll1l1l11_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡌࡡࡪ࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࢀࢃࠠࡢࡶࡷࡩࡲࡶࡴࡴࠤᕘ").format(bstack1llll1l1l11_opy_))
    self.bstack1lll1llll11_opy_ = True
    return False
  def bstack1llll1ll1l1_opy_(self, bstack1llll1l1l11_opy_ = 0):
    try:
      if bstack1llll1l1l11_opy_ > 10:
        return False
      bstack1lll1lll1l1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡘࡋࡒࡗࡇࡕࡣࡆࡊࡄࡓࡇࡖࡗࠬᕙ"), bstack1ll1l11_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵ࠼࠸࠷࠸࠾ࠧᕚ"))
      bstack1llll1l11ll_opy_ = bstack1lll1lll1l1_opy_ + bstack111ll1l1ll_opy_
      response = requests.get(bstack1llll1l11ll_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1llll11l1ll_opy_(self):
    bstack1lll1lll11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࠫᕛ") if self.bstack11111lll1_opy_ else bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᕜ")
    bstack11111l111l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡤࡴ࡮࠵ࡡࡱࡲࡢࡴࡪࡸࡣࡺ࠱ࡪࡩࡹࡥࡰࡳࡱ࡭ࡩࡨࡺ࡟ࡵࡱ࡮ࡩࡳࡅ࡮ࡢ࡯ࡨࡁࢀࢃࠦࡵࡻࡳࡩࡂࢁࡽࠣᕝ").format(self.config[bstack1ll1l11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᕞ")], bstack1lll1lll11l_opy_)
    uri = bstack11ll1l1l1_opy_(bstack11111l111l_opy_)
    try:
      response = bstack1l11ll1ll_opy_(bstack1ll1l11_opy_ (u"ࠫࡌࡋࡔࠨᕟ"), uri, {}, {bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡪࠪᕠ"): (self.config[bstack1ll1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᕡ")], self.config[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᕢ")])})
      if response.status_code == 200:
        bstack1lll1lll111_opy_ = response.json()
        if bstack1ll1l11_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᕣ") in bstack1lll1lll111_opy_:
          return bstack1lll1lll111_opy_[bstack1ll1l11_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᕤ")]
        else:
          raise bstack1ll1l11_opy_ (u"ࠪࡘࡴࡱࡥ࡯ࠢࡑࡳࡹࠦࡆࡰࡷࡱࡨࠥ࠳ࠠࡼࡿࠪᕥ").format(bstack1lll1lll111_opy_)
      else:
        raise bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡰࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡴࡶࡤࡸࡺࡹࠠ࠮ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡄࡲࡨࡾࠦ࠭ࠡࡽࢀࠦᕦ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡶࡲࡰ࡬ࡨࡧࡹࠨᕧ").format(e))
  def bstack1llll11l1l1_opy_(self):
    bstack1llll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠨࡰࡦࡴࡦࡽࡈࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠤᕨ"))
    try:
      if bstack1ll1l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕩ") not in self.bstack1llll11ll11_opy_:
        self.bstack1llll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᕪ")] = 2
      with open(bstack1llll111111_opy_, bstack1ll1l11_opy_ (u"ࠩࡺࠫᕫ")) as fp:
        json.dump(self.bstack1llll11ll11_opy_, fp)
      return bstack1llll111111_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡣࡳࡧࡤࡸࡪࠦࡰࡦࡴࡦࡽࠥࡩ࡯࡯ࡨ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕬ").format(e))
  def bstack1llll11l11l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll1ll111_opy_ == bstack1ll1l11_opy_ (u"ࠫࡼ࡯࡮ࠨᕭ"):
        bstack1lllll11l1l_opy_ = [bstack1ll1l11_opy_ (u"ࠬࡩ࡭ࡥ࠰ࡨࡼࡪ࠭ᕮ"), bstack1ll1l11_opy_ (u"࠭࠯ࡤࠩᕯ")]
        cmd = bstack1lllll11l1l_opy_ + cmd
      cmd = bstack1ll1l11_opy_ (u"ࠧࠡࠩᕰ").join(cmd)
      self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡔࡸࡲࡳ࡯࡮ࡨࠢࡾࢁࠧᕱ").format(cmd))
      with open(self.bstack1llll111ll1_opy_, bstack1ll1l11_opy_ (u"ࠤࡤࠦᕲ")) as bstack1lll1lll1ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1lll1lll1ll_opy_, text=True, stderr=bstack1lll1lll1ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1lll1llll11_opy_ = True
      self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠤࡼ࡯ࡴࡩࠢࡦࡱࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᕳ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1l1l1l_opy_:
        self.logger.info(bstack1ll1l11_opy_ (u"ࠦࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡐࡦࡴࡦࡽࠧᕴ"))
        cmd = [self.binary_path, bstack1ll1l11_opy_ (u"ࠧ࡫ࡸࡦࡥ࠽ࡷࡹࡵࡰࠣᕵ")]
        self.bstack1llll11l11l_opy_(cmd)
        self.bstack1llll1l1l1l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡴࡶࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᕶ").format(cmd, e))
  def bstack111l1l1l1_opy_(self):
    if not self.bstack11l1l1l11_opy_:
      return
    try:
      bstack1llll1l1ll1_opy_ = 0
      while not self.bstack1llll1l1l1l_opy_ and bstack1llll1l1ll1_opy_ < self.bstack1lll1llllll_opy_:
        if self.bstack1lll1llll11_opy_:
          self.logger.info(bstack1ll1l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥ࡬ࡡࡪ࡮ࡨࡨࠧᕷ"))
          return
        time.sleep(1)
        bstack1llll1l1ll1_opy_ += 1
      os.environ[bstack1ll1l11_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡃࡇࡖࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓࠧᕸ")] = str(self.bstack1lll1ll1lll_opy_())
      self.logger.info(bstack1ll1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠥᕹ"))
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᕺ").format(e))
  def bstack1lll1ll1lll_opy_(self):
    if self.bstack11111lll1_opy_:
      return
    try:
      bstack1llll1l111l_opy_ = [platform[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᕻ")].lower() for platform in self.config.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕼ"), [])]
      bstack1llll1l1111_opy_ = sys.maxsize
      bstack1llll1lllll_opy_ = bstack1ll1l11_opy_ (u"࠭ࠧᕽ")
      for browser in bstack1llll1l111l_opy_:
        if browser in self.bstack1llll11l111_opy_:
          bstack1llll1111l1_opy_ = self.bstack1llll11l111_opy_[browser]
        if bstack1llll1111l1_opy_ < bstack1llll1l1111_opy_:
          bstack1llll1l1111_opy_ = bstack1llll1111l1_opy_
          bstack1llll1lllll_opy_ = browser
      return bstack1llll1lllll_opy_
    except Exception as e:
      self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡤࡨࡷࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᕾ").format(e))