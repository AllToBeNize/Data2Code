from dataclasses import dataclass

@dataclass(frozen=True)
class BasicType:
    name: str   # int / float / string / bool