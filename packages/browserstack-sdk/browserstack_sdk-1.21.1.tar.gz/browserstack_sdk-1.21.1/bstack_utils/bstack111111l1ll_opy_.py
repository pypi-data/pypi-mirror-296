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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l11ll1l_opy_
from browserstack_sdk.bstack1ll11ll1_opy_ import bstack1l1ll1l1l_opy_
def _1lllllllll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111111111l_opy_:
    def __init__(self, handler):
        self._111111l11l_opy_ = {}
        self._1111111ll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1ll1l1l_opy_.version()
        if bstack111l11ll1l_opy_(pytest_version, bstack1ll1l11_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᑾ")) >= 0:
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑿ")] = Module._register_setup_function_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒀ")] = Module._register_setup_module_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒁ")] = Class._register_setup_class_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒂ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒃ"))
            Module._register_setup_module_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒄ"))
            Class._register_setup_class_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᒅ"))
            Class._register_setup_method_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒆ"))
        else:
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᒇ")] = Module._inject_setup_function_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒈ")] = Module._inject_setup_module_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᒉ")] = Class._inject_setup_class_fixture
            self._111111l11l_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᒊ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᒋ"))
            Module._inject_setup_module_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒌ"))
            Class._inject_setup_class_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᒍ"))
            Class._inject_setup_method_fixture = self.bstack1llllllllll_opy_(bstack1ll1l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᒎ"))
    def bstack11111111ll_opy_(self, bstack11111111l1_opy_, hook_type):
        meth = getattr(bstack11111111l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111111ll1_opy_[hook_type] = meth
            setattr(bstack11111111l1_opy_, hook_type, self.bstack1111111lll_opy_(hook_type))
    def bstack111111l1l1_opy_(self, instance, bstack1111111l11_opy_):
        if bstack1111111l11_opy_ == bstack1ll1l11_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᒏ"):
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᒐ"))
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᒑ"))
        if bstack1111111l11_opy_ == bstack1ll1l11_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᒒ"):
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᒓ"))
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᒔ"))
        if bstack1111111l11_opy_ == bstack1ll1l11_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᒕ"):
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᒖ"))
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᒗ"))
        if bstack1111111l11_opy_ == bstack1ll1l11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᒘ"):
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᒙ"))
            self.bstack11111111ll_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᒚ"))
    @staticmethod
    def bstack111111l111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᒛ"), bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᒜ")]:
            _1lllllllll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111111lll_opy_(self, hook_type):
        def bstack111111ll11_opy_(arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᒝ"))
            result = None
            exception = None
            try:
                self.bstack111111l111_opy_(hook_type, self._1111111ll1_opy_[hook_type], (arg,))
                result = Result(result=bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒞ"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒟ"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᒠ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᒡ"), result)
        def bstack1111111111_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᒢ"))
            result = None
            exception = None
            try:
                self.bstack111111l111_opy_(hook_type, self._1111111ll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᒣ"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒤ"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᒥ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᒦ"), result)
        if hook_type in [bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᒧ"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᒨ")]:
            return bstack1111111111_opy_
        return bstack111111ll11_opy_
    def bstack1llllllllll_opy_(self, bstack1111111l11_opy_):
        def bstack1111111l1l_opy_(this, *args, **kwargs):
            self.bstack111111l1l1_opy_(this, bstack1111111l11_opy_)
            self._111111l11l_opy_[bstack1111111l11_opy_](this, *args, **kwargs)
        return bstack1111111l1l_opy_