from common.ma import ma
from marshmallow import validate


class bems():
    class bems_homepage_information(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        grid = ma.Float(required=True)
        pv = ma.Float(required=True)
        building = ma.Float(required=True)
        ess = ma.Float(required=True)
        ev = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)

    class bems_ess_display(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        cluster = ma.Int(required=True)
        power_display = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)

    class bems_ev_display(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        cluster = ma.Int(required=True)
        power = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)

    class bems_pv_display(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        cluster = ma.Int(required=True)
        PAC = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)

    class bems_wt_display(ma.Schema):
        id = ma.Int(required=True)
        field = ma.Str(required=True)
        cluster = ma.Int(required=True)
        WindGridPower = ma.Float(required=True)
        updated_at = ma.DateTime(required=True)
