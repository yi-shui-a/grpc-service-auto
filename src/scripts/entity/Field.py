class Field:
    def __init__(self):
        self._id: int = 0
        self._name: str = ""
        self._description: str = ""
        self._type: str = ""
        self._type_idl: str = ""
        self._type_proto: str = ""
        self._repeated: bool = False
        self._map: bool = False
        self._key: str = ""
        self._value: str = ""
        self._chinese_name: str = ""

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    # @staticmethod
    # def create_field(
    #     field_id, name,description:str = "", field_type, repeated, map, key, value, chinese_name
    # ):
    #     field = Field()
    #     field._id = field_id
    #     field._name = name
    #     field._description = description
    #     field._type = field_type
    #     field._repeated = repeated
    #     field._map = map
    #     field._key = key
    #     field._value = value
    #     field._chinese_name = chinese_name
    #     return field

    @staticmethod
    def create_field_by_dict(info: dict):
        field = Field()
        field._id = info.get("id", "")
        field._name = info.get("name", "")
        field._description = info.get("description", "")
        field._type = info.get("type", "")
        field._type_idl = info.get("type_idl", "")
        field._type_proto = info.get("type_proto", "")
        field._repeated = info.get("repeated", False)
        field._map = info.get("map", False)
        field._key = info.get("key", "")
        field._value = info.get("value", "")
        field._chinese_name = info.get("chinese_name", "")
        return field

    def set_info(self, info: dict):
        self._id = info.get("id", "")
        self._name = info.get("name", "")
        self._description = info.get("description", "")
        self._type = info.get("type", "")
        self._type_idl = info.get("type_idl", "")
        self._type_proto = info.get("type_proto", "")
        self._repeated = info.get("repeated", False)
        self._map = info.get("map", False)
        self._key = info.get("key", "")
        self._value = info.get("value", "")
        self._chinese_name = info.get("chinese_name", "")

    def to_dict(self):
        res_dict = dict()
        res_dict["id"] = self._id
        res_dict["name"] = self._name
        res_dict["description"] = self._description
        res_dict["type"] = self._type
        res_dict["type_idl"] = self._type_idl
        res_dict["type_proto"] = self._type_proto
        res_dict["repeated"] = self._repeated
        res_dict["map"] = self._map
        res_dict["key"] = self._key
        res_dict["value"] = self._value
        res_dict["chinese_name"] = self._chinese_name
        return res_dict

    def __str__(self):
        return f"ID: {self._id}, Name: {self._name}, Type: {self._type}, Chinese Name: {self._chinese_name}"
