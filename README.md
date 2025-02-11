# Centre d'Échecs - Gestionnaire de Tournois

Ce projet est un gestionnaire de tournois d'échecs qui permet d'organiser et de suivre des tournois selon le système suisse.

## Lien du Repository GitHub

[Lien vers le repository GitHub](https://github.com/votre-username/projet4openclassroom)

## Fonctionnalités

- Création et gestion de joueurs
- Création et gestion de tournois
- Système de tournoi suisse
- Génération de rapports (classements, historique des matchs)
- Interface en ligne de commande conviviale

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/projet4openclassroom.git
cd projet4openclassroom
```

2. Créez un environnement virtuel :
```bash
python -m venv env
```

3. Activez l'environnement virtuel :
- Sous Windows :
```bash
env\Scripts\activate
```
- Sous Linux/Mac :
```bash
source env/bin/activate
```

4. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Pour lancer l'application :
```bash
python main.py
```

2. Menu principal :
   - 1️⃣ Créer un joueur
   - 2️⃣ Créer un tournoi
   - 3️⃣ Afficher les rapports
   - 4️⃣ Gérer les tournois en cours
   - 5️⃣ Quitter

## Vérification du Style de Code

1. Pour vérifier le style avec flake8 :
```bash
flake8 . --max-line-length=119
```

2. Pour générer un rapport HTML avec flake8-html :
```bash
flake8 --format=html --htmldir=flake8_rapport --max-line-length=119
```
Le rapport sera généré dans le dossier `flake8_rapport`.

## Structure du Projet

```
projet4openclassroom/
├── controllers/
│   ├── player_controller.py
│   └── tournament_controller.py
├── models/
│   ├── player.py
│   ├── round.py
│   └── tournament.py
├── views/
│   └── menu.py
├── data/
│   ├── players.json
│   └── tournaments.json
├── main.py
├── requirements.txt
└── README.md
```

## Génération des Rapports

L'application peut générer différents types de rapports :
- Liste de tous les joueurs par ordre alphabétique
- Liste de tous les joueurs par classement
- Liste de tous les tournois
- Liste des joueurs d'un tournoi
- Liste des tours d'un tournoi
- Liste des matchs d'un tournoi

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Auteur

Sacha Redelberger

## Licence

Ce projet est sous licence MIT. 