from flask_restful import Resource
from flask import request
import models.schema.bems as bems_schema
import models.schema.hems as hems_schema
from config import app

class Hems (Resource):
    def post(self, name):
        if name not in app.config['HEMS_ACCEPT']:
            return {
                'message': 'Type Not Included!'
            }, 403
        type_schema = hems_schema.aggregator_distribution(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 400

        return {
            'message': 'OK!'
        }, 200

# 拆掉
class Bems (Resource):
    def post(self, name):
        if name not in app.config['BEMS_ACCEPT']:
            return {
                'message': 'Type Not Included!'
            }, 403
        type_schema = bems_schema.appliances(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 400
        
        return {
            'message': 'OK!',
        }, 200
