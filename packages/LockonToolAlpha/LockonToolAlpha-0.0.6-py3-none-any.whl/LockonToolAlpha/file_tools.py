#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/7 10:35
# @Author  : @Zhenxi Zhang
# @File    : file_tools.py
# @Software: PyCharm

import datetime
import os
import shutil


def get_fp_creation_time(fp):
    """
    获取指定位置文件创建的时间
    :param fp: 文件路径
    :type fp: str
    :return: 文件创建的时间
    :rtype:  datetime.datetime
    """
    if not os.path.exists(fp):
        raise ValueError("文件夹路径不存在,先导出文件夹到桌面")
    # 获取文件的创建时间戳
    creation_time = os.path.getctime(fp)

    # 将时间戳转换为本地时间
    dt_object = datetime.datetime.fromtimestamp(creation_time)

    return dt_object


def path2path(src_fp, dst_fp, operation, cpy_type="replace"):
    operation_list = ["COPY", "MOVE"]
    if operation not in operation_list:
        raise ValueError("operation must be one of %s" % operation_list)

    if os.path.isdir(src_fp):
        fp_type = "DIR"
    else:
        fp_type = "FILE"

    if fp_type == "DIR":
        if operation == "COPY":
            return _copy_dir2path(src_fp, dst_fp, cpy_type)
        elif operation == "MOVE":
            return _move_dir2path(src_fp, dst_fp, cpy_type)
    elif fp_type == "FILE":
        if operation == "COPY":
            return _copy_file2path(src_fp, dst_fp, cpy_type)
        elif operation == "MOVE":
            return _move_file2path(src_fp, dst_fp, cpy_type)


def _copy_dir2path(src_dir_fp, dst_dir_fp, cpy_type="replace"):
    """
    复制文件夹到指定位置
    :param src_dir_fp: 源文件夹路径
    :type src_dir_fp: str
    :param dst_dir_fp: 目标文件夹路径
    :type dst_dir_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_dir_fp):
        shutil.rmtree(dst_dir_fp)
    shutil.copytree(src_dir_fp, dst_dir_fp)
    return f"Successfully copied {src_dir_fp} to {dst_dir_fp}"


def _move_dir2path(src_dir_fp, dst_dir_fp, cpy_type="replace"):
    """
    移动文件夹到指定位置
    :param src_dir_fp: 源文件夹路径
    :type src_dir_fp: str
    :param dst_dir_fp: 目标文件夹路径
    :type dst_dir_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_dir_fp):
        shutil.rmtree(dst_dir_fp)
    shutil.move(src_dir_fp, dst_dir_fp)
    return f"Successfully moved {src_dir_fp} to {dst_dir_fp}"


def _move_file2path(src_fp, dst_fp, cpy_type="replace"):
    """
    移动文件到指定位置
    :param src_fp: 源文件路径
    :type src_fp: str
    :param dst_fp: 目标文件路径
    :type dst_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_fp):
        os.remove(dst_fp)
    shutil.move(src_fp, dst_fp)
    return f"Successfully moved {src_fp} to {dst_fp}"


def _copy_file2path(src_fp, dst_fp, cpy_type="replace"):
    """
    复制文件到指定位置
    :param src_fp: 源文件路径
    :type src_fp: str
    :param dst_fp: 目标文件路径
    :type dst_fp: str
    :param cpy_type: 复制类型，replace表示替换，append表示追加
    :type cpy_type: str
    :return: 复制结果
    :rtype: str
    """
    types = ["replace", "append"]
    if cpy_type not in types:
        raise ValueError("cpy_type must be one of %s" % types)
    if cpy_type == "replace" and os.path.exists(dst_fp):
        os.remove(dst_fp)
    shutil.copy2(src_fp, dst_fp)
    return f"Successfully copied {src_fp} to {dst_fp}"
