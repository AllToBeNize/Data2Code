from backends.csharp.exporter import CSharpBackend
# from backends.python.exporter import PythonBackend
# from backends.cpp.exporter import CppBackend

def get_backend(language: str):
    """
    根据语言选择导出后端
    """
    language = language.lower()
    if language == "csharp":
        return CSharpBackend()
    # elif language == "python":
    #     return PythonBackend()
    # elif language == "cpp":
    #     return CppBackend()
    else:
        raise ValueError(f"未知导出语言: {language}")
