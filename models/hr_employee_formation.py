# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HrEmployeeFormation(models.Model):
    """Modèle intermédiaire pour gérer les statuts de formation par employé"""
    _name = 'ange.employee.formation'
    _description = 'Formation Employé Ange Security - Statut Individuel'
    _order = 'employee_id, formation_id'
    _rec_name = 'display_name'
    

    # Relations
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        required=True,
        ondelete='cascade',
        help='Employé concerné par cette formation'
    )
    
    formation_id = fields.Many2one(
        'hr.formation',
        string='Formation',
        required=True,
        ondelete='cascade',
        help='Formation assignée à cet employé'
    )
    
    # Statut individuel de la formation pour cet employé
    statut = fields.Selection([
        ('non_fait', 'Non effectuée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('recyclage_requis', 'Recyclage requis')
    ], string='Statut', default='non_fait', store=True,
       compute='_compute_statut', readonly=False,
       help='Statut de la formation pour cet employé')
    
    # Dates spécifiques à cet employé
    date_debut = fields.Date(
        string='Date de début',
        help='Date de début de la formation pour cet employé'
    )
    
    date_fin = fields.Date(
        string='Date de fin',
        help='Date de fin de la formation pour cet employé'
    )
    
    date_recyclage = fields.Date(
        string='Date de recyclage',
        compute='_compute_date_recyclage',
        store=True,
        help='Date calculée pour le recyclage de cette formation'
    )
    
    # Champs calculés
    duree_formation = fields.Integer(
        string='Durée (jours)',
        compute='_compute_duree_formation',
        store=True,
        help='Durée de la formation en jours'
    )
    
    jours_avant_recyclage = fields.Integer(
        string='Jours avant recyclage',
        compute='_compute_jours_avant_recyclage',
        help='Nombre de jours avant la date de recyclage'
    )
    
    alerte_recyclage = fields.Boolean(
        string='Alerte recyclage',
        compute='_compute_alerte_recyclage',
        search='_search_alerte_recyclage',
        help='Indique si une alerte de recyclage doit être affichée'
    )

    
    duree_avant_recyclage = fields.Integer(
        related='formation_id.duree_avant_recyclage',
        string='Durée avant recyclage (mois)',
        store=True
    )
    
    # Champ name pour l'affichage (related au nom de la formation)
    name = fields.Char(
        related='formation_id.name',
        string='Nom de la formation',
        store=True,
        readonly=True
    )
    
    # Nom d'affichage
    display_name = fields.Char(
        string='Nom d\'affichage',
        compute='_compute_display_name',
        store=True
    )

    @api.depends('employee_id', 'formation_id')
    def _compute_display_name(self):
        """Calculer le nom d'affichage"""
        for record in self:
            if record.employee_id and record.formation_id:
                record.display_name = f"{record.formation_id.name} - {record.employee_id.name}"
            else:
                record.display_name = "Formation Employé"

    @api.depends('date_debut', 'date_fin')
    def _compute_statut(self):
        """Calculer le statut automatiquement basé sur les dates et la date actuelle"""
        today = fields.Date.today()
        for record in self:
            if not record.date_debut:
                record.statut = 'non_fait'
            elif record.date_debut and not record.date_fin:
                # Si on a une date de début mais pas de fin
                if today >= record.date_debut:
                    record.statut = 'en_cours'
                else:
                    record.statut = 'non_fait'
            elif record.date_debut and record.date_fin:
                # Si on a les deux dates
                if today < record.date_debut:
                    record.statut = 'non_fait'
                elif record.date_debut <= today <= record.date_fin:
                    record.statut = 'en_cours'
                elif today > record.date_fin:
                    record.statut = 'terminee'
            else:
                record.statut = 'non_fait'

    @api.depends('date_debut', 'date_fin')
    def _compute_duree_formation(self):
        """Calculer la durée de la formation"""
        for formation in self:
            if formation.date_debut and formation.date_fin:
                delta = formation.date_fin - formation.date_debut
                formation.duree_formation = delta.days + 1
            else:
                formation.duree_formation = 0

    @api.depends('date_fin', 'duree_avant_recyclage', 'statut')
    def _compute_date_recyclage(self):
        """Calculer automatiquement la date de recyclage"""
        for formation in self:
            if formation.statut == 'terminee' and formation.date_fin and formation.duree_avant_recyclage > 0:
                # Ajouter le nombre de mois à la date de fin
                formation.date_recyclage = formation.date_fin + relativedelta(months=formation.duree_avant_recyclage)
            else:
                formation.date_recyclage = False

    @api.depends('date_recyclage')
    def _compute_jours_avant_recyclage(self):
        """Calculer le nombre de jours avant recyclage"""
        for formation in self:
            if formation.date_recyclage:
                today = fields.Date.today()
                delta = formation.date_recyclage - today
                formation.jours_avant_recyclage = delta.days
            else:
                formation.jours_avant_recyclage = 0

    @api.depends('date_recyclage', 'statut')
    def _compute_alerte_recyclage(self):
        """Calculer si une alerte de recyclage doit être affichée"""
        for formation in self:
            if formation.statut == 'terminee' and formation.date_recyclage:
                # Récupérer le nombre de jours d'alerte depuis les paramètres
                jours_alerte = self.env['ir.config_parameter'].sudo().get_param(
                    'ange_sec_employee.jours_alerte_recyclage', '30'
                )
                try:
                    jours_alerte = int(jours_alerte)
                except ValueError:
                    jours_alerte = 30
                
                today = fields.Date.today()
                date_limite = formation.date_recyclage - timedelta(days=jours_alerte)
                formation.alerte_recyclage = today >= date_limite
            else:
                formation.alerte_recyclage = False

    def _search_alerte_recyclage(self, operator, value):
        """Recherche pour le champ alerte_recyclage"""
        jours_alerte = self.env['ir.config_parameter'].sudo().get_param(
            'ange_sec_employee.jours_alerte_recyclage', '30'
        )
        try:
            jours_alerte = int(jours_alerte)
        except ValueError:
            jours_alerte = 30
        
        today = fields.Date.today()
        date_limite = today + timedelta(days=jours_alerte)
        
        if operator == '=' and value:
            return [
                ('statut', '=', 'terminee'),
                ('date_recyclage', '!=', False),
                ('date_recyclage', '<=', date_limite)
            ]
        elif operator == '=' and not value:
            return [
                '|',
                ('statut', '!=', 'terminee'),
                '|',
                ('date_recyclage', '=', False),
                ('date_recyclage', '>', date_limite)
            ]
        return []

    @api.depends('date_recyclage')
    def _compute_auto_recyclage_status(self):
        """Passer automatiquement au statut recyclage_requis si la date est atteinte"""
        for formation in self:
            if (formation.statut == 'terminee' and 
                formation.date_recyclage and 
                formation.date_recyclage <= fields.Date.today()):
                formation.statut = 'recyclage_requis'

    @api.onchange('statut')
    def _onchange_statut(self):
        """Gérer les changements de statut"""
        if self.statut == 'non_fait':
            self.date_debut = False
            self.date_fin = False
        elif self.statut == 'en_cours' and not self.date_debut:
            self.date_debut = fields.Date.today()
        elif self.statut == 'terminee' and not self.date_fin:
            self.date_fin = fields.Date.today()

    @api.constrains('date_debut', 'date_fin')
    def _check_dates_formation(self):
        """Vérifier la cohérence des dates de formation"""
        for formation in self:
            if formation.date_debut and formation.date_fin:
                if formation.date_debut > formation.date_fin:
                    raise models.ValidationError(
                        _('La date de début doit être antérieure à la date de fin.')
                    )

    @api.constrains('employee_id', 'formation_id')
    def _check_unique_employee_formation(self):
        """Vérifier qu'un employé n'a qu'un seul enregistrement par formation"""
        for record in self:
            if record.employee_id and record.formation_id:
                existing = self.search([
                    ('employee_id', '=', record.employee_id.id),
                    ('formation_id', '=', record.formation_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise models.ValidationError(
                        _('Cet employé a déjà un enregistrement pour cette formation.')
                    )

    @api.model
    def cron_update_recyclage_status(self):
        """Cron job pour mettre à jour automatiquement les statuts de recyclage"""
        formations_terminees = self.search([
            ('statut', '=', 'terminee'),
            ('date_recyclage', '!=', False),
            ('date_recyclage', '<=', fields.Date.today())
        ])
        
        for formation in formations_terminees:
            formation.statut = 'recyclage_requis'
        
        return len(formations_terminees)

    def action_marquer_en_cours(self):
        """Action pour marquer la formation comme en cours"""
        for record in self:
            if not record.date_debut:
                record.date_debut = fields.Date.today()
            record.statut = 'en_cours'
        return True

    def action_marquer_terminee(self):
        """Action pour marquer la formation comme terminée"""
        for record in self:
            if not record.date_fin:
                record.date_fin = fields.Date.today()
            record.statut = 'terminee'
        return True

    def action_marquer_non_fait(self):
        """Action pour marquer la formation comme non effectuée"""
        for record in self:
            record.statut = 'non_fait'
            record.date_debut = False
            record.date_fin = False
        return True

    def name_get(self):
        """Personnaliser l'affichage du nom"""
        result = []
        for record in self:
            result.append((record.id, record.display_name))
        return result
