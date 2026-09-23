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

    @http.route('/fleet/deployment/<int:deployment_id>', auth='public', website=True)
    def deployment_detail(self, deployment_id, **kw):
        deployment = request.env['bus.deployment'].sudo().browse(deployment_id)
        return request.render(
            'fleet_control.portal_deployment_detail',
            {
                'deployment': deployment,
            }
        )
