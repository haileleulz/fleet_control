from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date


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


class FleetDashboard(models.TransientModel):
    _name = 'fleet.dashboard'
    _description = 'Fleet Dashboard'

    today_date = fields.Date(compute='_compute_today_date')
    total_buses = fields.Integer(readonly=True)
    total_routes = fields.Integer(readonly=True)
    total_depots = fields.Integer(readonly=True)
    total_deployments = fields.Integer(readonly=True)
    total_deployments_today = fields.Integer(readonly=True)

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        today = date.today()

        res['total_buses'] = self.env['bus.information'].search_count([])
        res['total_routes'] = self.env['bus.route'].search_count([])
        res['total_depots'] = self.env['bus.depot'].search_count([])
        res['total_deployments'] = self.env['bus.deployment'].search_count([])
        res['total_deployments_today'] = self.env['bus.deployment'].search_count([
            ('date', '=', today)
        ])
        return res

    def _compute_today_date(self):
        for rec in self:
            rec.today_date = fields.Date.today()

    def action_print_dashboard(self):
        return self.env.ref(
            'fleet_control.action_fleet_dashboard_report'
        ).report_action(self)


class ResUsers(models.Model):
    _inherit = 'res.users'

    depot_id = fields.Many2one(
        'bus.depot',
        string='Assigned Depot'
    )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    role = fields.Selection([
        ('driver', 'Driver'),
        ('conductor', 'Conductor'),
    ], string='Role')
