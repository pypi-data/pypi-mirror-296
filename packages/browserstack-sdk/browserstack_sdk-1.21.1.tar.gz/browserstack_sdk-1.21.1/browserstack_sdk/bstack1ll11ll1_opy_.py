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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from browserstack_sdk.bstack1l11l11l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll1llll1l_opy_
class bstack1l1ll1l1l_opy_:
    def __init__(self, args, logger, bstack11l1l1ll11_opy_, bstack11l1l11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1ll11_opy_ = bstack11l1l1ll11_opy_
        self.bstack11l1l11l11_opy_ = bstack11l1l11l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll111ll_opy_ = []
        self.bstack11l1l1l11l_opy_ = None
        self.bstack1ll11lll1_opy_ = []
        self.bstack11l1l1111l_opy_ = self.bstack1l1111ll11_opy_()
        self.bstack1lll1lll1_opy_ = -1
    def bstack1l11l1ll_opy_(self, bstack11l1l1llll_opy_):
        self.parse_args()
        self.bstack11l1l1l1ll_opy_()
        self.bstack11l1l11l1l_opy_(bstack11l1l1llll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1ll1111_opy_():
        import importlib
        if getattr(importlib, bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧ໔"), False):
            bstack11l1l11ll1_opy_ = importlib.find_loader(bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ໕"))
        else:
            bstack11l1l11ll1_opy_ = importlib.util.find_spec(bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭໖"))
    def bstack11l1l1l111_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll1lll1_opy_ = -1
        if self.bstack11l1l11l11_opy_ and bstack1ll1l11_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ໗") in self.bstack11l1l1ll11_opy_:
            self.bstack1lll1lll1_opy_ = int(self.bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭໘")])
        try:
            bstack11l1ll111l_opy_ = [bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ໙"), bstack1ll1l11_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ໚"), bstack1ll1l11_opy_ (u"ࠩ࠰ࡴࠬ໛")]
            if self.bstack1lll1lll1_opy_ >= 0:
                bstack11l1ll111l_opy_.extend([bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫໜ"), bstack1ll1l11_opy_ (u"ࠫ࠲ࡴࠧໝ")])
            for arg in bstack11l1ll111l_opy_:
                self.bstack11l1l1l111_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1l1l1ll_opy_(self):
        bstack11l1l1l11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
        return bstack11l1l1l11l_opy_
    def bstack1ll1111lll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1ll1111_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1ll1llll1l_opy_)
    def bstack11l1l11l1l_opy_(self, bstack11l1l1llll_opy_):
        bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
        if bstack11l1l1llll_opy_:
            self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩໞ"))
            self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"࠭ࡔࡳࡷࡨࠫໟ"))
        if bstack1lll11ll_opy_.bstack11l1l111ll_opy_():
            self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭໠"))
            self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠨࡖࡵࡹࡪ࠭໡"))
        self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠩ࠰ࡴࠬ໢"))
        self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ໣"))
        self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭໤"))
        self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ໥"))
        if self.bstack1lll1lll1_opy_ > 1:
            self.bstack11l1l1l11l_opy_.append(bstack1ll1l11_opy_ (u"࠭࠭࡯ࠩ໦"))
            self.bstack11l1l1l11l_opy_.append(str(self.bstack1lll1lll1_opy_))
    def bstack11l1l1lll1_opy_(self):
        bstack1ll11lll1_opy_ = []
        for spec in self.bstack1lll111ll_opy_:
            bstack1l11lll1l_opy_ = [spec]
            bstack1l11lll1l_opy_ += self.bstack11l1l1l11l_opy_
            bstack1ll11lll1_opy_.append(bstack1l11lll1l_opy_)
        self.bstack1ll11lll1_opy_ = bstack1ll11lll1_opy_
        return bstack1ll11lll1_opy_
    def bstack1l1111ll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l1l1111l_opy_ = True
            return True
        except Exception as e:
            self.bstack11l1l1111l_opy_ = False
        return self.bstack11l1l1111l_opy_
    def bstack11lll1l1_opy_(self, bstack11l1l1ll1l_opy_, bstack1l11l1ll_opy_):
        bstack1l11l1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ໧")] = self.bstack11l1l1ll11_opy_
        multiprocessing.set_start_method(bstack1ll1l11_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ໨"))
        bstack1l111llll_opy_ = []
        manager = multiprocessing.Manager()
        bstack11llllll1_opy_ = manager.list()
        if bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ໩") in self.bstack11l1l1ll11_opy_:
            for index, platform in enumerate(self.bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭໪")]):
                bstack1l111llll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1l1ll1l_opy_,
                                                            args=(self.bstack11l1l1l11l_opy_, bstack1l11l1ll_opy_, bstack11llllll1_opy_)))
            bstack11l1l1l1l1_opy_ = len(self.bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ໫")])
        else:
            bstack1l111llll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1l1ll1l_opy_,
                                                        args=(self.bstack11l1l1l11l_opy_, bstack1l11l1ll_opy_, bstack11llllll1_opy_)))
            bstack11l1l1l1l1_opy_ = 1
        i = 0
        for t in bstack1l111llll_opy_:
            os.environ[bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ໬")] = str(i)
            if bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ໭") in self.bstack11l1l1ll11_opy_:
                os.environ[bstack1ll1l11_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ໮")] = json.dumps(self.bstack11l1l1ll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ໯")][i % bstack11l1l1l1l1_opy_])
            i += 1
            t.start()
        for t in bstack1l111llll_opy_:
            t.join()
        return list(bstack11llllll1_opy_)
    @staticmethod
    def bstack1lll11ll1l_opy_(driver, bstack11l1l11lll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭໰"), None)
        if item and getattr(item, bstack1ll1l11_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬ໱"), None) and not getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭໲"), False):
            logger.info(
                bstack1ll1l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦ໳"))
            bstack11l1l111l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1ll111l_opy_.bstack1l11ll11ll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)