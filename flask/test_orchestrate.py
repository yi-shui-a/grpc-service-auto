# test_orchestrate.py
import unittest
from unittest.mock import patch, MagicMock
import json
from flask import Flask, request
from flask_main import orchestrate
import os


class TestOrchestrate(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app.add_url_rule(
            "/orchestrate", "orchestrate", orchestrate, methods=["POST"]
        )

    def test_success(self):
        # 测试成功的情况
        # 读取json文件
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../example/client_json/SERVICE2.json",
            "r",
        ) as f:
            orchestration_file = json.load(f)
        response = self.client.post(
            "/orchestrate", data={"orchestration_file": json.dumps(orchestration_file)}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["code"], 200)
        self.assertEqual(data["message"], "orchestrate success")


if __name__ == "__main__":
    unittest.main()
