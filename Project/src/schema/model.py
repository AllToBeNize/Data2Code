from dataclasses import dataclass
from .field import FieldDef

@dataclass
class ModelDef:
    name: str
    fields: list[FieldDef]