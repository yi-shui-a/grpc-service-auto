import sys
import os
from jinja2 import Template
import subprocess


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
