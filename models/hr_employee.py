# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    """Extension du modèle hr.employee pour Ange Security"""
    _inherit = 'hr.employee'

    # ========================================
    # CHAMPS POUR L'ONGLET ÉQUIPEMENT ET SANTÉ
    # ========================================
    
    uniforme_travail = fields.Text(
        string='Uniforme de travail',
        help='Description de l\'uniforme de travail attribué à l\'employé'
    )
    
    date_renouvellement_uniforme = fields.Date(
        string='Date renouvellement uniforme',
        help='Date prévue pour le renouvellement de l\'uniforme'
    )
    
    visite_medicale_ids = fields.One2many(
        'visite.medicale',
        'employee_id',
        string='Visites médicales',
        help='Visites médicales associées à cet employé'
    )
    
    etat_formations = fields.Text(
        string='État des formations',
        help='État actuel des formations de l\'employé'
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

    # ========================================
    # MÉTHODES ET CONTRAINTES
    # ========================================
    
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

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type='form', **options):
        """Override pour s'assurer que les vues sont correctement mises à jour"""
        key = super()._get_view_cache_key(view_id, view_type, **options)
        return key + (self._name,)
