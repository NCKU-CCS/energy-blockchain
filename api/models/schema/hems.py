from common.ma import ma
from marshmallow import validate

# HEMS
class hems():
    class aggregator_distribution(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        address = ma.Str(required=True)
        bidding_price = ma.Float(required=True)
        amount = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)
