# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    jours_alerte_recyclage = fields.Integer(
        string='Jours d\'alerte avant recyclage',
        default=30,
        config_parameter='ange_sec_employee.jours_alerte_recyclage',
        help='Nombre de jours avant la date de recyclage pour déclencher une alerte'
    )

    @api.constrains('jours_alerte_recyclage')
    def _check_jours_alerte_recyclage(self):
        """Vérifier que le nombre de jours est positif"""
        for record in self:
            if record.jours_alerte_recyclage < 0:
                raise models.ValidationError(
                    'Le nombre de jours d\'alerte doit être positif.'
                )
