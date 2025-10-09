# Module Ange Security - Employee Extensions

## Description

Ce module étend les fonctionnalités du formulaire employé d'Odoo 18 pour répondre aux besoins spécifiques d'Ange Security, avec des systèmes avancés de gestion des formations et des équipements par employé.

## 🎯 Fonctionnalités Principales

### 1. 📚 **SYSTÈME DE FORMATIONS AVANCÉ**

#### **Catalogue de Formations**
- **Formations centralisées** : Catalogue réutilisable de toutes les formations disponibles
- **Descriptions détaillées** : Chaque formation a sa description et durée de recyclage
- **Statistiques en temps réel** : Suivi du nombre d'employés par statut
- **Pourcentage de complétion** : Vue d'ensemble de l'avancement global

#### **Statuts Individuels par Employé**
- ✅ **Terminée** : Formation complétée avec succès
- 🔄 **En cours** : Formation actuellement en progression
- ⚠️ **Recyclage requis** : Formation nécessitant un renouvellement
- ❌ **Non effectuée** : Formation pas encore commencée

#### **Gestion Intelligente des Recyclages**
- **Calcul automatique** : Dates de recyclage calculées selon la durée configurée
- **Alertes proactives** : Notifications avant expiration (configurable)
- **Suivi des échéances** : Compteur de jours avant recyclage
- **Gestion des retards** : Identification des formations expirées

### 2. 🛠️ **SYSTÈME DE GESTION D'ÉQUIPEMENTS**

#### **Catalogue d'Équipements**
- **Équipements centralisés** : Catalogue réutilisable de tous les équipements disponibles
- **Gestion des coûts** : Montants déductibles configurables par équipement
- **Périodes de renouvellement** : Durées personnalisables (en mois)
- **Statistiques temps réel** : Suivi du nombre d'employés par équipement

#### **Assignations d'Équipements par Employé**
- ✅ **Actif** : Équipement en cours d'utilisation
- ⚠️ **Expiré** : Équipement nécessitant un renouvellement
- 🔄 **Renouvelé** : Équipement remplacé par une nouvelle version
- ❌ **Retiré** : Équipement restitué ou hors service

#### **Gestion Intelligente des Renouvellements**
- **Calcul automatique** : Dates de renouvellement calculées selon la période configurée
- **Alertes visuelles** : Notifications avant expiration avec codes couleur
- **Action de renouvellement** : Création automatique de nouveaux enregistrements
- **Historique complet** : Conservation de tous les équipements passés

### 3. 🏥 **Onglet "ÉQUIPEMENT ET SANTÉ" Intégré**

#### **Section Équipement**
- **Smart Buttons** : Compteurs d'équipements actifs et expirés
- **Liste interactive** : Gestion directe des assignations d'équipements
- **Actions rapides** : Boutons de renouvellement intégrés
- **Alertes visuelles** : Codes couleur selon les statuts et échéances

#### **Section Santé**
- **Visites médicales** : Suivi médical complet avec dates et descriptions
- **Synchronisation calendrier** : Création automatique d'événements
- **Participants intelligents** : Employé concerné + organisateur

### 4. 📋 **Onglet "FORMATIONS" Révolutionné**

#### **Smart Buttons Informatifs**
- 🎓 **Total** : Nombre total de formations assignées
- ✅ **Terminées** : Formations complétées (vert)
- ⏳ **En cours** : Formations en progression (bleu)
- 🔄 **Recyclage** : Formations à renouveler (rouge)

#### **Interface Moderne**
- **Liste éditable** : Modification directe des statuts et dates
- **Codes couleur** : Identification visuelle rapide des statuts
- **Statistiques personnelles** : Pourcentage de réussite individuel

### 5. 🔐 **Modifications "INFORMATIONS PRIVÉES"**

#### **Zone Citoyenneté**
- **Numéro CNI** : Carte Nationale d'Identité
- **Date de validité CNI** : Suivi des expirations
- **Numéro carte de séjour** : Pour les employés étrangers
- **Date de validité carte de séjour** : Gestion des renouvellements

#### **Zone Agent**
- **Matricule agent** : Identifiant unique sécurisé
- **Faction** : Assignation aux équipes de travail

### 6. 🏥 **Modèle Visite Médicale avec Intégration Calendrier**

- **Suivi médical complet** : Dates, descriptions, statuts
- **Interface intuitive** : Gestion directe depuis la fiche employé
- **Historique** : Conservation de toutes les visites passées
- **📅 Synchronisation calendrier automatique** : Création d'événements calendrier
- **👥 Participants intelligents** : Employé concerné + organisateur
- **🔗 Accès direct** : Bouton "Voir dans Calendrier" depuis la visite

