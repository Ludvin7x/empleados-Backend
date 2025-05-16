from app.routes import departments, employees
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.db import init_db, seed_data, init_app

api = Api(version='1.0', title='API Gestión Empleados', description='Una API para gestionar empleados y departamentos')

def create_app():
    app = Flask(__name__)

    import re
    def cors_origin_checker(origin):
        if origin is None:
            return False
        allowed_origins = [
            "http://localhost:4200",
            "https://portafolio-lud.netlify.app",
        ]
        netlify_pattern = re.compile(r"^https://.*\.netlify\.app$")
        return origin in allowed_origins or netlify_pattern.match(origin)

    CORS(
        app,
        origins=cors_origin_checker,
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )

    # Inicializar extensión DB y cerrar conexión automáticamente
    init_app(app)

    from app.routes import health

    api.init_app(app)
    api.add_namespace(employees.ns, path='/api/empleados')
    api.add_namespace(departments.ns, path='/api/departamentos')
    api.add_namespace(health.ns, path='/health')

    # Comandos CLI para base de datos
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Base de datos inicializada desde CLI")

    @app.cli.command("insert-data")
    def insert_data_command():
        insertar_datos()
        print("Datos insertados desde CLI")

    return app