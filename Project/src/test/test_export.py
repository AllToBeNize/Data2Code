from test_schema import skill_model
from backends.csharp.exporter import CSharpBackend


backend = CSharpBackend()
cs_code = backend.export_model(skill_model)

print(cs_code)
