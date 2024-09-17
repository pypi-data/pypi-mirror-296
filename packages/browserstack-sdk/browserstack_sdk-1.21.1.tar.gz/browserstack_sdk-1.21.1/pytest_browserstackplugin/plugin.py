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
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll111l1_opy_, bstack1l11ll111_opy_, update, bstack1l1l1111l_opy_,
                                       bstack1lllll1lll_opy_, bstack1ll1111ll1_opy_, bstack1llll1ll1_opy_, bstack111llll1l_opy_,
                                       bstack1l111ll1_opy_, bstack1lll11lll_opy_, bstack1ll111l11_opy_, bstack11111ll1l_opy_,
                                       bstack11l1ll1l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l11l1l11_opy_)
from browserstack_sdk.bstack1ll11ll1_opy_ import bstack1l1ll1l1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1l11ll_opy_
from bstack_utils.capture import bstack11llll1l1l_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1llll11lll_opy_, bstack111l11l1_opy_, bstack1llll11l1l_opy_, \
    bstack1l111ll1ll_opy_
from bstack_utils.helper import bstack1ll1l1l1_opy_, bstack1111l11l1l_opy_, bstack11ll1l1l11_opy_, bstack1lll1lllll_opy_, bstack1111lll111_opy_, bstack11ll111l_opy_, \
    bstack1111ll11l1_opy_, \
    bstack111l1111ll_opy_, bstack1l1ll11111_opy_, bstack11111llll_opy_, bstack1111ll1l1l_opy_, bstack1111l1111_opy_, Notset, \
    bstack1ll1ll1ll_opy_, bstack1111l1l111_opy_, bstack11111l1l1l_opy_, Result, bstack11111l1lll_opy_, bstack11111llll1_opy_, bstack11ll111l11_opy_, \
    bstack1l1111l1ll_opy_, bstack1l111l111l_opy_, bstack1llll111_opy_, bstack111l1lllll_opy_
from bstack_utils.bstack111111l1ll_opy_ import bstack111111111l_opy_
from bstack_utils.messages import bstack1l1l1llll1_opy_, bstack1ll1ll1l_opy_, bstack1l11lll1_opy_, bstack11111l1ll_opy_, bstack1ll1llll1l_opy_, \
    bstack11l1111ll_opy_, bstack1l1lll1ll1_opy_, bstack1l1l1l1ll1_opy_, bstack1lll1l11l1_opy_, bstack1ll11l111l_opy_, \
    bstack1l1l1ll1_opy_, bstack11l1l1ll1_opy_
from bstack_utils.proxy import bstack111111l11_opy_, bstack111111111_opy_
from bstack_utils.bstack11l1lll11_opy_ import bstack1lll11l1lll_opy_, bstack1lll1l11111_opy_, bstack1lll11lll11_opy_, bstack1lll11l1l11_opy_, \
    bstack1lll11l1l1l_opy_, bstack1lll11ll11l_opy_, bstack1lll11ll1ll_opy_, bstack1l11ll111l_opy_, bstack1lll11l1ll1_opy_
from bstack_utils.bstack1ll1ll11ll_opy_ import bstack1l1lll11_opy_
from bstack_utils.bstack111llllll_opy_ import bstack1ll1ll1l1l_opy_, bstack1lll111ll1_opy_, bstack11ll1l1l_opy_, \
    bstack1lll1ll11l_opy_, bstack111l1ll1_opy_
