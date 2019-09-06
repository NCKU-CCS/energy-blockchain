from flask_restful import Resource
from flask import request, current_app
from models.schema.bems import bems
from helpers import check_ip


class Bems (Resource):
    @check_ip()
    def post(self):
        name = ''
        if name not in current_app.config.get('BEMS_ACCEPT'):
            return {
                'message': 'Type Not Included!'
            }, 403

        # choose Schema
        target_schema = getattr(bems, name)
        type_schema = target_schema(many=False)

        result = type_schema.load(request.get_json(force='true'))

        if len(result.errors) > 0:
            errors = result.errors.copy()
            for error in list(errors):
                if errors[error] == ["Missing data for required field."]:
                    del errors[error]
            if len(errors) > 0:
                return errors, 400
            else:
                return {
                    'message': 'Input Data Error.'
                }, 400

        return {
            'message': 'OK!',
        }, 200
