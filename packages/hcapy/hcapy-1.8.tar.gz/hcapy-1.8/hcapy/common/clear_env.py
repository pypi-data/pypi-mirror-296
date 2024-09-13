import os
import subprocess

subprocess.run(['pip', 'freeze'])

# 将包列表保存到文件
with open('packages.txt', 'w') as f:
    subprocess.run(['pip', 'freeze'], stdout=f)

# 读取文件中的包列表
with open('packages.txt') as f:
    packages = f.read().splitlines()

# 卸载每个包
for package in packages:
    package = package.split('==')[0]
    if package in ['pip', 'setuptools']:
        continue
    print(f"Uninstalling {package}...")
    subprocess.run(['pip', 'uninstall', '-y', package])

os.remove('packages.txt')
