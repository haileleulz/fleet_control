from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class BusInformation(models.Model):
    _name = "bus.information"
    _description = "Bus"
    _rec_name = "side_plate"

    bus_type = fields.Selection([('onai', 'Onai'), ('express', 'Express'), ('yutong', 'Yutong'),
                                 ('higer', 'Higer'), ('daf', 'Daf')], string="Bus Type", required=True)
    side_plate = fields.Char(string="Side Plate", required=True)
    license_plate = fields.Char(string="License Plate", required=True)
    depot_id = fields.Many2one('bus.depot', string="Depot", required=True)
    status = fields.Selection([('active', 'Active'), ('maintenance', 'Maintenance'),
                               ('inactive', 'Inactive')], string="Status", default='active', required=True)

    @api.constrains('side_plate', 'depot_id')
    def _check_side_plate(self):
        for rec in self:
            if not rec.side_plate:
                continue

            # To make the side plate a number only field
            if not rec.side_plate.isdigit():
                raise ValidationError(
                    "Side plate must contain exactly 4 digits."
                )

            # only four digits allowed not more not less
            if len(rec.side_plate) != 4:
                raise ValidationError(
                    "Side plate must contain exactly 4 digits."
                )

            # always must start with depot code
            depot_code = str(rec.depot_id.code)

            if not rec.side_plate.startswith(depot_code):
                raise ValidationError(
                    # f"Side plate must start with {rec.depot.name} code {depot_code}."
                    f"for {rec.depot_id.name} enter code{depot_code}"
                )

    _sql_constraints = [('unique_side_plate', 'unique(side_plate)', 'Side plate must be unique!'),
                        ('unique_license_plate', 'unique(license_plate)', 'License plate must be unique!'), ]
