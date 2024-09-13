import geopandas as gpd


def read_geojson_data(features):
    """解析geojson数据，到shapely.geometry对象"""
    geometry_list = []
    # 转换为GeoDataFrame
    # features = json.loads(features)
    gdf = gpd.GeoDataFrame.from_features(features)
    for index, geometry in enumerate(gdf.geometry):
        geometry_list.append({"name": gdf.id[index],
                              'geometry': geometry})
    return geometry_list
