from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {
            'message': 'Hello World!'
        }, 200


api.add_resource(HelloWorld, '/helloworld/')

if __name__ == '__main__':
    app.run(debug=True)
