from common.ma import ma
from marshmallow import validate

# CEMS


class cems():
    class aggregator_distribution(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        address = ma.Str(required=True)
        bidding_price = ma.Float(required=True)
        amount = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)

    class aggregator_dr_event(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        eventID = ma.Str(required=True)
        eventdate = ma.DateTime(required=True)
        bidding_price = ma.Float(required=True)
        bidding_capacity = ma.Float(required=True)
        get_bidding = ma.Int(required=True)
        amount = ma.Float(required=True)
        start_at = ma.DateTime(required=True)
        end_at = ma.DateTime(required=True)
        baseline = ma.Float(required=True)
        max_consumption = ma.Float(required=True)
        actual_load_shedding = ma.Float(required=True)
        expected_reward = ma.Float(required=True)
        actual_reward = ma.Float(required=True)
        feedback_ratio = ma.Float(required=True)
        result = ma.Float(required=True)
        inserted_at = ma.DateTime(required=True)
