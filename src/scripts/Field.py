class Field:
    def __init__(self):
        self._id: int = 0
        self._name = ""
        self._type = ""
        self._type_proto = ""
        self._repeated: bool = False
        self._map: bool = False
        self._key = ""
        self._value = ""
        self._chinese_name = ""


    def get_id(self):
        return self._id

    def get_name(self):
        return self._name
    
    def __type_convert(self):
        
        pass
    

    @staticmethod
    def create_field(field_id, name, field_type, repeated,map, key, value, chinese_name):
        field = Field()
        field._id = field_id
        field._name = name
        field._type = field_type
        field._repeated = repeated
        field._map = map
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
        field._type_proto = info.get("type_proto","")
        field._repeated = info.get("repeated",False)
        field._map = info.get("map",False)
        field._key = info.get("key","")
        field._value = info.get("value","")
        field._chinese_name = info.get("chinese_name","")
        return field

    def to_dict(self):
        res_dict = dict()
        res_dict["id"] = self._id
        res_dict["name"] = self._name
        res_dict["type"] = self._type
        res_dict["type_proto"] = self._type_proto
        res_dict["repeated"] = self._repeated
        res_dict["map"] = self._map
        res_dict["key"] = self._key
        res_dict["value"] = self._value
        res_dict["chinese_name"] = self._chinese_name
        return res_dict

    def __str__(self):
        return str(
            f"id: {self._id}, name: {self._name}, type: {self._type},repeated: {self._repeated}, key: {self._key}, value: {self._value}, chinese_name: {self._chinese_name}")
