import json
import os

class Player:
    @staticmethod
    def save_player(player, filename='players.json'):
        """
        Enregistre un joueur dans le fichier JSON dans le dossier 'data'.
        """
        os.makedirs('data', exist_ok=True)
        file_path = os.path.join('data', filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"_default": {}}
        
        new_id = str(len(data["_default"]) + 1)
        data["_default"][new_id] = player
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        from views.menu import MainView
        MainView.show_success_msg()

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
