# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HrFormation(models.Model):
    """Modèle pour gérer les formations (catalogue de formations)"""
    _name = 'hr.formation'
    _description = 'Formation (Catalogue)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Nom de la formation',
        required=True,
        help='Nom de la formation'
    )
    
    # Relation One2many avec les employés via le modèle intermédiaire
    employee_formation_ids = fields.One2many(
        'ange.employee.formation',
        'formation_id',
        string='Employés assignés',
        help='Employés assignés à cette formation avec leurs statuts'
    )
    
    employee_ids = fields.Many2many(
        'hr.employee',
        'hr_formation_employee_rel',
        'formation_id',
        'employee_id',
        string='Employés',
        help='Employés assignés à cette formation'
    )
    
    description = fields.Text(
        string='Description',
        help='Description détaillée de la formation'
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True,
        help='Indique si cette formation est active'
    )
    
    # Durée par défaut avant recyclage pour cette formation
    duree_avant_recyclage = fields.Integer(
        string='Durée avant recyclage (mois)',
        default=12,
        help='Nombre de mois avant le recyclage obligatoire par défaut'
    )
    
    # Champs calculés pour statistiques
    nb_employes_total = fields.Integer(
        string='Nombre d\'employés total',
        compute='_compute_statistiques',
        help='Nombre total d\'employés assignés à cette formation'
    )
    
    nb_employes_termines = fields.Integer(
        string='Nombre d\'employés ayant terminé',
        compute='_compute_statistiques',
        help='Nombre d\'employés ayant terminé cette formation'
    )
    
    nb_employes_en_cours = fields.Integer(
        string='Nombre d\'employés en cours',
        compute='_compute_statistiques',
        help='Nombre d\'employés en cours de formation'
    )
    
    nb_employes_recyclage = fields.Integer(
        string='Nombre d\'employés en recyclage',
        compute='_compute_statistiques',
        help='Nombre d\'employés nécessitant un recyclage'
    )
    
    pourcentage_completion = fields.Float(
        string='Pourcentage de complétion',
        compute='_compute_statistiques',
        help='Pourcentage d\'employés ayant terminé la formation'
    )
    
    @api.depends('employee_formation_ids.statut')
    def _compute_statistiques(self):
        """Calculer les statistiques de la formation"""
        for formation in self:
            employee_formations = formation.employee_formation_ids
            formation.nb_employes_total = len(employee_formations)
            formation.nb_employes_termines = len(employee_formations.filtered(lambda ef: ef.statut == 'terminee'))
            formation.nb_employes_en_cours = len(employee_formations.filtered(lambda ef: ef.statut == 'en_cours'))
            formation.nb_employes_recyclage = len(employee_formations.filtered(lambda ef: ef.statut == 'recyclage_requis'))
            
            if formation.nb_employes_total > 0:
                formation.pourcentage_completion = (formation.nb_employes_termines / formation.nb_employes_total) * 100
            else:
                formation.pourcentage_completion = 0.0

    def action_assign_employees(self):
        """Action pour assigner des employés à cette formation"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Assigner un employé à {self.name}',
            'res_model': 'ange.employee.formation',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_formation_id': self.id,
                'default_statut': 'non_fait'
            }
        }
    
    def action_view_employee_formations(self):
        """Action pour voir les statuts des employés pour cette formation"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Statuts - {self.name}',
            'res_model': 'ange.employee.formation',
            'view_mode': 'list,form',
            'domain': [('formation_id', '=', self.id)],
            'context': {'default_formation_id': self.id}
        }

    def name_get(self):
        """Personnaliser l'affichage du nom"""
        result = []
        for record in self:
            name = record.name
            if record.nb_employes_total > 0:
                name = f"{record.name} ({record.nb_employes_total} employés)"
            result.append((record.id, name))
        return result
