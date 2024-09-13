#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 10:39
# @Author  : @Zhenxi Zhang
# @File    : logg_conf.py
# @Software: PyCharm
import logging
from logging.handlers import RotatingFileHandler
import configparser


def setup_logger(log_file="", name=None, level=logging.INFO):
    """
    配置日志记录器
    :param log_file: str - 指定日志文件路径
    :param name: str - 指定日志记录器的名字
    :param level: logger.level - logger 的消息等级，默认为logging.Info
    :return:  logger object - 消息记录器
    """

    logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    if log_file != "":
        handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def read_config(config_file, encoding="utf-8"):
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding=encoding)
    except Exception as e:
        raise Exception(f"读取配置文件{config_file}失败{e}：")

    return config
