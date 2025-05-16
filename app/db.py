import sqlite3
import click
import os

# Ruta absoluta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'empleados.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
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
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO departamentos (id, nombre) VALUES (?, ?)", departamentos)
        cursor.executemany(
            "INSERT OR IGNORE INTO empleados (id, nombre, apellido, departamento_id, fecha_contratacion, nombre_cargo) VALUES (?, ?, ?, ?, ?, ?)", 
            empleados
        )
    click.echo('Datos iniciales insertados')
