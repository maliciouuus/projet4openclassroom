import json
import os

class Player:
    FILE_PATH = os.path.join("data", "players.json")

    @staticmethod
    def save_player(player):
        """
        Enregistre un joueur dans le fichier JSON dans le bon format.
        """
        os.makedirs("data", exist_ok=True)

        # Charger ou créer le fichier JSON
        try:
            with open(Player.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"_default": {}}

        # Vérifier si le joueur est bien un dictionnaire
        if not isinstance(player, dict):
            raise ValueError("Le joueur doit être un dictionnaire")

        # Assurer que les clés sont bien formatées
        formatted_player = {
            "name": player.get("last_name", player.get("name", "Inconnu")),  # Toujours "name"
            "first_name": player.get("first_name", ""),
            "dob": player.get("dob", ""),  # Date de naissance si disponible
            "sex": player.get("sex", ""),  # Sexe si disponible
            "national_id": player.get("national_id", ""),  # ID national si dispo
            "rank": player.get("ranking", player.get("rank", 0))  # Toujours "rank"
        }

        # Trouver le nouvel ID
        existing_ids = list(map(int, data["_default"].keys()))
        new_id = str(max(existing_ids) + 1) if existing_ids else "1"

        # Ajouter le joueur
        data["_default"][new_id] = formatted_player

        # Sauvegarder le fichier mis à jour
        with open(Player.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        from views.menu import MainView
        MainView.show_success_msg()


    @staticmethod
    def load_players():
        """
        Charge les joueurs depuis le fichier JSON et s'assure qu'ils sont bien des dictionnaires.
        """
        try:
            with open(Player.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            players = list(data.get("_default", {}).values())

            # Vérifier que chaque joueur est bien un dictionnaire et possède les bonnes clés
            valid_players = []
            for player in players:
                if isinstance(player, dict) and "name" in player and "rank" in player:
                    valid_players.append(player)
                else:
                    print(f"❌ Données incorrectes ignorées : {player}")

            return valid_players

        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retourne une liste vide si le fichier est vide ou absent

    @staticmethod
    def alphabetic_players():
        """
        Retourne une liste triée des joueurs par ordre alphabétique du nom.
        """
        players = Player.load_players()
        sorted_players = sorted(players, key=lambda x: x["name"].lower())

        return json.dumps(sorted_players, indent=4, ensure_ascii=False)

    @staticmethod
    def load_and_sort_players_by_rank():
        """
        Retourne une liste triée des joueurs par rang (du plus haut au plus bas).
        """
        players = Player.load_players()

        # Vérification du type de rang et conversion si nécessaire
        for player in players:
            if not isinstance(player.get("rank"), int):
                try:
                    player["rank"] = int(player["rank"])
                except (ValueError, TypeError):
                    raise TypeError(f"Le joueur {player.get('name', 'Inconnu')} a un rang non valide: {player.get('rank')}")

        sorted_players = sorted(players, key=lambda x: x["rank"], reverse=True)

        return json.dumps(sorted_players, indent=4, ensure_ascii=False)
