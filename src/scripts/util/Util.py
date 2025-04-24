import sys
import os
from jinja2 import Template
import subprocess
from typing import List
import shutil
import json

from ..enums.FileEnum import FileEnum


class Util(object):

    @staticmethod
    def compileCmakeProject(cmake_dir: str, file_name: str, file_type: str = "cpp"):
        # 判断是否存在该文件
        if not os.path.exists(cmake_dir + "CMakeLists.txt"):
            print(cmake_dir + "CMakeLists.txt文件不存在")
        if not os.path.exists(cmake_dir + f"{file_name}.{file_type}"):
            print(cmake_dir + f"{file_name}.{file_type}文件不存在")

        # 创建 build 目录
        build_dir = os.path.join(cmake_dir, "build")
        # 准备 build 目录：如果目录已存在，则清空目录内容；否则创建空目录。
        if os.path.exists(build_dir):
            print(f"清空 build 目录：{build_dir}")
            # 删除目录中的所有内容
            for item in os.listdir(build_dir):
                item_path = os.path.join(build_dir, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # 删除文件或符号链接
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # 删除子目录
        else:
            print(f"创建 build 目录：{build_dir}")
            os.makedirs(build_dir)

        # 运行编译程序
        try:
            # 进入 build 目录
            os.chdir(build_dir)
            # 运行 cmake
            print("运行 cmake...")
            subprocess.run(["cmake", ".."], check=True)

            # 运行 make
            print("运行 make...")
            subprocess.run(["make"], check=True)

            print("文件生成成功！")
        except subprocess.CalledProcessError as e:
            print(f"错误：命令执行失败。{e}")
        finally:
            # 返回原始目录
            os.chdir(cmake_dir)

        # 删除 build 目录
        if os.path.exists(build_dir):
            print(f"删除 build 目录：{build_dir}")
            shutil.rmtree(build_dir)

    @staticmethod
    def generateHeaderHppAndCpp(path: str):
        # 定义模板
        cpp_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/registry_comm_template/HeaderCpp.j2"
            ).read()
        )
        cpp_str = cpp_template.render()
        hpp_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/registry_comm_template/HeaderHpp.j2"
            ).read()
        )
        hpp_str = hpp_template.render()

        # 确保目录存在
        os.makedirs(path, exist_ok=True)

        # 将cpp_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{path}/Header.cpp",
            "w",
        ) as file:
            file.write(cpp_str)
        print(f"{path}/Header.cpp generated successfully!")

        # 将hpp_str写入框架内的hpp文件中，同名不同路径
        with open(
            f"{path}/Header.h",
            "w",
        ) as file:
            file.write(hpp_str)
        print(f"{path}/Header.h generated successfully!")

    @staticmethod
    def run_executable_in_path(path, executable_name):
        """
        进入指定路径并运行该路径中的可执行文件，实时输出可执行文件的打印内容。

        :param path: 目标路径
        :param executable_name: 可执行文件的名称
        :return: 可执行文件的返回码
        """
        # 检查路径是否存在
        if not os.path.exists(path):
            raise FileNotFoundError(f"executable_path '{path}' does not exist")

        # 切换到目标路径
        os.chdir(path)

        # 检查可执行文件是否存在
        executable_path = os.path.join(path, executable_name)
        if not os.path.isfile(executable_path):
            raise FileNotFoundError(
                f"executable_file '{executable_name}' is not exist  in path '{path}' "
            )

        # 运行可执行文件并实时输出
        try:
            process = subprocess.Popen(
                [executable_path],  # 可执行文件路径
                stdout=subprocess.PIPE,  # 捕获 stdout
                stderr=subprocess.PIPE,  # 捕获 stderr
                text=True,  # 以文本模式返回输出
                bufsize=1,  # 行缓冲
                universal_newlines=True,  # 确保跨平台兼容性
            )

            # 实时读取并输出 stdout 和 stderr
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                if output == "" and error == "" and process.poll() is not None:
                    break
                if output:
                    print(output.strip())  # 输出 stdout
                if error:
                    print(error.strip(), file=sys.stderr)  # 输出 stderr

            # 等待进程结束并获取返回码
            return_code = process.wait()
            return return_code
        except Exception as e:
            raise RuntimeError(
                f"Failed to run executable file '{executable_name}' , exception: {e}"
            )

    @staticmethod
    def saveFile(name_list: List[str], content: str, type: FileEnum):
        path = ""
        filepath = ""

        # 根据类型选择路径和文件名
        if type == FileEnum.ATOM_SERIVCE_JSON:
            # 确保目录存在
            path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}"
            filepath = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/{name_list[-1]}.json"
        elif type == FileEnum.HPP:
            path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_include"
            filepath = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_include/{name_list[-1]}.h"
        elif type == FileEnum.CPP:
            path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_src"
            filepath = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_src/{name_list[-1]}.cpp"
        elif type == FileEnum.CPP_CMAKE:
            path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_src"
            filepath = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{'/'.join(name_list)}/atomic_src/CMakeLists.txt"
        elif type == FileEnum.SERVER_JSON:
            path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{'/'.join(name_list)}"
            filepath = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{'/'.join(name_list)}/{name_list[-1]}.json"
        if path == "" or filepath == "":
            print("Error: saveFile path is empty")
            return

        os.makedirs(
            path,
            exist_ok=True,
        )
        with open(
            filepath,
            "w",
        ) as file:
            file.write(content)
            print("SUCCESS: generated " + filepath)
