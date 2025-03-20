from typing import List
import sys
import os

from .Field import Field


class Message:
    def __init__(self):
        self._name: str = ""
        self._label: str = ""
        self._description: str = ""
        self._fields: List[Field] = list()  # vector of fields

    def get_name(self) -> str:
        return self._name

    def get_label(self) -> str:
        return self._label

    def get_description(self) -> str:
        return self._description

    def add_field(self, field: Field):
        if field is not None:
            self._fields.append(field)
        else:
            print("Warning: Attempted to add None to fields list")

    def remove_field(self, name: str):
        for field in self._fields:
            if field.get_name() == name:
                self._fields.remove(field)

    def set_info(self, info: dict):
        self._name = info.get("name", "")
        self._label = info.get("label", "")
        self._description = info.get("description", "")
        for field_dict in info["fields"]:
            temp = Field()
            temp.set_info(field_dict)  # set field info using field_dict
            self.add_field(temp)

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name
        res_dict["label"] = self._label
        res_dict["description"] = self._description
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
        return (
            f"Message Name: {self._name}, Label: {self._label}, Fields: {self._fields}"
        )
