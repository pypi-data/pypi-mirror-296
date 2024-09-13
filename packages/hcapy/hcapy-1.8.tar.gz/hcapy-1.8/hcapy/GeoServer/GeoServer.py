import copy
from typing import List, Optional

import requests


def get_workspace_list(geoserver: dict) -> Optional[List[str]]:
    """
    获取工作空间列表
    :param geoserver： ip_port、username和password配置的字典
    :return: 工作空间列表
    """
    response = requests.get(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces',
        auth=(geoserver["username"], geoserver["password"]),
    )
    # 检查请求是否成功
    if response.status_code == 200:
        # 如果你知道响应是JSON格式，可以这样处理
        workspaces = response.json()['workspaces']['workspace']
        workspace_names = [wp['name'] for wp in workspaces]
        return workspace_names
    else:
        return None


def create_workspace(geoserver: dict, workspace_name: str) -> bool:
    """
    创建工作空间
    :param geoserver： ip_port、username和password配置的字典
    :param workspace_name: 工作空间名称
    :return: 是否创建成功
    """
    response = requests.post(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces',
        headers={'Content-Type': 'application/json'},
        json={
            "workspace": {
                "name": workspace_name
            }
        },
        auth=(geoserver["username"], geoserver["password"]),
    )
    if response.status_code == 201:
        print(f'工作区{workspace_name}创建成功')
        return True
    else:
        print(f'工作区{workspace_name}创建失败')
        return False


def publish_tif(geoserver: dict, workspace: str, layer: str, tif_path: str, fileData: bytes = None) -> bool:
    """
    发布tif文件
    :param geoserver： ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :param layer: 图层名称
    :param tif_path: tif文件路径
    :param fileData: tif文件数据
    :return: 是否发布成功
    """
    if fileData:
        file_data = fileData
    else:
        file = open(tif_path, 'rb')
        file_data = file.read()
        file.close()

    delete_datastore(geoserver, workspace, layer)
    delete_coveragestore(geoserver, workspace, layer)

    response = requests.put(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/coveragestores/{layer}/file.geotiff',
        headers={'Content-Type': 'image/tiff'},
        data=file_data,
        auth=(geoserver["username"], geoserver["password"]),
    )
    if response.status_code == 201 or response.status_code == 200:
        print('geoserver发布成功')
        return True
    else:
        return False


def publish_shp_with_zip(geoserver: dict, workspace: str, layer: str, zip_path: str) -> tuple[bool, str]:
    """
    发布shp文件
    :param geoserver: ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :param layer: 图层名称
    :param zip_path: shp文件路径
    :return: shp文件是否成功发布的布尔值。如果发布失败，则返回具体的错误信息；若成功，则为空字符串
    """
    file = open(zip_path, 'rb')
    file_data = file.read()

    delete_datastore(geoserver, workspace, layer)
    delete_coveragestore(geoserver, workspace, layer)

    response = requests.put(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/datastores/{layer}/file.shp',
        headers={'Content-type': 'application/zip'},
        data=file_data,
        auth=(geoserver["username"], geoserver["password"]),
    )
    if response.status_code == 201 or response.status_code == 200:  # 发布请求成功
        state, data = judge_publish_state(geoserver, workspace, layer)  # 判断图层启用状态
        if state is False:  # 图层未启用
            if data.get('srs') is None:
                if reset_CRS_and_publish(geoserver, workspace, layer, data):
                    return True, ""
            else:
                return False, "数据入库成功但发布服务失败，可能由于错误的坐标系定义"
        else:  # 图层启用
            return True, ""
    else:  # 发布请求成功
        return False, "数据入库成功但发布服务失败，未知的原始数据错误"


def judge_publish_state(geoserver: dict, workspace: str, layer: str) -> tuple[bool, dict]:
    """
    判断shp文件发布状态
    :param geoserver: ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :param layer: 图层名称
    :return: shp文件是否成功发布的布尔值；存储仓库属性值字典
    """
    response = requests.get(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/datastores/{layer}/featuretypes/{layer}',
        auth=(geoserver["username"], geoserver["password"]),
        headers={"Accept": "application/json"}
    )
    data = response.json()
    featureType = data.get('featureType', None)
    if featureType and featureType.get('enabled'):
        return True, featureType
    else:
        return False, featureType


def reset_CRS_and_publish(geoserver: dict, workspace: str, layer: str, data: dict) -> bool:
    # https://docs.geoserver.org/stable/en/api/#1.0.0/featuretypes.yaml

    body = copy.deepcopy(data)
    body.update({"srs": "EPSG:4326",
                 "enabled": True})
    response = requests.put(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/datastores/{layer}/featuretypes/{layer}',
        auth=(geoserver["username"], geoserver["password"]),
        headers={'Content-Type': 'application/json'},
        json={'featureType': body},
        params={'recalculate': ['nativebbox', 'latlonbbox']}
    )
    if response.status_code == 201 or response.status_code == 200:
        return True
    else:
        return False


def delete_datastore(geoserver: dict, workspace: str, datastore: str) -> bool:
    """
    删除数据存储
    :param geoserver： ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :param datastore: 数据存储名称
    :return: 是否删除成功
    """
    name_list = get_datastores(geoserver, workspace)
    if name_list and datastore in name_list:
        response = requests.delete(
            f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/datastores/{datastore}?recurse=true',
            auth=(geoserver["username"], geoserver["password"]))
        if response.status_code == 200:
            print(f'{datastore}删除成功')
            return True
        else:
            return False
    else:
        print(f'{datastore}：datastore不存在')
        return True


def get_datastores(geoserver: dict, workspace: str) -> Optional[List[str]]:
    """
    获取数据存储列表
    :param geoserver： ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :return: 数据存储列表
    """
    response = requests.get(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/datastores',
        auth=(geoserver["username"], geoserver["password"]),
    )
    if response.status_code == 200:
        response_json = response.json()['dataStores']
        if response_json:
            datastores = response_json['dataStore']
            datastores_names = [str(i['name']) for i in datastores]
            return datastores_names
        else:
            return None
    else:
        print(f'{workspace}：datastores查询失败')
        return None


def delete_coveragestore(geoserver: dict, workspace: str, coveragestore: str) -> bool:
    """
    删除数据存储
    :param geoserver： ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :param coveragestore: 数据存储名称
    :return: 是否删除成功
    """
    name_list = get_coveragestores(geoserver, workspace)

    if name_list and coveragestore in name_list:
        response = requests.delete(
            f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/coveragestores/{coveragestore}?purge=all&recurse=true',
            auth=(geoserver["username"], geoserver["password"]))
        if response.status_code == 200:
            print(f'{coveragestore}：coveragestore删除成功')
            return True
        else:
            return False
    else:
        print(f'{coveragestore}：coveragestore不存在')
        return True


def get_coveragestores(geoserver: dict, workspace: str) -> Optional[List[str]]:
    """
    获取数据存储列表
    :param geoserver： ip_port、username和password配置的字典
    :param workspace: 工作空间名称
    :return: 数据存储列表
    """
    response = requests.get(
        f'http://{geoserver["ip_port"]}/geoserver/rest/workspaces/{workspace}/coveragestores',
        auth=(geoserver["username"], geoserver["password"]),
    )
    if response.status_code == 200:
        response_json = response.json()['coverageStores']
        if response_json:
            coveragestores = response_json['coverageStore']
            coveragestores_name = [str(wp['name']) for wp in coveragestores]
            return coveragestores_name
        else:
            return None
    else:
        print(f'{workspace}：coveragestores查询失败')
        return None
