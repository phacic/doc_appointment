from enum import Enum


class ChoiceBase(Enum):
    """base class for model choice fields as Enum"""

    @classmethod
    def model_choice(cls):
        """return a list of (name, value) to be used as choice field in models"""
        return [(d.value, d.name) for d in cls]

    @classmethod
    def to_list(cls):
        return [d.value for d in cls]