## 🚀 Installation

### Prérequis
- **Odoo 18.0** ou supérieur
- Modules de base : `hr` (Ressources Humaines)

### Étapes d'installation
1. Copiez le dossier `ange_sec_employee` dans le répertoire des addons d'Odoo
2. Redémarrez le serveur Odoo
3. Activez le mode développeur
4. Allez dans **Apps** > **Mettre à jour la liste des applications**
5. Recherchez "**Ange Security - Employee Extensions**"
6. Cliquez sur "**Installer**"

## 📖 Utilisation

### 🎓 **Gestion des Formations**

#### **1. Créer le Catalogue de Formations**
- Allez dans **Ressources Humaines** > **Catalogue de Formations**
- Créez vos formations avec descriptions et durées de recyclage
- Activez/désactivez selon les besoins

#### **2. Assigner des Formations aux Employés**
- Depuis une formation : Bouton "**Assigner des Employés**"
- Depuis un employé : Onglet "**FORMATIONS**" > Ajouter manuellement
- Gestion des statuts individuels en temps réel

#### **3. Suivi des Statuts**
- **Vue globale** : Menu "**Formations par Employé**"
- **Vue Kanban** : Groupement par statut avec codes couleur
- **Filtres intelligents** : Par statut, employé, formation, alertes

### 🛠️ **Gestion des Équipements**

#### **1. Créer le Catalogue d'Équipements**
- Allez dans **Ressources Humaines** > **Équipements**
- Créez vos équipements avec descriptions et périodes de renouvellement
- Configurez les montants déductibles si nécessaire

#### **2. Assigner des Équipements aux Employés**
- Depuis un équipement : Liste "**Employés Assignés**" (éditable)
- Depuis un employé : Onglet "**ÉQUIPEMENT ET SANTÉ**" > Section Équipement
- Gestion des dates de remise et statuts en temps réel

#### **3. Suivi des Renouvellements**
- **Alertes automatiques** : Codes couleur selon les échéances
- **Action de renouvellement** : Bouton direct dans les listes
- **Historique complet** : Conservation de tous les équipements passés
- **Vue Kanban moderne** : Cartes visuelles avec alertes d'expiration

### 👤 **Gestion des Employés**

#### **Onglet ÉQUIPEMENT ET SANTÉ**
- **Section Équipement** : Smart buttons avec compteurs actifs/expirés
- **Liste interactive** : Gestion directe des assignations d'équipements
- **Actions de renouvellement** : Boutons intégrés pour renouveler les équipements
- **Section Santé** : Ajoutez les visites médicales avec suivi des statuts
- **📅 Synchronisation automatique** : Les visites créent automatiquement des événements calendrier
- **👥 Participants** : L'employé concerné et l'organisateur sont ajoutés comme participants

#### **Onglet FORMATIONS**
- **Smart buttons** : Vue d'ensemble des statistiques
- **Liste interactive** : Modification directe des dates et statuts
- **Codes couleur** : Identification visuelle immédiate

#### **Informations Privées**
- Complétez les informations CNI et cartes de séjour
- Assignez un matricule agent unique
- Définissez la faction de travail (optionnelle)

## 🎨 **Interfaces Utilisateur**

### **Vues Modernes**
- ✅ **Vue Liste** : Édition rapide en ligne
- 🎯 **Vue Kanban** : Cartes visuelles avec statistiques
- 📊 **Smart Buttons** : Compteurs colorés par statut
- 🔍 **Filtres Avancés** : Recherche multicritères

### **Codes Couleur**

#### **Formations**
- 🟢 **Vert** : Formations terminées
- 🔵 **Bleu** : Formations en cours
- 🔴 **Rouge** : Recyclage requis
- ⚫ **Gris** : Non effectuées

#### **Équipements**
- 🟢 **Vert** : Équipements actifs et valides
- 🟡 **Orange** : Équipements expirant bientôt (≤ 30 jours)
- 🔴 **Rouge** : Équipements expirés
- 🔵 **Bleu** : Équipements renouvelés
- ⚫ **Gris** : Équipements retirés

## ⚙️ **Configuration**

### **Paramètres Système**
- **Jours d'alerte recyclage** : Configurable via les paramètres système
- **Durées de recyclage** : Personnalisables par formation
- **Droits d'accès** : Configurés par groupe utilisateur

### **Données de Démonstration**

#### **Catalogue de Formations**
Le module inclut des formations prêtes à l'emploi :
- Agent de liaison, Superviseur, Agent de sécurité
- Agent cynophile, Hôtesse d'accueil, etc.

