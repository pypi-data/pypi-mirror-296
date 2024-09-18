import numpy as np
import struct
import os
from .save_type import SaveType
from pyresample.geometry import AreaDefinition
from pyresample.kd_tree import resample_nearest
from .grid_data import GridData


class LambertData:
    def __init__(self, values, x1, x2, y1, y2, latitude_of_projection_origin, longitude_of_central_meridian,
                 standard_parallel_lat1, standard_parallel_lat2, earth_radius):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.nx = len(values[0])
        self.ny = len(values)
        self.latitude_of_projection_origin = latitude_of_projection_origin
        self.longitude_of_central_meridian = longitude_of_central_meridian
        self.standard_parallel_lat1 = standard_parallel_lat1
        self.standard_parallel_lat2 = standard_parallel_lat2
        self.earth_radius = earth_radius
        self.values = values
        self.x_values = np.linspace(x1, x2, len(values[0]))
        self.y_values = np.linspace(y1, y2, len(values))
        self.grid_data: GridData = None
        self.latitudes = np.linspace(y1, y2, self.ny)
        self.longitudes = np.linspace(x1, x2, self.nx)

    def save_to_file(self, file_path, save_type=SaveType.WIZGRD03, d_time=None, desc=None, level=None, hour=None,
                     contour=" 1 10 50 1 0", m4_fmt="%.2f", nc_key="value", lat_key="latitude", lon_key="longitude"):
        # flag: "WIZGRD03"

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
        if save_type == SaveType.WIZGRD03:
            flag = b"WIZGRD03"
            missing = 65534

            # 这里最大值加1，确保正确的数据没有这个值，遇到这个值代表是缺测，为了后续还原正常数据用
            mx = self.values.max() + ((self.values.max() - self.values.min()) / 1000)
            mn = self.values.min()
            delta = (mx - mn) / (pow(2, 16) - 2)
            values = np.where(((self.values == 9999.) | (np.isnan(self.values))), np.nan, self.values)
            array = np.where(np.isnan(values), missing, ((values - mn) / delta).astype(np.ushort)).flatten()

            fmt = ('8sffffiifffffffff%dH' % len(array))
            result = struct.pack(fmt, flag, self.x1,
                                 self.x2, self.y1, self.y2, self.nx, self.ny, mn, mx, delta,
                                 missing, self.longitude_of_central_meridian, self.latitude_of_projection_origin,
                                 self.standard_parallel_lat1, self.standard_parallel_lat2, self.earth_radius, *array)
            try:
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))
            except FileExistsError:
                pass

            with open(file_path, 'wb+') as fl:
                fl.write(result)
        else:
            if self.grid_data is None:
                raise Exception("请先初始化 transform_to_latlon 函数！！！")

            self.grid_data.save_to_file(file_path, save_type, d_time, desc, level, hour, contour, fmt=m4_fmt)

    def transform_to_latlon(self, dx, dy, lat1=None, lat2=None, lon1=None, lon2=None,
                            radius_of_influence=10000, fill_value=np.nan):
        units = "km"
        if self.earth_radius > 1000000:
            units = "m"
        from pyproj import Proj, transform
        lambert_dict = {'proj': 'lcc', "lat_1": self.standard_parallel_lat1,
                        "lat_2": self.standard_parallel_lat2,
                        'lat_0': self.latitude_of_projection_origin,
                        'lon_0': self.longitude_of_central_meridian, 'a': self.earth_radius,
                        'x_0': 0, 'y_0': 0, "units": units, 'no_defs': True}

        proj_lambert = Proj(
            "+proj=lcc +lat_1={} +lat_2={} +lat_0={} +lon_0={} +x_0=0 +y_0=0 +ellps=WGS84 +units={}".format(
                self.standard_parallel_lat1, self.standard_parallel_lat2, self.latitude_of_projection_origin,
                self.longitude_of_central_meridian, units))
        # 等经纬度的投影定义
        proj_lat_lon = Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

        x_values, y_values = np.meshgrid(self.x_values, self.y_values)
        longitudes, latitudes = transform(proj_lambert, proj_lat_lon, x_values, y_values)
        _lat1, _lat2, _lon1, _lon2 = np.nanmin(latitudes), np.nanmax(latitudes), np.nanmin(longitudes), np.nanmax(
            longitudes)
        if lat1 is None:
            lat1, lat2, lon1, lon2 = np.round(_lat1, 3), np.round(_lat2, 3), np.round(_lon1, 3), np.round(_lon2, 3)
        target_extent = (_lon1, _lat1, _lon2, _lat2)  # 经纬度范围
        source_area = AreaDefinition('Source', 'Lambert Conformal Conic', 'Source',
                                     lambert_dict,
                                     len(longitudes[0]), len(latitudes), target_extent, lons=longitudes,
                                     lats=latitudes)

        lat_lon_dict = {'proj': 'latlong', 'lat_min': lat1, 'lat_max': lat2, 'lon_min': lon1, 'lon_max': lon2}
        lons = np.arange(lon1, lon2 + dx, dx)
        lats = np.arange(lat1, lat2 + dy, dy)
        lons_1, lats_1 = np.meshgrid(lons, lats)
        lat_lon_area_def = AreaDefinition(
            'wgs84', 'WGS84', 'wgs84', lat_lon_dict, len(lons), len(lats), [lon1, lat1, lon2, lat2],
            lons=lons_1, lats=lats_1)
        result_data = resample_nearest(
            source_area, self.values, lat_lon_area_def,
            radius_of_influence=radius_of_influence, fill_value=fill_value)
        self.grid_data = GridData(lat1, lat2, lon1, lon2, len(lons), len(lats), dx, dy, result_data)
