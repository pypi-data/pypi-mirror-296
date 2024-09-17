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
class bstack111llll11l_opy_(object):
  bstack1l1ll11l_opy_ = os.path.join(os.path.expanduser(bstack1ll1l11_opy_ (u"ࠨࢀࠪྥ")), bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩྦ"))
  bstack111llll1ll_opy_ = os.path.join(bstack1l1ll11l_opy_, bstack1ll1l11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪྦྷ"))
  bstack111llll1l1_opy_ = None
  perform_scan = None
  bstack1111lll1l_opy_ = None
  bstack1l11ll11l_opy_ = None
  bstack11l111ll11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭ྨ")):
      cls.instance = super(bstack111llll11l_opy_, cls).__new__(cls)
      cls.instance.bstack111lll1lll_opy_()
    return cls.instance
  def bstack111lll1lll_opy_(self):
    try:
      with open(self.bstack111llll1ll_opy_, bstack1ll1l11_opy_ (u"ࠬࡸࠧྩ")) as bstack111l11ll1_opy_:
        bstack111llll111_opy_ = bstack111l11ll1_opy_.read()
        data = json.loads(bstack111llll111_opy_)
        if bstack1ll1l11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨྪ") in data:
          self.bstack11l11l1l11_opy_(data[bstack1ll1l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩྫ")])
        if bstack1ll1l11_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩྫྷ") in data:
          self.bstack11l111l11l_opy_(data[bstack1ll1l11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪྭ")])
    except:
      pass
  def bstack11l111l11l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1ll1l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨྮ")]
      self.bstack1111lll1l_opy_ = scripts[bstack1ll1l11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨྯ")]
      self.bstack1l11ll11l_opy_ = scripts[bstack1ll1l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩྰ")]
      self.bstack11l111ll11_opy_ = scripts[bstack1ll1l11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫྱ")]
  def bstack11l11l1l11_opy_(self, bstack111llll1l1_opy_):
    if bstack111llll1l1_opy_ != None and len(bstack111llll1l1_opy_) != 0:
      self.bstack111llll1l1_opy_ = bstack111llll1l1_opy_
  def store(self):
    try:
      with open(self.bstack111llll1ll_opy_, bstack1ll1l11_opy_ (u"ࠧࡸࠩྲ")) as file:
        json.dump({
          bstack1ll1l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥླ"): self.bstack111llll1l1_opy_,
          bstack1ll1l11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥྴ"): {
            bstack1ll1l11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣྵ"): self.perform_scan,
            bstack1ll1l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣྶ"): self.bstack1111lll1l_opy_,
            bstack1ll1l11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤྷ"): self.bstack1l11ll11l_opy_,
            bstack1ll1l11_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦྸ"): self.bstack11l111ll11_opy_
          }
        }, file)
    except:
      pass
  def bstack1ll1lll1_opy_(self, bstack111lllll11_opy_):
    try:
      return any(command.get(bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬྐྵ")) == bstack111lllll11_opy_ for command in self.bstack111llll1l1_opy_)
    except:
      return False
bstack1l1ll1l1l1_opy_ = bstack111llll11l_opy_()