from odoo import http
from odoo.http import request


class deployment(http.Controller):
    @http.route('/fleet/deployment/', auth='public', website=True)
    def bus_dispatcher(self, **kw):
        deployments = request.env['bus.deployment'].sudo().search([])

        return request.render(
            'fleet_control.portal_deployments',
            {
                'deployments': deployments,
            }
        )
