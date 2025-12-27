# exporters/bin_exporter.py
import os
import struct
from .base import BaseDataExporter
from .json_exporter import JSONExporter

class BinaryExporter(BaseDataExporter):
    file_ext = "bin"

    def export_data(self, file_path, models, enums):
        # 复用 JSONExporter 解析 Excel
        return JSONExporter().export_data(file_path, models, enums)

    def write_file(self, data_dict, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for model_name, data_list in data_dict.items():
            out_file = os.path.join(output_dir, f"DT_{model_name}.{self.file_ext}")
            with open(out_file, "wb") as f:
                for row in data_list:
                    for value in row.values():
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
                                if isinstance(e, int):
                                    f.write(struct.pack("<i", e))
                                elif isinstance(e, float):
                                    f.write(struct.pack("<f", e))
                                elif isinstance(e, str):
                                    encoded = e.encode("utf-8")
                                    f.write(struct.pack("<I", len(encoded)))
                                    f.write(encoded)
                                else:
                                    raise TypeError(f"不支持的列表元素类型: {type(e)}")
                        else:
                            raise TypeError(f"不支持的数据类型: {type(value)}")
            print(f"导出 DataTable {model_name} 到 {out_file}")
