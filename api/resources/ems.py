from flask_restful import Resource
from flask import request
import models.schema.ems as schema
# from models.ems import UserModel

HEMS_ACCEPT = ['aggregator_distribution']
BEMS_ACCEPT = ['appliances']

class Hems (Resource):
    def post(self, name):
        if name not in HEMS_ACCEPT:
            return {
                'message': 'Type Not Included!'
            }, 403
        type_schema = schema.aggregator_distribution(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 400

        return {
            'message': 'OK!'
        }, 200

# 拆掉
class Bems (Resource):
    def post(self, name):
        if name not in BEMS_ACCEPT:
            return {
                'message': 'Type Not Included!'
            }, 403
        type_schema = schema.appliances(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 400
        print(result.data)
        return {
            'message': 'OK!',
        }, 200
