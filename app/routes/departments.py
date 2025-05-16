from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db

ns = Namespace('departments', description='Department operations')

@ns.route('/')
class DepartmentList(Resource):
    def options(self):
        return {}, 200

    def get(self):
        conn = get_db()
        departments = conn.execute('SELECT * FROM departments').fetchall()
        return [dict(d) for d in departments], 200

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or not data['name'].strip():
            return {'message': "The 'name' field is required and cannot be empty."}, 400
        try:
            conn = get_db()
            cur = conn.execute(
                'INSERT INTO departments (name) VALUES (?)',
                (data['name'].strip(),)
            )
            conn.commit()
            data['id'] = cur.lastrowid
            return data, 201
        except Exception as e:
            return {'message': 'Error inserting department: ' + str(e)}, 500


@ns.route('/<int:id>')
class Department(Resource):
    def options(self):
        return {}, 200

    def get(self, id):
        conn = get_db()
        department = conn.execute('SELECT * FROM departments WHERE id = ?', (id,)).fetchone()
        if department is None:
            return {'message': 'Department not found'}, 404
        return dict(department), 200

    def put(self, id):
        data = request.get_json()
        if not data or 'name' not in data or not data['name'].strip():
            return {'message': "The 'name' field is required and cannot be empty."}, 400
        conn = get_db()
        department = conn.execute('SELECT * FROM departments WHERE id = ?', (id,)).fetchone()
        if department is None:
            return {'message': 'Department not found'}, 404
        try:
            conn.execute(
                'UPDATE departments SET name = ? WHERE id = ?',
                (data['name'].strip(), id)
            )
            conn.commit()
            return {'id': id, 'name': data['name'].strip()}, 200
        except Exception as e:
            return {'message': 'Error updating department: ' + str(e)}, 500

    def delete(self, id):
        conn = get_db()
        department = conn.execute('SELECT * FROM departments WHERE id = ?', (id,)).fetchone()
        if department is None:
            return {'message': 'Department not found'}, 404
        try:
            conn.execute('DELETE FROM departments WHERE id = ?', (id,))
            conn.commit()
            return {'message': f'Department with id {id} deleted successfully'}, 200
        except Exception as e:
            return {'message': 'Error deleting department: ' + str(e)}, 500
