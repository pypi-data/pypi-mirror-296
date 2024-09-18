# coding=utf-8
import zlib

import xarray as xr
import numpy as np
import os
import struct
from .save_type import SaveType
from pathlib import Path


class GridData(object):
    MISS = 9999.

    def __init__(self, lat1, lat2, lon1, lon2, nx, ny, dx, dy, values):

        self.latitudes = np.linspace(lat1, lat2, ny)
        self.longitudes = np.linspace(lon1, lon2, nx)
        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.nx = nx
        self.ny = ny
        self.dx = dx
        self.dy = dy
        self.grd_attrs = dict(lat1=lat1, lat2=lat2, lon1=lon1, lon2=lon2, nx=nx, ny=ny, dx=dx, dy=dy)
        self.values = np.array(values, dtype=float)
        self.xr_data = xr.DataArray(self.values, coords=[self.latitudes, self.longitudes],
                                    dims=["latitude", "longitude"])

    def __update_grd_attr(self):
        self.grd_attrs.update(lat1=self.lat1)
        self.grd_attrs.update(lat2=self.lat2)
        self.grd_attrs.update(lon2=self.lon2)
        self.grd_attrs.update(lon1=self.lon1)
        self.grd_attrs.update(dx=self.dx)
        self.grd_attrs.update(dy=self.dy)

    def interp(self, lat1, lat2, lon1, lon2, dx=None, dy=None, nx=None, ny=None, method="linear"):
        if dx:
            self.latitudes = np.arange(lat1, lat2 + dy, dy)
            self.longitudes = np.arange(lon1, lon2 + dx, dx)
            self.nx = len(self.longitudes)
            self.ny = len(self.latitudes)
            self.dx = dx
            self.dy = dy
        if ny:
            self.latitudes = np.linspace(lat1, lat2, ny)
            self.longitudes = np.linspace(lon1, lon2, nx)
            self.dx = round(self.latitudes[1] - self.latitudes[0], 2)
            self.dy = round(self.longitudes[1] - self.longitudes[0], 2)
            self.nx = nx
            self.ny = ny

        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.__update_grd_attr()
        self.values = self.xr_data.interp(latitude=self.latitudes, longitude=self.longitudes, method=method).values

    def interp_one(self, lat, lon):
        return self.xr_data.interp(latitude=lat, longitude=lon).values

    def crop(self, lat1, lat2, lon1, lon2, ):
        xr_data = self.xr_data
        if self.lat2 < self.lat1 and lat1 < lat2:
            xr_data = self.xr_data.sortby('latitude')
        elif self.lat1 < self.lat2 and lat2 < lat1:
            xr_data = self.xr_data.sortby('latitude', ascending=False)
        crop_data = xr_data.sel(latitude=slice(lat1, lat2), longitude=slice(lon1, lon2))
        self.values = crop_data.values
        self.latitudes = crop_data["latitude"].values
        self.longitudes = crop_data["longitude"].values
        self.lat1 = np.round(self.latitudes[0], 3)
        self.lat2 = np.round(self.latitudes[-1], 3)
        self.lon1 = np.round(self.longitudes[0], 3)
        self.lon2 = np.round(self.longitudes[-1], 3)
        self.nx = len(self.longitudes)
        self.ny = len(self.latitudes)
        self.__update_grd_attr()

    def save_to_file(self, file_path, save_type=SaveType.BIN, d_time=None, desc=None, level=None, hour=None,
                     contour=" 1 10 50 1 0", fmt="%.2f", lat_key="lat", lon_key="lon", dtime_key="dtime", dtime=0,
                     value_key="data0"):

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if save_type == SaveType.BIN:
            array = np.array(self.values).reshape(-1, )
            array_byte = struct.pack("%df" % (len(array)), *array)
            with open(file_path, 'wb+') as fl:
                fl.write(array_byte)

        if save_type == SaveType.M4:
            if d_time is None or desc is None or level is None or hour is None:
                raise Exception("{d_time,desc,level,hour}的参数不能为空!!!")

            dx, dy, nx, ny, lon1, lon2, lat1, lat2 = self.dx, self.dy, self.nx, self.ny, self.lon1, self.lon2, self.lat1, self.lat2
            level = "9999" if level is None else level
            np.savetxt(file_path, self.values, fmt=fmt, comments="",
                       header=
                       f"diamond 4 {d_time:%Y年%m月%d日%H时}{hour:03d}时效_{desc}\n{d_time:%Y %m %d %H} {hour} {level} {dx:.3f} {dy:.3f} {lon1} {lon2} {lat1} {lat2} {nx} {ny} {contour}",
                       encoding="utf-8")

        if save_type == SaveType.WIZGRD02:
            self.__save_wiz_grd02(file_path)

        if save_type == SaveType.NC:
            self.__save_nc_file_for_data_array(file_path, lat_key, lon_key, time_key=dtime_key, dtime=dtime,
                                               value_key=value_key)

    def __save_wiz_grd02(self, file_path):
        # flag: "WIZGRD02"

        #  * 文件头大小，格式：<br>
        #  * 文件格式标记： 8，string WIZGRD02<br>
        #  * 版本号： 4，int<br>
        #  * 经度0： 4，float<br>
        #  * 经度1： 4，float<br>
        #  * 维度0： 4，float<br>
        #  * 维度1： 4，float<br>
        #  * 经度间隔：4，float<br>
        #  * 维度间隔：4，float<br>
        #  * 经度列数：4，int<br>
        #  * 维度行数：4，int<br>
        #  * 数据长度：4，int<br>
        #  * 最小值 4， float<br>
        #  * 最大值 4，float<br>
        #  * 数据精度 4， float<br>
        #  * 缺测值： 4， float<br>
        #  * -----------------<br>
        #  * 共：64字节
        # 8siffffffiiffff
        flag = b"WIZGRD02"
        version = 2
        length = 1

        # 这里最大值加1，确保正确的数据没有这个值，遇到这个值代表是缺测，为了后续还原正常数据用
        mx = np.nanmax(self.values) + ((np.nanmax(self.values) - np.nanmin(self.values)) / 1000)
        mn = np.nanmin(self.values)
        delta = (mx - mn) / (pow(2, 16) - 2)
        values = np.where(((self.values == self.MISS) | (np.isnan(self.values))), np.nan, self.values)
        array = np.where(np.isnan(values), 65535, ((values - mn) / delta))
        array = array.astype(np.ushort).flatten()
        fmt = ('8siffffffiiiffff%dH' % len(array))
        result = struct.pack(fmt, flag, version, self.lon1,
                             self.lon2, self.lat1, self.lat2, self.dx, self.dy, int(self.nx), int(self.ny), length, mn,
                             mx, delta,
                             self.MISS, *array)

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb+') as fl:
            fl.write(result)

    def save_wiz_grd04(self, file_path, data_type=float, if_zlib=1, zlib_level=4):
        #  * 文件头大小，格式：<br>
        #  * 文件格式标记： 8，string WIZGRD02<br>
        #  * 版本号： 4，int<br>
        #  * 经度0： 4，float<br>
        #  * 经度1： 4，float<br>
        #  * 维度0： 4，float<br>
        #  * 维度1： 4，float<br>
        #  * 经度间隔：4，float<br>
        #  * 维度间隔：4，float<br>
        #  * 经度列数：4，int<br>
        #  * 维度行数：4，int<br>
        #  * 数据长度：4，int<br>
        #  * 最小值 4， float<br>
        #  * 最大值 4，float<br>
        #  * 数据精度 4， float<br>
        #  * 缺测值： 4， float<br>
        #  * 数据类型  ushort 1 | char 2
        #  * 是否启用zlib压缩 启用 0 | 不启用 1
        # 48s 总长度120减去72个
        # 8 + 4 +24 + 12 + 16 + 8
        flag = b"WIZGRD04"
        version = 4
        data_fmt = "8si6f3i4fii"
        total_fmt = "48s"
        title_fmt = f"{data_fmt}{total_fmt}"
        if data_type not in [float, int]:
            raise Exception("无法匹配的数据类型")
        result_data_type = 1
        if data_type == float:
            # 这里最大值加1，确保正确的数据没有这个值，遇到这个值代表是缺测，为了后续还原正常数据用
            mx = np.nanmax(self.values) + ((np.nanmax(self.values) - np.nanmin(self.values)) / 1000)
            mn = np.nanmin(self.values)
            delta = (mx - mn) / (pow(2, 16) - 2)
            values = np.where(((self.values == self.MISS) | (np.isnan(self.values))), np.nan, self.values)
            array = np.where(np.isnan(values), 65535, ((values - mn) / delta))
            array = array.astype(np.ushort).flatten()
            data_format = f"{len(array)}H"
        else:
            mx = 0.
            mn = 0.
            delta = 0.
            values = np.where(((self.values == self.MISS) | (np.isnan(self.values))), np.nan, self.values)
            array = np.where(np.isnan(values), 255, values)
            array = array.astype(np.char).flatten()
            result_data_type = 2
            data_format = f"{len(array)}B"

        length = len(array)
        title_result = struct.pack(title_fmt, flag, version, self.lon1, self.lon2, self.lat1, self.lat2, self.dx,
                                   self.dy,
                                   int(self.nx), int(self.ny), length, mn, mx, delta, self.MISS, result_data_type,
                                   if_zlib, b" " * 48)

        data_result = struct.pack(data_format, *array)

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if if_zlib == 0:
            data_result = zlib.compress(data_result, level=zlib_level)
        with open(file_path, 'wb+') as fl:
            fl.write(title_result)
            fl.write(data_result)

    def transform_to180(self):
        latitudes = np.linspace(self.lat1, self.lat2, self.ny)
        longitudes = np.linspace(self.lon1, self.lon2, self.nx)
        grd_data = xr.DataArray(self.values, coords=[latitudes, longitudes], dims=["latitude", "longitude"])
        # 此种情况下，不需要做-180-180的转换
        if (self.lon1 < 0 and self.lon2 <= 180) or (self.lon1 >= 0 and self.lon2 < 180):
            return GridData(self.lat1, self.lat2, self.lon1, self.lon2, self.nx, self.ny, self.dx, self.dy, self.values)
        lon_0 = grd_data["longitude"].values[0]
        lon_0_data = None
        if lon_0 != 0:
            lon_0_data = xr.DataArray(grd_data.sel(longitude=lon_0).values.reshape((len(latitudes), 1)),
                                      coords=[latitudes, [0]], dims=["latitude", "longitude"])
        lon_final_data = None
        lon_final = grd_data["longitude"].values[-1]
        if lon_final != 360:
            lon_final_data = xr.DataArray(grd_data.sel(longitude=lon_final).values.reshape((len(latitudes), 1)),
                                          coords=[latitudes, [360]], dims=["latitude", "longitude"])

        grd_data['longitude'] = xr.where(grd_data['longitude'] > 180, grd_data['longitude'] - 360,
                                         grd_data['longitude'])

        if lon_0_data is not None:
            grd_data = xr.concat([grd_data, lon_0_data], dim="longitude")
        if lon_final_data is not None:
            grd_data = xr.concat([grd_data, lon_final_data], dim="longitude")

        copy_data = grd_data.sortby("longitude")

        lon1, lon2 = copy_data["longitude"].values[0], copy_data["longitude"].values[-1]

        return GridData(self.lat1, self.lat2, lon1, lon2, len(copy_data['longitude'].values),
                        len(copy_data["latitude"].values), self.dx, self.dy,
                        copy_data.values)

    def __save_nc_file_for_dataset(self, file_path, nc_key, lat_key, lon_key):
        grd_data = xr.Dataset({nc_key: ([lat_key, lon_key], self.values)},
                              coords={lat_key: self.latitudes, lon_key: self.longitudes})
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        grd_data.to_netcdf(file_path, encoding={nc_key: {"zlib": True}}, engine="netcdf4")

    def __save_nc_file_for_data_array(self, file_path, lat_key, lon_key, time_key="dtime", dtime=0, value_key="data0"):
        grd_data = xr.DataArray([self.values], coords=[[dtime], self.latitudes, self.longitudes],
                                dims=[time_key, lat_key, lon_key], name=value_key)
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        grd_data.to_netcdf(file_path, engine="netcdf4")

    @classmethod
    def open_data_array(cls, file_path, lat_key="lat", lon_key="lon"):
        xr_data = xr.open_dataarray(file_path)
        xr_data = xr_data.sortby(lat_key)
        xr_data = xr_data.sortby(lon_key)
        latitudes = xr_data[lat_key].values
        longitudes = xr_data[lon_key].values
        lat1, lat2 = latitudes[0], latitudes[-1]
        lon1, lon2 = longitudes[0], longitudes[-1]
        dx = np.round(longitudes[1] - longitudes[0], 2)
        dy = np.round(longitudes[1] - longitudes[0], 2)
        grd_data = GridData(lat1, lat2, lon1, lon2, len(longitudes), len(latitudes), dx, dy,
                            xr_data.values.squeeze())
        xr_data.close()
        return grd_data
