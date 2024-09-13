#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonToolAlpha
@File    ：time_tools.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/18 下午2:34
@explain : 文件说明
"""
# !/usr/bin/env python
# -*- coding: UTF-8 -*-

from pandas import Timestamp
import datetime
from numpy import datetime64
from ._date_param import calender_days
import time
import pandas as pd


class TimeCounter:
    """
    用于计时，用法:
    with Timecounter():
        run()
    """

    def __enter__(self):
        self.s_time = time.perf_counter()

    def __exit__(self, type, value, traceback):
        print("time cost: %.3f" % (time.perf_counter() - self.s_time))


# 增加一个工具函数专门处理字符串到日期时间的转换
def str2datetime(date_str):
    """
    将日期字符串转换为datetime对象。
    支持的格式：'%Y-%m-%d', '%Y/%m/%d', '%Y%m%d'
    """
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"无法解析日期字符串: {date_str}")


def date2dtdate(date):
    """
    将传入的date形式转为datetime.date
    :param date:
    :return: date的datetime形式
    :rtype: datetime.date
    """
    if isinstance(date, Timestamp):
        return date.to_pydatetime().date()

    if isinstance(date, datetime64):
        return date.astype("datetime64[D]").astype(datetime.date)

    if isinstance(date, str):
        return str2datetime(date)

    if isinstance(date, datetime.date):
        return date

    else:
        raise TypeError("不支持的日期类型")


def date2str(date, date_format="%Y-%m-%d"):
    """
    将传入的date形式转为str
    :param date_format:
    :type date_format:
    :param date:
    :return: date的str形式
    :rtype: str
    """
    if isinstance(date, Timestamp):
        return date2str(str(date.to_pydatetime().date()), date_format)

    if isinstance(date, datetime64):
        return date2str(
            str(date.astype("datetime64[D]").astype(datetime.date)), date_format
        )

    if isinstance(date, str):
        try:
            if len(date) == 8:
                return "%s-%s-%s" % (date[:4], date[4:6], date[6:8])
            else:
                return date.replace("/", "-")
        except:
            raise TypeError("不支持的日期字符串类型")

    if isinstance(date, datetime.date):
        return date.strftime(date_format)


def get_trading_calender(start_date, days_len, include_sday=True):
    """
    获取指定长度的工作日日历
    :param include_sday: 是否包括起始日期
    :type include_sday:  bool
    :param start_date: 起始日期
    :type start_date: str
    :param days_len: 工作日日历长度
    :type days_len: int
    :return: 工作日日历列表
    :rtype: list
    """
    s_date = date2dtdate(start_date)
    i = days_len
    tmp = s_date
    res = []
    if include_sday:
        res.append(s_date)
    while i > 0:
        tmp = get_next_trade_date(tmp)
        res.append(date2dtdate(tmp))
        i -= 1
    return res


def get_trade_date_range(start_date, end_date):
    """
    获取指定日期之间的交易日列表
    :param start_date: 起始日期 YYYY-MM-DD
    :type start_date: str
    :param end_date: 结束日期 YYYY-MM-DD
    :type end_date: str
    :return: 交易日列表
    :rtype: list
    """
    dt_series = pd.Series(calender_days.index).apply(pd.to_datetime)
    dt_series = dt_series[
        dt_series.apply(
            lambda x: date2dtdate(start_date) <= x.date() <= date2dtdate(end_date)
        )
    ]
    return dt_series.dt.date


def get_natural_days_diff(start_date, end_date):
    """计算 任意两天之间的自然天数
    @param start_date: 起始日 datetime.date / str
    @param end_date: 结束日 datetime.date / str
    @return: Int类型的自然天数。 For example: 60
    """
    s_date, e_date = date2dtdate(start_date), date2dtdate(end_date)

    return (e_date - s_date).days


def get_trading_days_diff(start_date, end_date):
    """计算出任意两天之间的交易日天数
    @param start_date: 起始日 datetime.date
    @param end_date: 结束日 datetime.date
    @return: Int类型的交易日天数。 For example: 60
    """
    s_date, e_date = date2dtdate(start_date), date2dtdate(end_date)
    # 将calender_days的键转换为集合，提高查找效率
    trading_days = set(calender_days.keys())
    while str(e_date) not in trading_days:
        e_date = e_date + datetime.timedelta(days=1)
    while str(s_date) not in trading_days:
        s_date = s_date + datetime.timedelta(days=1)
    return max(0, int(calender_days[str(e_date)] - calender_days[str(s_date)]))


def get_last_trade_date(date):
    """
    获取上一个交易日，如果date本身不为交易日，则返回上一个交易日
    :param date: T日日期
    :return: 上一个交易日
    :rtype: datetime.date
    """
    trigger = False
    date_formatted = date2str(date)
    trading_days = set(calender_days.keys())  # 使用集合优化查找
    while date_formatted not in trading_days:
        date_formatted = str(date2dtdate(date_formatted) - datetime.timedelta(days=1))
        trigger = True
    if trigger:
        return date2dtdate(date_formatted)
    t = calender_days.index[calender_days[date_formatted] - 1]

    return date2dtdate(t)


def get_next_trade_date(date):
    """
    获取下一个交易日，如果date本身不为交易日，则返回下一个交易日
    :param date: T日日期
    :return: 下一个交易日
    :rtype:datetime.date
    """
    trigger = False
    date_formatted = date2str(date)
    trading_days = set(calender_days.keys())  # 使用集合优化查找
    while date_formatted not in trading_days:
        date_formatted = str(date2dtdate(date_formatted) + datetime.timedelta(days=1))
        trigger = True
    if trigger:
        return date2dtdate(date_formatted)
    t = calender_days.index[calender_days[date_formatted] + 1]
    return date2dtdate(t)


def is_trade_date(date):
    date_str_formatted = date2str(date)
    return date_str_formatted in calender_days.index


def get_natural_days_between(start_date, end_date):
    """
    获取两个日期之间的所有自然日列表

    :param start_date: 开始日期，可以是字符串或datetime.date对象
    :type start_date: str | datetime.date
    :param end_date: 结束日期，可以是字符串或datetime.date对象
    :type end_date: str | datetime.date
    :return: 日期字符串列表，包含开始日期和结束日期
    :rtype: List[str]
    """
    start_date = date2dtdate(start_date)
    end_date = date2dtdate(end_date)

    # 初始化日期列表
    date_list = []

    # 遍历开始日期到结束日期之间的每一天
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += datetime.timedelta(days=1)

    return date_list
