import sqlite3

def get_db():
    conn = sqlite3.connect('empleados.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            departamento_id INTEGER NOT NULL,
            fecha_contratacion TEXT NOT NULL,
            nombre_cargo TEXT NOT NULL
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )''')
        conn.commit()