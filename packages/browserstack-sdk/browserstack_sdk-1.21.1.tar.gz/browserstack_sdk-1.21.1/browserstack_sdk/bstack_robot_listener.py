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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11l1llllll_opy_ import RobotHandler
from bstack_utils.capture import bstack11llll1l1l_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11l1lll111_opy_, bstack11llllll11_opy_, bstack11lllll11l_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack1ll11l11l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1l1l1_opy_, bstack11ll111l_opy_, Result, \
    bstack11ll111l11_opy_, bstack11ll1l1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬจ"): [],
        bstack1ll1l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨฉ"): [],
        bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧช"): []
    }
    bstack11ll1lllll_opy_ = []
    bstack11ll1l1lll_opy_ = []
    @staticmethod
    def bstack11lllll1ll_opy_(log):
        if not (log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬซ")] and log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ฌ")].strip()):
            return
        active = bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_()
        log = {
            bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬญ"): log[bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ฎ")],
            bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫฏ"): bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫฐ"),
            bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫฑ"): log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬฒ")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪณ")] == bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫด"):
                log[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧต")] = active[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨถ")]
            elif active[bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧท")] == bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨธ"):
                log[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫน")] = active[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬบ")]
        bstack1ll11l11l_opy_.bstack11llll11l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll1lll1l_opy_ = None
        self._11l1lll11l_opy_ = None
        self._11ll1ll1l1_opy_ = OrderedDict()
        self.bstack11lll11ll1_opy_ = bstack11llll1l1l_opy_(self.bstack11lllll1ll_opy_)
    @bstack11ll111l11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11l1llll1l_opy_()
        if not self._11ll1ll1l1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩป")), None):
            self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪผ"))] = {}
        bstack11ll111111_opy_ = bstack11lllll11l_opy_(
                bstack11ll1llll1_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫฝ")),
                name=name,
                bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩพ")], start=os.getcwd()) if attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪฟ")) != bstack1ll1l11_opy_ (u"ࠫࠬภ") else bstack1ll1l11_opy_ (u"ࠬ࠭ม"),
                framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬย")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪร"), None)
        self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫฤ"))][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬล")] = bstack11ll111111_opy_
    @bstack11ll111l11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11ll1lll11_opy_()
        self._11ll1l1ll1_opy_(messages)
        for bstack11l1lll1ll_opy_ in self.bstack11ll1lllll_opy_:
            bstack11l1lll1ll_opy_[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬฦ")][bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪว")].extend(self.store[bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫศ")])
            bstack1ll11l11l_opy_.bstack11ll11l11l_opy_(bstack11l1lll1ll_opy_)
        self.bstack11ll1lllll_opy_ = []
        self.store[bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬษ")] = []
    @bstack11ll111l11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lll11ll1_opy_.start()
        if not self._11ll1ll1l1_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪส")), None):
            self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫห"))] = {}
        driver = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨฬ"), None)
        bstack11lll1lll1_opy_ = bstack11lllll11l_opy_(
            bstack11ll1llll1_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭อ")),
            name=name,
            bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫฮ")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1ll1ll1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬฯ"), None)),
            framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬะ"),
            tags=attrs[bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬั")],
            hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧา")],
            bstack11ll11llll_opy_=bstack1ll11l11l_opy_.bstack11ll11ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1l11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦำ").format(bstack1ll1l11_opy_ (u"ࠥࠤࠧิ").join(attrs[bstack1ll1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩี")]), name) if attrs[bstack1ll1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪึ")] else name
        )
        self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩื"))][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣุࠪ")] = bstack11lll1lll1_opy_
        threading.current_thread().current_test_uuid = bstack11lll1lll1_opy_.bstack11l1lll1l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧูࠫ"), None)
        self.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦฺࠪ"), bstack11lll1lll1_opy_)
    @bstack11ll111l11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lll11ll1_opy_.reset()
        bstack11ll11l1ll_opy_ = bstack11ll1111ll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ฻")), bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ฼"))
        self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ฽"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ฾")].stop(time=bstack11ll111l_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ฿"), bstack1ll1l11_opy_ (u"ࠨ࠲ࠪเ"))), result=Result(result=bstack11ll11l1ll_opy_, exception=attrs.get(bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪแ")), bstack11lll11lll_opy_=[attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫโ"))]))
        self.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ใ"), self._11ll1ll1l1_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨไ"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩๅ")], True)
        self.store[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫๆ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11ll111l11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11l1llll1l_opy_()
        current_test_id = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ็"), None)
        bstack11l1ll11ll_opy_ = current_test_id if bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧ่ࠫ"), None) else bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ้࠭"), None)
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦ๊ࠩ"), bstack1ll1l11_opy_ (u"๋ࠬ࠭")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ์"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩํ")]:
            hook_type = bstack11ll11l1l1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭๎")), bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭๏"), None))
            hook_name = bstack1ll1l11_opy_ (u"ࠪࡿࢂ࠭๐").format(attrs.get(bstack1ll1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ๑"), bstack1ll1l11_opy_ (u"ࠬ࠭๒")))
            if hook_type in [bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ๓"), bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ๔")]:
                hook_name = bstack1ll1l11_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩ๕").format(bstack11lll11l11_opy_.get(hook_type), attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ๖"), bstack1ll1l11_opy_ (u"ࠪࠫ๗")))
            bstack11ll11ll11_opy_ = bstack11llllll11_opy_(
                bstack11ll1llll1_opy_=bstack11l1ll11ll_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭๘") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ๙"), bstack1ll1l11_opy_ (u"࠭ࠧ๚")).lower(),
                name=hook_name,
                bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ๛")), start=os.getcwd()),
                framework=bstack1ll1l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ๜"),
                tags=attrs[bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ๝")],
                scope=RobotHandler.bstack11l1ll1ll1_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ๞"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11ll11ll11_opy_.bstack11l1lll1l1_opy_()
            threading.current_thread().current_hook_id = bstack11l1ll11ll_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭๟") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ๠"), bstack1ll1l11_opy_ (u"࠭ࠧ๡")).lower()
            self.store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ๢")] = [bstack11ll11ll11_opy_.bstack11l1lll1l1_opy_()]
            if bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ๣"), None):
                self.store[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭๤")].append(bstack11ll11ll11_opy_.bstack11l1lll1l1_opy_())
            else:
                self.store[bstack1ll1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ๥")].append(bstack11ll11ll11_opy_.bstack11l1lll1l1_opy_())
            if bstack11l1ll11ll_opy_:
                self._11ll1ll1l1_opy_[bstack11l1ll11ll_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭๦") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ๧"), bstack1ll1l11_opy_ (u"࠭ࠧ๨")).lower()] = { bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ๩"): bstack11ll11ll11_opy_ }
            bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ๪"), bstack11ll11ll11_opy_)
        else:
            bstack11lll1llll_opy_ = {
                bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬ๫"): uuid4().__str__(),
                bstack1ll1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨ๬"): bstack1ll1l11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ๭").format(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ๮")), attrs.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ๯"), bstack1ll1l11_opy_ (u"ࠧࠨ๰"))) if attrs.get(bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭๱"), []) else attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ๲")),
                bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ๳"): attrs.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩ๴"), []),
                bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ๵"): bstack11ll111l_opy_(),
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭๶"): bstack1ll1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ๷"),
                bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭๸"): attrs.get(bstack1ll1l11_opy_ (u"ࠩࡧࡳࡨ࠭๹"), bstack1ll1l11_opy_ (u"ࠪࠫ๺"))
            }
            if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ๻"), bstack1ll1l11_opy_ (u"ࠬ࠭๼")) != bstack1ll1l11_opy_ (u"࠭ࠧ๽"):
                bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ๾")] = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ๿"))
            if not self.bstack11ll1l1lll_opy_:
                self._11ll1ll1l1_opy_[self._11ll1l111l_opy_()][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ຀")].add_step(bstack11lll1llll_opy_)
                threading.current_thread().current_step_uuid = bstack11lll1llll_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ກ")]
            self.bstack11ll1l1lll_opy_.append(bstack11lll1llll_opy_)
    @bstack11ll111l11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11ll1lll11_opy_()
        self._11ll1l1ll1_opy_(messages)
        current_test_id = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ຂ"), None)
        bstack11l1ll11ll_opy_ = current_test_id if current_test_id else bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ຃"), None)
        bstack11ll1l1l1l_opy_ = bstack11ll1111ll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ຄ")), bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ຅"))
        bstack11l1ll11l1_opy_ = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຆ"))
        if bstack11ll1l1l1l_opy_ != bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪງ") and not attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຈ")) and self._11ll1lll1l_opy_:
            bstack11l1ll11l1_opy_ = self._11ll1lll1l_opy_
        bstack11lll1ll11_opy_ = Result(result=bstack11ll1l1l1l_opy_, exception=bstack11l1ll11l1_opy_, bstack11lll11lll_opy_=[bstack11l1ll11l1_opy_])
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩຉ"), bstack1ll1l11_opy_ (u"ࠬ࠭ຊ")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ຋"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩຌ")]:
            bstack11l1ll11ll_opy_ = current_test_id if current_test_id else bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫຍ"), None)
            if bstack11l1ll11ll_opy_:
                bstack11llll11ll_opy_ = bstack11l1ll11ll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠰ࠦຎ") + attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨຏ"), bstack1ll1l11_opy_ (u"ࠫࠬຐ")).lower()
                self._11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨຑ")].stop(time=bstack11ll111l_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫຒ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩຓ"))), result=bstack11lll1ll11_opy_)
                bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪດ"), self._11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬຕ")])
        else:
            bstack11l1ll11ll_opy_ = current_test_id if current_test_id else bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬຖ"), None)
            if bstack11l1ll11ll_opy_ and len(self.bstack11ll1l1lll_opy_) == 1:
                current_step_uuid = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨທ"), None)
                self._11ll1ll1l1_opy_[bstack11l1ll11ll_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨຘ")].bstack11llll1lll_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫນ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩບ"))), result=bstack11lll1ll11_opy_)
            else:
                self.bstack11lll11111_opy_(attrs)
            self.bstack11ll1l1lll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡱࡱ࠭ປ"), bstack1ll1l11_opy_ (u"ࠩࡱࡳࠬຜ")) == bstack1ll1l11_opy_ (u"ࠪࡽࡪࡹࠧຝ"):
                return
            self.messages.push(message)
            bstack11ll111l1l_opy_ = []
            if bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_():
                bstack11ll111l1l_opy_.append({
                    bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧພ"): bstack11ll111l_opy_(),
                    bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຟ"): message.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຠ")),
                    bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ມ"): message.get(bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧຢ")),
                    **bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_()
                })
                if len(bstack11ll111l1l_opy_) > 0:
                    bstack1ll11l11l_opy_.bstack11llll11l_opy_(bstack11ll111l1l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll11l11l_opy_.bstack11l1lllll1_opy_()
    def bstack11lll11111_opy_(self, bstack11ll11lll1_opy_):
        if not bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_():
            return
        kwname = bstack1ll1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨຣ").format(bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ຤")), bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩລ"), bstack1ll1l11_opy_ (u"ࠬ࠭຦"))) if bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫວ"), []) else bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧຨ"))
        error_message = bstack1ll1l11_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢຩ").format(kwname, bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩສ")), str(bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຫ"))))
        bstack11ll1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥຬ").format(kwname, bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬອ")))
        bstack11lll1111l_opy_ = error_message if bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຮ")) else bstack11ll1l1111_opy_
        bstack11l1llll11_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪຯ"): self.bstack11ll1l1lll_opy_[-1].get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬະ"), bstack11ll111l_opy_()),
            bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪັ"): bstack11lll1111l_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩາ"): bstack1ll1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪຳ") if bstack11ll11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬິ")) == bstack1ll1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫີ") else bstack1ll1l11_opy_ (u"ࠧࡊࡐࡉࡓࠬຶ"),
            **bstack11ll1ll1l_opy_.bstack11lll11l1l_opy_()
        }
        bstack1ll11l11l_opy_.bstack11llll11l_opy_([bstack11l1llll11_opy_])
    def _11ll1l111l_opy_(self):
        for bstack11ll1llll1_opy_ in reversed(self._11ll1ll1l1_opy_):
            bstack11ll11l111_opy_ = bstack11ll1llll1_opy_
            data = self._11ll1ll1l1_opy_[bstack11ll1llll1_opy_][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫື")]
            if isinstance(data, bstack11llllll11_opy_):
                if not bstack1ll1l11_opy_ (u"ࠩࡈࡅࡈࡎຸࠧ") in data.bstack11l1ll1lll_opy_():
                    return bstack11ll11l111_opy_
            else:
                return bstack11ll11l111_opy_
    def _11ll1l1ll1_opy_(self, messages):
        try:
            bstack11ll11111l_opy_ = BuiltIn().get_variable_value(bstack1ll1l11_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤູ")) in (bstack11lll111ll_opy_.DEBUG, bstack11lll111ll_opy_.TRACE)
            for message, bstack11l1ll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩ຺ࠬ"))
                level = message.get(bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫົ"))
                if level == bstack11lll111ll_opy_.FAIL:
                    self._11ll1lll1l_opy_ = name or self._11ll1lll1l_opy_
                    self._11l1lll11l_opy_ = bstack11l1ll1l11_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢຼ")) if bstack11ll11111l_opy_ and bstack11l1ll1l11_opy_ else self._11l1lll11l_opy_
        except:
            pass
    @classmethod
    def bstack11lll1l11l_opy_(self, event: str, bstack11ll111ll1_opy_: bstack11l1lll111_opy_, bstack11ll1l11ll_opy_=False):
        if event == bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩຽ"):
            bstack11ll111ll1_opy_.set(hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ຾")])
        if event == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ຿"):
            event = bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬເ")
        if bstack11ll1l11ll_opy_:
            bstack11l1ll1l1l_opy_ = {
                bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨແ"): event,
                bstack11ll111ll1_opy_.bstack11ll1ll11l_opy_(): bstack11ll111ll1_opy_.bstack11lll111l1_opy_(event)
            }
            self.bstack11ll1lllll_opy_.append(bstack11l1ll1l1l_opy_)
        else:
            bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(event, bstack11ll111ll1_opy_)
class Messages:
    def __init__(self):
        self._11ll1ll111_opy_ = []
    def bstack11l1llll1l_opy_(self):
        self._11ll1ll111_opy_.append([])
    def bstack11ll1lll11_opy_(self):
        return self._11ll1ll111_opy_.pop() if self._11ll1ll111_opy_ else list()
    def push(self, message):
        self._11ll1ll111_opy_[-1].append(message) if self._11ll1ll111_opy_ else self._11ll1ll111_opy_.append([message])
class bstack11lll111ll_opy_:
    FAIL = bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪໂ")
    ERROR = bstack1ll1l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬໃ")
    WARNING = bstack1ll1l11_opy_ (u"ࠧࡘࡃࡕࡒࠬໄ")
    bstack11ll1ll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭໅")
    DEBUG = bstack1ll1l11_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨໆ")
    TRACE = bstack1ll1l11_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ໇")
    bstack11ll1l11l1_opy_ = [FAIL, ERROR]
def bstack11ll1111l1_opy_(bstack11ll111lll_opy_):
    if not bstack11ll111lll_opy_:
        return None
    if bstack11ll111lll_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ່ࠧ"), None):
        return getattr(bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ້")], bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧ໊ࠫ"), None)
    return bstack11ll111lll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨ໋ࠬ"), None)
def bstack11ll11l1l1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ໌"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫໍ")]:
        return
    if hook_type.lower() == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ໎"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ໏")
        else:
            return bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ໐")
    elif hook_type.lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ໑"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ໒")
        else:
            return bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ໓")