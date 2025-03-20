import json
from typing import Any, Dict
import os


class Config:
    _instance = None  # 单例实例

    def __new__(cls, *args, **kwargs):
        # 单例模式：确保只有一个实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        config_file: str = f"{os.path.dirname(os.path.abspath(__file__))}/../config/config.json",
    ):
        # 如果配置数据已经加载，则不再重复加载
        if not hasattr(self, "_config_loaded"):
            self._load_config(config_file)
            self._config_loaded = True

    def _load_config(self, config_file: str):
        """加载 JSON 配置文件，并将其内容设置为类的属性"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                self._set_attributes(config_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_file} 未找到")
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {config_file} 格式错误")

    def _set_attributes(self, config_data: Dict[str, Any]):
        """将 JSON 数据设置为类的属性"""
        for key, value in config_data.items():
            if isinstance(value, dict):
                # 如果值是字典，递归设置为嵌套属性
                setattr(self, key, Config._create_nested_config(value))
            else:
                # 否则直接设置为属性
                setattr(self, key, value)

    @staticmethod
    def _create_nested_config(data: Dict[str, Any]) -> "Config":
        """创建嵌套的 Config 对象"""
        nested_config = Config()
        nested_config._set_attributes(data)
        return nested_config

    def __str__(self):
        """返回配置信息的字符串表示"""
        return str(self.__dict__)
