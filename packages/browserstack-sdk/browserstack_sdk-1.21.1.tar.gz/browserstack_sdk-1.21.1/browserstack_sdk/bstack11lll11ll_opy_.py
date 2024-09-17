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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11lll1lll1_opy_ import bstack11llllll11_opy_, bstack11lllll11l_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.helper import bstack1ll1l1l1_opy_, bstack11ll111l_opy_, Result
from bstack_utils.bstack1lll1111ll_opy_ import bstack1ll11l11l_opy_
from bstack_utils.capture import bstack11llll1l1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11lll11ll_opy_:
    def __init__(self):
        self.bstack11lll11ll1_opy_ = bstack11llll1l1l_opy_(self.bstack11lllll1ll_opy_)
        self.tests = {}
    @staticmethod
    def bstack11lllll1ll_opy_(log):
        if not (log[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨශ")] and log[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩෂ")].strip()):
            return
        active = bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_()
        log = {
            bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨස"): log[bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩහ")],
            bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧළ"): bstack11ll111l_opy_(),
            bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ"): log[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෇")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ෈")] == bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭෉"):
                log[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ්ࠩ")] = active[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ෋")]
            elif active[bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ෌")] == bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪ෍"):
                log[bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭෎")] = active[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧා")]
        bstack1ll11l11l_opy_.bstack11llll11l_opy_([log])
    def start_test(self, name, attrs):
        bstack11llll11l1_opy_ = uuid4().__str__()
        self.tests[bstack11llll11l1_opy_] = {}
        self.bstack11lll11ll1_opy_.start()
        bstack11lll1lll1_opy_ = bstack11lllll11l_opy_(
            name=name,
            uuid=bstack11llll11l1_opy_,
            bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
            file_path=attrs.filename,
            result=bstack1ll1l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤැ"),
            framework=bstack1ll1l11_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩෑ"),
            scope=[attrs.feature.name],
            meta={},
            tags=attrs.tags
        )
        self.tests[bstack11llll11l1_opy_][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ි")] = bstack11lll1lll1_opy_
        threading.current_thread().current_test_uuid = bstack11llll11l1_opy_
        bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬී"), bstack11lll1lll1_opy_)
    def end_test(self, attrs):
        bstack11llll1ll1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥු"): attrs.feature.name,
            bstack1ll1l11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ෕"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11lll1lll1_opy_ = self.tests[current_test_uuid][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪූ")]
        meta = {
            bstack1ll1l11_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ෗"): bstack11llll1ll1_opy_,
            bstack1ll1l11_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣෘ"): bstack11lll1lll1_opy_.meta.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩෙ"), []),
            bstack1ll1l11_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨේ"): {
                bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥෛ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11lll1lll1_opy_.bstack11llll1l11_opy_(meta)
        bstack11llll111l_opy_, exception = self._11lll1l111_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll11lll_opy_=[bstack11llll111l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩො")].stop(time=bstack11ll111l_opy_(), duration=int(attrs.duration)*1000, result=bstack11lll1ll11_opy_)
        bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩෝ"), self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫෞ")])
    def bstack1ll1ll1l1_opy_(self, attrs):
        bstack11lll1llll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬෟ"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ෠"): attrs.keyword,
            bstack1ll1l11_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ෡"): [],
            bstack1ll1l11_opy_ (u"ࠬࡺࡥࡹࡶࠪ෢"): attrs.name,
            bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ෣"): bstack11ll111l_opy_(),
            bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ෤"): bstack1ll1l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ෥"),
            bstack1ll1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ෦"): bstack1ll1l11_opy_ (u"ࠪࠫ෧")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ෨")].add_step(bstack11lll1llll_opy_)
        threading.current_thread().current_step_uuid = bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ෩")]
    def bstack1l1111llll_opy_(self, attrs):
        current_test_id = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ෪"), None)
        current_step_uuid = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫ෫"), None)
        bstack11llll111l_opy_, exception = self._11lll1l111_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll11lll_opy_=[bstack11llll111l_opy_])
        self.tests[current_test_id][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෬")].bstack11llll1lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11lll1ll11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l11l111_opy_(self, name, attrs):
        bstack11lllll111_opy_ = uuid4().__str__()
        self.tests[bstack11lllll111_opy_] = {}
        self.bstack11lll11ll1_opy_.start()
        scopes = []
        if name in [bstack1ll1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ෭"), bstack1ll1l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ෮")]:
            file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
            scopes = [attrs.config.environment_file]
        elif name in [bstack1ll1l11_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ෯"), bstack1ll1l11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ෰")]:
            file_path = attrs.filename
            scopes = [attrs.name]
        else:
            file_path = attrs.filename
            scopes = [attrs.feature.name]
        hook_data = bstack11llllll11_opy_(
            name=name,
            uuid=bstack11lllll111_opy_,
            bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
            file_path=file_path,
            framework=bstack1ll1l11_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨ෱"),
            scope=scopes,
            result=bstack1ll1l11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣෲ"),
            hook_type=bstack11lllll1l1_opy_[name]
        )
        self.tests[bstack11lllll111_opy_][bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦෳ")] = hook_data
        current_test_id = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨ෴"), None)
        if current_test_id:
            hook_data.bstack11lll1l1l1_opy_(current_test_id)
        if name == bstack1ll1l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ෵"):
            threading.current_thread().before_all_hook_uuid = bstack11lllll111_opy_
        threading.current_thread().current_hook_uuid = bstack11lllll111_opy_
        bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧ෶"), hook_data)
    def bstack1l111l1l11_opy_(self, attrs):
        bstack11llll11ll_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ෷"), None)
        hook_data = self.tests[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෸")]
        status = bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ෹")
        exception = None
        bstack11llll111l_opy_ = None
        if hook_data.name == bstack1ll1l11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ෺"):
            self.bstack11lll11ll1_opy_.reset()
            bstack11llll1111_opy_ = self.tests[bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ෻"), None)][bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෼")].result.result
            if bstack11llll1111_opy_ == bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ෽"):
                if attrs.hook_failures == 1:
                    status = bstack1ll1l11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ෾")
                elif attrs.hook_failures == 2:
                    status = bstack1ll1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ෿")
            elif attrs.bstack11lll1l1ll_opy_:
                status = bstack1ll1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ฀")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬก") and attrs.hook_failures == 1:
                status = bstack1ll1l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤข")
            elif hasattr(attrs, bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪฃ")) and attrs.error_message:
                status = bstack1ll1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦค")
            bstack11llll111l_opy_, exception = self._11lll1l111_opy_(attrs)
        bstack11lll1ll11_opy_ = Result(result=status, exception=exception, bstack11lll11lll_opy_=[bstack11llll111l_opy_])
        hook_data.stop(time=bstack11ll111l_opy_(), duration=0, result=bstack11lll1ll11_opy_)
        bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧฅ"), self.tests[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩฆ")])
        threading.current_thread().current_hook_uuid = None
    def _11lll1l111_opy_(self, attrs):
        try:
            import traceback
            bstack11ll11l11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11llll111l_opy_ = bstack11ll11l11_opy_[-1] if bstack11ll11l11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦง"))
            bstack11llll111l_opy_ = None
            exception = None
        return bstack11llll111l_opy_, exception