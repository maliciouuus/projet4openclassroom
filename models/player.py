import json
import os

class Player:
    def __init__(self, first_name, last_name, national_id, ranking=0):
        """Initialise un joueur avec les données fournies."""
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.ranking = ranking

    #def 


    @staticmethod
    def save_players(players, filename='players.json'):
        """Enregistre la liste des joueurs dans un fichier JSON dans le dossier 'data'."""
        # Vérifie si le dossier 'data' existe, sinon crée-le
        os.makedirs('data', exist_ok=True)

        # Spécifie le chemin complet du fichier
        file_path = os.path.join('data', filename)

        with open(file_path, 'w') as f:
            json.dump([player.to_dict() for player in players], f, indent=4)

    @staticmethod
    def load_players(filename='players.json'):
        """Charge la liste des joueurs à partir d'un fichier JSON dans le dossier 'data'."""
        # Spécifie le chemin complet du fichier
        file_path = os.path.join('data', filename)

        try:
            with open(file_path, 'r') as f:
                players_data = json.load(f)
                return [Player(**data) for data in players_data]  # Crée une instance de Player pour chaque dictionnaire
        except FileNotFoundError:
            return []  # Si le fichier n'existe pas encore, retourne une liste vide