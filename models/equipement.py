# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Equipement(models.Model):
    """Modèle pour gérer les équipements"""
    _name = 'ange.equipement'
    _description = 'Équipement'
    _order = 'name'

    name = fields.Char(
        string='Nom de l\'équipement',
        required=True,
        help='Nom de l\'équipement'
    )
    
    description = fields.Text(
        string='Description',
        help='Description détaillée de l\'équipement'
    )
    
    periode_renouvellement = fields.Integer(
        string='Période de renouvellement (mois)',
        default=12,
        required=True,
        help='Période en mois après laquelle l\'équipement doit être renouvelé'
    )
    
    deductible = fields.Boolean(
        string='Déductible ?',
        default=False,
        help='Indique si cet équipement est déductible du salaire'
    )
    
    montant_deductible = fields.Float(
        string='Montant déductible',
        help='Montant à déduire du salaire si l\'équipement est déductible'
    )
    
    # Relation avec les employés via le modèle intermédiaire
    employee_equipement_ids = fields.One2many(
        'ange.employee.equipement',
        'equipement_id',
        string='Assignations aux employés'
    )
    
    # Champ calculé pour le nombre d'employés ayant cet équipement
    nb_employees = fields.Integer(
        string='Nombre d\'employés',
        compute='_compute_nb_employees',
        store=True
    )
    
    @api.depends('employee_equipement_ids')
    def _compute_nb_employees(self):
        """Calculer le nombre d'employés ayant cet équipement"""
        for equipement in self:
            equipement.nb_employees = len(equipement.employee_equipement_ids)
    
    @api.onchange('deductible')
    def _onchange_deductible(self):
        """Réinitialiser le montant déductible si pas déductible"""
        if not self.deductible:
            self.montant_deductible = 0.0

    def name_get(self):
        """Personnaliser l'affichage du nom"""
        result = []
        for record in self:
            name = record.name
            if record.deductible and record.montant_deductible:
                name += f" (Déductible: {record.montant_deductible}€)"
            result.append((record.id, name))
        return result
