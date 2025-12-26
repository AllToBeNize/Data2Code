from abc import ABC, abstractmethod

class BaseBackend(ABC):
    file_ext: str = ""  # 文件扩展名

    @abstractmethod
    def export_enum(self, enum):
        """导出枚举代码"""
        pass

    @abstractmethod
    def export_model(self, model):
        """导出模型代码"""
        pass
