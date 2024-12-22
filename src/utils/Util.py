import sys
import os
from jinja2 import Template
import subprocess
from typing import List


class Util(object):

    @staticmethod
    def compile_idl(file_path: str):
        file_name = file_path.split(".")[0].split("/")[-1]
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "IDL_make",
            f"IDL_FILE={file_name}.idl",
        ]
        try:
            # 调用make命令，并等待其完成
            result = subprocess.run(
                make_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 如果make命令成功执行，则打印其输出
            if result.stdout:
                print("Make Output:\n", result.stdout)

        except subprocess.CalledProcessError as e:
            # 如果make命令失败，则捕获异常并打印错误信息
            print("Make failed with error:", e)
            print("Error Output:\n", e.stderr)

    @staticmethod
    def compile_dds(file_path: str):
        file_name = file_path.split(".")[0].split("/")[-1]
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "DDS_make",
            f"DDS_FILE={file_name}.cpp",
        ]
        try:
            # 调用make命令，并等待其完成
            result = subprocess.run(
                make_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 如果make命令成功执行，则打印其输出
            if result.stdout:
                print("Make Output:\n", result.stdout)

        except subprocess.CalledProcessError as e:
            # 如果make命令失败，则捕获异常并打印错误信息
            print("Make failed with error:", e)
            print("Error Output:\n", e.stderr)

    @staticmethod
    def compileServerDemo(service_list: List[str], filename):
        # 将 service_list 列表中的每个元素组成一个字符串，元素之间用空格相连
        services_str = " ".join(service_list)

        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "test2_make",
            f"SERVICE={services_str}",
            f"SERVER={filename}",
        ]
        try:
            # 调用make命令，并等待其完成
            result = subprocess.run(
                make_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 如果make命令成功执行，则打印其输出
            if result.stdout:
                print("Make Output:\n", result.stdout)

        except subprocess.CalledProcessError as e:
            # 如果make命令失败，则捕获异常并打印错误信息
            print("Make failed with error:", e)
            print("Error Output:\n", e.stderr)

    @staticmethod
    def compileClientDemo(
        service_list: List[str], topic_list: List[str], filename: str
    ):
        filename = filename.split(".")[0]

        service_str = " ".join(service_list)
        topic_str = " ".join(topic_list)
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "DDS_client_make",
            f"SERVICE={service_str}",
            f"TOPIC={topic_str}",
            f"SERVER={filename}",
        ]
        try:
            # 调用make命令，并等待其完成
            result = subprocess.run(
                make_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 如果make命令成功执行，则打印其输出
            if result.stdout:
                print("Make Output:\n", result.stdout)

        except subprocess.CalledProcessError as e:
            # 如果make命令失败，则捕获异常并打印错误信息
            print("Make failed with error:", e)
            print("Error Output:\n", e.stderr)
