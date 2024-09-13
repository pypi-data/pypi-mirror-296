from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/* --verbose

setup(
    name='hcapy',
    version='1.7',
    packages=find_packages(),
    description='HCA private package',
    author='huochunan',
    author_email='huochunan@163.com',
    license='MIT',
    install_requires=[
        'ezdxf',
        'geopandas',
        'pyshp',
        'rasterio',
        'numpy',
        'pyproj'
    ],
    classifiers=[
        # 分类信息
    ]
)
