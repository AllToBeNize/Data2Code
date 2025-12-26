# export.py

import os
import argparse
from schema.parser import parse_models_sheet, parse_enums_sheet, validate_schema
from backends.factory import get_backend
from exporters.factory import get_data_exporter

def find_excel_files(root_dir):
    """递归查找目录下所有 .xlsx / .xls 文件"""
    excel_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith((".xlsx", ".xls")) and not f.startswith("~$"):
                excel_files.append(os.path.join(dirpath, f))
    return excel_files

def export_code(models, enums, backend, base_dir):
    """统一导出枚举和模型代码"""
    # Enums
    enums_dir = os.path.join(base_dir, "Enums")
    os.makedirs(enums_dir, exist_ok=True)
    for enum in enums.values():
        out_file = os.path.join(enums_dir, f"{enum.name}.{backend.file_ext}")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(backend.export_enum(enum))
        print(f"导出 Enum {enum.name} 到 {out_file}")

    # Models
    models_dir = os.path.join(base_dir, "Models")
    os.makedirs(models_dir, exist_ok=True)
    for model in models:
        out_file = os.path.join(models_dir, f"{model.name}.{backend.file_ext}")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(backend.export_model(model))
        print(f"导出 Model {model.name} 到 {out_file}")

def export_data(file_path, models, enums, data_exporter, base_dir):
    """统一导出 DataTables"""
    data_dict = data_exporter.export_data(file_path, models, enums)
    data_dir = os.path.join(base_dir, "DataTables")
    os.makedirs(data_dir, exist_ok=True)
    data_exporter.write_file(data_dict, data_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="Excel 文件所在目录")
    parser.add_argument("--lang", default="csharp", help="选择导出语言: csharp, python, cpp")
    parser.add_argument("--data", default="json", help="数据导出类型: json, bin")
    parser.add_argument("--out", default="output", help="输出目录")
    args = parser.parse_args()

    backend = get_backend(args.lang)
    data_exporter = get_data_exporter(args.data)

    excel_files = find_excel_files(args.dir)
    if not excel_files:
        print(f"未找到 Excel 文件: {args.dir}")
        return

    for file_path in excel_files:
        print(f"\n处理文件: {file_path}")
        enums = parse_enums_sheet(file_path)
        models = parse_models_sheet(file_path, enums)
        validate_schema(file_path, models, enums)

        base_out_dir = args.out
        os.makedirs(base_out_dir, exist_ok=True)

        # 导出代码
        export_code(models, enums, backend, base_out_dir)

        # 导出数据
        if data_exporter:
            export_data(file_path, models, enums, data_exporter, base_out_dir)

if __name__ == "__main__":
    main()
