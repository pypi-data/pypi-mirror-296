from .custom_configuration import CustomConfigExample
from batchframe import inject
from dataclasses import dataclass

@inject()
@dataclass()
class CustomConfigOne(CustomConfigExample):
    new_field: str = "overwritten"
    newer_field: str = "hey"