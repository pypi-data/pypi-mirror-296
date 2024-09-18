# -*- coding: UTF-8 -*-
"""
@Name:wizgrd.py
@Auth:yujw
@Date:2023/6/5-10:39
"""
from pathlib import Path

from wz_weather_utils.micaps import open_diamond4_file

from .grid_data import GridData
from .save_type import SaveType
from .lambert_data import LambertData
import struct
import numpy as np


def open_wizgrd_03(file_path) -> LambertData:
    with open(file_path, 'rb') as f:
        c = f.read()
        fmt_header = 'ffffiifffffffff'
        x1, x2, y1, y2, nx, ny, mn, mx, delta, missing, longitude_of_central_meridian, latitude_of_projection_origin, \
            standard_parallel_lat1, standard_parallel_lat2, earth_radius = struct.unpack(fmt_header, c[8:68])
        fmt_array = '%dH' % (nx * ny)
        array = np.array(struct.unpack(
            fmt_array, c[68:]), np.float32).reshape(ny, nx)

        array = array * delta + mn

    lambert = LambertData(array, x1, x2, y1, y2, latitude_of_projection_origin,
                          longitude_of_central_meridian,
                          standard_parallel_lat1, standard_parallel_lat2, earth_radius)

    return lambert


def open_wizgrd_04(file_path) -> GridData:
    with open(file_path, 'rb') as f:
        cc = f.read()
        fmt_header = "8si6f3i4fii"
        title, version, lon0, lon1, lat0, lat1, dx, dy, nx, ny, length, mn, mx, delta, missing, = struct.unpack(
            fmt_header, cc[0:72])
    return None


def open_wizgrd_02(file_path):
    with open(file_path, 'rb') as f:
        c = f.read()
        fmt_header = 'iffffffiiiffff'
        version, lon0, lon1, lat0, lat1, dx, dy, nx, ny, length, mn, mx, delta, missing = struct.unpack(
            fmt_header, c[8:64])
        fmt_array = '%dH' % (nx * ny)
        array = np.array(struct.unpack(
            fmt_array, c[64:]), dtype=float).reshape(ny, nx)

        array = np.where(array == 65535, missing, array * delta + mn)

        grd_data = GridData(lat0, lat1, lon0, lon1, nx, ny, dx, dy, array)

    return grd_data


def open_wizgrd_file(file_path):
    if not Path(file_path).exists():
        return None
    try:
        with open(file_path, "rb") as f:
            flag = f.read(8).decode("utf-8")
        save_type = SaveType[flag]
        if save_type == SaveType.WIZGRD03:
            return open_wizgrd_03(file_path)
        if save_type == SaveType.WIZGRD02:
            return open_wizgrd_02(file_path)
    except Exception:
        ...

    return None


def open_grid_file(file_path, data_type):
    if data_type == SaveType.M4:
        return open_diamond4_file(file_path)
    if data_type == SaveType.NC:
        return GridData.open_data_array(file_path)
    return open_wizgrd_file(file_path)
