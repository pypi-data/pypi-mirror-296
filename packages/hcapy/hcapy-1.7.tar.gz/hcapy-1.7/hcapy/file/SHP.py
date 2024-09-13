import json
import os
import shutil
import zipfile
from typing import Optional

import geopandas as gpd
import shapefile
from shapely.geometry import shape, Point, Polygon, mapping
# https://pypi.org/project/pyshp/#the-writer-class

from ..GeoServer import GeoServer
from .ZIP import unpack_zip


def get_shp_data(zip_path, geometry=None, rec_name=None) -> Optional[list]:

    originalRoot, _ = os.path.split(zip_path)
    unpack_zip(zip_path=zip_path, new_path=originalRoot)

    temp_shp_path = os.path.join(originalRoot, os.path.basename(zip_path))
    sf = shapefile.Reader(temp_shp_path)
    records = sf.records()
    shapes = sf.shapes()

    results = []
    for index, (shape_rec, record) in enumerate(zip(shapes, records)):
        shapely_geom = shape(shape_rec.__geo_interface__)

        if isinstance(geometry, Point):
            if geometry.within(shapely_geom):  # within是检查geometry是否完全位于shapely_geom内部
                results.append({'geometry': json.dumps(mapping(geometry)),
                                'data': record[rec_name]})
        elif isinstance(geometry, Polygon):
            if geometry.intersects(shapely_geom):  # 用intersects方法来检查两个几何对象是否相交
                results.append({'geometry': json.dumps(mapping(shapely_geom.intersection(geometry))),
                                'data': record[rec_name]})

    if results:
        return results
    else:
        return None


def get_feature_types(shpPath) -> list:
    """
    获取 SHP 文件中的要素类型。

    :param shpPath: SHP 文件的路径
    :return: 要素类型列表
    """
    # 读取 SHP 文件
    gdf = gpd.read_file(shpPath)
    # 获取要素类型
    feature_types = gdf.geometry.geom_type.unique().tolist()

    return feature_types


def shp_to_zip(shp_path, new_zip_path):
    """
    将shp文件转换为zip文件，并保存到指定路径。
    """

    zip_file = zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_STORED)  # 新建zip
    for root, dirs, files in os.walk(shp_path):
        for f in files:
            file_path = os.path.join(root, f)
            zip_file.write(file_path, os.path.basename(file_path))  # 写入
    zip_file.close()  # 保存且关闭
    return True


def create_shp_prj(shp_file_path):
    gdf = gpd.GeoDataFrame(columns=['geometry'], crs='epsg:4326')
    gdf['geometry'] = gpd.GeoSeries(None, name='geometry', crs=gdf.crs)
    gdf.to_file(shp_file_path)
    os.remove(shp_file_path.replace('.shp', '.dbf'))
    os.remove(shp_file_path.replace('.shp', '.shx'))
    os.remove(shp_file_path.replace('.shp', '.cpg'))
    os.remove(shp_file_path)


def write_shp_fields(shapeType, file_path, fields):
    """
    写入shape文件
    :param shapeType: 要素类型
                      NULL = 0；       POINT = 1；       POLYLINE = 3；       POLYGON = 5；        MULTIPOINT = 8；
                      POINTZ = 11；    POLYLINEZ = 13；  POLYGONZ = 15；      MULTIPOINTZ = 18；   POINTM = 21；
                      POLYLINEM = 23； POLYGONM = 25；   MULTIPOINTM = 28；   MULTIPATCH = 31
    :param file_path: shp文件路径
    :param fields: 字段配置列表，列表中每个元素代表一个字段。每个元素是一个列表，依次是字段名，字段类型，字段长度
                   Field name: the name describing the data at this column index.
                   Field type: the type of data at this column index. Types can be:
                               "C": Characters, text.
                               "N": Numbers, with or without decimals.
                               "F": Floats (same as "N").
                               "L": Logical, for boolean True/False values.
                               "D": Dates.
                               "M": Memo, has no meaning within a GIS and is part of the xbase spec instead.
                   Field length: the length of the data found at this column index.
                                 Older GIS software may truncate this length to 8 or 11 characters for "Character" fields.
                   Decimal length: the number of decimal places found in "Number" fields.
    :return: 工作空间列表
    """
    writer = shapefile.Writer(file_path, shapeType=shapeType)
    writer.autoBalance = 1
    for field_name, field_type, decimal in fields:
        writer.field(field_name, field_type, decimal=decimal)
    return writer


def write_shp_geometry(writer: shapefile.Writer, coordinates, attributes, geo_type):
    if geo_type == 'Point':
        writer.point(*coordinates)
    elif geo_type == 'Polygon':
        writer.poly(coordinates)

    writer.record(*attributes.values())
    return writer


def publish_shp(zip_path=None, workspace=None, layer=None, geoserver=None) -> bool:
    """
    发布shp文件
    :param zip_path： shp文件的压缩包路径
    :param workspace: 工作空间名称
    :param layer: 图层名称
    :param geoserver: ip_port、username和password配置的字典
    :return: 是否发布成功
    """

    """工作区管理"""
    # 查询现有workspace列表
    workspace_names = GeoServer.get_workspace_list(geoserver)
    if not workspace_names:
        print(f'workspace列表获取失败')
        return False

    # 如果工作区不存在，则创建workspace
    if workspace not in workspace_names:
        if not GeoServer.create_workspace(geoserver, workspace):
            print(f'{workspace}工作区不存在，创建workspace失败')
            return False
    else:
        print(f'{workspace}工作区已存在')

    """开始处理geoserver发布"""
    zip_name = os.path.basename(zip_path).replace('.zip', '')
    if not layer:
        layer = zip_name

    originalRoot, _ = os.path.split(zip_path)

    output_path = os.path.join(originalRoot, "temp", zip_name)
    unpack_zip(zip_path, output_path)

    # 获取文件夹中的所有文件
    files = [f for f in os.listdir(output_path) if os.path.isfile(os.path.join(output_path, f))]
    # 遍历文件
    for filename in files:
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        # 构建新的文件名
        new_filename = f"{layer}{ext}"
        # 完整的旧文件路径
        old_filepath = os.path.join(output_path, filename)
        # 完整的新文件路径
        new_filepath = os.path.join(output_path, new_filename)
        # 重命名文件
        try:
            os.rename(old_filepath, new_filepath)
        except Exception as e:
            print(f"重命名文件失败：{e}")
            return False

    temp_ZIP_path = os.path.join(originalRoot, "temp", zip_name + '.zip')
    shp_to_zip(shp_path=output_path, new_zip_path=temp_ZIP_path)
    shutil.rmtree(output_path)

    if GeoServer.publish_shp_with_zip(geoserver, workspace, layer, temp_ZIP_path):
        return True


def find_shp_files(directory):
    """
    在给定的目录中查找所有shp文件
    """
    shp_files = []
    # os.walk()返回一个生成器，它会遍历directory及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.shp'):
                # os.path.join()用于构建完整的文件路径
                shp_files.append(os.path.join(root, file))
    return shp_files


def shp_to_geojsonList(shp_file_path):
    # 读取Shapefile
    try:
        sf = shapefile.Reader(shp_file_path)
    except UnicodeDecodeError:
        sf = shapefile.Reader(shp_file_path, encoding='gbk')

    geojsonList = []

    for i in range(len(sf)):
        # 获取每个形状的几何数据
        geometry_shape = sf.shape(i)
        try:
            geojsonList.append(mapping(geometry_shape))
        except Exception as e:
            print(f"shp转geojson失败：{e}")
    return geojsonList
