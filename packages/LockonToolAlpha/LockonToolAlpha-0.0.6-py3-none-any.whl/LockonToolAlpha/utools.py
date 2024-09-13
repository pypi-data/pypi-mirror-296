#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：LockonToolAlpha
@File    ：utools.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/7/18 下午2:33
@explain : 文件说明
"""
import logging
import shutil

# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import warnings
import time


class WarningFilter:
    """
    用于忽略Warning
    with WarningFilter():
        df = pd.read_excel(io.BytesIO(attr_data))
    """

    def __enter__(self):
        self.old_filters = warnings.filters
        warnings.filterwarnings("ignore", category=UserWarning)

    def __exit__(self, type, value, traceback):
        warnings.filters = self.old_filters


def print_calc_time(func):
    """此函数为python修饰符，用于计算目标函数执行的时间
    usage:
        @printCalcTime
        def getPricePathByNumpy(spot, volatility, tau, steps):
            simulationTimes = publicParams.simulationTimes
            dt = tau / steps
            S = np.zeros((steps+1, simulationTimes))
            S[0] = spot
        #     np.random.seed(2000)
            for t in range(1, steps+1):
                z = np.random.standard_normal(simulationTimes)
                S[t] = S[t-1] * np.exp((publicParams.rf- 0.5 * volatility **2)* dt + volatility * np.sqrt(dt)*z)
            return S
    """

    def decorator(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        print("time cost:  %.6f seconds" % total_time)
        return result

    return decorator


def log_function_call(func, info_level=logging.DEBUG, logger=None):
    """
    记录函数调用日志
    :param func:
    :return:
    """
    if logger is None:
        logger = logging.getLogger("Function_Logger")

    _dict = {
        logging.DEBUG: logging.debug,
        logging.INFO: logging.info,
        logging.WARNING: logging.warning,
        logging.ERROR: logging.error,
    }

    mes_func = _dict[info_level]

    def wrapper(*args, **kwargs):
        logger.mes_func(
            f"Calling function: {func.__name__} with args {args} and kwargs {kwargs}"
        )
        return func(*args, **kwargs)

    return wrapper
