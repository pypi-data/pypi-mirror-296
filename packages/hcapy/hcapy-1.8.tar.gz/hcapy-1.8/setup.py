from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/* --verbose

setup(
    name='hcapy',
    version='1.8',
    packages=find_packages(),
    description='HCA private package',
    long_description=open('readme.md', encoding='utf-8').read(),
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
