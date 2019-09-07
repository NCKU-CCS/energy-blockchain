from flask_restful import Resource
from flask import request
from models.schema.bems import bems
from helpers import check_ip
import threading
from config import app


class Bems (Resource):
    @check_ip()
    def post(self):
        try:
            data = request.get_json(force='true')
        except:
            return 'error', 400
        self.errors = []
        threads = []
        for idx, field in enumerate(data):
            self.errors.append([])
            threads.append(threading.Thread(target=self.process_data, args=(idx, data[field])))
            threads[idx].start()
        for i in range(len(threads)):
            threads[i].join()

        print('Error message:', self.errors)

        for error in self.errors:
            if len(error) > 0:
                # print(errors)
                return {
                    'message': 'Data Error.'
                }, 400

        return {
            'message': 'ACCEPT',
        }, 200

    def process_data(self, id, data):
        upload = []

        for name in data:
            # check table
            if name not in app.config[('BEMS_ACCEPT')]:
                self.errors[id] = 'Type Not Included!'
                continue

            # choose Schema
            target_schema = getattr(bems, name)
            type_schema = target_schema(many=False)

            # check data type
            result = type_schema.load(data[name])
            if len(result.errors) > 0:
                # Data Type Error
                self.errors[id] = result.errors.copy()
                # print(errors)
            else:
                # encrypt
                
                upload_data = {
                    "data": self.encrypt(data[name]),
                    "date": data[name]['updated_at']
                }

                upload.append((name, upload_data))
        # send data to iota (pt)
        print("*"*100)        
        print(upload)

    def encrypt(self, data):
        # encrypt

        return data
