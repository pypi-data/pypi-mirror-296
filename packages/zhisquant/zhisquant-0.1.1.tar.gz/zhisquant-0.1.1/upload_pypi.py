import os
import sys
import subprocess
import re


def increment_version(version):
    """
    递增版本号的修订号。

    Args:
        version (str): 当前版本号，例如 '0.1.0'

    Returns:
        str: 更新后的版本号，例如 '0.1.1'
    """
    major, minor, patch = version.split('.')
    patch = str(int(patch) + 1)
    return f"{major}.{minor}.{patch}"


def update_setup_py_version():
    """
    更新 setup.py 中的版本号。
    """
    setup_py = 'setup.py'
    if not os.path.isfile(setup_py):
        print("setup.py 文件不存在。")
        sys.exit(1)

    with open(setup_py, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式匹配版本号
    version_pattern = r"version=['\"]([^'\"]+)['\"]"
    match = re.search(version_pattern, content)
    if not match:
        print("未能在 setup.py 中找到版本号。")
        sys.exit(1)

    current_version = match.group(1)
    new_version = increment_version(current_version)

    # 更新版本号
    new_content = re.sub(version_pattern, f"version='{new_version}'", content)

    with open(setup_py, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"版本号已从 {current_version} 更新为 {new_version}")

    return new_version


def build_package():
    """
    构建分发包。
    """
    # 删除 dist/ 目录
    if os.path.isdir('dist'):
        import shutil
        shutil.rmtree('dist')

    # 运行构建命令
    result = subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    if result.returncode != 0:
        print("构建包时发生错误。")
        sys.exit(1)
    else:
        print("包构建成功。")


def upload_to_pypi():
    """
    上传包到 PyPI。
    """
    # 获取 PyPI API Token
    # pypi_token = os.getenv('PYPI_TOKEN')
    # if not pypi_token:
    #     print("请在环境变量中设置 PYPI_TOKEN。")
    #     sys.exit(1)

    # 运行上传命令
    result = subprocess.run([
        'twine', 'upload', 'dist/*',
        '-u', '__token__',
        '-p', 'pypi-AgEIcHlwaS5vcmcCJGRiOWFiNWQ5LTA2NTUtNGY5NC04OTBlLWY5NzczOTQ4MTBiNQACKlszLCI5M2MxMzE0Zi1iYmI2LTQ5M2YtOWZhMC1mYTU2NGQ0NzBiYzEiXQAABiBMmGjzhZ_Qk2HvuJ9RQslW4B_P1P3KNu4FuWa8_SoWdw'
    ])
    if result.returncode != 0:
        print("上传到 PyPI 时发生错误。")
        sys.exit(1)
    else:
        print("包已成功上传到 PyPI。")


if __name__ == '__main__':
    # 更新版本号
    new_version = update_setup_py_version()

    # 构建包
    build_package()

    # 上传到 PyPI
    upload_to_pypi()
