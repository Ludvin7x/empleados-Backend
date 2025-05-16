from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.db import init_db, insertar_datos  # importamos funciones DB

api = Api(version='1.0', title='API Gestión Empleados', description='Una API para gestionar empleados y departamentos')

def create_app():
    app = Flask(__name__)

    # Permitir Netlify y localhost
    ALLOWED_ORIGINS = [
        "http://localhost:4200",
        "https://portafolio-lud.netlify.app",
        r"https://.*\.netlify\.app"
    ]

    CORS(
        app,
        resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )

    # Importar namespaces después de crear la app
    from app.routes import empleados, departamentos, health
    api.init_app(app)
    api.add_namespace(empleados.ns, path='/api/empleados')
    api.add_namespace(departamentos.ns, path='/api/departamentos')
    api.add_namespace(health.ns, path='/health')

    # Comandos CLI
    @app.cli.command("init-db")
    def init_db_command():
        init_db()

    @app.cli.command("insert-data")
    def insert_data_command():
        insertar_datos()

    with app.app_context():
        init_db()
        insertar_datos()

    return app