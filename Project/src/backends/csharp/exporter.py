from backends.csharp.types import to_csharp_type
from backends.csharp.templates import CLASS_TEMPLATE, ENUM_TEMPLATE, FIELD_TEMPLATE, ENUM_MEMBER_TEMPLATE
from schema.model import ModelDef
from schema.field import FieldDef
from schema.types import EnumType

class CSharpBackend:
    file_ext = "cs"  # 文件扩展名

    def export_model(self, model: ModelDef) -> str:
        lines = []
        for field in model.fields:
            csharp_type = to_csharp_type(field.type)
            comment = f" // {field.comment}" if field.comment else ""
            if field.is_primary:
                comment += " [PrimaryKey]"
            lines.append(FIELD_TEMPLATE.format(
                type=csharp_type,
                name=field.name,
                comment=comment
            ))
        return CLASS_TEMPLATE.format(
            name=model.name,
            fields="\n".join(lines)
        )

    def export_enum(self, enum: EnumType) -> str:
        members_lines = [
            ENUM_MEMBER_TEMPLATE.format(name=name, value=value)
            for name, value in enum.members.items()
        ]
        return ENUM_TEMPLATE.format(
            name=enum.name,
            underlying=enum.underlying or "int",
            members="\n".join(members_lines)
        )
