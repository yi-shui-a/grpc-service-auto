from typing import List, Dict
import os
import sys
from jinja2 import Template
import subprocess
import shutil

from .Util import Util


class DDSUtil:

    @staticmethod
    def loadIdl(filePath: str):
        filename_with_ext = os.path.basename(filePath)
        filename_without_ext = os.path.splitext(filename_with_ext)[0]

        # 判断是否存在该文件
        if not os.path.exists(filePath):
            print(filePath + "文件不存在")
            return

        # 将idl文件加载到idl目录下
        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename_without_ext}/",
            exist_ok=True,
        )

        # 目标路径
        target_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename_without_ext}/{filename_with_ext}"

        # 将文件复制到db中
        try:
            shutil.copy2(filePath, target_path)
            print(f"文件 {filePath} 已成功复制到 {target_path}")
        except FileNotFoundError:
            print(f"源文件 {filePath} 未找到。")
        except PermissionError:
            print("没有足够的权限进行复制操作。")
        except Exception as e:
            print(f"复制文件时出现错误: {e}")

    @staticmethod
    def generateIdlCMakeLists(filename: str):
        filename = filename.split(".")[0]
        idl_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/"
        # 判断是否存在文件和目录
        if not os.path.exists(idl_path + filename):
            print(f"目录 {idl_path +filename} 不存在")
            return
        if not os.path.exists(os.path.join(idl_path, filename, filename + ".idl")):
            print(f"文件 {os.path.join(idl_path, filename, filename + '.idl')} 不存在")
            return

        # 生成CMakeLists.txt
        idl_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/dds_process_template/idl_compile_cmake_template.j2"
            ).read()
        )
        res_str = idl_template.render(
            project_name=filename,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename}/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename}/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename}/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileIdl(filename: str):
        filename = filename.split(".")[0]
        file_dir = (
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/idl/{filename}/"
        )
        Util.compileCmakeProject(
            file_dir,
            filename,
            file_type="idl",
        )

    @staticmethod
    def loadDDS(filePath: str):
        filename_with_ext = os.path.basename(filePath)
        filename_without_ext = os.path.splitext(filename_with_ext)[0]

        # 判断是否存在该文件
        if not os.path.exists(filePath):
            print(filePath + "文件不存在")
            return

        # 将idl文件加载到idl目录下
        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename_without_ext}/",
            exist_ok=True,
        )

        # 目标路径
        target_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename_without_ext}/{filename_with_ext}"

        # 将文件复制到db中
        try:
            shutil.copy2(filePath, target_path)
            print(f"文件 {filePath} 已成功复制到 {target_path}")
        except FileNotFoundError:
            print(f"源文件 {filePath} 未找到。")
        except PermissionError:
            print("没有足够的权限进行复制操作。")
        except Exception as e:
            print(f"复制文件时出现错误: {e}")

    @staticmethod
    def generateDDSCMakeLists(filename: str, idl_list: List[str]):
        filename = filename.split(".")[0]
        dds_src_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/"
        # 判断是否存在文件和目录
        if not os.path.exists(dds_src_path + filename):
            print(f"目录 {dds_src_path +filename} 不存在")
            return
        if not os.path.exists(os.path.join(dds_src_path, filename, filename + ".cpp")):
            print(
                f"文件 {os.path.join(dds_src_path, filename, filename + '.cpp')} 不存在"
            )
            return
        for idl in idl_list:
            if not os.path.exists(
                os.path.join(dds_src_path, "../idl/", idl, idl + ".idl")
            ):
                print(
                    f"idl {os.path.join(dds_src_path, '../idl/', idl + '.idl')} 不存在"
                )
                return

        # 生成CMakeLists.txt
        idl_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/dds_process_template/dds_src_compile_cmake_template.j2"
            ).read()
        )
        res_str = idl_template.render(project_name=filename, idl_list=idl_list)

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename}/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename}/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename}/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileDDS(filename: str):
        filename = filename.split(".")[0]
        file_dir = (
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/dds/{filename}/"
        )
        Util.compileCmakeProject(
            file_dir,
            filename,
            file_type="cpp",
        )
