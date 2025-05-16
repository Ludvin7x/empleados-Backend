from flask_restx import Namespace, Resource

ns = Namespace('health', description='Health Check')

@ns.route('/')
class HealthCheck(Resource):
    def get(self):
        return {'status': 'ok'}, 200
