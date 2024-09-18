import logging

import tushare as ts

from no996.platform.config import settings
from no996.platform.date import date_compare, date_now, str2date

logger = logging.getLogger(__name__)


def tushare_check() -> bool:
    ts.set_token(settings.TUSHARE_TOKEN)
    pro = ts.pro_api()

    try:
        df = pro.user(token=settings.TUSHARE_TOKEN)
        logger.info(df)
    except Exception as e:
        logger.error(f"tushare token 无效, {e}")
        return False

    if df.empty:
        logger.error("tushare token 无效")
        return False

    expire_scores = float(df.loc[0, "到期积分"])
    expire_date = df.loc[0, "到期时间"]

    logger.info(
        f"tushare token 有效，到期时间 {expire_date}, 剩余积分 {expire_scores}, 预期积分 {settings.TUSHARE_SCORE}"
    )

    now = date_now()
    expire_date = str2date(expire_date, "YYYY-MM-DD", "Asia/Shanghai")
    compare_result = date_compare(now, expire_date)

    if not compare_result:
        logger.error(f"tushare token 已过期，到期时间 {expire_date}")
        return False

    if expire_scores < settings.TUSHARE_SCORE:
        logger.error(
            f"tushare token 积分不足，剩余 {expire_scores}, 预期 {settings.TUSHARE_SCORE}"
        )
        return False

    return True


def tushare_qfq():
    ts.set_token(settings.TUSHARE_TOKEN)
    pro_api = ts.pro_api()
    data = pro_api.stk_factor(
        ts_code="601988.SH", start_date="20240101", end_date="20240529"
    )
    data = data[
        [
            "trade_date",
            "open_qfq",
            "high_qfq",
            "low_qfq",
            "close_qfq",
            "change",
            "pct_change",
            "open_hfq",
        ]
    ]
    logger.info(data)


def tushare_index_weight():
    ts.set_token(settings.TUSHARE_TOKEN)
    pro = ts.pro_api()

    df = pro.index_weight(index_code="930679.CSI", trade_date="20240628")
    logger.info(df)


def tushare_fina_mainbz_vip():
    ts.set_token(settings.TUSHARE_TOKEN)
    pro = ts.pro_api()

    df = pro.fina_mainbz_vip(ts_code="000001.SZ", period="20181231", type="I")
    logger.info(df)
