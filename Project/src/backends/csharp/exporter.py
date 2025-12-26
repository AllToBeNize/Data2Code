from base import Backend
from .types import CS_TYPE_MAP
from .templates import model_template

class CSharpBackend(Backend):
    def export_model(self, model):
        return model_template(model, CS_TYPE_MAP)
