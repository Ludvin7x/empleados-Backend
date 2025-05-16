from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db
from app.validators import validate_employee  # Cambiado a inglés

ns = Namespace('employees', description='Employee operations')

@ns.route('/')
class EmployeeList(Resource):
    def options(self):
        return {}, 200

    def get(self):
        conn = get_db()
        employees = conn.execute('SELECT * FROM employees').fetchall()
        return [dict(e) for e in employees], 200

    def post(self):
        data = request.get_json()
        is_valid, message = validate_employee(data)
        if not is_valid:
            return {'message': message}, 400
        try:
            conn = get_db()
            cur = conn.execute(
                '''INSERT INTO employees (first_name, last_name, department_id, hire_date, job_title)
                   VALUES (?, ?, ?, ?, ?)''',
                (data['first_name'], data['last_name'], data['department_id'], data['hire_date'], data['job_title'])
            )
            conn.commit()
            data['id'] = cur.lastrowid
            return data, 201
        except Exception as e:
            return {'message': 'Error inserting employee: ' + str(e)}, 500