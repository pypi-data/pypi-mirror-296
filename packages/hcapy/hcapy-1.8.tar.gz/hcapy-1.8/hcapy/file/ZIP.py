import zipfile
from pathlib import Path


def unpack_zip(zip_path, new_path=None) -> str:
    """
    解压zip文件
    :param zip_path: zip文件路径
    :param new_path: 解压后的文件存放路径，默认为zip文件所在目录
    :return: 解压后的文件存放路径
    """
    if not new_path:
        new_path = Path(zip_path).parent

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            # 处理中文文件名乱码问题
            try:
                info.filename = info.filename.encode('cp437').decode('gbk')
            except Exception as e:
                print(f'解压时编码错误：{e}')

            zip_ref.extract(info, new_path)
    return new_path
