import os
import json
from openpyxl import load_workbook
from exporters.base import BaseDataExporter
from schema.types import BasicType, EnumType, ArrayType, CustomType

class JSONExporter(BaseDataExporter):
    file_ext = "json"

    def export_data(self, file_path, models, enums):
        """返回 dict 数据，不写文件"""
        wb = load_workbook(file_path, data_only=True)
        data_dict = {}

        for model in models:
            sheet_name = model.name
            if sheet_name not in wb.sheetnames:
                continue
            ws = wb[sheet_name]

            data_list = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if all(v is None for v in row):
                    continue
                obj = {}
                for field, value in zip(model.fields, row):
                    if isinstance(field.type, BasicType):
                        obj[field.name] = value
                    elif isinstance(field.type, EnumType):
                        if isinstance(value, int):
                            obj[field.name] = value
                        elif isinstance(value, str):
                            obj[field.name] = field.type.members.get(value, 0)
                        else:
                            obj[field.name] = 0
                    elif isinstance(field.type, CustomType):
                        obj[field.name] = value
                    elif isinstance(field.type, ArrayType):
                        if isinstance(value, str):
                            obj[field.name] = [e.strip() for e in value.split(",")]
                        else:
                            obj[field.name] = []
                data_list.append(obj)
            data_dict[model.name] = data_list

        return data_dict

    def write_file(self, data_dict, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        mapping = {}

        for model_name, data_list in data_dict.items():
            out_file_name = f"DT_{model_name}.{self.file_ext}"
            out_file = os.path.join(output_dir, out_file_name)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"导出 DataTable {model_name} 到 {out_file}")
            mapping[model_name] = out_file_name

        # 写 mapping.json
        mapping_file = os.path.join(output_dir, "_mapping.json")
        with open(mapping_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=4)
        print(f"生成映射文件 {mapping_file}")
