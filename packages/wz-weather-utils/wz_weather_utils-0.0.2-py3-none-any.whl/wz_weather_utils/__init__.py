# -*- coding: UTF-8 -*-
"""
@Name:__init__.py
@Auth:yujw
@Date:2024/7/25-20:13
"""
import json
from datetime import datetime, timedelta
from enum import Enum
import chardet


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        if len(f.read()) < 248:
            _ch = f.read()
        else:
            _ch = f.read(248)
        return chardet.detect(_ch)['encoding']


def replace_path(path_format: str, d_time, cst_hour, ele, level="", ens=None):
    """
    用于路径替换
    :param path_format:
    :param d_time:
    :param cst_hour:
    :param ele:
    :param level:
    :param ens:
    :return:
    """
    ens = "" if ens is None else ens
    ens = ens if isinstance(ens, str) else "%02d"
    level = str(level) if isinstance(level, int) else level
    level = level if level != "9999" else ""
    return path_format.format(report_time=d_time, cst_hour=cst_hour, ens=ens, element=ele, level=level)


def read_file_to_dict(file_path):
    """
    读取json文件返回json
    :param file_path:
    :return:
    """
    with open(file_path, "r", encoding=get_encoding(file_path)) as f:
        return json.load(f)


class TimeZone(Enum):
    GMTO = "GMT0"
    GMT8 = "GMT8"


def get_report_time(time_interval: dict, time_zone: TimeZone):
    report_time = datetime.now()
    if time_zone == TimeZone.GMTO:
        report_time = datetime.utcnow()
    minute = report_time.minute
    if "hours" in time_interval.keys():
        report_time = datetime(report_time.year, report_time.month, report_time.day,
                               report_time.hour - report_time.hour % time_interval.get("hours"))
    if "minutes" in time_interval.keys():
        report_time = datetime(report_time.year, report_time.month, report_time.day,
                               report_time.hour,
                               minute=minute - minute % time_interval.get("minutes"))

    if time_zone == TimeZone.GMT8:
        report_time = report_time + timedelta(hours=8)
    return report_time
