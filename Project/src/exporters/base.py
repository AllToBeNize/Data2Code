# exporters/base_data_exporter.py
from abc import ABC, abstractmethod

class BaseDataExporter(ABC):
    file_ext: str = "data"

    @abstractmethod
    def export_data(self, file_path, models, enums):
        """解析 Excel 数据，返回 dict"""
        pass

    @abstractmethod
    def write_file(self, data_dict, output_dir):
        """写入文件"""
        pass
