# exporters/json_exporter.py

import os
import json
from openpyxl import load_workbook
from .base import BaseExporter
from schema.types import BasicType, EnumType, ArrayType, CustomType

class JSONExporter(BaseExporter):
    file_ext = "json"

    def export_data(self, file_path, models, enums):
        """返回 dict 数据，不写文件"""
        wb = load_workbook(file_path, data_only=True)
        data_dict = {}

        for model in models:
            sheet_name = model.name
            if sheet_name not in wb.sheetnames:
                print(f"跳过 {sheet_name}, sheet 不存在")
                continue
            ws = wb[sheet_name]

            data_list = []
            for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                if all(v is None for v in row):
                    continue

                if len(row) < len(model.fields):
                    raise ValueError(f"{file_path} Sheet {sheet_name} 第 {row_idx} 行字段数量不足，期望 {len(model.fields)} 列，实际 {len(row)} 列")

                obj = {}
                for field, value in zip(model.fields, row):
                    # 类型校验
                    if isinstance(field.type, BasicType):
                        obj[field.name] = value
                    elif isinstance(field.type, EnumType):
                        if isinstance(value, int):
                            obj[field.name] = value
                        elif isinstance(value, str):
                            if value not in field.type.members:
                                raise ValueError(f"{file_path} Sheet {sheet_name} 第 {row_idx} 行枚举值 '{value}' 无效")
                            obj[field.name] = field.type.members[value]
                        else:
                            raise ValueError(f"{file_path} Sheet {sheet_name} 第 {row_idx} 行枚举字段 '{field.name}' 类型错误")
                    elif isinstance(field.type, CustomType):
                        # 默认填的是引用 ID 或对象名
                        obj[field.name] = value
                    elif isinstance(field.type, ArrayType):
                        if isinstance(value, str):
                            obj[field.name] = [e.strip() for e in value.split(",")]
                        elif value is None:
                            obj[field.name] = []
                        else:
                            raise ValueError(f"{file_path} Sheet {sheet_name} 第 {row_idx} 行数组字段 '{field.name}' 类型错误")
                data_list.append(obj)
            data_dict[model.name] = data_list
        return data_dict

    def write_file(self, data_dict, output_dir):
        """写出 JSON 文件，每个 DataTable 文件名前加 DT_"""
        os.makedirs(output_dir, exist_ok=True)
        for model_name, data_list in data_dict.items():
            out_file = os.path.join(output_dir, f"DT_{model_name}.{self.file_ext}")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"导出 DataTable {model_name} 到 {out_file}")
