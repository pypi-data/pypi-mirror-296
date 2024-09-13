import os
import zipfile
from pathlib import Path


def unpack_zip(zip_path, new_path=None):
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


def check_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，创建文件夹
        os.makedirs(folder_path)
        # 创建成功后，你可以在这里添加一些其他操作
        print(f"文件夹'{folder_path}'已创建。")
    else:
        # 文件夹已经存在，你可以选择在这里做其他处理
        print(f"文件夹'{folder_path}'已存在。")
