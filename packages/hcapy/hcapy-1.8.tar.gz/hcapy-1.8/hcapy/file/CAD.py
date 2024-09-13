import os

from ezdxf import recover
from ezdxf.addons import odafc
from ezdxf.addons.drawing import matplotlib

from .Basic import check_folder

# 通过修改win_exec_path的值为自定义安装路径
# https://ezdxf.readthedocs.io/en/stable/addons/drawing.html#module-ezdxf.addons.drawing
odafc.win_exec_path = os.path.join('./', 'ODA File Converter/ODAFileConverter.exe')

def DWG2DXF(input_dwg, outputRoot=None):
    """
    DWG文件转换为DXF文件
    :param input_dwg: 输入的dwg文件路径
    :param outputRoot: 输出路径
    :return:
    """
    if not outputRoot:
        # 获取文件的目录和文件名
        outputRoot, file_name = os.path.split(input_dwg)

    check_folder(outputRoot)

    dxfName = os.path.basename(input_dwg).replace('.dwg', '.dxf')
    output_dxf = os.path.join(outputRoot, dxfName)
    # 转换dwg文件。replace=true允许覆盖已有文件。
    try:
        odafc.convert(input_dwg, output_dxf, version='R2018', replace=True)
        return output_dxf
    except Exception as e:
        print('dwg文件转换失败', e)
        return False


def DXF2PNG(input_dxf, pngName=None, outputRoot=None):
    """
    DXF文件转换为PNG文件
    :param input_dxf: 输入的dxf文件路径
    :param pngName: 输出png文件名称
    :param outputRoot: 输出路径
    :return:
    """
    if not outputRoot:
        # 获取文件的目录和文件名
        outputRoot, file_name = os.path.split(input_dwg)

    check_folder(outputRoot)

    if not pngName:
        pngName = os.path.basename(input_dxf).replace('.', '_') + '.png'
    output_png = os.path.join(outputRoot, pngName)

    doc, auditor = recover.readfile(input_dxf)
    if not auditor.has_errors:
        matplotlib.qsave(doc.modelspace(), output_png, dpi=300)
        return True
    else:
        return False
