from backends.base import Backend
from backends.csharp.types import CS_TYPE_MAP
from backends.csharp.templates import model_template

class CSharpBackend(Backend):
    def export_model(self, model):
        return model_template(model, CS_TYPE_MAP)
