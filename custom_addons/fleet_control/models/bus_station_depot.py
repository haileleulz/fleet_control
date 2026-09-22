from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class BusStation(models.Model):
    _name = "bus.station"
    _description = "registered stations for all routes and depots"

    name = fields.Char(string="Stations", required=True)
    station_type = fields.Selection([('main', 'Main'), ('sub', 'Sub')], string="Station Type", required=True)

    _sql_constraints = [('unique_station_name', 'unique(name)', 'Station name must be unique!')]


class BusDepot(models.Model):
    _name = "bus.depot"
    _description = "Bus Depot"

    name = fields.Char(string="Depot Name", required=True)
    code = fields.Integer(string="Code", required=True)
    _sql_constraints = [('unique_depot_name', 'unique(name)', 'Depot name must be unique!')]


class ResUsers(models.Model):
    _inherit = 'res.users'

    depot_id = fields.Many2one(
        'bus.depot',
        string='Assigned Depot'
    )
