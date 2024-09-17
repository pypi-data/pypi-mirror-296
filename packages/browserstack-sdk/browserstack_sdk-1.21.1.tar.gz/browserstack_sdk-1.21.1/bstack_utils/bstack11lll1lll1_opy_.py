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
from uuid import uuid4
from bstack_utils.helper import bstack11ll111l_opy_, bstack1111l1l111_opy_
from bstack_utils.bstack11l1lll11_opy_ import bstack1lll11lll1l_opy_
class bstack11l1lll111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lll1ll1l_opy_=None, framework=None, tags=[], scope=[], bstack1ll1lllll11_opy_=None, bstack1ll1llll11l_opy_=True, bstack1ll1lll111l_opy_=None, bstack1lll1l111l_opy_=None, result=None, duration=None, bstack11ll1llll1_opy_=None, meta={}):
        self.bstack11ll1llll1_opy_ = bstack11ll1llll1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1llll11l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lll1ll1l_opy_ = bstack11lll1ll1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1lllll11_opy_ = bstack1ll1lllll11_opy_
        self.bstack1ll1lll111l_opy_ = bstack1ll1lll111l_opy_
        self.bstack1lll1l111l_opy_ = bstack1lll1l111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l1lll1l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11llll1l11_opy_(self, meta):
        self.meta = meta
    def bstack1ll1lll1lll_opy_(self):
        bstack1ll1llll1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᘏ"): bstack1ll1llll1ll_opy_,
            bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᘐ"): bstack1ll1llll1ll_opy_,
            bstack1ll1l11_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᘑ"): bstack1ll1llll1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll1l11_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᘒ") + key)
            setattr(self, key, val)
    def bstack1ll1ll1ll1l_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᘓ"): self.name,
            bstack1ll1l11_opy_ (u"ࠪࡦࡴࡪࡹࠨᘔ"): {
                bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᘕ"): bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᘖ"),
                bstack1ll1l11_opy_ (u"࠭ࡣࡰࡦࡨࠫᘗ"): self.code
            },
            bstack1ll1l11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᘘ"): self.scope,
            bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᘙ"): self.tags,
            bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᘚ"): self.framework,
            bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘛ"): self.bstack11lll1ll1l_opy_
        }
    def bstack1ll1lll11ll_opy_(self):
        return {
         bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᘜ"): self.meta
        }
    def bstack1ll1llll111_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᘝ"): {
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᘞ"): self.bstack1ll1lllll11_opy_
            }
        }
    def bstack1ll1lll1l11_opy_(self, bstack1ll1lll1111_opy_, details):
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪᘟ")] == bstack1ll1lll1111_opy_, self.meta[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘠ")]), None)
        step.update(details)
    def bstack1ll1ll1l1_opy_(self, bstack1ll1lll1111_opy_):
        step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬᘡ")] == bstack1ll1lll1111_opy_, self.meta[bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᘢ")]), None)
        step.update({
            bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘣ"): bstack11ll111l_opy_()
        })
    def bstack11llll1lll_opy_(self, bstack1ll1lll1111_opy_, result, duration=None):
        bstack1ll1lll111l_opy_ = bstack11ll111l_opy_()
        if bstack1ll1lll1111_opy_ is not None and self.meta.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᘤ")):
            step = next(filter(lambda st: st[bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩᘥ")] == bstack1ll1lll1111_opy_, self.meta[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᘦ")]), None)
            step.update({
                bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᘧ"): bstack1ll1lll111l_opy_,
                bstack1ll1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᘨ"): duration if duration else bstack1111l1l111_opy_(step[bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘩ")], bstack1ll1lll111l_opy_),
                bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᘪ"): result.result,
                bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᘫ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1ll1lll1_opy_):
        if self.meta.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᘬ")):
            self.meta[bstack1ll1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᘭ")].append(bstack1ll1ll1lll1_opy_)
        else:
            self.meta[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘮ")] = [ bstack1ll1ll1lll1_opy_ ]
    def bstack1ll1llllll1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘯ"): self.bstack11l1lll1l1_opy_(),
            **self.bstack1ll1ll1ll1l_opy_(),
            **self.bstack1ll1lll1lll_opy_(),
            **self.bstack1ll1lll11ll_opy_()
        }
    def bstack1ll1lll11l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘰ"): self.bstack1ll1lll111l_opy_,
            bstack1ll1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᘱ"): self.duration,
            bstack1ll1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᘲ"): self.result.result
        }
        if data[bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘳ")] == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᘴ"):
            data[bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᘵ")] = self.result.bstack11l1l11111_opy_()
            data[bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᘶ")] = [{bstack1ll1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᘷ"): self.result.bstack11111ll1l1_opy_()}]
        return data
    def bstack1ll1lll1ll1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᘸ"): self.bstack11l1lll1l1_opy_(),
            **self.bstack1ll1ll1ll1l_opy_(),
            **self.bstack1ll1lll1lll_opy_(),
            **self.bstack1ll1lll11l1_opy_(),
            **self.bstack1ll1lll11ll_opy_()
        }
    def bstack11lll111l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll1l11_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᘹ") in event:
            return self.bstack1ll1llllll1_opy_()
        elif bstack1ll1l11_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᘺ") in event:
            return self.bstack1ll1lll1ll1_opy_()
    def bstack11ll1ll11l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1lll111l_opy_ = time if time else bstack11ll111l_opy_()
        self.duration = duration if duration else bstack1111l1l111_opy_(self.bstack11lll1ll1l_opy_, self.bstack1ll1lll111l_opy_)
        if result:
            self.result = result
