# -*- coding:utf-8 -*-

"""
资产更新服务器

NOTE:
    1. 默认每隔10秒钟获取一次账户资产信息；
    2. 将最新的资产信息通过EventAsset事件推送至事件中心；
    3. 资产数据结构
        assets
        {
            "BTC": {
                "free": 11.11,  # 可用资金
                "locked": 22.22,  # 冻结资金
                "total": 33.33  # 总资金
            },
            ...
        }

Author: HuangTao
Date:   2018/09/20
"""

import sys

from quant.quant import quant
from quant.const import OKEX, OKEX_FUTURE, BINANCE, HUOBI, DERIBIT, BITMEX, COINSUPER


def initialize():
    """ 初始化
    """
    from quant.utils import logger
    from quant.config import config

    for platform, info in config.platforms.items():
        for item in info["assets"]:
            if platform == OKEX:
                from assets.okex import OKExAsset as AssetServer
            elif platform == BINANCE:
                from assets.binance import BinanceAsset as AssetServer
            elif platform == HUOBI:
                from assets.huobi import HuobiAsset as AssetServer
            elif platform == OKEX_FUTURE:
                from assets.okex_future import OKExFutureAsset as AssetServer
            elif platform == DERIBIT:
                from assets.deribit import DeribitAsset as AssetServer
            elif platform == BITMEX:
                from assets.bitmex import BitmexAsset as AssetServer
            elif platform == COINSUPER:
                from assets.coinsuper import CoinsuperAsset as AssetServer
            else:
                logger.error("platform error! platform:", platform)
                continue
            item["platform"] = platform
            AssetServer(**item)


def main():
    config_file = sys.argv[1]  # 配置文件 config.json
    quant.initialize(config_file)
    initialize()
    quant.start()


if __name__ == "__main__":
    main()
