from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class BusRoute(models.Model):
    _name = "bus.route"
    _description = "Bus Routes and Areas of Location"
    _rec_name = "route_number"

    route_name = fields.Char(compute="_compute_route_name", store=True, string="Route Name")
    route_number = fields.Integer(string="Route Number", required=True)
    starting_station_id = fields.Many2one('bus.station', string="Starting Station", required=True)
    ending_station_id = fields.Many2one('bus.station', string="Ending Station", required=True)
    station_ids = fields.Many2many('bus.station', string="Stations")
    category = fields.Selection([('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')],
                                string="Category")
    tariff = fields.Integer(string="Tariff", required=True)
    trip_time = fields.Integer(string="Trip Time (Minutes)")
    number_of_stations = fields.Integer(compute="_compute_stations", string="Number of Stations")
    total_km = fields.Float(string="Total KM")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('station_ids')
    def _compute_stations(self):
        for rec in self:
            rec.number_of_stations = len(rec.station_ids)

    @api.constrains('station_ids')
    def _check_main_stations(self):
        for route in self:
            if len(route.station_ids.filtered(
                    lambda s: s.station_type == 'main'
            )) > 2:
                raise ValidationError(
                    "Only two main stations are allowed per route.")

    @api.depends('starting_station_id', 'ending_station_id')
    def _compute_route_name(self):
        for rec in self:
            if rec.starting_station_id and rec.ending_station_id:
                rec.route_name = (
                    f"{rec.starting_station_id.name} - "
                    f"{rec.ending_station_id.name}"
                )
            else:
                rec.route_name = False

    @api.constrains('tariff')
    def _check_tariff(self):
        for rec in self:
            if rec.tariff <= 0:
                raise ValidationError(
                    _("Tariff must be greater than zero.")
                )
