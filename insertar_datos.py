import sqlite3

def conectar():
    return sqlite3.connect('empleados.db')

def insertar_departamentos():
    departamentos = [
        ('Recursos Humanos',),
        ('Informatica',),
        ('Ventas',),
        ('Marketing',),
        ('Bodega',)
    ]
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO departamentos (nombre) VALUES (?)", departamentos)
            print("Departamentos insertados correctamente.")
        except sqlite3.IntegrityError:
            print("Los departamentos ya están insertados o hubo un error de integridad.")

def insertar_empleados():
    empleados = [
        ('Juan', 'Pérez', 1, '2023-01-01', 'Gerente'),  
        ('María', 'Gómez', 2, '2023-01-02', 'Desarrollador'),
        ('Carlos', 'Lopez', 3, '2023-01-03', 'Vendedor'),
        ('Ana', 'Fernández', 4, '2023-01-04', 'Marketing Specialist')
    ]
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany(
                "INSERT INTO empleados (nombre, apellido, departamento_id, fecha_contratacion, nombre_cargo) VALUES (?, ?, ?, ?, ?)", 
                empleados)
            print("Empleados insertados correctamente.")
        except sqlite3.IntegrityError:
            print("Los empleados ya están insertados o hubo un error de integridad.")

if __name__ == '__main__':
    insertar_departamentos()
    insertar_empleados()