def model_template(model, type_map):
    lines = [f"public class {model.name}", "{"]

    for f in model.fields:
        cs_type, _ = type_map[f.type.name]
        lines.append(f"    /// <summary>{f.comment}</summary>")
        lines.append(f"    public {cs_type} {f.name};\n")

    lines.append("}")
    return "\n".join(lines)
