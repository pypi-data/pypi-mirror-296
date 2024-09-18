# -*- coding: UTF-8 -*-
"""
@Name:cma_connect.py
@Auth:yujw
@Date:2024/8/14-下午5:06
"""
import requests
from wz_weather_utils.logging import logger
import pandas as pd


class CmaConnect:
    def __init__(self, data_code, interface_id, address, cma_user, cma_passwd):
        # 根据单个时间
        self.url = "http://%s/music-ws/api?serviceNodeId=NMIC_MUSIC_CMADAAS&userId=%s" \
                   "&pwd=%s&interfaceId=%s&dataCode=%s" \
                   "&elements={elements}&{time_key}={times}&dataFormat=json" % (
                       address, cma_user, cma_passwd, interface_id, data_code)

        # 根据自定义参数
        self.multi_url = "http://%s/music-ws/api?serviceNodeId=NMIC_MUSIC_CMADAAS&userId=%s" \
                         "&pwd=%s&interfaceId=%s&dataCode=%s" \
                         "&dataFormat=json&{multi}" % (
                             address, cma_user, cma_passwd, interface_id, data_code)
        # 根据时间范围
        self.range_url = "http://%s/music-ws/api?serviceNodeId=NMIC_MUSIC_CMADAAS&userId=%s" \
                         "&pwd=%s&interfaceId=%s&dataCode=%s" \
                         "&elements={elements}" \
                         "&timeRange={time_range}&dataFormat=json" % (
                             address, cma_user, cma_passwd, interface_id, data_code)
        self.blag = False

    def get_time_range_data(self, elements, start_time, end_time) -> pd.DataFrame:
        """
        根据时间范围获取数据
        :param elements:定义好的要素
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: pd.DataFrame
        """
        time_range = "[{:%Y%m%d%H}0000,{:%Y%m%d%H}0000]".format(start_time, end_time)
        http_url = self.range_url.format(elements=elements, time_range=time_range)
        print(http_url)
        return self.get_url_data(http_url)

    def get_obs_data(self, elements, start_time, date_format="{:%Y%m%d%H}0000", time_key="time") -> pd.DataFrame:
        """
        根据单个时间获取
        :param time_key:
        :param date_format:
        :param elements: 定义好的要素
        :param start_time: 开始时间
        :return: pd.DataFrame
        """
        times = date_format.format(start_time)
        http_url = self.url.format(elements=elements, times=times, time_key=time_key)
        return self.get_url_data(http_url)

    def get_multi_params_data(self, **kwargs):
        """
        定义好固定参数，将其他参数按传入的方式定义好，灵活方便
        :param kwargs:
        :return:
        """
        params = ""
        for ik, iv in kwargs.items():
            params = params + "{}={}&".format(ik, iv)

        http_url = self.multi_url.format(multi=params)
        logger.info(http_url)
        return self.get_url_data(http_url)

    def get_url_data(self, url):
        """
        拿到url，通过requests拿到返回的json数据
        :param url:
        :return:
        """
        self.blag = True
        req_conn = Request(url)
        logger.info(req_conn.get_json_data()["returnMessage"])
        ds_data = req_conn.get_json_data()
        if "DS" in ds_data.keys():
            return pd.DataFrame(ds_data["DS"])

        return None


class Request:
    def __init__(self, url, method="get"):
        self.http = requests.request(method, url, timeout=600)
        if self.http.status_code != 200:
            raise Exception(self.http.text)

    def get_content(self):
        return self.http.content

    def get_json_data(self):
        return self.http.json()

    def __del__(self):
        try:
            self.http.close()
        except AttributeError:
            pass
