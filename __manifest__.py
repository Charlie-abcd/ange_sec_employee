# -*- coding: utf-8 -*-
{
    'name': 'Ange Security - Employee Extensions',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Extensions des fonctionnalités du formulaire employé pour Ange Security',
    'description': """
Module d'extension des employés pour Ange Security
====================================================

Ce module étend les fonctionnalités du formulaire employé avec :

1. **Onglet ÉQUIPEMENT ET SANTÉ** :
   - Uniforme de travail
   - Date renouvellement uniforme
   - Visites médicales (many2many)
   - État des formations

2. **Onglet INFORMATIONS PRIVÉES** :
   - Renommage des champs d'identification
   - Ajout des dates de validité CNI et carte de séjour
   - Matricule agent

Fonctionnalités :
- Gestion des visites médicales
- Suivi des équipements et formations
- Informations d'identification complètes
    """,
    'author': 'Ange Security',
    'website': 'https://www.angesecurity.com',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
