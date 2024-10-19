import Field
from typing import List


class Message:
    def __init__(self):
        self._name = ""
        self._label = ""
        self._fields: List[Field.Field] = []  # vector of fields

    def get_name(self) -> str:
        return self._name

    def get_label(self) -> str:
        return self._label

    def add_field(self, field):
        self._fields.append(field)

    def remove_field(self, name: str):
        for field in self._fields:
            if field.get_name() == name:
                self._fields.remove(field)

    def set_info(self, info):
        self._name = info["name"]
        self._label = info["label"]
        for field_dict in info["fields"]:
            self.add_field(Field.Field.create_field_by_dict(field_dict))

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name
        res_dict["label"] = self._label
        fields_list = list()
        for field in self._fields:
            fields_list.append(field.to_dict())
        res_dict["fields"] = fields_list
        return res_dict

    def __str__(self) -> str:
        """
        Generate a string representation of the Message object.
    
        Parameters:
        -----------
        self : Message
            The Message object for which the string representation is to be generated.
    
        Returns:
        --------
        str
            A string representation of the Message object in the format:
            "Message Name: <name>, Label: <label>, Fields: <fields>"
        """
        return f"Message Name: {self._name}, Label: {self._label}, Fields: {self._fields}"
