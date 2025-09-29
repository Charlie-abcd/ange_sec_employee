# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VisiteMedicale(models.Model):
    """Modèle pour gérer les visites médicales des employés"""
    _name = 'visite.medicale'
    _description = 'Visite Médicale'
    _order = 'date desc'

    date = fields.Date(
        string='Date',
        required=True,
        help='Date de la visite médicale'
    )
    
    description = fields.Text(
        string='Description',
        help='Description détaillée de la visite médicale'
    )
    
    fait = fields.Boolean(
        string='Fait ?',
        default=False,
        help='Indique si la visite médicale a été effectuée'
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        required=True,
        help='Employé concerné par cette visite médicale'
    )

    def name_get(self):
        """Personnaliser l'affichage du nom"""
        result = []
        for record in self:
            name = f"{record.date}"
            if record.description:
                name += f" - {record.description[:50]}"
                if len(record.description) > 50:
                    name += "..."
            result.append((record.id, name))
        return result
