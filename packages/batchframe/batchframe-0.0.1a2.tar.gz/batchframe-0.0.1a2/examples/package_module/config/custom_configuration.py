from batchframe import Configuration
from dataclasses import dataclass

@dataclass()
class CustomConfigExample(Configuration):
    new_field: str = "new"