from bstack_utils.bstack11lll1lll1_opy_ import bstack11lllll11l_opy_
from bstack_utils.bstack1l1lll111_opy_ import bstack11ll1ll1l_opy_
import bstack_utils.bstack1ll1l1ll11_opy_ as bstack1l1ll111l_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack1ll11l11l_opy_
from bstack_utils.bstack1l1ll1l1l1_opy_ import bstack1l1ll1l1l1_opy_
bstack1l1l1l11_opy_ = None
bstack1111l11ll_opy_ = None
bstack11lll1111_opy_ = None
bstack11ll11ll1_opy_ = None
bstack1lll1l1ll_opy_ = None
bstack1111ll1l1_opy_ = None
bstack1l1llll11_opy_ = None
bstack1ll11lll1l_opy_ = None
bstack111ll111_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1l11l1ll1_opy_ = None
bstack11lll11l1_opy_ = None
bstack1ll111lll_opy_ = None
bstack1lll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࠨធ")
CONFIG = {}
bstack11l1l1111_opy_ = False
bstack1111l111_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩន")
bstack1l1lll111l_opy_ = bstack1ll1l11_opy_ (u"ࠩࠪប")
bstack1l1lll11l1_opy_ = False
bstack1l1ll111_opy_ = []
bstack11l1l1lll_opy_ = bstack1llll11lll_opy_
bstack1ll11ll1111_opy_ = bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪផ")
bstack1ll11l1ll11_opy_ = False
bstack11lllll1_opy_ = {}
bstack1ll11111l_opy_ = False
logger = bstack1l1l11ll_opy_.get_logger(__name__, bstack11l1l1lll_opy_)
store = {
    bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨព"): []
}
bstack1ll11l1l11l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll1ll1l1_opy_ = {}
current_test_uuid = None
def bstack1l1l11lll_opy_(page, bstack1ll1l1111l_opy_):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨភ"),
                      bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪម") + json.dumps(
                          bstack1ll1l1111l_opy_) + bstack1ll1l11_opy_ (u"ࠢࡾࡿࠥយ"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨរ"), e)
def bstack1111lll1_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll1l11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥល"), bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨវ") + json.dumps(
            message) + bstack1ll1l11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧឝ") + json.dumps(level) + bstack1ll1l11_opy_ (u"ࠬࢃࡽࠨឞ"))
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤស"), e)
def pytest_configure(config):
    bstack1lll11ll_opy_ = Config.bstack1l1ll1ll1l_opy_()
    config.args = bstack11ll1ll1l_opy_.bstack1ll11llll1l_opy_(config.args)
    bstack1lll11ll_opy_.bstack1ll111llll_opy_(bstack1llll111_opy_(config.getoption(bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫហ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11ll1lll_opy_ = item.config.getoption(bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪឡ"))
    plugins = item.config.getoption(bstack1ll1l11_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥអ"))
    report = outcome.get_result()
    bstack1ll11l1llll_opy_(item, call, report)
    if bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣឣ") not in plugins or bstack1111l1111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll1l11_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧឤ"), None)
    page = getattr(item, bstack1ll1l11_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦឥ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11lll1ll_opy_(item, report, summary, bstack1ll11ll1lll_opy_)
    if (page is not None):
        bstack1ll11ll1l11_opy_(item, report, summary, bstack1ll11ll1lll_opy_)
def bstack1ll11lll1ll_opy_(item, report, summary, bstack1ll11ll1lll_opy_):
    if report.when == bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬឦ") and report.skipped:
        bstack1lll11l1ll1_opy_(report)
    if report.when in [bstack1ll1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨឧ"), bstack1ll1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥឨ")]:
        return
    if not bstack1111lll111_opy_():
        return
    try:
        if (str(bstack1ll11ll1lll_opy_).lower() != bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧឩ")):
            item._driver.execute_script(
                bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨឪ") + json.dumps(
                    report.nodeid) + bstack1ll1l11_opy_ (u"ࠫࢂࢃࠧឫ"))
        os.environ[bstack1ll1l11_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨឬ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1ll1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨឭ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤឮ")))
    bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࠤឯ")
    bstack1lll11l1ll1_opy_(report)
    if not passed:
        try:
            bstack1l1l111l1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll1l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤឰ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111l1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧឱ")))
        bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠦࠧឲ")
        if not passed:
            try:
                bstack1l1l111l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧឳ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111l1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ឴")
                    + json.dumps(bstack1ll1l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣ឵"))
                    + bstack1ll1l11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦា")
                )
            else:
                item._driver.execute_script(
                    bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧិ")
                    + json.dumps(str(bstack1l1l111l1l_opy_))
                    + bstack1ll1l11_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨី")
                )
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤឹ").format(e))
def bstack1ll11l1lll1_opy_(test_name, error_message):
    try:
        bstack1ll111lll1l_opy_ = []
        bstack1l1ll111l1_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬឺ"), bstack1ll1l11_opy_ (u"࠭࠰ࠨុ"))
        bstack1l1l1ll11_opy_ = {bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬូ"): test_name, bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧួ"): error_message, bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨើ"): bstack1l1ll111l1_opy_}
        bstack1ll11ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨឿ"))
        if os.path.exists(bstack1ll11ll11ll_opy_):
            with open(bstack1ll11ll11ll_opy_) as f:
                bstack1ll111lll1l_opy_ = json.load(f)
        bstack1ll111lll1l_opy_.append(bstack1l1l1ll11_opy_)
        with open(bstack1ll11ll11ll_opy_, bstack1ll1l11_opy_ (u"ࠫࡼ࠭ៀ")) as f:
            json.dump(bstack1ll111lll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪេ") + str(e))
def bstack1ll11ll1l11_opy_(item, report, summary, bstack1ll11ll1lll_opy_):
    if report.when in [bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧែ"), bstack1ll1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤៃ")]:
        return
    if (str(bstack1ll11ll1lll_opy_).lower() != bstack1ll1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ោ")):
        bstack1l1l11lll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll1l11_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦៅ")))
    bstack1l1l111l1l_opy_ = bstack1ll1l11_opy_ (u"ࠥࠦំ")
    bstack1lll11l1ll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l111l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll1l11_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦះ").format(e)
                )
        try:
            if passed:
                bstack111l1ll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫៈ"), None), bstack1ll1l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ៉"))
            else:
                error_message = bstack1ll1l11_opy_ (u"ࠧࠨ៊")
                if bstack1l1l111l1l_opy_:
                    bstack1111lll1_opy_(item._page, str(bstack1l1l111l1l_opy_), bstack1ll1l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ់"))
                    bstack111l1ll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨ៌"), None), bstack1ll1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ៍"), str(bstack1l1l111l1l_opy_))
                    error_message = str(bstack1l1l111l1l_opy_)
                else:
                    bstack111l1ll1_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ៎"), None), bstack1ll1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ៏"))
                bstack1ll11l1lll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1ll1l11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥ័").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1ll1l11_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ៑"), default=bstack1ll1l11_opy_ (u"ࠣࡈࡤࡰࡸ࡫្ࠢ"), help=bstack1ll1l11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣ៓"))
    parser.addoption(bstack1ll1l11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ។"), default=bstack1ll1l11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ៕"), help=bstack1ll1l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ៖"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll1l11_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣៗ"), action=bstack1ll1l11_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨ៘"), default=bstack1ll1l11_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣ៙"),
                         help=bstack1ll1l11_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣ៚"))
def bstack11lllll1ll_opy_(log):
    if not (log[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ៛")] and log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬៜ")].strip()):
        return
    active = bstack11lll11l1l_opy_()
    log = {
        bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ៝"): log[bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ៞")],
        bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ៟"): bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠨ࡜ࠪ០"),
        bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ១"): log[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ២")],
    }
    if active:
        if active[bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩ៣")] == bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ៤"):
            log[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭៥")] = active[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៦")]
        elif active[bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭៧")] == bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺࠧ៨"):
            log[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៩")] = active[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៪")]
    bstack1ll11l11l_opy_.bstack11llll11l_opy_([log])
def bstack11lll11l1l_opy_():
    if len(store[bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ៫")]) > 0 and store[bstack1ll1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ៬")][-1]:
        return {
            bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ៭"): bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭៮"),
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ៯"): store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ៰")][-1]
        }
    if store.get(bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ៱"), None):
        return {
            bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ៲"): bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࠫ៳"),
            bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៴"): store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ៵")]
        }
    return None
