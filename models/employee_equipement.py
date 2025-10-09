# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EmployeeEquipement(models.Model):
    """Modèle intermédiaire pour gérer l'assignation des équipements aux employés"""
    _name = 'ange.employee.equipement'
    _description = 'Équipement Employé'
    _order = 'date_remise desc'
    _rec_name = 'display_name'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        required=True,
        ondelete='cascade',
        help='Employé concerné'
    )
    
    equipement_id = fields.Many2one(
        'ange.equipement',
        string='Équipement',
        required=True,
        ondelete='cascade',
        help='Équipement assigné'
    )
    
    date_remise = fields.Date(
        string='Date de remise',
        required=True,
        default=fields.Date.today,
        help='Date à laquelle l\'équipement a été remis à l\'employé'
    )
    
    date_renouvellement = fields.Date(
        string='Date de renouvellement',
        compute='_compute_date_renouvellement',
        store=True,
        help='Date calculée pour le renouvellement de l\'équipement'
    )
    
    statut = fields.Selection([
        ('actif', 'Actif'),
        ('expire', 'Expiré'),
        ('renouvele', 'Renouvelé'),
        ('retire', 'Retiré')
    ], string='Statut', default='actif', required=True)
    
    notes = fields.Text(
        string='Notes',
        help='Notes concernant cet équipement pour cet employé'
    )
    
    # Champs calculés pour l'affichage
    display_name = fields.Char(
        string='Nom d\'affichage',
        compute='_compute_display_name',
        store=True
    )
    
    jours_avant_expiration = fields.Integer(
        string='Jours avant expiration',
        compute='_compute_jours_avant_expiration'
    )
    
    @api.depends('equipement_id', 'date_remise', 'equipement_id.periode_renouvellement')
    def _compute_date_renouvellement(self):
        """Calculer la date de renouvellement basée sur la période de renouvellement"""
        for record in self:
            if record.date_remise and record.equipement_id.periode_renouvellement:
                record.date_renouvellement = record.date_remise + relativedelta(
                    months=record.equipement_id.periode_renouvellement
                )
            else:
                record.date_renouvellement = False
    
    @api.depends('employee_id.name', 'equipement_id.name', 'date_remise')
    def _compute_display_name(self):
        """Calculer le nom d'affichage"""
        for record in self:
            if record.employee_id and record.equipement_id:
                record.display_name = f"{record.equipement_id.name} - {record.employee_id.name}"
            else:
                record.display_name = "Nouvel équipement employé"
    
    @api.depends('date_renouvellement')
    def _compute_jours_avant_expiration(self):
        """Calculer le nombre de jours avant expiration"""
        today = fields.Date.today()
        for record in self:
            if record.date_renouvellement:
                delta = record.date_renouvellement - today
                record.jours_avant_expiration = delta.days
            else:
                record.jours_avant_expiration = 0
    
    @api.model_create_multi
    def create(self, vals_list):
        """Surcharger create pour calculer automatiquement la date de renouvellement"""
        records = super().create(vals_list)
        for record in records:
            record._compute_date_renouvellement()
        return records
    
    def write(self, vals):
        """Surcharger write pour recalculer la date de renouvellement si nécessaire"""
        result = super().write(vals)
        if 'date_remise' in vals or 'equipement_id' in vals:
            self._compute_date_renouvellement()
        return result
    
    @api.model
    def _cron_check_expiring_equipements(self):
        """Cron job pour vérifier les équipements qui arrivent à expiration"""
        # Chercher les équipements qui expirent dans les 30 prochains jours
        date_limite = fields.Date.today() + relativedelta(days=30)
        expiring_equipements = self.search([
            ('date_renouvellement', '<=', date_limite),
            ('date_renouvellement', '>=', fields.Date.today()),
            ('statut', '=', 'actif')
        ])
        
        # Ici on pourrait ajouter une notification ou un email
        # Pour l'instant, on met juste à jour le statut
        for equipement in expiring_equipements:
            if equipement.date_renouvellement <= fields.Date.today():
                equipement.statut = 'expire'
    
    def action_renouveler(self):
        """Action pour renouveler un équipement"""
        self.ensure_one()
        # Marquer l'ancien comme renouvelé
        self.statut = 'renouvele'
        
        # Créer un nouvel enregistrement avec une nouvelle date de remise
        new_vals = {
            'employee_id': self.employee_id.id,
            'equipement_id': self.equipement_id.id,
            'date_remise': fields.Date.today(),
            'notes': f"Renouvellement de l'équipement du {self.date_remise}"
        }
        
        new_record = self.create(new_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Équipement Renouvelé',
            'res_model': 'ange.employee.equipement',
            'res_id': new_record.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def name_get(self):
        """Personnaliser l'affichage du nom"""
        result = []
        for record in self:
            name = record.display_name or "Nouvel équipement"
            if record.date_remise:
                name += f" ({record.date_remise})"
            result.append((record.id, name))
        return result
