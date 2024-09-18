from pathlib import Path

import pandas as pd
import re
import numpy as np
from .grid_data import GridData
import struct
from . import get_encoding

p_s = re.compile("\\s+")


def open_diamond3_file(file_path, encoding="utf8"):
    with open(file_path, "r", encoding=encoding) as content:
        lines = content.readlines()

    data = [p_s.split(line.strip()) for line in lines if len(p_s.split(line.strip())) == 5]
    data = np.array(data, dtype=object)
    df_data = pd.DataFrame({
        "stationId": np.array(data[:, 0], dtype=str),
        "lon": np.array(data[:, 1], dtype=float),
        "lat": np.array(data[:, 2], dtype=float),
        "alti": np.array(data[:, 3], dtype=float),
        "value": np.array(data[:, 4], dtype=float),
    })
    return df_data


def save_diamond3_file(file_path, pd_data, text, obs_time, encoding="utf-8"):
    np_data = np.empty((len(pd_data.values), 5), dtype=object)
    np_data[:, 0] = pd_data["stationId"].values
    np_data[:, 1] = pd_data["lon"].values
    np_data[:, 2] = pd_data["lat"].values
    np_data[:, 4] = pd_data["values"].values
    np_data[:, 3] = 0
    if "alti" in pd_data.keys():
        np_data[:, 3] = pd_data["alti"].values

    Path(file_path).parent.mkdir(parents=True,exist_ok=True)
    np.savetxt(file_path, np_data, fmt=["%s", "%.3f", "%.3f", "%.3f", "%.3f"],
               header="diamond 3 {obs_time:%Y年%m月%d日%H时}_{text}\n{obs_time:%Y %m %d %H} 1000 0 0 0 0 1 {len}".format(
                   obs_time=obs_time, text=text, len=len(np_data)), encoding=encoding, comments="")


def open_diamond12_file(file):
    with open(file, "r", encoding=get_encoding(file)) as content:
        lines = content.readlines()
    data = [p_s.split(line.strip()) for line in lines if len(p_s.split(line.strip())) == 12]
    columns = ["sta_id", "lat", "lon", "aqi", "aqi_t", "pm25", "pm10", "co", "no2", "o31h", "o38h", "so2"]
    return pd.DataFrame(data, columns=columns)


def open_diamond4_file(file: str):
    """
    打开 m4文件
    :param file:
    :return:
    """
    if not Path(file).exists():
        return None
    # 打开文件，进行解析
    with open(file, "r", encoding=get_encoding(file)) as fh:
        lines = fh.readlines()
    p = re.compile("\\s+")
    array = []
    for line in lines:
        line_arr = p.split(line.replace("\n", "").strip())
        if len(line_arr) == 1 and len(line_arr[0]) <= 0:
            continue
        if len(line_arr) <= 0:
            continue
        array.extend(line_arr)

    delt_lon = float(array[9])
    delt_lat = float(array[10])
    start_lon = float(array[11])
    end_lon = float(array[12])
    start_lat = float(array[13])
    end_lat = float(array[14])
    lon_count = int(array[15])
    lat_count = int(array[16])

    _array = np.reshape(np.array(array[22:], dtype=float), (lat_count, lon_count))
    grd_data = GridData(start_lat, end_lat, start_lon, end_lon, lon_count, lat_count, delt_lon, delt_lat, _array)
    return grd_data


def open_bin_file(file_path, lat1, lat2, lon1, lon2, dx, dy, nx, ny):
    if not Path(file_path).exists():
        return None
    with open(file_path, 'rb') as f:
        c = f.read()
        data = struct.unpack(('%df' % (len(c) / 4)), c)
    z = np.array(data).reshape(ny, nx)  # 将一维数组分成二维数组

    return GridData(lat1, lat2, lon1, lon2, nx, ny, dx, dy, z)


def open_diamond2_file(file_path, encoding="utf-8"):
    lines = read_file_as_lines(file_path, encoding)
    line_arr = []
    [line_arr.extend(p_s.split(line.strip())) for line in lines]
    sta_length = int(line_arr[8])
    data_arr = np.array(line_arr[9:], dtype=object).reshape((sta_length, 10))
    data_pd = pd.DataFrame(data_arr,
                           columns=["station_id", "lon", "lat", "alt", "sta_lev", "level", "tem", "tem_dew_diff",
                                    "win_s", "win_s"])
    for key in data_pd.keys()[1:]:
        data_pd[key] = data_pd[key].values.astype("float32")

    return data_pd


def read_file_as_lines(file_path, encoding="utf-8"):
    with open(file_path, encoding=encoding) as f:
        return f.readlines()


def open_uv_bin_file(file_path, lat1, lat2, lon1, lon2, dx, dy, nx, ny):
    if not Path(file_path).exists():
        return None
    with open(file_path, 'rb') as f:
        c = f.read()
        data = struct.unpack(('%df' % (len(c) / 4)), c)
        # 将一维数组分成二维数组
    z = np.array(data, dtype=float).reshape((2, ny, nx))

    return (GridData(lat1, lat2, lon1, lon2, nx, ny, dx, dy, z[0]),
            GridData(lat1, lat2, lon1, lon2, nx, ny, dx, dy, z[1]))
