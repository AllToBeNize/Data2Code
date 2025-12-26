from dataclasses import dataclass
from schema.types import SchemaType

@dataclass
class FieldDef:
    name: str
    type: SchemaType
    comment: str = ""
    is_primary: bool = False