from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import sqlite3
import click

api = Api(version='1.0', title='API Gestión Empleados', description='Una API para gestionar empleados y departamentos')

def init_db():
    with sqlite3.connect('empleados.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            departamento_id INTEGER NOT NULL,
            fecha_contratacion TEXT NOT NULL,
            nombre_cargo TEXT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )''')
    click.echo('Base de datos inicializada')

def insertar_datos():
    departamentos = [
        (1, 'Recursos Humanos'),
        (2, 'Informatica'),
        (3, 'Ventas'),
        (4, 'Marketing'),
        (5, 'Bodega')
    ]
    empleados = [
        (1, 'Juan', 'Pérez', 1, '2023-01-01', 'Gerente'),
        (2, 'María', 'Gómez', 2, '2023-01-02', 'Desarrollador'),
        (3, 'Carlos', 'Lopez', 3, '2023-01-03', 'Vendedor'),
        (4, 'Ana', 'Fernández', 4, '2023-01-04', 'Marketing Specialist')
    ]
    with sqlite3.connect('empleados.db') as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO departamentos (id, nombre) VALUES (?, ?)", departamentos)
        cursor.executemany(
            "INSERT OR IGNORE INTO empleados (id, nombre, apellido, departamento_id, fecha_contratacion, nombre_cargo) VALUES (?, ?, ?, ?, ?, ?)", 
            empleados
        )
    click.echo('Datos iniciales insertados')

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {
        "origins": "http://localhost:4200",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True
    }})

    from app.routes import empleados, departamentos, health
    api.init_app(app)
    api.add_namespace(empleados.ns, path='/api/empleados')
    api.add_namespace(departamentos.ns, path='/api/departamentos')
    api.add_namespace(health.ns, path='/health')

    @app.cli.command("init-db")
    def init_db_command():
        """Inicializa la base de datos (crea tablas)"""
        init_db()

    @app.cli.command("insert-data")
    def insert_data_command():
        """Inserta datos iniciales en la base de datos"""
        insertar_datos()

    return app