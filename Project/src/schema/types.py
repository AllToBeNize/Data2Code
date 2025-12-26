from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class SchemaType:
    name: str


@dataclass(frozen=True)
class BasicType(SchemaType):
    pass


@dataclass(frozen=True)
class ArrayType:
    element_type: SchemaType

    @property
    def name(self) -> str:
        return f"{self.element_type.name}[]"


@dataclass(frozen=True)
class EnumType(SchemaType):
    members: Dict[str, int]
    underlying: str = "int"


@dataclass(frozen=True)
class CustomType(SchemaType):
    pass


@dataclass
class TypeRef:
    name: str
    resolved: Optional[SchemaType] = None
