from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BusDeployment(models.Model):
    _name = "bus.deployment"
    _description = "Bus Deployment"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute="_compute_name", store=True)
    date = fields.Date(string="Date", default=fields.Date.today, readonly=True)
    edited_on = fields.Date(string="Edited On", readonly=True)
    depot_id = fields.Many2one(related='bus_id.depot_id', store=True, tracking=True)
    bus_id = fields.Many2one('bus.information', string="Bus", required=True,
                             domain="[('status', 'in', ['active', 'maintenance'])]", tracking=True)
    route_id = fields.Many2one('bus.route', string="Route", required=True, tracking=True)
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
    additional_info_ids = fields.One2many("bus.deployment.note", "deployment_id",
                                          string="Additional Information")

    @api.depends('bus_id')
    def _compute_name(self):
        for rec in self:
            if rec.bus_id:
                rec.name = rec.bus_id.side_plate
            else:
                rec.name = ""

    @api.depends('morning_trip_count', 'afternoon_trip_count')
    def _compute_total_trip_count(self):
        for rec in self:
            rec.total_trip_count = (rec.morning_trip_count + rec.afternoon_trip_count)

    @api.constrains('bus_id', 'date')
    def _check_duplicate_deployment(self):
        for rec in self:
            duplicate = self.search([
                ('id', '!=', rec.id),
                ('bus_id', '=', rec.bus_id.id),
                ('date', '=', rec.date),
            ], limit=1)
            if duplicate:
                raise ValidationError("This bus is already deployed on the selected date.")

    @api.constrains('morning_start_time', 'morning_end_time')
    def _check_morning_time(self):
        for rec in self:
            if (rec.morning_start_time and
                    rec.morning_end_time and
                    rec.morning_end_time <= rec.morning_start_time):
                raise ValidationError("Morning end time must be after start time.")

    @api.constrains('morning_driver_id', 'afternoon_driver_id')
    def _check_drivers(self):
        for rec in self:
            if (rec.morning_driver_id and rec.afternoon_driver_id and
                    rec.morning_driver_id == rec.afternoon_driver_id):
                raise ValidationError("Morning and afternoon drivers must be different.")

    @api.constrains('morning_conductor_id', 'afternoon_conductor_id')
    def _check_conductors(self):
        for rec in self:
            if (rec.morning_conductor_id and rec.afternoon_conductor_id and
                    rec.morning_conductor_id == rec.afternoon_conductor_id):
                raise ValidationError("Morning and afternoon conductors must be different.")

    def write(self, vals):
        protected_fields = [
            'bus_id',
            'route_id',
            'date',
            'morning_driver_id',
            'morning_conductor_id',
            'afternoon_driver_id',
            'afternoon_conductor_id',
        ]

        for rec in self:
            if rec.state == 'approved':
                raise ValidationError("APPROVED RECORD DETECTED")

        return super().write(vals)

    def action_draft(self):
        self.state = 'draft'

    def action_submitted(self):
        self.state = 'submitted'
        admin_group = self.env.ref('fleet_control.group_bus_admin')
        partners = admin_group.users.mapped('partner_id')
        self.message_post(body="Deployment has been submitted for approval.",
                          partner_ids=partners.ids)

    def action_approved(self):
        self.state = 'approved'
        self.message_post(body="Deployment has been approved.",
                          partner_ids=[self.dispatcher_id.partner_id.id])

    def action_rejected(self):
        self.state = 'rejected'
        self.message_post(body="Deployment has been rejected.")

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
