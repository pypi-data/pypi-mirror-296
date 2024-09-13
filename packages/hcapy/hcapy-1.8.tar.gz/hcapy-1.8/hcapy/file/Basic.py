import os


def check_folder(folder_path):
    """检查文件夹是否存在，不存在则创建"""
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，创建文件夹
        os.makedirs(folder_path)
        # 创建成功后，你可以在这里添加一些其他操作
        print(f"文件夹'{folder_path}'已创建。")
    else:
        # 文件夹已经存在，你可以选择在这里做其他处理
        print(f"文件夹'{folder_path}'已存在。")


def get_subdirectories_and_files(directory) -> tuple[list, list]:
    """
    获取子目录和子文件
    :param directory: 目录路径
    :return: 子目录列表，子文件列表
    """
    subdirectories = []
    files = []
    for root, dirs, filenames in os.walk(directory):
        for DIR in dirs:
            subdirectories.append(os.path.join(root, DIR))
        for file in filenames:
            files.append(os.path.join(root, file))
    # 将目录的结构文件写道目录所在路径，避免对目录结构的影响
    # base_path = upper_dictionary(directory)
    base_path = directory

    # 写入子目录的绝对地址到txt文件
    with open(os.path.join(base_path, 'subdirectories.txt'), 'w', encoding='utf-8') as file:
        file.write('\n'.join(subdirectories))

    # 写入子文件的绝对地址到txt文件
    with open(os.path.join(base_path, 'files.txt'), 'w', encoding='utf-8') as file:
        file.write('\n'.join(files))

    return subdirectories, files


def upper_dictionary(dictionary, num):
    """
    获取文件绝对地址的父地址
    :param dictionary: 文件绝对地址
    :param num: 父级目录的层数
    :return: 父级目录的绝对地址
    """
    parent_dir = dictionary
    if num <= 0:
        pass
    else:
        for i in range(num):
            parent_dir = os.path.abspath(os.path.join(dictionary, ".."))
            dictionary = parent_dir
    return parent_dir
