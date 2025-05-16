def validate_empleado(data):
    required_fields = ['nombre', 'apellido', 'departamento_id', 'fecha_contratacion', 'nombre_cargo']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"El campo '{field}' es requerido."
    return True, ""