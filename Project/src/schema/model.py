from dataclasses import dataclass
from schema.field import FieldDef

@dataclass
class ModelDef:
    name: str
    fields: list[FieldDef]