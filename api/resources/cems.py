from flask_restful import Resource
from flask import request
from models.schema.cems import cems
from config import app
import json
import hashlib
import base64
from tangle import send_to_iota


class Cems (Resource):
    def post(self, name):
        if name not in app.config['CEMS_ACCEPT']:
            return {
                'message': 'Type Not Included!'
            }, 403

        # choose Schema
        target_schema = getattr(cems, name)
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
        elif name == 'aggregator_dr_event':
            data = request.get_json(force='true')
            try:
                if data['eventID'] == "--":
                    return {
                        'message': 'eventID error'
                    }, 400
                data['inserted_at'] = data['inserted_at'].strftime(
                    '%Y-%m-%dT%H:%M:%S')
                data['eventdate'] = data['eventdate'].strftime(
                    '%Y-%m-%dT%H:%M:%S')
                data['start_at'] = data['start_at'].strftime(
                    '%Y-%m-%d %H:%M:%S')
                data['end_at'] = data['end_at'].strftime(
                    '%Y-%m-%d %H:%M:%S')
            except:
                pass
            json_data = json.dumps(data).encode('utf-8')
            hash_data = hashlib.sha256(
                json_data).hexdigest().encode()
            base64_data = base64.b64encode(hash_data)
            send_datas = json.dumps(
                {
                    "eventID": data['eventID'],
                    "date": data['inserted_at'],
                    "value": base64_data.decode()
                }
            )
            Tx = send_to_iota(send_datas)
            return {
                'Tx': str(Tx)
            }, 200

        return {
            'message': 'OK!'
        }, 200
