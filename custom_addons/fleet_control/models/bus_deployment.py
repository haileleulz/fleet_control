from odoo import fields, models, api


class BusDeployment(models.Model):
    _name = "bus.deployment"
    _description = "Bus Deployment"
    _rec_name = "name"

    name = fields.Char(compute="_compute_name", store=True)
    date = fields.Date(string="Date", default=fields.Date.today, readonly=True)
    edited_on = fields.Date(string="Edited On", readonly=True)
    depot_id = fields.Many2one(related='bus_id.depot_id', store=True)
    bus_id = fields.Many2one('bus.information', string="Bus", required=True,
                             domain="[('status', 'in', ['active', 'maintenance'])]")
    route_id = fields.Many2one('bus.route', string="Route", required=True)
    dispatcher_id = fields.Many2one('res.users', string="Dispatcher",
                                    default=lambda self: self.env.user, readonly=True)
    morning_driver_id = fields.Many2one('res.partner', string="Morning Driver")
    morning_conductor_id = fields.Many2one('res.partner', string="Morning Conductor")
    afternoon_driver_id = fields.Many2one('res.partner', string="Afternoon Driver")
    afternoon_conductor_id = fields.Many2one('res.partner', string="Afternoon Conductor")
    morning_start_time = fields.Float(string="Morning Start Time", default=11.00)
    morning_end_time = fields.Float(string="Morning End Time", default=7.00)
    afternoon_start_time = fields.Float(string="Afternoon Start Time", default=7.00)
    afternoon_end_time = fields.Float(string="Afternoon End Time", default=3.00)
    morning_trip_count = fields.Integer(string="Morning Trips")
    afternoon_trip_count = fields.Integer(string="Afternoon Trips")
    total_trip_count = fields.Integer(compute="_compute_total_trip_count", store=True, string="Total Trips")
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'),
                              ('rejected', 'Rejected')], default='draft', string="Status")

    @api.depends('bus_id')
    def _compute_name(self):
        for rec in self:
            if rec.bus_id:
                rec.name = rec.bus_id.side_plate
            else:
                rec.name = ""

    @api.depends(
        'morning_trip_count',
        'afternoon_trip_count'
    )
    def _compute_total_trip_count(self):
        for rec in self:
            rec.total_trip_count = (
                    rec.morning_trip_count +
                    rec.afternoon_trip_count
            )

    additional_info_ids = fields.One2many(
        "bus.deployment.note",
        "deployment_id",
        string="Additional Information"
    )

    def action_draft(self):
        self.state = 'draft'

    def action_submitted(self):
        self.state = 'submitted'

    def action_approved(self):
        self.state = 'approved'

    def action_rejected(self):
        self.state = 'rejected'

    def action_resubmit(self):
        for record in self:
            record.edited_on = fields.Date.today()
            record.state = 'submitted'


class BusDeploymentNote(models.Model):
    _name = "bus.deployment.note"
    _description = "Deployment Additional Information"

    deployment_id = fields.Many2one(
        "bus.deployment",
        required=True,
        ondelete="cascade"
    )

    note = fields.Char(string="Details", required=True, help="Additional details on "
                                                             "rerouting or downtime please")
