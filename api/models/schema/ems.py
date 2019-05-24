from common.ma import ma
from marshmallow import validate


# HEMS
class aggregator_distribution(ma.Schema):
    id = ma.Int(required=True)
    field = ma.Str(required=True)
    address = ma.Str(required=True)
    bidding_price = ma.Float(required=True)
    amount = ma.Float(required=True)
    updated_at = ma.DateTime(required=True)


# BEMS
class appliances(ma.Schema):
    id = ma.Int(required=True)
    field = ma.Str(required=True)
    name = ma.Str(required=True)
    brand = ma.Str(required=True)
    switch = ma.Int(required=True)
    setting = ma.Int(required=True)
    power = ma.Float(required=True)
    controller_address = ma.Int(required=True)
    temperature = ma.Float(required=True)
    humidity = ma.Float(required=True)
    co2 = ma.Float(required=True)
    illuminance = ma.Float(required=True)
    dr_switch = ma.Int(required=True)
    dr_priority = ma.Int(required=True)
    dr_recover = ma.Int(required=True)
    sheeding_willing = ma.Int(required=True)
    update_time = ma.DateTime(required=True)