bstack11lll11ll1_opy_ = bstack11llll1l1l_opy_(bstack11lllll1ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll11l1ll11_opy_
        item._1ll111lllll_opy_ = True
        bstack11lllll11_opy_ = bstack1l1ll111l_opy_.bstack1l11111111_opy_(bstack111l1111ll_opy_(item.own_markers))
        item._a11y_test_case = bstack11lllll11_opy_
        if bstack1ll11l1ll11_opy_:
            driver = getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ៶"), None)
            item._a11y_started = bstack1l1ll111l_opy_.bstack1l11l1lll_opy_(driver, bstack11lllll11_opy_)
        if not bstack1ll11l11l_opy_.on() or bstack1ll11ll1111_opy_ != bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ៷"):
            return
        global current_test_uuid, bstack11lll11ll1_opy_
        bstack11lll11ll1_opy_.start()
        bstack11ll111lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ៸"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ៹"): bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡚࠭ࠨ៺")
        }
        current_test_uuid = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៻")]
        store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ៼")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ៽")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11ll1ll1l1_opy_[item.nodeid] = {**_11ll1ll1l1_opy_[item.nodeid], **bstack11ll111lll_opy_}
        bstack1ll111llll1_opy_(item, _11ll1ll1l1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ៾"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭៿"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11l1l11l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111ll1l1l_opy_():
        atexit.register(bstack1l1l111l11_opy_)
        if not bstack1ll11l1l11l_opy_:
            try:
                bstack1ll11l1l1ll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111l1lllll_opy_():
                    bstack1ll11l1l1ll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11l1l1ll_opy_:
                    signal.signal(s, bstack1ll111lll11_opy_)
                bstack1ll11l1l11l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨ᠀") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l1lll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᠁")
    try:
        if not bstack1ll11l11l_opy_.on():
            return
        bstack11lll11ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll111lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᠂"): uuid,
            bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᠃"): bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫ᠄"),
            bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ᠅"): bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ᠆"),
            bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ᠇"): bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ᠈"),
            bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ᠉"): bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ᠊")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᠋")] = item
        store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ᠌")] = [uuid]
        if not _11ll1ll1l1_opy_.get(item.nodeid, None):
            _11ll1ll1l1_opy_[item.nodeid] = {bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ᠍"): [], bstack1ll1l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ᠎"): []}
        _11ll1ll1l1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ᠏")].append(bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᠐")])
        _11ll1ll1l1_opy_[item.nodeid + bstack1ll1l11_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨ᠑")] = bstack11ll111lll_opy_
        bstack1ll11ll1l1l_opy_(item, bstack11ll111lll_opy_, bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᠒"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭᠓"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack11lllll1_opy_
        bstack1l1ll111l1_opy_ = 0
        if bstack1l1lll11l1_opy_ is True:
            bstack1l1ll111l1_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᠔")))
        if CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᠕"), False):
            if CONFIG.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ᠖"), bstack1ll1l11_opy_ (u"ࠢࡢࡷࡷࡳࠧ᠗")) == bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥ᠘"):
                bstack1ll11l111ll_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᠙"), None)
                bstack1lll11l1ll_opy_ = bstack1ll11l111ll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᠚")
                driver = getattr(item, bstack1ll1l11_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ᠛"), None)
                bstack11l1ll11_opy_ = item.get(bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᠜")) or bstack1ll1l11_opy_ (u"࠭ࠧ᠝")
                bstack1l11llll_opy_ = item.get(bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᠞")) or bstack1ll1l11_opy_ (u"ࠨࠩ᠟")
                PercySDK.screenshot(driver, bstack1lll11l1ll_opy_, bstack11l1ll11_opy_=bstack11l1ll11_opy_, bstack1l11llll_opy_=bstack1l11llll_opy_, bstack1ll1l1lll1_opy_=bstack1l1ll111l1_opy_)
        if getattr(item, bstack1ll1l11_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡵࡷࡥࡷࡺࡥࡥࠩᠠ"), False):
            bstack1l1ll1l1l_opy_.bstack1lll11ll1l_opy_(getattr(item, bstack1ll1l11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᠡ"), None), bstack11lllll1_opy_, logger, item)
        if not bstack1ll11l11l_opy_.on():
            return
        bstack11ll111lll_opy_ = {
            bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᠢ"): uuid4().__str__(),
            bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᠣ"): bstack11ll1l1l11_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡚࠭ࠨᠤ"),
            bstack1ll1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᠥ"): bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᠦ"),
            bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᠧ"): bstack1ll1l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᠨ"),
            bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᠩ"): bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᠪ")
        }
        _11ll1ll1l1_opy_[item.nodeid + bstack1ll1l11_opy_ (u"࠭࠭ࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᠫ")] = bstack11ll111lll_opy_
        bstack1ll11ll1l1l_opy_(item, bstack11ll111lll_opy_, bstack1ll1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᠬ"))
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰ࠽ࠤࢀࢃࠧᠭ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll11l11l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll11l1l11_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᠮ")] = request.node
    elif bstack1lll11l1l1l_opy_(fixturedef.argname):
        store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᠯ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1ll1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠰ"): fixturedef.argname,
            bstack1ll1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᠱ"): bstack1111ll11l1_opy_(outcome),
            bstack1ll1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᠲ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᠳ")]
        if not _11ll1ll1l1_opy_.get(current_test_item.nodeid, None):
            _11ll1ll1l1_opy_[current_test_item.nodeid] = {bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᠴ"): []}
        _11ll1ll1l1_opy_[current_test_item.nodeid][bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᠵ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᠶ"), str(err))
if bstack1111l1111_opy_() and bstack1ll11l11l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll1ll1l1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᠷ")].bstack1ll1ll1l1_opy_(id(step))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࡀࠠࡼࡿࠪᠸ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll1ll1l1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᠹ")].bstack11llll1lll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᠺ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1lll1_opy_: bstack11lllll11l_opy_ = _11ll1ll1l1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᠻ")]
            bstack11lll1lll1_opy_.bstack11llll1lll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᠼ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll11ll1111_opy_
        try:
            if not bstack1ll11l11l_opy_.on() or bstack1ll11ll1111_opy_ != bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᠽ"):
                return
            global bstack11lll11ll1_opy_
            bstack11lll11ll1_opy_.start()
            driver = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᠾ"), None)
            if not _11ll1ll1l1_opy_.get(request.node.nodeid, None):
                _11ll1ll1l1_opy_[request.node.nodeid] = {}
            bstack11lll1lll1_opy_ = bstack11lllll11l_opy_.bstack1ll1ll1llll_opy_(
                scenario, feature, request.node,
                name=bstack1lll11ll11l_opy_(request.node, scenario),
                bstack11lll1ll1l_opy_=bstack11ll111l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll1l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᠿ"),
                tags=bstack1lll11ll1ll_opy_(feature, scenario),
                bstack11ll11llll_opy_=bstack1ll11l11l_opy_.bstack11ll11ll1l_opy_(driver) if driver and driver.session_id else {}
            )
            _11ll1ll1l1_opy_[request.node.nodeid][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᡀ")] = bstack11lll1lll1_opy_
            bstack1ll11ll1ll1_opy_(bstack11lll1lll1_opy_.uuid)
            bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᡁ"), bstack11lll1lll1_opy_)
        except Exception as err:
            print(bstack1ll1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪᡂ"), str(err))
def bstack1ll11l11l11_opy_(bstack11lllll111_opy_):
    if bstack11lllll111_opy_ in store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᡃ")]:
        store[bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᡄ")].remove(bstack11lllll111_opy_)
def bstack1ll11ll1ll1_opy_(bstack11llll11l1_opy_):
    store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᡅ")] = bstack11llll11l1_opy_
    threading.current_thread().current_test_uuid = bstack11llll11l1_opy_
@bstack1ll11l11l_opy_.bstack1ll1l1l1ll1_opy_
def bstack1ll11l1llll_opy_(item, call, report):
    global bstack1ll11ll1111_opy_
    bstack11l11l11l_opy_ = bstack11ll111l_opy_()
    if hasattr(report, bstack1ll1l11_opy_ (u"ࠬࡹࡴࡰࡲࠪᡆ")):
        bstack11l11l11l_opy_ = bstack11111l1lll_opy_(report.stop)
    elif hasattr(report, bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬᡇ")):
        bstack11l11l11l_opy_ = bstack11111l1lll_opy_(report.start)
    try:
        if getattr(report, bstack1ll1l11_opy_ (u"ࠧࡸࡪࡨࡲࠬᡈ"), bstack1ll1l11_opy_ (u"ࠨࠩᡉ")) == bstack1ll1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧᡊ"):
            bstack11lll11ll1_opy_.reset()
        if getattr(report, bstack1ll1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡋ"), bstack1ll1l11_opy_ (u"ࠫࠬᡌ")) == bstack1ll1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᡍ"):
            if bstack1ll11ll1111_opy_ == bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᡎ"):
                _11ll1ll1l1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᡏ")] = bstack11l11l11l_opy_
                bstack1ll111llll1_opy_(item, _11ll1ll1l1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡐ"), report, call)
                store[bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᡑ")] = None
            elif bstack1ll11ll1111_opy_ == bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᡒ"):
                bstack11lll1lll1_opy_ = _11ll1ll1l1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡓ")]
                bstack11lll1lll1_opy_.set(hooks=_11ll1ll1l1_opy_[item.nodeid].get(bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᡔ"), []))
                exception, bstack11lll11lll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll11lll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1ll1l11_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬᡕ"), bstack1ll1l11_opy_ (u"ࠧࠨᡖ"))]
                bstack11lll1lll1_opy_.stop(time=bstack11l11l11l_opy_, result=Result(result=getattr(report, bstack1ll1l11_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᡗ"), bstack1ll1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᡘ")), exception=exception, bstack11lll11lll_opy_=bstack11lll11lll_opy_))
                bstack1ll11l11l_opy_.bstack11lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᡙ"), _11ll1ll1l1_opy_[item.nodeid][bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᡚ")])
        elif getattr(report, bstack1ll1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᡛ"), bstack1ll1l11_opy_ (u"࠭ࠧᡜ")) in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᡝ"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᡞ")]:
            bstack11llll11ll_opy_ = item.nodeid + bstack1ll1l11_opy_ (u"ࠩ࠰ࠫᡟ") + getattr(report, bstack1ll1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡠ"), bstack1ll1l11_opy_ (u"ࠫࠬᡡ"))
            if getattr(report, bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᡢ"), False):
                hook_type = bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᡣ") if getattr(report, bstack1ll1l11_opy_ (u"ࠧࡸࡪࡨࡲࠬᡤ"), bstack1ll1l11_opy_ (u"ࠨࠩᡥ")) == bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᡦ") else bstack1ll1l11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᡧ")
                _11ll1ll1l1_opy_[bstack11llll11ll_opy_] = {
                    bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᡨ"): uuid4().__str__(),
                    bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᡩ"): bstack11l11l11l_opy_,
                    bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᡪ"): hook_type
                }
            _11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᡫ")] = bstack11l11l11l_opy_
            bstack1ll11l11l11_opy_(_11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡬ")])
            bstack1ll11ll1l1l_opy_(item, _11ll1ll1l1_opy_[bstack11llll11ll_opy_], bstack1ll1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᡭ"), report, call)
            if getattr(report, bstack1ll1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᡮ"), bstack1ll1l11_opy_ (u"ࠫࠬᡯ")) == bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᡰ"):
                if getattr(report, bstack1ll1l11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᡱ"), bstack1ll1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᡲ")) == bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᡳ"):
                    bstack11ll111lll_opy_ = {
                        bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᡴ"): uuid4().__str__(),
                        bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᡵ"): bstack11ll111l_opy_(),
                        bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᡶ"): bstack11ll111l_opy_()
                    }
                    _11ll1ll1l1_opy_[item.nodeid] = {**_11ll1ll1l1_opy_[item.nodeid], **bstack11ll111lll_opy_}
                    bstack1ll111llll1_opy_(item, _11ll1ll1l1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᡷ"))
                    bstack1ll111llll1_opy_(item, _11ll1ll1l1_opy_[item.nodeid], bstack1ll1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᡸ"), report, call)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬ᡹"), str(err))
def bstack1ll11l11111_opy_(test, bstack11ll111lll_opy_, result=None, call=None, bstack1lll1l111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1lll1_opy_ = {
        bstack1ll1l11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᡺"): bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᡻")],
        bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ᡼"): bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ᡽"),
        bstack1ll1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᡾"): test.name,
        bstack1ll1l11_opy_ (u"࠭ࡢࡰࡦࡼࠫ᡿"): {
            bstack1ll1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᢀ"): bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᢁ"),
            bstack1ll1l11_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᢂ"): inspect.getsource(test.obj)
        },
        bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᢃ"): test.name,
        bstack1ll1l11_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᢄ"): test.name,
        bstack1ll1l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᢅ"): bstack11ll1ll1l_opy_.bstack11l1ll1ll1_opy_(test),
        bstack1ll1l11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᢆ"): file_path,
        bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᢇ"): file_path,
        bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢈ"): bstack1ll1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᢉ"),
        bstack1ll1l11_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᢊ"): file_path,
        bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢋ"): bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᢌ")],
        bstack1ll1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᢍ"): bstack1ll1l11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᢎ"),
        bstack1ll1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᢏ"): {
            bstack1ll1l11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᢐ"): test.nodeid
        },
        bstack1ll1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢑ"): bstack111l1111ll_opy_(test.own_markers)
    }
    if bstack1lll1l111l_opy_ in [bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᢒ"), bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᢓ")]:
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"࠭࡭ࡦࡶࡤࠫᢔ")] = {
            bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢕ"): bstack11ll111lll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᢖ"), [])
        }
    if bstack1lll1l111l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᢗ"):
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢘ")] = bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᢙ")
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢚ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᢛ")]
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᢜ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᢝ")]
    if result:
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᢞ")] = result.outcome
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᢟ")] = result.duration * 1000
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢠ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢡ")]
        if result.failed:
            bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᢢ")] = bstack1ll11l11l_opy_.bstack11l1l11111_opy_(call.excinfo.typename)
            bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᢣ")] = bstack1ll11l11l_opy_.bstack1ll1ll1l1ll_opy_(call.excinfo, result)
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢤ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᢥ")]
    if outcome:
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢦ")] = bstack1111ll11l1_opy_(outcome)
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᢧ")] = 0
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢨ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷᢩࠫ")]
        if bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢪ")] == bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᢫"):
            bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᢬")] = bstack1ll1l11_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ᢭")  # bstack1ll11l11l1l_opy_
            bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᢮")] = [{bstack1ll1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᢯"): [bstack1ll1l11_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᢰ")]}]
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢱ")] = bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢲ")]
    return bstack11lll1lll1_opy_
