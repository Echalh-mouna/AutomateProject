# Application de Gestion des Automates

Cette application permet de créer, manipuler et analyser des automates finis. Elle offre une interface graphique moderne et intuitive développée avec PyQt5.

## 📋 Prérequis

- Python 3.x
- PyQt5
- Graphviz (pour la visualisation des automates)

### Installation des dépendances

```bash
# Installation des packages Python nécessaires
pip install PyQt5 graphviz

# Installation de Graphviz
# Windows : Télécharger et installer depuis https://graphviz.org/download/
# Puis ajouter le dossier bin de Graphviz au PATH système
```

## 🚀 Fonctionnalités

L'application est divisée en trois sections principales :

### 1. Gestion Basique des Automates
- Création et chargement d'automates
- Ajout/suppression d'états
- Ajout/suppression de transitions
- Sauvegarde des automates au format JSON

### 2. Analyse des Automates
- Vérification du déterminisme
- Transformation en automate déterministe
- Vérification de la complétude
- Complétion d'automate
- Vérification de la minimalité
- Minimisation d'automate

### 3. Opérations sur les Mots et Langages
- Test de reconnaissance de mots
- Génération de mots acceptés/rejetés
- Test d'équivalence entre automates
- Calcul d'union d'automates
- Calcul d'intersection d'automates
- Calcul du complément d'un automate

## 📖 Guide d'Utilisation

### Démarrage de l'application

```bash
python main.py
```

### Création d'un Automate

1. Dans la section "Gestion Basique", cliquez sur "Choisir Dossier"
2. Donnez un nom à votre automate
3. Cliquez sur "Créer Automate"

### Ajout d'États et Transitions

1. Pour ajouter un état :
   - Entrez le nom de l'état
   - Cochez "Initial" et/ou "Final" si nécessaire
   - Cliquez sur "Ajouter État"

2. Pour ajouter une transition :
   - Remplissez les champs Source, Symbole et Destination
   - Cliquez sur "Ajouter Transition"

### Manipulation des Automates

1. Test de mots :
   - Entrez un mot dans le champ prévu
   - Cliquez sur "Tester le mot"

2. Génération de mots :
   - Spécifiez une longueur maximale
   - Choisissez entre "Générer mots acceptés" ou "Afficher mots rejetés"

3. Opérations binaires :
   - Chargez un automate principal et un automate secondaire
   - Utilisez les boutons d'opérations (union, intersection, etc.)

## 💾 Format des Fichiers

Les automates sont sauvegardés au format JSON avec la structure suivante :

```json
{
    "nom": "nom_automate",
    "etats": [
        {
            "nom": "q0",
            "est_initial": true,
            "est_final": false
        },
        ...
    ],
    "alphabet": ["a", "b", ...],
    "transitions": [
        {
            "source": "q0",
            "symbole": "a",
            "destination": "q1"
        },
        ...
    ]
}
```

## 🎨 Visualisation

- Les automates sont visualisés automatiquement après chaque modification
- Les états initiaux sont marqués par une flèche entrante
- Les états finaux sont représentés par un double cercle
- Les transitions sont représentées par des flèches étiquetées

## ⚠️ Résolution des Problèmes Courants

1. Si la visualisation ne fonctionne pas :
   - Vérifiez que Graphviz est correctement installé
   - Vérifiez que le dossier bin de Graphviz est dans le PATH
   - Redémarrez l'application

2. Si un automate ne se charge pas :
   - Vérifiez le format du fichier JSON
   - Vérifiez les permissions du dossier

## 🤝 Contribution

Pour contribuer au projet :
1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails. 

## 🙏 Remerciements

Nous tenons à exprimer notre sincère gratitude à :

- **Pr. LAZAIZ** et **Pr. KAMOUSS** pour leur encadrement et leur soutien précieux tout au long de ce projet.

## 👥 Réalisé par

- Echalh Mouna
- Wafaa El Maifi
- Hiba Kanafi
- Soufiane Nadifi 