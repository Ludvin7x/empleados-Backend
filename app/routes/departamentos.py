from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db

ns = Namespace('departamentos', description='Operaciones con departamentos')

@ns.route('/')
class DepartamentoList(Resource):
    def options(self):
        return {}, 200

    def get(self):
        conn = get_db()
        departamentos = conn.execute('SELECT * FROM departamentos').fetchall()
        return [dict(d) for d in departamentos], 200

    def post(self):
        data = request.json
        if 'nombre' not in data or not data['nombre']:
            return {'message': "El campo 'nombre' es requerido."}, 400
        conn = get_db()
        cursor = conn.execute(
            'INSERT INTO departamentos (nombre) VALUES (?)',
            (data['nombre'],)
        )
        data['id'] = cursor.lastrowid
        return data, 201
