class BaseInfo:
    def __init__(self, name: str, chinese_name: str, description: str, version: str, build_time: str, priority_level: int, license: str, servicePath: str):
        self.name = name
        self.chinese_name = chinese_name
        self.description = description
        self.version = version
        self.build_time = build_time
        self.priority_level = priority_level
        self.license = license
        self.servicePath = servicePath