# Module Ange Security - Employee Extensions

## Description

Ce module étend les fonctionnalités du formulaire employé d'Odoo 18 pour répondre aux besoins spécifiques d'Ange Security.

## Fonctionnalités

### 1. Onglet "ÉQUIPEMENT ET SANTÉ"

Le module ajoute un nouvel onglet dans le formulaire employé avec les champs suivants :

- **Uniforme de travail** : Champ texte pour décrire l'uniforme attribué
- **Date renouvellement uniforme** : Date prévue pour le renouvellement
- **Visites médicales** : Relation Many2many vers le modèle `visite.medicale`
- **État des formations** : Champ texte pour le suivi des formations

### 2. Modifications de l'onglet "INFORMATIONS PRIVÉES"

#### Zone Citoyenneté
- **Numéro CNI** : Renommage du champ "Numéro d'identification"
- **Numéro carte de séjour** : Renommage du champ "Numéro passport"
- **Date de validité CNI** : Nouveau champ pour la date d'expiration
- **Date de validité carte de séjour** : Nouveau champ pour la date d'expiration

#### Zone Coordonnées Privées
- **Matricule agent** : Nouveau champ unique pour identifier l'agent

### 3. Modèle Visite Médicale

Un nouveau modèle `visite.medicale` est créé avec :
- **Date** : Date de la visite
- **Description** : Description détaillée
- **Fait ?** : Indicateur booléen (cochable)
- Relation Many2many avec les employés

## Installation

1. Copiez le dossier `ange_sec_employee` dans le répertoire des addons d'Odoo
2. Redémarrez le serveur Odoo
3. Activez le mode développeur
4. Allez dans Apps > Mettre à jour la liste des applications
5. Recherchez "Ange Security - Employee Extensions"
6. Cliquez sur "Installer"

## Dépendances

- `base` : Module de base Odoo
- `hr` : Module Ressources Humaines

## Utilisation

Après installation, les nouveaux champs et onglets apparaîtront automatiquement dans le formulaire employé :

1. **Onglet ÉQUIPEMENT ET SANTÉ** : Accessible via le formulaire employé
2. **Champs modifiés** : Visibles dans l'onglet "Informations Privées"
3. **Recherche étendue** : Possibilité de rechercher par matricule agent
4. **Filtres** : Nouveaux filtres pour les employés avec matricule et uniformes à renouveler

## Fonctionnalités Avancées

- **Contrainte d'unicité** : Le matricule agent doit être unique
- **Vues étendues** : Liste, kanban et recherche incluent les nouveaux champs
- **Widget spécialisé** : Les visites médicales utilisent un widget many2many_tags avec couleur

## Support

Pour toute question ou problème, contactez l'équipe de développement d'Ange Security.

## Version

- **Version** : 18.0.1.0.0
- **Compatibilité** : Odoo 18.0
- **Licence** : LGPL-3
