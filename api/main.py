from flask import Flask
from flask_restful import Api
from resources import ems
from config import app

# app = Flask(__name__)
# app.config.from_pyfile('config.py')
api = Api(app)
# Hems
api.add_resource(ems.Hems,
                 "/hems/<string:name>")

# Bems
api.add_resource(ems.Bems,
                 "/bems/<string:name>")

if __name__ == "__main__":
    app.run(debug='no')
