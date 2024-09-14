import os
import shutil
import importlib.resources as pkg_resources  # 用于查找包内的资源文件

def copy_example_yml():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 查找包内的 example.yml 文件
    try:
        # 从包中获取 example.yml 文件的路径
        with pkg_resources.path(__package__, 'example.yml') as example_file:
            # 目标路径是当前目录下的 example.yml
            target_path = os.path.join(current_directory, 'example.yml')

            # 复制文件到当前目录
            shutil.copy(example_file, target_path)
            print(f"example.yml copied to {target_path}")
    except FileNotFoundError:
        print("example.yml not found in the package.")
    except IOError as e:
        print(f"Failed to copy example.yml: {e}")
