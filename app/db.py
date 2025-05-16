import sqlite3
import click
import os
from flask import g

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'employees.db')

def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                hire_date TEXT NOT NULL,
                job_title TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        click.echo('Database initialized successfully')
    except Exception as e:
        click.echo(f'Error initializing database: {e}')

def seed_data():
    departments = [
        (1, 'Human Resources'),
        (2, 'IT'),
        (3, 'Sales'),
        (4, 'Marketing'),
        (5, 'Warehouse')
    ]
    employees = [
        (1, 'John', 'Perez', 1, '2023-01-01', 'Manager'),
        (2, 'Mary', 'Gomez', 2, '2023-01-02', 'Developer'),
        (3, 'Charles', 'Lopez', 3, '2023-01-03', 'Salesperson'),
        (4, 'Anna', 'Fernandez', 4, '2023-01-04', 'Marketing Specialist')
    ]
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO departments (id, name) VALUES (?, ?)", departments)
        cursor.executemany(
            "INSERT OR IGNORE INTO employees (id, first_name, last_name, department_id, hire_date, job_title) VALUES (?, ?, ?, ?, ?, ?)", 
            employees
        )
        conn.commit()
        conn.close()
        click.echo('Seed data inserted successfully')
    except Exception as e:
        click.echo(f'Error inserting seed data: {e}')

def init_app(app):
    app.teardown_appcontext(close_db)

@click.group()
def cli():
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()

@cli.command()
def seed():
    """Insert initial seed data."""
    seed_data()

if __name__ == '__main__':
    cli()
