#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonToolAlpha
@File    ：test.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/11 上午11:34 
@explain : 文件说明
"""
# %%
import src.LockonToolAlpha as LT

date1 = "2024-06-01"
date2 = "2024-07-02"
d1 = LT.date2dtdate(date1)
LT.get_trading_calender(d1, 20)


date3 = "20240101"

LT.date2str(date3, "%Y-%m-%d")
