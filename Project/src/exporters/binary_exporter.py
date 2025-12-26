# exporters/bin_exporter.py
import os
import struct
from exporters.base import BaseDataExporter

class BinaryExporter(BaseDataExporter):
    file_ext = "bin"

    def export_data(self, file_path, models, enums):
        """
        返回 dict 数据，不写文件
        复用 JSONExporter 的解析逻辑
        """
        from .json_exporter import JSONExporter
        json_exporter = JSONExporter()
        return json_exporter.export_data(file_path, models, enums)

    def write_file(self, data_dict, output_dir):
        """
        写入二进制文件，并生成 mapping.json
        """
        os.makedirs(output_dir, exist_ok=True)
        mapping = {}

        for model_name, data_list in data_dict.items():
            out_file_name = f"DT_{model_name}.{self.file_ext}"
            out_file = os.path.join(output_dir, out_file_name)
            with open(out_file, "wb") as f:
                for row in data_list:
                    for key, value in row.items():
                        if isinstance(value, int):
                            f.write(struct.pack("<i", value))
                        elif isinstance(value, float):
                            f.write(struct.pack("<f", value))
                        elif isinstance(value, str):
                            encoded = value.encode("utf-8")
                            f.write(struct.pack("<I", len(encoded)))
                            f.write(encoded)
                        elif isinstance(value, list):
                            f.write(struct.pack("<I", len(value)))
                            for e in value:
                                if isinstance(e, str):
                                    encoded = e.encode("utf-8")
                                    f.write(struct.pack("<I", len(encoded)))
                                    f.write(encoded)
                                elif isinstance(e, int):
                                    f.write(struct.pack("<i", e))
                                elif isinstance(e, float):
                                    f.write(struct.pack("<f", e))
                                else:
                                    raise TypeError(f"不支持的列表元素类型: {type(e)}")
                        else:
                            raise TypeError(f"不支持的数据类型: {type(value)}")
            print(f"导出 DataTable {model_name} 到 {out_file}")
            mapping[model_name] = out_file_name

        # 生成 mapping.json
        mapping_file = os.path.join(output_dir, "mapping.json")
        with open(mapping_file, "w", encoding="utf-8") as f:
            import json
            json.dump(mapping, f, ensure_ascii=False, indent=4)
        print(f"生成映射文件 {mapping_file}")