#### **Catalogue d'Équipements**
Le module inclut des équipements de sécurité prêts à l'emploi :
- Uniforme complet, Gilet pare-balles, Matraque télescopique
- Talkie-walkie, Lampe torche, Sifflet de sécurité, etc.
- Montants déductibles et périodes de renouvellement configurés

## 🔧 **Architecture Technique**

### **Modèles Principaux**
- `hr.formation` : Catalogue de formations
- `hr.employee.formation` : Statuts individuels par employé
- `ange.equipement` : Catalogue d'équipements
- `ange.employee.equipement` : Assignations d'équipements par employé
- `visite.medicale` : Suivi médical avec intégration calendrier
- `hr.faction` : Gestion des équipes

### **Fonctionnalités Avancées**
- **Calculs automatiques** : Dates de recyclage/renouvellement, alertes, statistiques
- **Contraintes de données** : Unicité des matricules, cohérence des dates
- **Relations intelligentes** : Many2many avec modèles intermédiaires
- **Actions de renouvellement** : Création automatique de nouveaux enregistrements d'équipements
- **Intégration calendrier** : Synchronisation automatique des visites médicales
- **Compatibilité Odoo 18** : Nouvelle syntaxe des vues (sans `attrs`), accessibilité WCAG 2.1
- **Vues Kanban modernes** : Template `card` avec alertes visuelles et codes couleur

## 🛡️ **Sécurité et Droits**

### **Groupes d'Accès**
- **Utilisateurs** : Lecture seule
- **Utilisateurs RH** : Lecture/écriture (sans suppression)
- **Managers RH** : Accès complet

### **Contraintes**
- **Matricule agent unique** : Validation automatique
- **Dates cohérentes** : Vérification début/fin de formation
- **Intégrité référentielle** : Suppression en cascade sécurisée

## 📞 **Support**

Pour toute question ou problème :
- **Documentation** : Consultez ce README
- **Support technique** : Équipe de développement Ange Security
- **Contributions** : Bienvenues via pull requests

## 📋 **Informations Techniques**

- **Version** : 18.0.3.0.0
- **Compatibilité** : Odoo 18.0+
- **Licence** : LGPL-3
- **Auteur** : Ange Security
- **Dernière mise à jour** : Octobre 2024

## 🔄 **Changelog**

### Version 18.0.3.0.0 - **SYSTÈME D'ÉQUIPEMENTS COMPLET**
- ✅ **Nouveau** : Système de gestion d'équipements avec catalogue centralisé
- ✅ **Nouveau** : Assignations d'équipements par employé avec statuts (actif, expiré, renouvelé, retiré)
- ✅ **Nouveau** : Gestion intelligente des renouvellements avec calculs automatiques
- ✅ **Nouveau** : Alertes visuelles d'expiration avec codes couleur (≤ 30 jours)
- ✅ **Nouveau** : Actions de renouvellement automatique avec historique complet
- ✅ **Nouveau** : Vues Kanban modernes avec template `card` et alertes Bootstrap
- ✅ **Nouveau** : Intégration dans l'onglet "ÉQUIPEMENT ET SANTÉ" avec smart buttons
- ✅ **Nouveau** : Montants déductibles configurables par équipement
- ✅ **Nouveau** : Données de démonstration avec équipements de sécurité
- ✅ **Amélioré** : Compatibilité WCAG 2.1 avec attributs `title` et rôles ARIA
- ✅ **Amélioré** : Méthode `create` batch-compatible (`@api.model_create_multi`)
- ✅ **Corrigé** : Champ faction rendu optionnel (suppression `required="1"`)
- ✅ **Corrigé** : Syntaxe QWeb avec balises `<t>` pour éviter conflits XML

### Version 18.0.2.0.0 - **SYSTÈME DE FORMATIONS AVANCÉ**
- ✅ **Nouveau** : Système de formations avec statuts par employé
- ✅ **Nouveau** : Catalogue de formations centralisé
- ✅ **Nouveau** : Gestion intelligente des recyclages
- ✅ **Nouveau** : Intégration calendrier pour les visites médicales
- ✅ **Amélioré** : Interface utilisateur moderne avec smart buttons
- ✅ **Amélioré** : Compatibilité complète Odoo 18 (syntaxe sans `attrs`)
- ✅ **Amélioré** : Vues Kanban avec codes couleur et statistiques
- ✅ **Amélioré** : Synchronisation automatique des événements calendrier

### Version 18.0.1.0.0 - **BASE EMPLOYÉ ÉTENDUE**
- ✅ Extension du formulaire employé
- ✅ Gestion des uniformes et visites médicales
- ✅ Informations privées étendues
