# test_parser.py

import os
from schema.parser import parse_models_sheet, parse_enums_sheet, validate_schema
from backends.csharp.exporter import CSharpBackend

# -------------------------
# 配置 Excel 文件路径
# -------------------------
file_path = r"D:\Data2Code\Excel\Skill.xlsx"

# -------------------------
# 解析枚举和模型
# -------------------------
enums = parse_enums_sheet(file_path)
models = parse_models_sheet(file_path, enums)

# -------------------------
# 校验 schema
# -------------------------
try:
    validate_schema(file_path, models, enums)
except ValueError as e:
    print("Schema 校验失败:", e)
    exit(1)

# -------------------------
# 导出 C# 代码
# -------------------------
backend = CSharpBackend()

print("\n=== C# Enums ===\n")
for enum in enums.values():
    cs_enum_code = backend.export_enum(enum)
    print(cs_enum_code)
    print()

print("\n=== C# Models ===\n")
for model in models:
    cs_class_code = backend.export_model(model)
    print(cs_class_code)
    print()