def bstack1ll11l1l1l1_opy_(test, bstack11ll11ll11_opy_, bstack1lll1l111l_opy_, result, call, outcome, bstack1ll11ll11l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᢳ")]
    hook_name = bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᢴ")]
    hook_data = {
        bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᢵ"): bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᢶ")],
        bstack1ll1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᢷ"): bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᢸ"),
        bstack1ll1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᢹ"): bstack1ll1l11_opy_ (u"ࠩࡾࢁࠬᢺ").format(bstack1lll1l11111_opy_(hook_name)),
        bstack1ll1l11_opy_ (u"ࠪࡦࡴࡪࡹࠨᢻ"): {
            bstack1ll1l11_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᢼ"): bstack1ll1l11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᢽ"),
            bstack1ll1l11_opy_ (u"࠭ࡣࡰࡦࡨࠫᢾ"): None
        },
        bstack1ll1l11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᢿ"): test.name,
        bstack1ll1l11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᣀ"): bstack11ll1ll1l_opy_.bstack11l1ll1ll1_opy_(test, hook_name),
        bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᣁ"): file_path,
        bstack1ll1l11_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᣂ"): file_path,
        bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣃ"): bstack1ll1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᣄ"),
        bstack1ll1l11_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᣅ"): file_path,
        bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᣆ"): bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᣇ")],
        bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᣈ"): bstack1ll1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᣉ") if bstack1ll11ll1111_opy_ == bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᣊ") else bstack1ll1l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᣋ"),
        bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᣌ"): hook_type
    }
    bstack1ll1lllll1l_opy_ = bstack11ll1111l1_opy_(_11ll1ll1l1_opy_.get(test.nodeid, None))
    if bstack1ll1lllll1l_opy_:
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᣍ")] = bstack1ll1lllll1l_opy_
    if result:
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣎ")] = result.outcome
        hook_data[bstack1ll1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᣏ")] = result.duration * 1000
        hook_data[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣐ")] = bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣑ")]
        if result.failed:
            hook_data[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣒ")] = bstack1ll11l11l_opy_.bstack11l1l11111_opy_(call.excinfo.typename)
            hook_data[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣓ")] = bstack1ll11l11l_opy_.bstack1ll1ll1l1ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᣔ")] = bstack1111ll11l1_opy_(outcome)
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᣕ")] = 100
        hook_data[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣖ")] = bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣗ")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣘ")] == bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᣙ"):
            hook_data[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᣚ")] = bstack1ll1l11_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᣛ")  # bstack1ll11l11l1l_opy_
            hook_data[bstack1ll1l11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᣜ")] = [{bstack1ll1l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᣝ"): [bstack1ll1l11_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᣞ")]}]
    if bstack1ll11ll11l1_opy_:
        hook_data[bstack1ll1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣟ")] = bstack1ll11ll11l1_opy_.result
        hook_data[bstack1ll1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᣠ")] = bstack1111l1l111_opy_(bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᣡ")], bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣢ")])
        hook_data[bstack1ll1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣣ")] = bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣤ")]
        if hook_data[bstack1ll1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᣥ")] == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᣦ"):
            hook_data[bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣧ")] = bstack1ll11l11l_opy_.bstack11l1l11111_opy_(bstack1ll11ll11l1_opy_.exception_type)
            hook_data[bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᣨ")] = [{bstack1ll1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᣩ"): bstack11111l1l1l_opy_(bstack1ll11ll11l1_opy_.exception)}]
    return hook_data
