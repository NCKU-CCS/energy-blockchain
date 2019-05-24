from flask_restful import Resource
from flask import request
import models.schema.ems as schema
# from models.ems import UserModel


class Hems_aggregator_distribution (Resource):
    def post(self):
        type_schema = schema.aggregator_distribution_schema(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 433

        return {
            'message': 'OK!'
        }, 200


class Bems_appliances (Resource):
    def post(self):
        type_schema = schema.appliances(many=False)
        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 433
        print(result.data)
        return {
            'message': 'OK!',
        }, 200
