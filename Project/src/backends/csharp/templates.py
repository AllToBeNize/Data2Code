CLASS_TEMPLATE = """public class {name}
{{
{fields}
}}
"""

ENUM_TEMPLATE = """public enum {name} : {underlying}
{{
{members}
}}
"""

FIELD_TEMPLATE = "    public {type} {name} {{ get; set; }}{comment}"
ENUM_MEMBER_TEMPLATE = "    {name} = {value},"
