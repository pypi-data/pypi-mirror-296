# https://blog.csdn.net/weixin_43931979/article/details/130191956
# https://blog.csdn.net/Tonque/article/details/113615135

import math
from pyproj import Proj
from pyproj import Transformer

pi = 3.1415926535897932384626  # 圆周率π
x_pi = pi * 3000.0 / 180.0  # 圆周率转换量
a = 6378245.0  # 卫星椭球坐标投影到平面地图坐标系的投影因子
ee = 0.00669342162296594323  # 椭球偏心率


def _out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


def _transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转火星坐标系(GCJ - 02)
    :param lng: WGS84坐标系的经度
    :param lat: WGS84坐标系的纬度
    :return:
    """
    # 判断是否在国内
    if _out_of_china(lng, lat):
        return lng, lat
    d_lat = _transform_lat(lng - 105.0, lat - 35.0)
    d_lng = _transform_lng(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * pi
    magic = math.sin(rad_lat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * pi)
    d_lng = (d_lng * 180.0) / (a / sqrt_magic * math.cos(rad_lat) * pi)
    mg_lat = lat + d_lat
    mg_lng = lng + d_lng
    return mg_lng, mg_lat


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转WGS84
    :param lng: 火星坐标系的经度
    :param lat: 火星坐标系纬度
    :return:
    """
    # 判断是否在国内
    if _out_of_china(lng, lat):
        return lng, lat
    d_lat = _transform_lat(lng - 105.0, lat - 35.0)
    d_lng = _transform_lng(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * pi
    magic = math.sin(rad_lat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * pi)
    d_lng = (d_lng * 180.0) / (a / sqrt_magic * math.cos(rad_lat) * pi)
    mg_lat = lat + d_lat
    mg_lng = lng + d_lng
    return [lng * 2 - mg_lng, lat * 2 - mg_lat]


def from_geo_to_proj(lon, lat, crs_id=None):
    """
    只能从geo向proj转换，其中proj是CGCS2000系列
    无法进行带有带号的转换
    """
    if crs_id:
        pass
    else:
        crs_base = 4534
        if 73.5 < lon < 136.5:
            result = divmod(lon - 75, 3)

            shang = result[0]
            yu = result[1]

            if yu < 1.5:
                num = shang
            else:
                num = shang + 1
            crs_id = crs_base + num

        elif lon < 73.5:
            crs_id = 4534

        else:
            crs_id = 4554

    # EPSG = 'epsg:' + str(int(crs_id))
    # proj = Proj(EPSG)

    proj = Proj(int(crs_id))
    x, y = proj(lon, lat)

    return x, y, crs_id

def from_proj_to_geo(x, y, crs_id=None):
    # https://pyproj4.github.io/pyproj/stable/examples.html#transformations-from-crs-to-crs

    # 目标地理坐标系，GCS_China_Geodetic_Coordinate_System_2000，WKID: 4490 权限: EPSG
    transformer = Transformer.from_crs(int(crs_id), 4490, always_xy=True)

    # 转换到经纬度
    lon, lat = transformer.transform(x, y)
    return lon, lat

