from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db
from app.validators import validate_empleado

ns = Namespace('empleados', description='Operaciones con empleados')

@ns.route('/')
class EmpleadoList(Resource):
    def options(self):
        return {}, 200

    def get(self):
        conn = get_db()
        empleados = conn.execute('SELECT * FROM empleados').fetchall()
        return [dict(e) for e in empleados], 200

    def post(self):
        data = request.json
        is_valid, message = validate_empleado(data)
        if not is_valid:
            return {'message': message}, 400
        conn = get_db()
        cur = conn.execute('''INSERT INTO empleados (nombre, apellido, departamento_id, fecha_contratacion, nombre_cargo)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (data['nombre'], data['apellido'], data['departamento_id'], data['fecha_contratacion'], data['nombre_cargo']))
        data['id'] = cur.lastrowid
        return data, 201
