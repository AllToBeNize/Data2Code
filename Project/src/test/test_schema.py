# test_schema.py
from schema.types import BasicType
from schema.field import FieldDef
from schema.model import ModelDef

INT    = BasicType("int")
FLOAT  = BasicType("float")
STRING = BasicType("string")
BOOL   = BasicType("bool")

skill_model = ModelDef(
    name="SkillConfig",
    fields=[
        FieldDef("Id", INT, "主键"),
        FieldDef("Name", STRING, "技能名"),
        FieldDef("Damage", FLOAT, "伤害"),
        FieldDef("IsPassive", BOOL, "是否被动"),
    ]
)
