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
    def load_players():
        """
        Charge les joueurs depuis le fichier JSON.
        """
        with open("data/players.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return list(data.get("_default", {}).values())

    @staticmethod
    def alphabetic_players():
        """
        Retourne la liste des joueurs triés par ordre alphabétique du nom.
        """
        players = Player.load_players()
        sorted_players = sorted(players, key=lambda x: x["name"].lower())
        return json.dumps(sorted_players, indent=4, ensure_ascii=False)

    @staticmethod
    def load_and_sort_players_by_rank():
        """
        Retourne la liste des joueurs triés par rang.
        """
        players = Player.load_players()
        sorted_players = sorted(players, key=lambda x: x["rank"], reverse=True)
        return json.dumps(sorted_players, indent=4, ensure_ascii=False)
