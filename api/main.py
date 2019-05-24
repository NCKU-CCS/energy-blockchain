from flask import Flask
from flask_restful import Api
from resources import ems

app = Flask(__name__)
api = Api(app)
# Hems
api.add_resource(ems.Hems_aggregator_distribution,
                 "/hems/aggregator_distribution")

# Bems
api.add_resource(ems.Bems_appliances,
                 "/bems/appliances")


if __name__ == "__main__":
    app.run(debug='no')
