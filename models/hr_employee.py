# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    """Extension du modèle hr.employee pour Ange Security"""
    _inherit = 'hr.employee'

    # ========================================
    # CHAMPS POUR L'ONGLET ÉQUIPEMENT ET SANTÉ
    # ========================================
    
    
    visite_medicale_ids = fields.One2many(
        'visite.medicale',
        'employee_id',
        string='Visites médicales',
        help='Visites médicales associées à cet employé'
    )
    
    # Nouvelle relation avec les formations via le modèle intermédiaire
    formation_ids = fields.One2many(
        'ange.employee.formation',
        'employee_id',
        string='Formations',
        help='Formations assignées à cet employé avec leurs statuts'
    )
    
    
    # Champs calculés pour statistiques
    nb_formations_total = fields.Integer(
        string='Nombre de formations total',
        compute='_compute_formation_stats',
        help='Nombre total de formations assignées'
    )
    
    nb_formations_terminees = fields.Integer(
        string='Formations terminées',
        compute='_compute_formation_stats',
        help='Nombre de formations terminées'
    )
    
    nb_formations_en_cours = fields.Integer(
        string='Formations en cours',
        compute='_compute_formation_stats',
        help='Nombre de formations en cours'
    )
    
    nb_formations_recyclage = fields.Integer(
        string='Formations à recycler',
        compute='_compute_formation_stats',
        help='Nombre de formations nécessitant un recyclage'
    )
    

    # ========================================
    # CHAMPS POUR L'ONGLET INFORMATIONS PRIVÉES
    # ========================================
    
    # Renommage des champs existants via les labels
    identification_id = fields.Char(
        string='Numéro CNI',
        help='Numéro de la Carte Nationale d\'Identité'
    )
    
    passport_id = fields.Char(
        string='Numéro carte de séjour',
        help='Numéro de la carte de séjour'
    )
    
    # Nouveaux champs de dates de validité
    date_validite_cni = fields.Date(
        string='Date de validité CNI',
        help='Date d\'expiration de la Carte Nationale d\'Identité'
    )
    
    date_validite_carte_sejour = fields.Date(
        string='Date de validité carte de séjour',
        help='Date d\'expiration de la carte de séjour'
    )
    
    # Matricule agent
    matricule_agent = fields.Char(
        string='Matricule agent',
        help='Matricule unique de l\'agent de sécurité'
    )
    
    # Faction de travail
    # Champ pour choisir le type de faction d'abord
    type_faction_choisi = fields.Selection([
        ('jour', 'Jour'),
        ('nuit', 'Nuit'),
        ('custom', 'Personnalisée')
    ], string='Type de faction', 
       help='Choisissez d\'abord le type de faction pour filtrer les options')
    
    faction_id = fields.Many2one(
        'hr.faction',
        string='Faction',
        help='Faction par défaut du collaborateur'
    )

    # ========================================
    # MÉTHODES ET CONTRAINTES
    # ========================================
    
    @api.onchange('type_faction_choisi')
    def _onchange_type_faction_choisi(self):
        """Réinitialiser la faction quand le type change"""
        if self.type_faction_choisi:
            # Réinitialiser la faction sélectionnée pour forcer un nouveau choix
            self.faction_id = False
    
    @api.depends('formation_ids.statut')
    def _compute_formation_stats(self):
        """Calculer les statistiques de formation de l'employé"""
        for employee in self:
            formations = employee.formation_ids
            employee.nb_formations_total = len(formations)
            employee.nb_formations_terminees = len(formations.filtered(lambda f: f.statut == 'terminee'))
            employee.nb_formations_en_cours = len(formations.filtered(lambda f: f.statut == 'en_cours'))
            employee.nb_formations_recyclage = len(formations.filtered(lambda f: f.statut == 'recyclage_requis'))
            
    
    @api.constrains('matricule_agent')
    def _check_matricule_agent_unique(self):
        """Vérifier l'unicité du matricule agent"""
        for record in self:
            if record.matricule_agent:
                existing = self.search([
                    ('matricule_agent', '=', record.matricule_agent),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise models.ValidationError(_(
                        'Le matricule agent "%s" est déjà utilisé par un autre employé.'
                    ) % record.matricule_agent)
    
    # Relation avec les équipements via le modèle intermédiaire
    equipement_ids = fields.One2many(
        'ange.employee.equipement',
        'employee_id',
        string='Équipements assignés'
    )
    
    # Champs calculés pour les équipements
    nb_equipements_actifs = fields.Integer(
        string='Équipements actifs',
        compute='_compute_equipements_stats',
        store=True
    )
    
    nb_equipements_expires = fields.Integer(
        string='Équipements expirés',
        compute='_compute_equipements_stats',
        store=True
    )
    
    @api.depends('equipement_ids.statut')
    def _compute_equipements_stats(self):
        """Calculer les statistiques des équipements"""
        for employee in self:
            equipements = employee.equipement_ids
            employee.nb_equipements_actifs = len(equipements.filtered(lambda e: e.statut == 'actif'))
            employee.nb_equipements_expires = len(equipements.filtered(lambda e: e.statut == 'expire'))

    def action_view_formations(self):
        """Action pour voir les formations de cet employé"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Formations - {self.name}',
            'res_model': 'ange.employee.formation',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id}
        }
    
    def action_view_equipements(self):
        """Action pour voir les équipements de cet employé"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Équipements - {self.name}',
            'res_model': 'ange.employee.equipement',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id}
        }

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type='form', **options):
        """Override pour s'assurer que les vues sont correctement mises à jour"""
        key = super()._get_view_cache_key(view_id, view_type, **options)
        return key + (self._name,)
