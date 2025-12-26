from abc import ABC, abstractmethod
from schema import ModelDef

class Backend(ABC):

    @abstractmethod
    def export_model(self, model: ModelDef) -> str:
        pass