# exporters/base.py

from abc import ABC, abstractmethod

class BaseExporter(ABC):
    """导出器基类（JSON / Binary / CSV 等）"""

    @property
    @abstractmethod
    def file_ext(self):
        """文件扩展名，例如 json / bin"""
        pass

    @abstractmethod
    def export_data(self, file_path, models, enums):
        """解析 Excel 并返回数据字典 {model_name: data_list}"""
        pass

    def write_file(self, data_dict, output_dir):
        """统一写文件操作"""
        import os, json
        os.makedirs(output_dir, exist_ok=True)
        for model_name, data_list in data_dict.items():
            out_file = os.path.join(output_dir, f"{model_name}.{self.file_ext}")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"导出 {model_name} 到 {out_file}")
