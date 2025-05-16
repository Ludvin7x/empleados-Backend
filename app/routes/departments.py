# app/routes/departments.py
from flask import request
from flask_restx import Namespace, Resource
from app.db import get_db

ns = Namespace('departments', description='Department operations')

def row_to_department(row):
    return {
        "id": row["id"],
        "name": row["name"].strip() if row["name"] else "Unknown"
    }

@ns.route('/')
class DepartmentList(Resource):
    def options(self):
        return {}, 200

    # GET /api/departments
    def get(self):
        db = get_db()
        rows = db.execute('SELECT * FROM departments ORDER BY id').fetchall()
        return [row_to_department(r) for r in rows], 200

    # POST /api/departments
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or not data['name'].strip():
            return {"message": "The 'name' field is required and cannot be empty."}, 400

        try:
            db = get_db()
            cur = db.execute(
                'INSERT INTO departments (name) VALUES (?)',
                (data['name'].strip(),)
            )
            db.commit()
            department_id = cur.lastrowid
            row = db.execute('SELECT * FROM departments WHERE id = ?', (department_id,)).fetchone()
            return row_to_department(row), 201
        except Exception as e:
            return {"message": f"Error inserting department: {e}"}, 500


@ns.route('/<int:id>')
class Department(Resource):
    def options(self, id):
        return {}, 200

    # GET /api/departments/<id>
    def get(self, id):
        db = get_db()
        row = db.execute('SELECT * FROM departments WHERE id = ?', (id,)).fetchone()
        if not row:
            return {"message": "Department not found"}, 404
        return row_to_department(row), 200

    # PUT /api/departments/<id>
    def put(self, id):
        data = request.get_json()
        if not data or 'name' not in data or not data['name'].strip():
            return {"message": "The 'name' field is required and cannot be empty."}, 400

        db = get_db()
        if not db.execute('SELECT 1 FROM departments WHERE id = ?', (id,)).fetchone():
            return {"message": "Department not found"}, 404

        try:
            db.execute(
                'UPDATE departments SET name = ? WHERE id = ?',
                (data['name'].strip(), id)
            )
            db.commit()
            row = db.execute('SELECT * FROM departments WHERE id = ?', (id,)).fetchone()
            return row_to_department(row), 200
        except Exception as e:
            return {"message": f"Error updating department: {e}"}, 500

    # DELETE /api/departments/<id>
    def delete(self, id):
        db = get_db()
        if not db.execute('SELECT 1 FROM departments WHERE id = ?', (id,)).fetchone():
            return {"message": "Department not found"}, 404
        try:
            db.execute('DELETE FROM departments WHERE id = ?', (id,))
            db.commit()
            return {"message": f"Department with id {id} deleted successfully"}, 200
        except Exception as e:
            return {"message": f"Error deleting department: {e}"}, 500