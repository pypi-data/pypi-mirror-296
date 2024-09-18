# -*- coding: UTF-8 -*-
"""
@Name:open_scmoc.py
@Auth:yujw
@Date:2023/8/18-10:05
"""
import numpy as np
import re

import pandas as pd

from .logging import logger
import chardet
from datetime import datetime

p_s = re.compile("\\s+")


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read(248))['encoding']


class GowfsScmoc:
    def __init__(self, file_path):
        with open(file_path, "r", encoding=get_encoding(file_path)) as f:
            self.lines = f.readlines()

        self.d_type = p_s.split(self.lines[3])[0]

        self.date_time = datetime.strptime(p_s.split(self.lines[3])[1], "%Y%m%d%H")
        self.station_number = int(self.lines[4].strip())
        self.columns = ["时效", "温度", "相对湿度", "风向", "风速", "气压", "降水量", "总云量", "低云量", "天气现象",
                        "能见度", "最高气温", "最低气温", "最大相对湿度", "最小相对湿度", "累计降水量_24小时",
                        "累计降水量_12小时", "总云量_12小时", "低云量_12小时", "天气现象_12小时", "风向_12小时",
                        "风速_12小时"]
        self.data_type = [np.int32] + [np.float32] * (len(self.columns) - 1)

    def to_dict_dataframe(self):
        """
        数据从第五行开始
        :return: pd.DataFrame
        """
        data_row = 5
        sta_details = []
        all_rows_dict = {}
        while True:
            sta1 = p_s.split(self.lines[data_row])
            sta_details.append([*sta1[0:4]])
            count1 = int(sta1[4])
            rows = [p_s.split(row.strip()) for row in self.lines[data_row + 1: data_row + count1 + 1]]
            sta_data = pd.DataFrame(rows, columns=self.columns)

            for d_type, col in zip(self.data_type, self.columns):
                sta_data[col] = sta_data[col].values.astype(d_type)
            sta_data.insert(0, "海拔高度", np.array([float(sta1[3])] * len(sta_data.values), dtype=float))
            sta_data.insert(0, "纬度", np.array([float(sta1[2])] * len(sta_data.values), dtype=float))
            sta_data.insert(0, "经度", np.array([float(sta1[1])] * len(sta_data.values), dtype=float))
            sta_data.insert(0, "站号", np.array([sta1[0]] * len(sta_data.values), dtype=str))

            all_rows_dict[sta1[0]] = sta_data
            data_row += count1 + 1
            if len(all_rows_dict.keys()) == self.station_number:
                break

        return all_rows_dict

    def to_dataframe_all(self):
        """
        将所有的站合并在一起返回
        :return:
        """
        all_rows_dict = self.to_dict_dataframe()
        dataframe_all = [val for key, val in all_rows_dict.items()]
        concat_data = pd.concat(dataframe_all, ignore_index=True)
        return concat_data