class bstack11lllll11l_opy_(bstack11l1lll111_opy_):
    def __init__(self, hooks=[], bstack11ll11llll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll11llll_opy_ = bstack11ll11llll_opy_
        super().__init__(*args, **kwargs, bstack1lll1l111l_opy_=bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࠬᘻ"))
    @classmethod
    def bstack1ll1ll1llll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫᘼ"): id(step),
                bstack1ll1l11_opy_ (u"ࠩࡷࡩࡽࡺࠧᘽ"): step.name,
                bstack1ll1l11_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᘾ"): step.keyword,
            })
        return bstack11lllll11l_opy_(
            **kwargs,
            meta={
                bstack1ll1l11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᘿ"): {
                    bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙀ"): feature.name,
                    bstack1ll1l11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᙁ"): feature.filename,
                    bstack1ll1l11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᙂ"): feature.description
                },
                bstack1ll1l11_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᙃ"): {
                    bstack1ll1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᙄ"): scenario.name
                },
                bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᙅ"): steps,
                bstack1ll1l11_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᙆ"): bstack1lll11lll1l_opy_(test)
            }
        )
    def bstack1ll1ll1ll11_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙇ"): self.hooks
        }
    def bstack1ll1lll1l1l_opy_(self):
        if self.bstack11ll11llll_opy_:
            return {
                bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᙈ"): self.bstack11ll11llll_opy_
            }
        return {}
    def bstack1ll1lll1ll1_opy_(self):
        return {
            **super().bstack1ll1lll1ll1_opy_(),
            **self.bstack1ll1ll1ll11_opy_()
        }
    def bstack1ll1llllll1_opy_(self):
        return {
            **super().bstack1ll1llllll1_opy_(),
            **self.bstack1ll1lll1l1l_opy_()
        }
    def bstack11ll1ll11l_opy_(self):
        return bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᙉ")
class bstack11llllll11_opy_(bstack11l1lll111_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1lllll1l_opy_ = None
        super().__init__(*args, **kwargs, bstack1lll1l111l_opy_=bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᙊ"))
    def bstack11l1ll1lll_opy_(self):
        return self.hook_type
    def bstack1ll1llll1l1_opy_(self):
        return {
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᙋ"): self.hook_type
        }
    def bstack1ll1lll1ll1_opy_(self):
        return {
            **super().bstack1ll1lll1ll1_opy_(),
            **self.bstack1ll1llll1l1_opy_()
        }
    def bstack1ll1llllll1_opy_(self):
        return {
            **super().bstack1ll1llllll1_opy_(),
            bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᙌ"): self.bstack1ll1lllll1l_opy_,
            **self.bstack1ll1llll1l1_opy_()
        }
    def bstack11ll1ll11l_opy_(self):
        return bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ᙍ")
    def bstack11lll1l1l1_opy_(self, bstack1ll1lllll1l_opy_):
        self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_