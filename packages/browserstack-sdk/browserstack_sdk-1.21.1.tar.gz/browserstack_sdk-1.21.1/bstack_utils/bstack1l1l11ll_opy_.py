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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111lll1111_opy_, bstack111ll1ll11_opy_
import tempfile
import json
bstack1lllllll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬࠭ᒩ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1ll1l11_opy_ (u"ࠬࡢ࡮ࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᒪ"),
      datefmt=bstack1ll1l11_opy_ (u"࠭ࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨᒫ"),
      stream=sys.stdout
    )
  return logger
def bstack1llllllll11_opy_():
  global bstack1lllllll11l_opy_
  if os.path.exists(bstack1lllllll11l_opy_):
    os.remove(bstack1lllllll11l_opy_)
def bstack1ll11l11l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll1l1ll_opy_(config, log_level):
  bstack1llllll1ll1_opy_ = log_level
  if bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᒬ") in config and config[bstack1ll1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪᒭ")] in bstack111lll1111_opy_:
    bstack1llllll1ll1_opy_ = bstack111lll1111_opy_[config[bstack1ll1l11_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫᒮ")]]
  if config.get(bstack1ll1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᒯ"), False):
    logging.getLogger().setLevel(bstack1llllll1ll1_opy_)
    return bstack1llllll1ll1_opy_
  global bstack1lllllll11l_opy_
  bstack1ll11l11l1_opy_()
  bstack1llllll11l1_opy_ = logging.Formatter(
    fmt=bstack1ll1l11_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩᒰ"),
    datefmt=bstack1ll1l11_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧᒱ")
  )
  bstack1lllllll1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllllll11l_opy_)
  file_handler.setFormatter(bstack1llllll11l1_opy_)
  bstack1lllllll1ll_opy_.setFormatter(bstack1llllll11l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllllll1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1ll1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨᒲ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllllll1ll_opy_.setLevel(bstack1llllll1ll1_opy_)
  logging.getLogger().addHandler(bstack1lllllll1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1llllll1ll1_opy_
def bstack1llllll1111_opy_(config):
  try:
    bstack1llllll1lll_opy_ = set(bstack111ll1ll11_opy_)
    bstack1lllllll111_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨᒳ")
    with open(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᒴ")) as bstack1llllll11ll_opy_:
      bstack1llllll1l11_opy_ = bstack1llllll11ll_opy_.read()
      bstack1lllllll111_opy_ = re.sub(bstack1ll1l11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪᒵ"), bstack1ll1l11_opy_ (u"ࠪࠫᒶ"), bstack1llllll1l11_opy_, flags=re.M)
      bstack1lllllll111_opy_ = re.sub(
        bstack1ll1l11_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧᒷ") + bstack1ll1l11_opy_ (u"ࠬࢂࠧᒸ").join(bstack1llllll1lll_opy_) + bstack1ll1l11_opy_ (u"࠭ࠩ࠯ࠬࠧࠫᒹ"),
        bstack1ll1l11_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᒺ"),
        bstack1lllllll111_opy_, flags=re.M | re.I
      )
    def bstack1lllllll1l1_opy_(dic):
      bstack1llllllll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1llllll1lll_opy_:
          bstack1llllllll1l_opy_[key] = bstack1ll1l11_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᒻ")
        else:
          if isinstance(value, dict):
            bstack1llllllll1l_opy_[key] = bstack1lllllll1l1_opy_(value)
          else:
            bstack1llllllll1l_opy_[key] = value
      return bstack1llllllll1l_opy_
    bstack1llllllll1l_opy_ = bstack1lllllll1l1_opy_(config)
    return {
      bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬᒼ"): bstack1lllllll111_opy_,
      bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᒽ"): json.dumps(bstack1llllllll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack11llll11l_opy_(config):
  global bstack1lllllll11l_opy_
  try:
    if config.get(bstack1ll1l11_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᒾ"), False):
      return
    uuid = os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᒿ"))
    if not uuid or uuid == bstack1ll1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᓀ"):
      return
    bstack1llllll1l1l_opy_ = [bstack1ll1l11_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᓁ"), bstack1ll1l11_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᓂ"), bstack1ll1l11_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᓃ"), bstack1lllllll11l_opy_]
    bstack1ll11l11l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᓄ") + uuid + bstack1ll1l11_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᓅ"))
    with tarfile.open(output_file, bstack1ll1l11_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᓆ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llllll1l1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1llllll1111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll111l_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll111l_opy_))
    bstack1l11l111l_opy_ = MultipartEncoder(
      fields= {
        bstack1ll1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᓇ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1ll1l11_opy_ (u"ࠧࡳࡤࠪᓈ")), bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᓉ")),
        bstack1ll1l11_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᓊ"): uuid
      }
    )
    response = requests.post(
      bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧᓋ"),
      data=bstack1l11l111l_opy_,
      headers={bstack1ll1l11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᓌ"): bstack1l11l111l_opy_.content_type},
      auth=(config[bstack1ll1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᓍ")], config[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᓎ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭ᓏ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧᓐ") + str(e))
  finally:
    try:
      bstack1llllllll11_opy_()
    except:
      pass