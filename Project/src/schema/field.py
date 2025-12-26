from dataclasses import dataclass
from .types import BasicType

@dataclass
class FieldDef:
    name: str
    type: BasicType
    comment: str