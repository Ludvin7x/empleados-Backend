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
        origins=["http://localhost:4200", "https://portafolio-lud.netlify.app"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"]
    )

    init_app(app)

    from app.routes import health

    api.init_app(app)
    api.add_namespace(employees.ns, path='/api/empleados')
    api.add_namespace(departments.ns, path='/api/departamentos')
    api.add_namespace(health.ns, path='/health')

  # ---- CLI commands 
    @app.cli.command("init-db")
    def init_db_command():
        """Create tables."""
        init_db()
        print("Database initialized via CLI")

    @app.cli.command("seed-data")
    def seed_data_command():
        """Insert seed data."""
        seed_data()
        print("Seed data inserted via CLI")

    return app