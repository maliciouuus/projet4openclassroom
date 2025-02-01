import json
import os

class Player:
    def __init__(self, player_dict):
        """Initialise un joueur avec les données fournies."""
        self.player_dict = player_dict
    #def 


    @staticmethod
    def save_players(players, filename='players.json'):
        """Enregistre la liste des joueurs dans un fichier JSON dans le dossier 'data'."""
        # Vérifie si le dossier 'data' existe, sinon crée-le
        os.makedirs('data', exist_ok=True)

        # Spécifie le chemin complet du fichier
        file_path = os.path.join('data', filename)

        print(self.player_dict)

#       with open(file_path, 'w') as f:
            #json.dump([player.to_dict() for player in players], f, indent=4)

    @staticmethod
    def load_players(filename='players.json'):
        """Charge la liste des joueurs à partir d'un fichier JSON dans le dossier 'data'."""
        # Spécifie le chemin complet du fichier
        file_path = os.path.join('data', filename)

        with open(file_path, "r") as read_file:
            data = json.load(read_file)
            return data
