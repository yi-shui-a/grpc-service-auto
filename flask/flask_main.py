from flask import Flask
from flask import jsonify
from flask import request

import time
import sys
import json
import os
import copy
from typing import List
from contextlib import redirect_stdout
import io

from utils import getResponse

app = Flask(__name__)

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from src.scripts.util.ClientUtil import ClientUtil
from src.scripts.entity import Client

atom_service_develop = "develop"
atom_service_orchestrate = "orchestrate"
atom_service_deploy = "deploy"
atom_service_monitor = "monitor"


response_dict = {
    "code": 200,
    "message": "success",
    "data": {},
}


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route(f"/{atom_service_develop}/uploadcpp", methods=["POST"])
def uploadCpp():
    """
    上传cpp文件
    """
    # 检查是否有文件字符串
    cpp_content: str = request.form.get("content", "")
    service_name: str = request.form.get("service", "")
    if cpp_content == "" or service_name == "":
        # 深拷贝response_dict
        res = copy.deepcopy(response_dict)
        res["code"] = 400
        res["message"] = "cpp_content or service_name is empty"
        return jsonify(getResponse(400, "cpp_content or service_name is empty"))

    # 定义保存目录
    save_directory = f"{os.path.dirname(os.path.abspath(__file__))}/../db/input_service/{service_name}"
    # 如果目录不存在，则创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # 保存接收到的文件
    if cpp_content:
        with open(
            f"{save_directory}/{service_name}.cpp",
            "w",
        ) as file:
            file.write(cpp_content)
        return jsonify(getResponse(200, "File uploaded successfully!"))
    return jsonify(getResponse(400, "File upload failed!"))


@app.route(f"/{atom_service_orchestrate}/uploadhpp", methods=["POST"])
def uploadHpp():
    """
    上传h文件
    """
    # 检查是否有文件字符串
    hpp_content: str = request.form.get("content", "")
    service_name: str = request.form.get("service", "")
    if hpp_content == "" or service_name == "":
        # 深拷贝response_dict
        res = copy.deepcopy(response_dict)
        res["code"] = 400
        res["message"] = "hpp_content or service_name is empty"
        return jsonify(getResponse(400, "hpp_content or service_name is empty"))
    # 定义保存目录
    save_directory = f"{os.path.dirname(os.path.abspath(__file__))}/../db/input_service/{service_name}"
    # 如果目录不存在，则创建它
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # 保存接收到的文件
    if hpp_content:
        with open(
            f"{save_directory}/{service_name}.h",
            "w",
        ) as file:
            file.write(hpp_content)
        return jsonify(getResponse(200, "File uploaded successfully!"))
    return jsonify(getResponse(400, "File upload failed!"))


@app.route(f"/{atom_service_develop}/parseatomservice", methods=["POST"])
def parseAtomService():
    """
    解析原子服务
    """

    pass


@app.route(f"/{atom_service_develop}/loadatomservice", methods=["POST"])
def loadAtomService():
    pass


@app.route(f"/{atom_service_orchestrate}/orchestrate", methods=["POST"])
def orchestrate():
    """
    编排服务
    """
    orchestrattion_file: dict = json.loads(request.form.get("orchestration_file", ""))
    client_name: str = orchestrattion_file.get("name", "")
    client_id: str = orchestrattion_file.get("id", "")
    if client_id == "" or client_name == "":
        return jsonify(getResponse(400, "client_id or client_name is empty"))
    node_list: List[dict] = list()
    for node in orchestrattion_file.get("nodes", []):
        res: dict = dict()
        res["type"] = node.get("type", "")
        res["id"] = node.get("id", "")
        res["title"] = node.get("file", "").split("/")[-1].split(".")[0]
        print(res["title"])
        res["method"] = node.get("method", "")
        res["module"] = node.get("module", "")
        res["topic"] = node.get("topic", "")
        res["struct_name"] = node.get("struct_name", "")
        res["struct"] = node.get("struct", "")
        res["dataBind"] = node.get("dataBind", dict())
        if (
            res["type"] == "SERVICE"
            and res["method"] == ""
            and res["dataBind"] == dict()
        ):
            return jsonify(
                getResponse(400, f"title {res['title']} : method or dataBind is empty")
            )
        node_list.append(res)
    orchestrattion_info: dict = dict()
    orchestrattion_info["name"] = client_name
    orchestrattion_info["id"] = client_id
    orchestrattion_info["nodes"] = node_list
    orchestrattion_info["connections"] = orchestrattion_file.get("connections", [])
    if orchestrattion_info["connections"] == []:
        return jsonify(getResponse(400, "connections is empty"))
    if len(orchestrattion_info["nodes"]) == 0:
        return jsonify(getResponse(400, "nodes is empty"))

    ClientUtil.accomplishAllClient(orchestrattion_info)
    return jsonify(getResponse(200, "orchestrate success"))


if __name__ == "__main__":
    app.run(debug=True)
