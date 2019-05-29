from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def get_choices(cls):
        return [(item.name, item.value) for item in cls]
