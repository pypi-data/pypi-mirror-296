# -*- coding: UTF-8 -*-
"""
@Name:__init__.py
@Auth:yujw
@Date:2024/7/25-20:13
"""

import copy
import math
import numpy as np
from metpy import calc as mp_calc
from metpy.units import units
import xarray as xr


def calc_wind_dir_and_wind_speed(u_data, v_data):
    u = u_data * units("m/s")
    v = v_data * units("m/s")
    return np.array(mp_calc.wind_direction(u, v), dtype=float), np.array(mp_calc.wind_speed(u, v), dtype=float)


def calc_relative_humidity(t_data, d_data):
    """

    :param t_data: 单位：℃
    :param d_data:单位：℃
    :return:
    """
    return np.array(mp_calc.relative_humidity_from_dewpoint(t_data * units.degC, d_data * units.degC), dtype=float)


def calc_advection(u, v, latitudes, longitudes):
    """
    计算 涡度平流，metpy
    :param dy:
    :param dx:
    :param u:
    :param v:
    :param latitudes:
    :param longitudes:
    :return:
    """
    u_data = xr.DataArray(u, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    v_data = xr.DataArray(v, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    vo = calc_vorticity(u, v, latitudes, longitudes)
    dx, dy = mp_calc.lat_lon_grid_deltas(longitudes, latitudes)
    vort_adv = mp_calc.advection(vo, u_data,
                                 v_data, dx=dx,
                                 dy=dy, x_dim="longitudes", y_dim="latitudes") * 1e9
    return np.array(vort_adv, dtype=float)


def calc_vorticity(u, v, latitudes, longitudes):
    u_data = xr.DataArray(u, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    v_data = xr.DataArray(v, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    lon, lat = np.meshgrid(longitudes, latitudes)
    dx, dy = mp_calc.lat_lon_grid_deltas(longitudes, latitudes)
    f = mp_calc.coriolis_parameter(np.deg2rad(lat)).to(units('1/sec'))
    vo = mp_calc.vorticity(u_data, v_data, dx=dx, dy=dy) + f
    vo = vo * units('1/s')
    return vo


def calc_theta(tmp, dpt, pres):
    tmp = tmp * units.degC
    dpt = dpt * units.degC
    pres = pres * units("hPa")
    return mp_calc.equivalent_potential_temperature(pres, tmp, dpt).m


def calc_ivt_single_level(spfh, wsp):
    return wsp * spfh / 9.8


def calc_vapor_flux_and_vapor_flux_divergence(q, u, v, latitudes, longitudes):
    wd, ws = calc_wind_dir_and_wind_speed(u, v)
    q = q * units('g/kg')
    vapor_flux = calc_ivt_single_level(q, ws).m
    u = u * units('m/s')
    v = v * units('m/s')
    dx, dy = mp_calc.lat_lon_grid_deltas(longitudes, latitudes)

    return vapor_flux, mp_calc.divergence(u, v, dx=dx, dy=dy).m


def calc_at(t2m, r2m, u10, v10):
    """
    体感温度
    :param t2m:
    :param r2m:
    :param u10:
    :param v10:
    :return:
    """
    p_vapor_p = (r2m / 100.) * 6.105 * (math.e ** (17.27 * t2m / (237.7 + t2m)))
    wd, ws = calc_wind_dir_and_wind_speed(u10, v10)
    at_p = 1.07 * t2m + 0.2 * p_vapor_p - 0.65 * ws - 2.7
    return at_p


def calc_tem_advection(t, u, v, latitudes, longitudes):
    """
    :param t: 气温 degC
    :param u:
    :param v:
    :param latitudes:
    :param longitudes:
    :return:
    """
    u_data = xr.DataArray(u, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    v_data = xr.DataArray(v, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    t_data = xr.DataArray(t, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("degC")

    dx, dy = mp_calc.lat_lon_grid_deltas(longitudes, latitudes)

    values = mp_calc.advection(t_data, u_data, v_data, dx=dx, dy=dy, x_dim="longitude", y_dim="latitude")
    values = values.values * -100000
    return values


def calc_tem_delta_decline_rate(lev1, lev2, t1, t2):
    """
    递减率计算
    :param lev1: 层次 hPa
    :param lev2: 要减去的层次
    :param t1: 温度1
    :param t2: 要减去的温度
    :return:
    """
    height1 = mp_calc.pressure_to_height_std(lev1 * units("hPa")).to("m").m
    height2 = mp_calc.pressure_to_height_std(lev2 * units("hPa")).to("m").m
    t_delta = np.array(t1) - np.array(t2)
    decline_rate = t_delta / (height1 - height2) * 100

    return decline_rate


def calc_tem_delta_decline_rate_2(lev1, lev2, t1, t2):
    """
    递减率计算
    :param lev1: 高度1
    :param lev2: 要减去的高度
    :param t1: 温度1
    :param t2: 要减去的温度
    :return:
    """
    # 标准大气压
    height1 = mp_calc.pressure_to_height_std(lev1 * units("hPa"))
    height2 = mp_calc.pressure_to_height_std(lev2 * units("hPa"))
    t_delta = np.array(t1) - np.array(t2)
    decline_rate = t_delta / (height1 - height2) * 100
    return decline_rate


def calc_w_transform(w_data, tmp_data, level):
    return mp_calc.vertical_velocity(w_data * units("Pa/s"), level * units.hPa, tmp_data * units.degC).m


def calc_vorticity(u, v, latitudes, longitudes):
    u_data = xr.DataArray(u, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")
    v_data = xr.DataArray(v, coords=[latitudes, longitudes], dims=["latitude", "longitude"]) * units("m/s")

    dx, dy = mp_calc.lat_lon_grid_deltas(longitudes, latitudes)

    values = mp_calc.vorticity(u_data, v_data, dx=dx, dy=dy, x_dim="longitude", y_dim="latitude")
    u_data.close()
    v_data.close()
    return values.values


def calc_dpt(t_data, r_data):
    """
    计算露点温度
    :param t_data:
    :param r_data:
    :return:
    """
    if t_data.max() >= 273.15 or t_data.min() >= 100:
        t_data = t_data - 273.15

    if r_data.max() <= 2:
        r_data = r_data * 100

    return mp_calc.dewpoint_from_relative_humidity(t_data * units("degC"), r_data * units.percent).m


def calc_wind_shear(dataset: xr.Dataset, level_key="level", u_key="u", v_key="v", lat_key="lat", lon_key="lon",
                    height: int = 3000):
    from metpy.calc import bulk_shear
    from metpy.units import units
    levels = dataset[level_key].values
    heights = mp_calc.pressure_to_height_std(levels * units("hPa")).to("m").m * units.m
    shear = bulk_shear(levels * units("hPa"), dataset["u"].values * units.knot, dataset["v"].values * units.knot,
                       heights,
                       depth=height * units.m, bottom=heights[0])


def calc_hot_index(t2m, r2m):
    """
    :param t2m 两米气温
    :param r2m 两米相对湿度
    :return:
    """
    t2m_tmp = copy.copy(t2m)
    r2m_tmp = copy.copy(r2m)
    if np.nanmin(t2m) >= 100:
        t2m_tmp = t2m_tmp - 273.15
    if np.nanmax(r2m_tmp) <= 2:
        r2m_tmp = r2m_tmp * 100

    c1, c2, c3, c4, c5, c6, c7, c8, c9 = (
        -8.78469475556, 1.61139411, 2.33854883889,
        -0.14611605, -0.012308094, -0.0164248277778, 2.211732 * math.pow(10, -3),
        7.2546 * math.pow(10, -4), -3.582 * math.pow(-10, 6))

    return c1 + c2 * t2m_tmp + c3 * r2m_tmp + c4 * t2m_tmp * r2m_tmp + c5 * np.square(t2m_tmp) + c6 * np.square(
        r2m_tmp) + c7 * np.square(t2m_tmp) * r2m_tmp + c8 * t2m_tmp * np.square(r2m_tmp) + c9 * np.square(
        t2m_tmp) * np.square(r2m_tmp)


def effective_layer(p, t, td, h, height_layer=False):
    from metpy.calc import cape_cin, parcel_profile
    from metpy.units import units

    pbot = None

    for i in range(p.shape[0]):
        prof = parcel_profile(p[i:], t[i], td[i])
        sbcape, sbcin = cape_cin(p[i:], t[i:], td[i:], prof)
        if sbcape >= 100 * units('J/kg') and sbcin > -250 * units('J/kg'):
            pbot = p[i]
            hbot = h[i]
            bot_idx = i
            break
    if not pbot:
        return None, None

    for i in range(bot_idx + 1, p.shape[0]):
        prof = parcel_profile(p[i:], t[i], td[i])
        sbcape, sbcin = cape_cin(p[i:], t[i:], td[i:], prof)
        if sbcape < 100 * units('J/kg') or sbcin < -250 * units('J/kg'):
            ptop = p[i]
            htop = h[i]
            break

    if height_layer:
        return hbot, htop
    else:
        return pbot, ptop


from metpy.calc import storm_relative_helicity, pressure_to_height_std


class CalcMetH:
    def __init__(self, u_data, v_data, gh_data, pressure, depth=3000, bottom=0):
        self.height = pressure_to_height_std(gh_data * units.hPa).to("m").m
        self.u_data = np.array(u_data, dtype=float)
        self.v_data = np.array(v_data, dtype=float)
        self.pressure = pressure * units.hPa
        self.bottom = bottom
        self.depth = depth
        print(self.height.shape)

    def __calc_srh(self, height, u, v):
        return storm_relative_helicity(height, u, v, depth=self.depth * units.m, bottom=self.bottom * units.m)[0].m

    def calc_storm_relative_hel(self):
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=120)
        h_c = lambda h, u, v: self.__calc_srh(h, u, v)

        results = [self.__append(pool, idx, idy, h_c) for idx in range(501) for idy in range(301)]
        pool.close()
        pool.join()

        values = [res.get() for res in results]
        print(np.array(values, dtype=float).reshape((301, 501)))

    def __append(self, pool, idx, idy, func):
        return pool.apply_async(func, (
            self.height[:, idy, idx] * units.m, self.u_data[:, idy, idx] * units("m/s"),
            self.v_data[:, idy, idx] * units("m/s")))
