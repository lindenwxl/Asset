# -*- coding:utf-8 -*-

"""
OKEx 账户资产

Author: HuangTao
Date:   2019/01/20
"""

from quant.utils import tools
from quant.utils import logger
from quant.event import EventAsset
from quant.tasks import LoopRunTask
from quant.platform.okex import OKExRestAPI


class OKExAsset:
    """ 账户资金
    """

    def __init__(self, **kwargs):
        """ 初始化
        """
        self._platform = kwargs["platform"]
        self._host = kwargs.get("host", "https://www.okex.com")
        self._account = kwargs["account"]
        self._access_key = kwargs["access_key"]
        self._secret_key = kwargs["secret_key"]
        self._passphrase = kwargs["passphrase"]
        self._update_interval = kwargs.get("update_interval", 10)  # 更新时间间隔(秒)，默认10秒

        self._assets = {}  # 所有资金详情

        # 创建rest api请求对象
        self._rest_api = OKExRestAPI(self._host, self._access_key, self._secret_key, self._passphrase)

        # 注册心跳定时任务
        LoopRunTask.register(self.check_asset_update, self._update_interval)

    async def check_asset_update(self, *args, **kwargs):
        """ 检查账户资金是否更新
        """
        result, error = await self._rest_api.get_user_account()
        if error:
            logger.warn("platform:", self._platform, "account:", self._account, "get asset info failed!", caller=self)
            return

        assets = {}
        for item in result:
            symbol = item["currency"]
            total = float(item["balance"])
            free = float(item["available"])
            locked = float(item["frozen"])
            if total > 0:
                assets[symbol] = {
                    "total": "%.8f" % total,
                    "free": "%.8f" % free,
                    "locked": "%.8f" % locked
                }

        if assets == self._assets:
            update = False
        else:
            update = True
        self._assets = assets

        # 推送当前资产
        timestamp = tools.get_cur_timestamp_ms()
        EventAsset(self._platform, self._account, self._assets, timestamp, update).publish()
        logger.info("platform:", self._platform, "account:", self._account, "asset:", self._assets, caller=self)
