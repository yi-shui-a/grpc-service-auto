class Field:
    def __init__(self):
        self._id: int = 0
        self._name = ""
        self._type = ""
        self._repeated: bool = False
        self._key = ""
        self._value = ""
        self._chinese_name = ""


    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    @staticmethod
    def create_field(field_id, name, field_type, repeated, key, value, chinese_name):
        field = Field()
        field._id = field_id
        field._name = name
        field._type = field_type
        field._repeated = repeated
        field._key = key
        field._value = value
        field._chinese_name = chinese_name
        return field

    @staticmethod
    def create_field_by_dict(info):
        field = Field()
        field._id = info.get("id","")
        field._name = info.get("name","")
        field._type = info.get("type","")
        field._repeated = info.get("repeated",False)
        field._key = info.get("key","")
        field._value = info.get("value","")
        field._chinese_name = info.get("chinese_name","")
        return field

    def to_dict(self):
        res_dict = dict()
        res_dict["id"] = self._id
        res_dict["name"] = self._name
        res_dict["type"] = self._type
        res_dict["repeated"] = self._repeated
        res_dict["key"] = self._key
        res_dict["value"] = self._value
        return res_dict

    def __str__(self):
        return str(
            f"id: {self._id}, name: {self._name}, type: {self._type},repeated: {self._repeated}, key: {self._key}, value: {self._value}, chinese_name: {self._chinese_name}")
