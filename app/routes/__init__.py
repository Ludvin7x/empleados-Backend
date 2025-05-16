from flask import Flask
from flask_restx import Api
from flask_cors import CORS

api = Api(version='1.0', title='API Gestión Empleados', description='Una API para gestionar empleados y departamentos')

def create_app():
    app = Flask(__name__)

    # Configurar CORS
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
    api.add_namespace(health.ns, path='api/health')

    return app