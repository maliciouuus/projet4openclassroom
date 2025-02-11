"""Module de gestion des joueurs."""
import json
import os
import re
from datetime import datetime


class Player:
    """Classe représentant un joueur d'échecs."""

    FILE_PATH = os.path.join("data", "players.json")
    NATIONAL_ID_PATTERN = re.compile(r'^.+$')

    @staticmethod
    def validate_national_id(national_id):
        """Valide le format de l'identifiant national.

        Args:
            national_id (str): Identifiant national à valider

        Returns:
            bool: True si l'identifiant est valide
        """
        return bool(Player.NATIONAL_ID_PATTERN.match(national_id))

    @staticmethod
    def validate_date(date_str):
        """Valide le format de la date.

        Args:
            date_str (str): Date au format JJ-MM-AAAA

        Returns:
            bool: True si la date est valide
        """
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def save_player(player):
        """Enregistre un joueur dans le fichier JSON.

        Args:
            player (dict): Dictionnaire contenant les informations du joueur

        Raises:
            ValueError: Si le joueur n'est pas un dictionnaire ou si les données sont invalides
        """
        os.makedirs("data", exist_ok=True)

        if not isinstance(player, dict):
            raise ValueError("Le joueur doit être un dictionnaire")

        # Validation des données
        if not player.get("last_name"):
            raise ValueError("Le nom de famille est obligatoire")
        if not player.get("first_name"):
            raise ValueError("Le prénom est obligatoire")
        if not player.get("dob") or not Player.validate_date(player["dob"]):
            raise ValueError("La date de naissance est invalide (format: JJ-MM-AAAA)")
        if not player.get("national_id") or not Player.validate_national_id(player["national_id"]):
            raise ValueError("L'identifiant national est invalide (format: AB12345)")

        try:
            with open(Player.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"_default": {}}

        # Vérifier si l'identifiant national existe déjà
        for existing_player in data["_default"].values():
            if existing_player.get("national_id") == player["national_id"]:
                raise ValueError("Cet identifiant national existe déjà")

        formatted_player = {
            "name": player.get("last_name", player.get("name", "Inconnu")),
            "first_name": player.get("first_name", ""),
            "dob": player.get("dob", ""),
            "sex": player.get("sex", ""),
            "national_id": player.get("national_id", ""),
            "rank": player.get("ranking", player.get("rank", 0))
        }

        existing_ids = list(map(int, data["_default"].keys())) if data["_default"] else []
        new_id = str(max(existing_ids) + 1) if existing_ids else "1"

        data["_default"][new_id] = formatted_player

        with open(Player.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        from views.menu import MainView
        MainView.show_success_msg()

    @staticmethod
    def load_players():
        """Charge les joueurs depuis le fichier JSON.

        Returns:
            list: Liste des joueurs valides
        """
        try:
            with open(Player.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            players = list(data.get("_default", {}).values())

            valid_players = []
            for player in players:
                if isinstance(player, dict) and "name" in player and "rank" in player:
                    valid_players.append(player)
                else:
                    print(f"❌ Données incorrectes ignorées : {player}")

            return valid_players

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def alphabetic_players():
        """Retourne une liste triée des joueurs par ordre alphabétique.

        Returns:
            str: Liste des joueurs au format JSON
        """
        players = Player.load_players()
        sorted_players = sorted(players, key=lambda x: x["name"].lower())
        return json.dumps(sorted_players, indent=4, ensure_ascii=False)

    @staticmethod
    def load_and_sort_players_by_rank():
        """Retourne une liste triée des joueurs par rang.

        Returns:
            str: Liste des joueurs au format JSON

        Raises:
            TypeError: Si un joueur a un rang non valide
        """
        players = Player.load_players()

        for player in players:
            if not isinstance(player.get("rank"), int):
                try:
                    player["rank"] = int(player["rank"])
                except (ValueError, TypeError):
                    raise TypeError(
                        f"Le joueur {player.get('name', 'Inconnu')} a un rang non valide: {player.get('rank')}"
                    )

        sorted_players = sorted(players, key=lambda x: x["rank"], reverse=True)
        return json.dumps(sorted_players, indent=4, ensure_ascii=False)
