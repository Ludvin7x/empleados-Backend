from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db
from app.validators import validate_employee

ns = Namespace('employees', description='Employee operations')

def row_to_employee(row):
    return {
        "id": row["id"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "job_title": row["job_title"],
        "hire_date": row["hire_date"],
        "department": {
            "id": row["department_id"],
            "name": row["department_name"] or "Unknown"
        }
    }

@ns.route('/')
class EmployeeList(Resource):
    def options(self):
        return {}, 200

    def get(self):
        conn = get_db()
        query = '''
            SELECT e.id, e.first_name, e.last_name, e.job_title, e.hire_date,
                   d.id as department_id, d.name as department_name
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            ORDER BY e.id
        '''
        rows = conn.execute(query).fetchall()
        return [row_to_employee(r) for r in rows], 200

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
            new_id = cur.lastrowid
            row = conn.execute('''
                SELECT e.id, e.first_name, e.last_name, e.job_title, e.hire_date,
                       d.id as department_id, d.name as department_name
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE e.id = ?
            ''', (new_id,)).fetchone()
            return row_to_employee(row), 201
        except Exception as e:
            return {'message': 'Error inserting employee: ' + str(e)}, 500
        
@ns.route('/<int:id>')
@ns.route('/<int:id>/')
class Employee(Resource):
    def options(self, id):
        return {}, 200

    def get(self, id):
        conn = get_db()
        row = conn.execute('''
            SELECT e.id, e.first_name, e.last_name, e.job_title, e.hire_date,
                   d.id as department_id, d.name as department_name
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = ?
        ''', (id,)).fetchone()

        if row is None:
            return {'message': 'Employee not found'}, 404
        return row_to_employee(row), 200

    def put(self, id):
        data = request.get_json()
        is_valid, message = validate_employee(data)
        if not is_valid:
            return {'message': message}, 400

        conn = get_db()
        cur = conn.execute(
            '''UPDATE employees SET first_name=?, last_name=?, department_id=?, hire_date=?, job_title=? WHERE id=?''',
            (data['first_name'], data['last_name'], data['department_id'], data['hire_date'], data['job_title'], id)
        )
        conn.commit()

        if cur.rowcount == 0:
            return {'message': 'Employee not found'}, 404
        
        row = conn.execute('''
            SELECT e.id, e.first_name, e.last_name, e.job_title, e.hire_date,
                   d.id as department_id, d.name as department_name
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = ?
        ''', (id,)).fetchone()

        return row_to_employee(row), 200
    
    def delete(self, id):
        conn = get_db()
        cur = conn.execute('DELETE FROM employees WHERE id = ?', (id,))
        conn.commit()

        if cur.rowcount == 0:
            return {'message': 'Employee not found'}, 404
        return {'message': 'Employee deleted successfully'}, 200