def bstack1ll111llll1_opy_(test, bstack11ll111lll_opy_, bstack1lll1l111l_opy_, result=None, call=None, outcome=None):
    bstack11lll1lll1_opy_ = bstack1ll11l11111_opy_(test, bstack11ll111lll_opy_, result, call, bstack1lll1l111l_opy_, outcome)
    driver = getattr(test, bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᣪ"), None)
    if bstack1lll1l111l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᣫ") and driver:
        bstack11lll1lll1_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᣬ")] = bstack1ll11l11l_opy_.bstack11ll11ll1l_opy_(driver)
    if bstack1lll1l111l_opy_ == bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᣭ"):
        bstack1lll1l111l_opy_ = bstack1ll1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᣮ")
    bstack11l1ll1l1l_opy_ = {
        bstack1ll1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᣯ"): bstack1lll1l111l_opy_,
        bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᣰ"): bstack11lll1lll1_opy_
    }
    bstack1ll11l11l_opy_.bstack11ll11l11l_opy_(bstack11l1ll1l1l_opy_)
def bstack1ll11ll1l1l_opy_(test, bstack11ll111lll_opy_, bstack1lll1l111l_opy_, result=None, call=None, outcome=None, bstack1ll11ll11l1_opy_=None):
    hook_data = bstack1ll11l1l1l1_opy_(test, bstack11ll111lll_opy_, bstack1lll1l111l_opy_, result, call, outcome, bstack1ll11ll11l1_opy_)
    bstack11l1ll1l1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᣱ"): bstack1lll1l111l_opy_,
        bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᣲ"): hook_data
    }
    bstack1ll11l11l_opy_.bstack11ll11l11l_opy_(bstack11l1ll1l1l_opy_)
def bstack11ll1111l1_opy_(bstack11ll111lll_opy_):
    if not bstack11ll111lll_opy_:
        return None
    if bstack11ll111lll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᣳ"), None):
        return getattr(bstack11ll111lll_opy_[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᣴ")], bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᣵ"), None)
    return bstack11ll111lll_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᣶"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll11l11l_opy_.on():
            return
        places = [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᣷"), bstack1ll1l11_opy_ (u"ࠨࡥࡤࡰࡱ࠭᣸"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ᣹")]
        bstack11ll111l1l_opy_ = []
        for bstack1ll11ll111l_opy_ in places:
            records = caplog.get_records(bstack1ll11ll111l_opy_)
            bstack1ll11l111l1_opy_ = bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᣺") if bstack1ll11ll111l_opy_ == bstack1ll1l11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩ᣻") else bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᣼")
            bstack1ll11l1111l_opy_ = request.node.nodeid + (bstack1ll1l11_opy_ (u"࠭ࠧ᣽") if bstack1ll11ll111l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ᣾") else bstack1ll1l11_opy_ (u"ࠨ࠯ࠪ᣿") + bstack1ll11ll111l_opy_)
            bstack11llll11l1_opy_ = bstack11ll1111l1_opy_(_11ll1ll1l1_opy_.get(bstack1ll11l1111l_opy_, None))
            if not bstack11llll11l1_opy_:
                continue
            for record in records:
                if bstack11111llll1_opy_(record.message):
                    continue
                bstack11ll111l1l_opy_.append({
                    bstack1ll1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᤀ"): bstack1111l11l1l_opy_(record.created).isoformat() + bstack1ll1l11_opy_ (u"ࠪ࡞ࠬᤁ"),
                    bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᤂ"): record.levelname,
                    bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᤃ"): record.message,
                    bstack1ll11l111l1_opy_: bstack11llll11l1_opy_
                })
        if len(bstack11ll111l1l_opy_) > 0:
            bstack1ll11l11l_opy_.bstack11llll11l_opy_(bstack11ll111l1l_opy_)
    except Exception as err:
        print(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪᤄ"), str(err))
def bstack1l11llll11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1ll11111l_opy_
    bstack1l1l11l1l_opy_ = bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᤅ"), None) and bstack1ll1l1l1_opy_(
            threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᤆ"), None)
    bstack1l1ll1ll11_opy_ = getattr(driver, bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᤇ"), None) != None and getattr(driver, bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᤈ"), None) == True
    if sequence == bstack1ll1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᤉ") and driver != None:
      if not bstack1ll11111l_opy_ and bstack1111lll111_opy_() and bstack1ll1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᤊ") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᤋ")] == True and bstack1l1ll1l1l1_opy_.bstack1ll1lll1_opy_(driver_command) and (bstack1l1ll1ll11_opy_ or bstack1l1l11l1l_opy_) and not bstack1l11l1l11_opy_(args):
        try:
          bstack1ll11111l_opy_ = True
          logger.debug(bstack1ll1l11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡻࡾࠩᤌ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1ll1l11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵ࡫ࡲࡧࡱࡵࡱࠥࡹࡣࡢࡰࠣࡿࢂ࠭ᤍ").format(str(err)))
        bstack1ll11111l_opy_ = False
    if sequence == bstack1ll1l11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᤎ"):
        if driver_command == bstack1ll1l11_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᤏ"):
            bstack1ll11l11l_opy_.bstack1lll111111_opy_({
                bstack1ll1l11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᤐ"): response[bstack1ll1l11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫᤑ")],
                bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᤒ"): store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᤓ")]
            })
