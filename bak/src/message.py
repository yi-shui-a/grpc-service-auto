from typing import List
from .field import Field

class Message:
    def __init__(self, label: str, name: str, fields: List[Field]):
        self.label = label
        self.name = name
        self.fields = fields

    def __str__(self):
        return f"Message(label={self.label}, name={self.name}, fields={self.fields})"