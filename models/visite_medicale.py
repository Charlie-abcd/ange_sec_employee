# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging


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
    
    # Champs pour l'intégration calendrier
    calendar_event_id = fields.Many2one(
        'calendar.event',
        string='Événement Calendrier',
        help='Événement calendrier associé à cette visite médicale'
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Créer la visite médicale et synchroniser avec le calendrier automatiquement"""
        records = super().create(vals_list)
        # Différer la création de l'événement calendrier après validation complète
        for record in records:
            if record.employee_id and record.date:  # S'assurer que les champs obligatoires sont présents
                record._create_calendar_event()
        return records

    def write(self, vals):
        """Mettre à jour la visite médicale et synchroniser avec le calendrier"""
        result = super().write(vals)
        
        for record in self:
            # Si l'événement calendrier n'existe pas encore et qu'on a maintenant tous les champs requis
            if not record.calendar_event_id and record.employee_id and record.date:
                record._create_calendar_event()
            # Si la date, description ou employé change, mettre à jour l'événement calendrier existant
            elif record.calendar_event_id and ('date' in vals or 'description' in vals or 'employee_id' in vals):
                record._update_calendar_event()
        
        return result

    def unlink(self):
        """Supprimer la visite médicale et l'événement calendrier associé"""
        for record in self:
            if record.calendar_event_id:
                record._delete_calendar_event()
        return super().unlink()

    def _create_calendar_event(self):
        """Créer un événement calendrier pour cette visite médicale"""
        if not self.employee_id or not self.date:
            return
        
        # ORGANISATEUR : Toujours l'utilisateur actuel
        organizer_user_id = self.env.user.id
        
        # PARTICIPANTS : L'employé + l'utilisateur actuel
        participant_ids = []
        
        # Ajouter l'employé concerné comme participant
        if self.employee_id.work_contact_id:
            participant_ids.append(self.employee_id.work_contact_id.id)

        
        # Créer l'événement calendrier - Odoo gère automatiquement les attendees
        event_vals = {
            'name': f"Visite médicale - {self.employee_id.name}",
            'description': self.description or "Visite médicale",
            'start': datetime.combine(self.date, datetime.min.time()),
            'stop': datetime.combine(self.date, datetime.max.time().replace(microsecond=0)),
            'allday': True,
            'user_id': organizer_user_id,  # ORGANISATEUR
            'partner_ids': [(6, 0, participant_ids)],  # PARTICIPANTS (liste vide si pas de participants)
            'categ_ids': [(6, 0, self._get_medical_visit_category())],
            'privacy': 'public',
            'show_as': 'busy',
        }
        
        calendar_event = self.env['calendar.event'].create(event_vals)
        self.calendar_event_id = calendar_event.id

    def _update_calendar_event(self):
        """Mettre à jour l'événement calendrier existant"""
        if not self.calendar_event_id:
            return
        
        # Recalculer les participants au cas où l'employé aurait changé
        participant_ids = []
        if self.employee_id.work_contact_id:
            participant_ids.append(self.employee_id.work_contact_id.id)
        if self.env.user.partner_id and self.env.user.partner_id.id not in participant_ids:
            participant_ids.append(self.env.user.partner_id.id)
        
        update_vals = {
            'name': f"Visite médicale - {self.employee_id.name}",
            'description': self.description or "Visite médicale",
            'start': datetime.combine(self.date, datetime.min.time()),
            'stop': datetime.combine(self.date, datetime.max.time().replace(microsecond=0)),
            'allday': True,
            'partner_ids': [(6, 0, participant_ids)],  # Mettre à jour les participants aussi
        }
        
        try:
            self.calendar_event_id.write(update_vals)
        except Exception as e:
            logging.getLogger(__name__).error(f"Erreur lors de la mise à jour de l'événement calendrier: {e}")

    def _delete_calendar_event(self):
        """Supprimer l'événement calendrier associé"""
        if self.calendar_event_id:
            try:
                event_id = self.calendar_event_id.id
                self.calendar_event_id.unlink()
                self.calendar_event_id = False
            except Exception as e:
                logging.getLogger(__name__).error(f"Erreur lors de la suppression de l'événement calendrier: {e}")

    def _get_medical_visit_category(self):
        """Obtenir ou créer la catégorie pour les visites médicales"""
        category = self.env['calendar.event.type'].search([('name', '=', 'Visite Médicale')], limit=1)
        if not category:
            category = self.env['calendar.event.type'].create({
                'name': 'Visite Médicale',
                'color': 3,  # Couleur rouge pour les visites médicales
            })
        return [category.id]

    def action_view_calendar_event(self):
        """Action pour ouvrir l'événement calendrier associé"""
        if not self.calendar_event_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Aucun événement calendrier',
                    'message': 'Cette visite médicale n\'est pas synchronisée avec le calendrier.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Calendrier - Visite Médicale',
            'res_model': 'calendar.event',
            'view_mode': 'calendar,list,form',
            'target': 'current',
            'context': {
                'default_mode': 'month',
                'initial_date': self.date.strftime('%Y-%m-%d'),
                # Pas de filtre restrictif - afficher tous les événements
            },
            # Pas de domaine restrictif - laisser tous les événements visibles dans le calendrier
            # 'domain': [('id', '=', self.calendar_event_id.id)],
        }

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