def bstack1l1l111l11_opy_():
    global bstack1l1ll111_opy_
    bstack1l1l11ll_opy_.bstack1ll11l11l1_opy_()
    logging.shutdown()
    bstack1ll11l11l_opy_.bstack11l1lllll1_opy_()
    for driver in bstack1l1ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll111lll11_opy_(*args):
    global bstack1l1ll111_opy_
    bstack1ll11l11l_opy_.bstack11l1lllll1_opy_()
    for driver in bstack1l1ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll11llll_opy_(self, *args, **kwargs):
    bstack1l11lll1ll_opy_ = bstack1l1l1l11_opy_(self, *args, **kwargs)
    bstack1ll11l11l_opy_.bstack1l1llll1ll_opy_(self)
    return bstack1l11lll1ll_opy_
def bstack111lll11_opy_(framework_name):
    global bstack1lll11ll11_opy_
    global bstack1l11l1ll11_opy_
    bstack1lll11ll11_opy_ = framework_name
    logger.info(bstack11l1l1ll1_opy_.format(bstack1lll11ll11_opy_.split(bstack1ll1l11_opy_ (u"ࠨ࠯ࠪᤔ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111lll111_opy_():
            Service.start = bstack1llll1ll1_opy_
            Service.stop = bstack111llll1l_opy_
            webdriver.Remote.__init__ = bstack1lll1lll1l_opy_
            webdriver.Remote.get = bstack1l111111_opy_
            if not isinstance(os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪᤕ")), str):
                return
            WebDriver.close = bstack1l111ll1_opy_
            WebDriver.quit = bstack1l1ll1lll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111lll111_opy_() and bstack1ll11l11l_opy_.on():
            webdriver.Remote.__init__ = bstack1lll11llll_opy_
        bstack1l11l1ll11_opy_ = True
    except Exception as e:
        pass
    bstack1l1lllll_opy_()
    if os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨᤖ")):
        bstack1l11l1ll11_opy_ = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᤗ")))
    if not bstack1l11l1ll11_opy_:
        bstack1ll111l11_opy_(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢᤘ"), bstack1l1l1ll1_opy_)
    if bstack1ll11llll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11lll1l1l_opy_
        except Exception as e:
            logger.error(bstack11l1111ll_opy_.format(str(e)))
    if bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᤙ") in str(framework_name).lower():
        if not bstack1111lll111_opy_():
            return
        try:
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
def bstack1l1ll1lll1_opy_(self):
    global bstack1lll11ll11_opy_
    global bstack1l1l1l1l_opy_
    global bstack1111l11ll_opy_
    try:
        if bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᤚ") in bstack1lll11ll11_opy_ and self.session_id != None and bstack1ll1l1l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᤛ"), bstack1ll1l11_opy_ (u"ࠩࠪᤜ")) != bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᤝ"):
            bstack111ll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᤞ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᤟")
            bstack1l111l111l_opy_(logger, True)
            if self != None:
                bstack1lll1ll11l_opy_(self, bstack111ll1l1_opy_, bstack1ll1l11_opy_ (u"࠭ࠬࠡࠩᤠ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᤡ"), None)
        if item is not None and bstack1ll11l1ll11_opy_:
            bstack1l1ll1l1l_opy_.bstack1lll11ll1l_opy_(self, bstack11lllll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1ll1l11_opy_ (u"ࠨࠩᤢ")
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥᤣ") + str(e))
    bstack1111l11ll_opy_(self)
    self.session_id = None
def bstack1lll1lll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1l1l1l_opy_
    global bstack1l1ll11l11_opy_
    global bstack1l1lll11l1_opy_
    global bstack1lll11ll11_opy_
    global bstack1l1l1l11_opy_
    global bstack1l1ll111_opy_
    global bstack1111l111_opy_
    global bstack1l1lll111l_opy_
    global bstack1ll11l1ll11_opy_
    global bstack11lllll1_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᤤ")] = str(bstack1lll11ll11_opy_) + str(__version__)
    command_executor = bstack11111llll_opy_(bstack1111l111_opy_)
    logger.debug(bstack11111l1ll_opy_.format(command_executor))
    proxy = bstack11l1ll1l1_opy_(CONFIG, proxy)
    bstack1l1ll111l1_opy_ = 0
    try:
        if bstack1l1lll11l1_opy_ is True:
            bstack1l1ll111l1_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᤥ")))
    except:
        bstack1l1ll111l1_opy_ = 0
    bstack1ll111l1_opy_ = bstack1llll111l1_opy_(CONFIG, bstack1l1ll111l1_opy_)
    logger.debug(bstack1l1l1l1ll1_opy_.format(str(bstack1ll111l1_opy_)))
    bstack11lllll1_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᤦ"))[bstack1l1ll111l1_opy_]
    if bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᤧ") in CONFIG and CONFIG[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᤨ")]:
        bstack11ll1l1l_opy_(bstack1ll111l1_opy_, bstack1l1lll111l_opy_)
    if bstack1l1ll111l_opy_.bstack1lllllll11_opy_(CONFIG, bstack1l1ll111l1_opy_) and bstack1l1ll111l_opy_.bstack11ll11l1_opy_(bstack1ll111l1_opy_, options, desired_capabilities):
        bstack1ll11l1ll11_opy_ = True
        bstack1l1ll111l_opy_.set_capabilities(bstack1ll111l1_opy_, CONFIG)
    if desired_capabilities:
        bstack1lll1l11l_opy_ = bstack1l11ll111_opy_(desired_capabilities)
        bstack1lll1l11l_opy_[bstack1ll1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᤩ")] = bstack1ll1ll1ll_opy_(CONFIG)
        bstack1l111l111_opy_ = bstack1llll111l1_opy_(bstack1lll1l11l_opy_)
        if bstack1l111l111_opy_:
            bstack1ll111l1_opy_ = update(bstack1l111l111_opy_, bstack1ll111l1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll11lll_opy_(options, bstack1ll111l1_opy_)
    if not options:
        options = bstack1l1l1111l_opy_(bstack1ll111l1_opy_)
    if proxy and bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᤪ")):
        options.proxy(proxy)
    if options and bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᤫ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1ll11111_opy_() < version.parse(bstack1ll1l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ᤬")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll111l1_opy_)
    logger.info(bstack1l11lll1_opy_)
    if bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ᤭")):
        bstack1l1l1l11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ᤮")):
        bstack1l1l1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ᤯")):
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
        bstack1l1llllll_opy_ = bstack1ll1l11_opy_ (u"ࠨࠩᤰ")
        if bstack1l1ll11111_opy_() >= version.parse(bstack1ll1l11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪᤱ")):
            bstack1l1llllll_opy_ = self.caps.get(bstack1ll1l11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥᤲ"))
        else:
            bstack1l1llllll_opy_ = self.capabilities.get(bstack1ll1l11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᤳ"))
        if bstack1l1llllll_opy_:
            bstack1l1111l1ll_opy_(bstack1l1llllll_opy_)
            if bstack1l1ll11111_opy_() <= version.parse(bstack1ll1l11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᤴ")):
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᤵ") + bstack1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᤶ")
            else:
                self.command_executor._url = bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᤷ") + bstack1l1llllll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᤸ")
            logger.debug(bstack1ll1ll1l_opy_.format(bstack1l1llllll_opy_))
        else:
            logger.debug(bstack1l1l1llll1_opy_.format(bstack1ll1l11_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ᤹ࠦ")))
    except Exception as e:
        logger.debug(bstack1l1l1llll1_opy_.format(e))
    bstack1l1l1l1l_opy_ = self.session_id
    if bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᤺") in bstack1lll11ll11_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮᤻ࠩ"), None)
        if item:
            bstack1ll11l11ll1_opy_ = getattr(item, bstack1ll1l11_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ᤼"), False)
            if not getattr(item, bstack1ll1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᤽"), None) and bstack1ll11l11ll1_opy_:
                setattr(store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᤾")], bstack1ll1l11_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᤿"), self)
        bstack1ll11l11l_opy_.bstack1l1llll1ll_opy_(self)
    bstack1l1ll111_opy_.append(self)
    if bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᥀") in CONFIG and bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᥁") in CONFIG[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᥂")][bstack1l1ll111l1_opy_]:
        bstack1l1ll11l11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᥃")][bstack1l1ll111l1_opy_][bstack1ll1l11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᥄")]
    logger.debug(bstack1ll11l111l_opy_.format(bstack1l1l1l1l_opy_))
def bstack1l111111_opy_(self, url):
    global bstack111ll111_opy_
    global CONFIG
    try:
        bstack1lll111ll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll1l11l1_opy_.format(str(err)))
    try:
        bstack111ll111_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1l11l1ll_opy_ = str(e)
            if any(err_msg in bstack1l1l11l1ll_opy_ for err_msg in bstack1llll11l1l_opy_):
                bstack1lll111ll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll1l11l1_opy_.format(str(err)))
        raise e
def bstack11l1llll_opy_(item, when):
    global bstack11lll11l1_opy_
    try:
        bstack11lll11l1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1l11llll_opy_(item, call, rep):
    global bstack1ll111lll_opy_
    global bstack1l1ll111_opy_
    name = bstack1ll1l11_opy_ (u"ࠨࠩ᥅")
    try:
        if rep.when == bstack1ll1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ᥆"):
            bstack1l1l1l1l_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11ll1lll_opy_ = item.config.getoption(bstack1ll1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᥇"))
            try:
                if (str(bstack1ll11ll1lll_opy_).lower() != bstack1ll1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩ᥈")):
                    name = str(rep.nodeid)
                    bstack1l1ll1l11_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᥉"), name, bstack1ll1l11_opy_ (u"࠭ࠧ᥊"), bstack1ll1l11_opy_ (u"ࠧࠨ᥋"), bstack1ll1l11_opy_ (u"ࠨࠩ᥌"), bstack1ll1l11_opy_ (u"ࠩࠪ᥍"))
                    os.environ[bstack1ll1l11_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭᥎")] = name
                    for driver in bstack1l1ll111_opy_:
                        if bstack1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1l11_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ᥏").format(str(e)))
            try:
                bstack1l11ll111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᥐ"):
                    status = bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᥑ") if rep.outcome.lower() == bstack1ll1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᥒ") else bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᥓ")
                    reason = bstack1ll1l11_opy_ (u"ࠩࠪᥔ")
                    if status == bstack1ll1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᥕ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᥖ") if status == bstack1ll1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᥗ") else bstack1ll1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᥘ")
                    data = name + bstack1ll1l11_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩᥙ") if status == bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᥚ") else name + bstack1ll1l11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬᥛ") + reason
                    bstack11l11l1l_opy_ = bstack1ll1ll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᥜ"), bstack1ll1l11_opy_ (u"ࠫࠬᥝ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᥞ"), bstack1ll1l11_opy_ (u"࠭ࠧᥟ"), level, data)
                    for driver in bstack1l1ll111_opy_:
                        if bstack1l1l1l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack11l11l1l_opy_)
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᥠ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬᥡ").format(str(e)))
    bstack1ll111lll_opy_(item, call, rep)
notset = Notset()
def bstack1l1l1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l11l1ll1_opy_
    if str(name).lower() == bstack1ll1l11_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᥢ"):
        return bstack1ll1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᥣ")
    else:
        return bstack1l11l1ll1_opy_(self, name, default, skip)
def bstack11lll1l1l_opy_(self):
    global CONFIG
    global bstack1l1llll11_opy_
    try:
        proxy = bstack111111l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll1l11_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᥤ")):
                proxies = bstack111111111_opy_(proxy, bstack11111llll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1lll1l11ll_opy_ = proxies.popitem()
                    if bstack1ll1l11_opy_ (u"ࠧࡀ࠯࠰ࠤᥥ") in bstack1lll1l11ll_opy_:
                        return bstack1lll1l11ll_opy_
                    else:
                        return bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᥦ") + bstack1lll1l11ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦᥧ").format(str(e)))
    return bstack1l1llll11_opy_(self)
def bstack1ll11llll_opy_():
    return (bstack1ll1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᥨ") in CONFIG or bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᥩ") in CONFIG) and bstack1lll1lllll_opy_() and bstack1l1ll11111_opy_() >= version.parse(
        bstack111l11l1_opy_)
def bstack111l1ll1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1ll11l11_opy_
    global bstack1l1lll11l1_opy_
    global bstack1lll11ll11_opy_
    CONFIG[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᥪ")] = str(bstack1lll11ll11_opy_) + str(__version__)
    bstack1l1ll111l1_opy_ = 0
    try:
        if bstack1l1lll11l1_opy_ is True:
            bstack1l1ll111l1_opy_ = int(os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᥫ")))
    except:
        bstack1l1ll111l1_opy_ = 0
    CONFIG[bstack1ll1l11_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᥬ")] = True
    bstack1ll111l1_opy_ = bstack1llll111l1_opy_(CONFIG, bstack1l1ll111l1_opy_)
    logger.debug(bstack1l1l1l1ll1_opy_.format(str(bstack1ll111l1_opy_)))
    if CONFIG.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᥭ")):
        bstack11ll1l1l_opy_(bstack1ll111l1_opy_, bstack1l1lll111l_opy_)
    if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᥮") in CONFIG and bstack1ll1l11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᥯") in CONFIG[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᥰ")][bstack1l1ll111l1_opy_]:
        bstack1l1ll11l11_opy_ = CONFIG[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᥱ")][bstack1l1ll111l1_opy_][bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᥲ")]
    import urllib
    import json
    bstack1l1lll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧᥳ") + urllib.parse.quote(json.dumps(bstack1ll111l1_opy_))
    browser = self.connect(bstack1l1lll11ll_opy_)
    return browser
def bstack1l1lllll_opy_():
    global bstack1l11l1ll11_opy_
    global bstack1lll11ll11_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1lll1l1l11_opy_
        if not bstack1111lll111_opy_():
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
def bstack1ll11l1l111_opy_():
    global CONFIG
    global bstack11l1l1111_opy_
    global bstack1111l111_opy_
    global bstack1l1lll111l_opy_
    global bstack1l1lll11l1_opy_
    global bstack11l1l1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬᥴ")))
    bstack11l1l1111_opy_ = eval(os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ᥵")))
    bstack1111l111_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ᥶"))
    bstack11111ll1l_opy_(CONFIG, bstack11l1l1111_opy_)
    bstack11l1l1lll_opy_ = bstack1l1l11ll_opy_.bstack1ll1l1ll_opy_(CONFIG, bstack11l1l1lll_opy_)
    global bstack1l1l1l11_opy_
    global bstack1111l11ll_opy_
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
    except Exception as e:
        pass
    if (bstack1ll1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ᥷") in CONFIG or bstack1ll1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᥸") in CONFIG) and bstack1lll1lllll_opy_():
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
        logger.debug(bstack1ll1l11_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ᥹"))
    bstack1l1lll111l_opy_ = CONFIG.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᥺"), {}).get(bstack1ll1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᥻"))
    bstack1l1lll11l1_opy_ = True
    bstack111lll11_opy_(bstack1l111ll1ll_opy_)
if (bstack1111ll1l1l_opy_()):
    bstack1ll11l1l111_opy_()
@bstack11ll111l11_opy_(class_method=False)
def bstack1ll11lll11l_opy_(hook_name, event, bstack1ll11lll111_opy_=None):
    if hook_name not in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ᥼"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ᥽"), bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ᥾"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ᥿"), bstack1ll1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᦀ"), bstack1ll1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᦁ"), bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᦂ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᦃ")]:
        return
    node = store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᦄ")]
    if hook_name in [bstack1ll1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᦅ"), bstack1ll1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᦆ")]:
        node = store[bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᦇ")]
    elif hook_name in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᦈ"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᦉ")]:
        node = store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᦊ")]
    if event == bstack1ll1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᦋ"):
        hook_type = bstack1lll11lll11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11ll11ll11_opy_ = {
            bstack1ll1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᦌ"): uuid,
            bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᦍ"): bstack11ll111l_opy_(),
            bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᦎ"): bstack1ll1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᦏ"),
            bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᦐ"): hook_type,
            bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᦑ"): hook_name
        }
        store[bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᦒ")].append(uuid)
        bstack1ll11l1ll1l_opy_ = node.nodeid
        if hook_type == bstack1ll1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᦓ"):
            if not _11ll1ll1l1_opy_.get(bstack1ll11l1ll1l_opy_, None):
                _11ll1ll1l1_opy_[bstack1ll11l1ll1l_opy_] = {bstack1ll1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᦔ"): []}
            _11ll1ll1l1_opy_[bstack1ll11l1ll1l_opy_][bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᦕ")].append(bstack11ll11ll11_opy_[bstack1ll1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᦖ")])
        _11ll1ll1l1_opy_[bstack1ll11l1ll1l_opy_ + bstack1ll1l11_opy_ (u"࠭࠭ࠨᦗ") + hook_name] = bstack11ll11ll11_opy_
        bstack1ll11ll1l1l_opy_(node, bstack11ll11ll11_opy_, bstack1ll1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᦘ"))
    elif event == bstack1ll1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᦙ"):
        bstack11llll11ll_opy_ = node.nodeid + bstack1ll1l11_opy_ (u"ࠩ࠰ࠫᦚ") + hook_name
        _11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᦛ")] = bstack11ll111l_opy_()
        bstack1ll11l11l11_opy_(_11ll1ll1l1_opy_[bstack11llll11ll_opy_][bstack1ll1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᦜ")])
        bstack1ll11ll1l1l_opy_(node, _11ll1ll1l1_opy_[bstack11llll11ll_opy_], bstack1ll1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᦝ"), bstack1ll11ll11l1_opy_=bstack1ll11lll111_opy_)
def bstack1ll11lll1l1_opy_():
    global bstack1ll11ll1111_opy_
    if bstack1111l1111_opy_():
        bstack1ll11ll1111_opy_ = bstack1ll1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᦞ")
    else:
        bstack1ll11ll1111_opy_ = bstack1ll1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᦟ")
@bstack1ll11l11l_opy_.bstack1ll1l1l1ll1_opy_
def bstack1ll11l11lll_opy_():
    bstack1ll11lll1l1_opy_()
    if bstack1lll1lllll_opy_():
        bstack1l1lll11_opy_(bstack1l11llll11_opy_)
    try:
        bstack111111111l_opy_(bstack1ll11lll11l_opy_)
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡸࠦࡰࡢࡶࡦ࡬࠿ࠦࡻࡾࠤᦠ").format(e))
bstack1ll11l11lll_opy_()