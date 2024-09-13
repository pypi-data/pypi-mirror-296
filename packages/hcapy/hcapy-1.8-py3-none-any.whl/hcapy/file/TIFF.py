import os

import numpy as np
import rasterio
from numpy import inf
from rasterio.mask import mask
from shapely.geometry import Polygon, Point
from typing import Optional

from ..GeoServer import GeoServer


def get_tif_data(tif_path, geometry=None) -> Optional[list[float]]:
    """
    获取 几何对象 对应的栅格数据
    :param tif_path: tif文件路径
    :param geometry: shapely.geometry的几何对象
    :return: 最小值、平均值、最大值的列表
    """
    # 打开.tif文件
    with rasterio.open(tif_path, 'r') as dataset:
        if geometry.type == 'Point':
            geometry: Point
            lon = geometry.x
            lat = geometry.y
            if -180 <= lon <= 180 and -90 <= lat <= 90:
                pass
            else:
                return None

            # 获取数据集的元数据
            transform = dataset.transform  # 变换矩阵，用于坐标转换
            width = dataset.width  # 数据宽度（列数）
            height = dataset.height  # 数据高度（行数）
            # 将经纬度转换为图像的行列索引
            row, col = rasterio.transform.rowcol(transform, lon, lat)

            # 检查行列索引是否在数据范围内
            if 0 <= row < height and 0 <= col < width:
                # 读取该位置的像素值
                pixel_value = float(dataset.read(1, window=((row, row + 1), (col, col + 1)))[0, 0])
                if pixel_value == dataset.nodata:
                    return None
                pixel_value = round(pixel_value, 2)
                return [pixel_value, pixel_value, pixel_value]
            else:
                print("Coordinates are outside the dataset bounds.")
                return None
        elif geometry.type == 'Polygon':
            poly: Polygon = geometry

            try:
                # 裁剪数据
                clipped_data, _ = mask(dataset=dataset, shapes=[poly], nodata=float(inf), filled=True, crop=True)
            except ValueError:
                return None

            # 使用布尔索引选出非零元素
            useful_elements = clipped_data[clipped_data != float(inf)].tolist()
            if useful_elements:
                # 计算非零元素的平均值
                average_elements = float(np.mean(useful_elements))
                max_elements = float(np.max(useful_elements))
                min_elements = float(np.min(useful_elements))

                if dataset.nodata in [min_elements, average_elements, max_elements]:
                    return None

                min_elements, average_elements, max_elements = \
                    round(min_elements, 2), round(average_elements, 2), round(max_elements, 2)
                return [min_elements, average_elements, max_elements]
            else:
                return None


def publish_tif(tif_path=None, fileData=None, workspace=None, layer=None, geoserver=None) -> bool:
    """工作区管理"""
    # 查询现有workspace列表
    workspace_names = GeoServer.get_workspace_list(geoserver)
    if not workspace_names:
        print('workspace列表获取失败')
        return False

    # 如果工作区不存在，则创建workspace
    if workspace not in workspace_names:
        if not GeoServer.create_workspace(geoserver, workspace):
            print(f'{workspace}工作区不存在，创建workspace失败')
            return False
    else:
        print(f'{workspace}工作区已存在')

    """开始处理geoserver发布"""
    tif_name = os.path.basename(tif_path).replace('.tif', '')
    if not layer:
        layer = tif_name

    if GeoServer.publish_tif(geoserver, workspace, layer, tif_path, fileData=fileData):
        # 使用序列化器更新数据
        content_data = {
            'geoserver_state': '1',
            'wmsUrl': f'http://{geoserver["ip_port"]}/geoserver/',
            'workplace': workspace,
            'layer': layer,
            'data_type': '栅格数据'
        }
        return True


def get_min_max_value(tif_path) -> tuple[float, float, float]:
    """
    获取 TIFF 图像的最大值和最小值。

    :param tif_path: TIFF 文件的路径
    :return: 最小值和最大值的元组 (min_value, max_value)
    """
    with rasterio.open(tif_path, 'r') as src:
        # 读取图像数据
        image_data = src.read(1)  # 读取第一个波段的数据

        # 排除 NoData 值
        valid_data = image_data[image_data != src.nodata]

        # 计算最小值和最大值
        min_value = float(valid_data.min())
        max_value = float(valid_data.max())
        noData = float(src.nodata)

    return min_value, max_value, noData
