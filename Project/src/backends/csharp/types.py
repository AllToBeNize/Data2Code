from schema.types import BasicType, ArrayType, EnumType, CustomType

C_SHARP_TYPE_MAP = {
    "int": "int",
    "float": "float",
    "string": "string",
    "bool": "bool",
}

def to_csharp_type(type_obj):
    if isinstance(type_obj, BasicType):
        return C_SHARP_TYPE_MAP.get(type_obj.name.lower(), "object")
    elif isinstance(type_obj, ArrayType):
        elem_type = to_csharp_type(type_obj.element_type)
        return f"{elem_type}[]"
    elif isinstance(type_obj, CustomType):
        return type_obj.name
    elif isinstance(type_obj, EnumType):
        return type_obj.name
    else:
        return "object"
