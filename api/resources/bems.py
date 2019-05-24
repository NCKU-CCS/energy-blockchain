from flask_restful import Resource
from flask import request
from models.schema.bems import bems
from config import app

class Bems (Resource):
    def post(self, name):
        if name not in app.config['BEMS_ACCEPT']:
            return {
                'message': 'Type Not Included!'
            }, 403
        # choose Schema
        target_schema = getattr(bems, name)
        type_schema = target_schema(many=False)
        # type_schema = hems_schema.aggregator_distribution(many=False)

        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            return result.errors, 400
        
        return {
            'message': 'OK!',
        }, 200
