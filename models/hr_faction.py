# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrFaction(models.Model):
    """Modèle pour gérer les factions de travail des employés"""
    _name = 'hr.faction'
    _description = 'Faction de Travail'
    _order = 'name'

    name = fields.Char(
        string='Nom de la faction',
        required=True,
        help='Nom de la faction de travail'
    )
    
    heure_debut = fields.Float(
        string='Heure de début',
        required=True,
        help='Heure de début de la faction (format 24h, ex: 6.0 pour 6h00)'
    )
    
    heure_fin = fields.Float(
        string='Heure de fin',
        required=True,
        help='Heure de fin de la faction (format 24h, ex: 18.0 pour 18h00)'
    )
    
    type_faction = fields.Selection([
        ('jour', 'Jour'),
        ('nuit', 'Nuit'),
        ('custom', 'Personnalisée')
    ], string='Type de faction', required=True, default='jour',
       help='Type de faction de travail')
    
    description = fields.Text(
        string='Description',
        help='Description détaillée de la faction'
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True,
        help='Indique si la faction est active'
    )
    
    employee_ids = fields.One2many(
        'hr.employee',
        'faction_id',
        string='Employés',
        help='Employés assignés à cette faction'
    )
    
    nb_employees = fields.Integer(
        string='Nombre d\'employés',
        compute='_compute_nb_employees',
        store=True,
        help='Nombre d\'employés assignés à cette faction'
    )

    @api.depends('employee_ids')
    def _compute_nb_employees(self):
        """Calculer le nombre d'employés par faction"""
        for faction in self:
            faction.nb_employees = len(faction.employee_ids)

    def name_get(self):
        """Personnaliser l'affichage du nom avec les horaires"""
        result = []
        for record in self:
            # Convertir les heures float en format HH:MM
            debut_h = int(record.heure_debut)
            debut_m = int((record.heure_debut - debut_h) * 60)
            fin_h = int(record.heure_fin)
            fin_m = int((record.heure_fin - fin_h) * 60)
            
            horaire = f"{debut_h:02d}:{debut_m:02d} - {fin_h:02d}:{fin_m:02d}"
            name = f"{record.name} ({horaire})"
            result.append((record.id, name))
        return result

    @api.constrains('heure_debut', 'heure_fin')
    def _check_horaires(self):
        """Vérifier la cohérence des horaires"""
        for record in self:
            if record.heure_debut < 0 or record.heure_debut >= 24:
                raise models.ValidationError(_('L\'heure de début doit être entre 0 et 23.59'))
            if record.heure_fin < 0 or record.heure_fin >= 24:
                raise models.ValidationError(_('L\'heure de fin doit être entre 0 et 23.59'))
            # Note: On permet que heure_fin < heure_debut pour les factions de nuit
