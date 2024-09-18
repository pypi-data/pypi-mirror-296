import os
import struct
import zlib

import numpy as np
import pandas as pd


def save_wiz_sta01(pd_data: pd.DataFrame, file_path, sta_len=None, more_text: str = None, data_zip=False, zip_level=9):

    # 8字节
    flag = b"WIZSTA01"
    if sta_len is None:
        sta_len_arr = np.array([len(sta) for sta in pd_data["stationId"].values])
        sta_len = np.max(sta_len_arr)
    total = len(pd_data.values)  # 数据长度
    fix_length = 24
    keys = ",".join(list(pd_data.keys().values))
    desc_len = 0
    desc = "".encode("utf-8")
    zip_value = 1 if data_zip else 2
    if more_text:
        desc = (";" + more_text).encode("utf-8")
        desc_len = len(desc)
    data_position = len(keys) + fix_length + desc_len
    title_fmt = "=8s4i%ds%ds" % (len(keys), desc_len)
    fmt = ''.join(["%ds%df" % (sta_len, len(pd_data.keys()) - 1)] * total)
    values = pd_data.values
    values[:, 0] = [v.rjust(sta_len, " ").encode("utf-8") for v in values[:, 0]]
    values = values.flatten()
    title_result = struct.pack(title_fmt, flag, total, sta_len, data_position, zip_value, keys.encode("utf-8"), desc)
    result = struct.pack("={}".format(fmt), *values)
    if data_zip:
        result = zlib.compress(result, zip_level)
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'wb') as fl:
        fl.write(title_result)
        fl.write(result)


def open_wiz_grd_01(file_path):
    """
    flag 版本号 8字节
    total 站点总数量 4字节
    sta_len 站号的长度 4字节
    position 数据的开始位置 4字节
    :param file_path:
    :return:
    """
    fix_length = 24
    with open(file_path, "rb") as f:
        arr = f.read()
        flag, total, sta_len, position, zip_value = struct.unpack("8s4i", arr[0:fix_length])
        # 所有的要素id，固定长度到数据的起始位置，逗号隔开
        keys, = struct.unpack("=%ds" % (position - fix_length), arr[fix_length:position])
        element_msg = keys.decode("utf-8").split(";")
        elements = element_msg[0].split(",")
        msg = None
        if len(element_msg) == 2:
            msg = element_msg[1]
        # 除站号以外，其他军用float类型存储
        fmt = ('=' + ''.join(["%ds%df" % (sta_len, len(elements) - 1)] * total))
        data_rb = zlib.decompress(arr[position:]) if zip_value == 1 else arr[position:]
        values = struct.unpack(fmt, data_rb)
        values = np.array(values, dtype=object).reshape((total, len(elements)))

    values[:, 0] = np.array(values[:, 0], dtype=str)
    pd_data = pd.DataFrame(values, columns=elements)
    pd_data[elements[0]] = pd_data[elements[0]].str.strip()
    return pd_data


def open_wiz_grd_01_his(file_path):
    """
    flag 版本号 8字节
    total 站点总数量 4字节
    sta_len 站号的长度 4字节
    position 数据的开始位置 4字节
    :param file_path:
    :return:
    """
    fix_length = 20
    with open(file_path, "rb") as f:
        arr = f.read()
        flag, total, sta_len, position = struct.unpack("8s3i", arr[0:fix_length])
        # 所有的要素id，固定长度到数据的起始位置，逗号隔开
        keys, = struct.unpack("=%ds" % (position - fix_length), arr[fix_length:position])
        element_msg = keys.decode("utf-8").split(";")
        elements = element_msg[0].split(",")
        msg = None
        if len(element_msg) == 2:
            msg = element_msg[1]
        print(msg)
        # 除站号以外，其他军用float类型存储
        fmt = ('=' + ''.join(["%ds%df" % (sta_len, len(elements) - 1)] * total))  #
        values = struct.unpack(fmt, arr[position:])
        values = np.array(values, dtype=object).reshape((total, len(elements)))
    values[:, 0] = np.array(values[:, 0], dtype=str)
    return pd.DataFrame(values, columns=elements)
