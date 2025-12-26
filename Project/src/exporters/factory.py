# exporters/factory.py

from .json_exporter import JSONExporter
from .binary_exporter import BinaryExporter

def get_data_exporter(data_type: str):
    """
    根据类型返回数据导出器
    data_type: 'json' 或 'bin'
    """
    data_type = data_type.lower()
    if data_type == "json":
        return JSONExporter()
    elif data_type in ("bin", "binary"):
        return BinaryExporter()
    else:
        raise ValueError(f"未知数据导出类型: {data_type}")
