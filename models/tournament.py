"""Module de gestion des tournois."""
import json
import os
import random
from datetime import datetime
from models.round import Round


class Tournament:
    """Classe représentant un tournoi d'échecs."""

    FILE_PATH = os.path.join("data", "tournaments.json")

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

    def __init__(
            self, name, place, date, time_control,
            players=None, nb_rounds=4, rounds=None, desc="",
            current_round=0, player_scores=None
    ):
        """Initialise un nouveau tournoi.

        Args:
            name (str): Nom du tournoi
            place (str): Lieu du tournoi
            date (str): Date du tournoi
            time_control (str): Type de contrôle du temps
            players (list, optional): Liste des joueurs. Defaults to None.
            nb_rounds (int, optional): Nombre de tours. Defaults to 4.
            rounds (list, optional): Liste des tours. Defaults to None.
            desc (str, optional): Description du tournoi. Defaults to "".
            current_round (int, optional): Tour actuel. Defaults to 0.
            player_scores (dict, optional): Scores des joueurs. Defaults to None.

        Raises:
            ValueError: Si la date n'est pas au bon format
        """
        if not self.validate_date(date):
            raise ValueError("La date doit être au format JJ-MM-AAAA")

        self.name = name
        self.place = place
        self.date = date
        self.time_control = time_control
        self.players = players if players is not None else []
        self.nb_rounds = nb_rounds
        self.rounds = rounds if rounds is not None else []
        self.desc = desc
        self.current_round = current_round
        self.player_scores = player_scores if player_scores is not None else {}

    def start_tournament(self):
        """Démarre le tournoi en créant le premier tour."""
        if not self.players or len(self.players) % 2 != 0:
            raise ValueError("Le nombre de joueurs doit être pair pour démarrer le tournoi.")

        if self.current_round >= self.nb_rounds:
            raise ValueError("Le tournoi est déjà terminé.")

        if not self.player_scores:
            self.player_scores = {player["national_id"]: 0 for player in self.players}

        pairs = self._generate_pairs()

        round_name = f"Round {self.current_round + 1}"
        current_round = Round(round_name)

        for player1, player2 in pairs:
            current_round.add_match(player1, player2)

        self.rounds.append(current_round)
        self.current_round += 1
        self.save_tournament(self)

    def end_current_round(self, results):
        """Termine le tour actuel et met à jour les scores.

        Args:
            results (list): Liste des résultats (1 pour victoire joueur1, 2 pour victoire joueur2, 0 pour nul)
        """
        if not self.rounds or self.current_round == 0:
            raise ValueError("Aucun tour en cours.")

        current_round = self.rounds[-1]

        for match_index, result in enumerate(results):
            current_round.update_score(match_index, result)
            match = current_round.matches[match_index]

            if result == 1:
                self.player_scores[match[0][0]["national_id"]] += 1
            elif result == 2:
                self.player_scores[match[1][0]["national_id"]] += 1
            else:  # Match nul
                self.player_scores[match[0][0]["national_id"]] += 0.5
                self.player_scores[match[1][0]["national_id"]] += 0.5

        current_round.end_round()
        self.save_tournament(self)

    def _generate_pairs(self):
        """Génère les paires de joueurs selon le système suisse.

        Returns:
            list: Liste des paires de joueurs
        """
        if self.current_round == 0:
            players = self.players.copy()
            random.shuffle(players)
        else:
            players = sorted(
                self.players,
                key=lambda x: (self.player_scores[x["national_id"]], x["rank"]),
                reverse=True
            )

        pairs = []
        used_players = set()

        for i in range(0, len(players), 2):
            player1 = players[i]

            for j in range(i + 1, len(players)):
                player2 = players[j]
                if player2["national_id"] not in used_players and not self._have_played_together(player1, player2):
                    pairs.append((player1, player2))
                    used_players.add(player1["national_id"])
                    used_players.add(player2["national_id"])
                    break
            else:
                for j in range(i + 1, len(players)):
                    player2 = players[j]
                    if player2["national_id"] not in used_players:
                        pairs.append((player1, player2))
                        used_players.add(player1["national_id"])
                        used_players.add(player2["national_id"])
                        break

        return pairs

    def _have_played_together(self, player1, player2):
        """Vérifie si deux joueurs ont déjà joué ensemble.

        Args:
            player1 (dict): Premier joueur
            player2 (dict): Deuxième joueur

        Returns:
            bool: True si les joueurs ont déjà joué ensemble
        """
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if ((match[0][0]["national_id"] == player1["national_id"] and
                     match[1][0]["national_id"] == player2["national_id"]) or
                    (match[0][0]["national_id"] == player2["national_id"] and
                     match[1][0]["national_id"] == player1["national_id"])):
                    return True
        return False

    def get_rankings(self):
        """Retourne le classement actuel du tournoi.

        Returns:
            list: Liste des joueurs triée par score puis par rang
        """
        return sorted(
            self.players,
            key=lambda x: (self.player_scores.get(x["national_id"], 0), x["rank"]),
            reverse=True
        )

    def to_dict(self):
        """Convertit un objet Tournament en dictionnaire pour le stockage JSON.

        Returns:
            dict: Dictionnaire représentant le tournoi
        """
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "time_control": self.time_control,
            "players": self.players,
            "nb_rounds": self.nb_rounds,
            "rounds": [round_obj.to_dict() for round_obj in self.rounds],
            "desc": self.desc,
            "current_round": self.current_round,
            "player_scores": self.player_scores
        }

    @staticmethod
    def save_tournament(tournament):
        """Sauvegarde un tournoi dans le fichier JSON.

        Args:
            tournament (Tournament): Le tournoi à sauvegarder
        """
        os.makedirs("data", exist_ok=True)

        try:
            with open(Tournament.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"_default": {}}

        existing_ids = list(map(int, data["_default"].keys())) if data["_default"] else []
        new_id = str(max(existing_ids) + 1) if existing_ids else "1"

        data["_default"][new_id] = tournament.to_dict()

        with open(Tournament.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_tournaments():
        """Charge les tournois depuis le fichier JSON.

        Returns:
            list: Liste des tournois ou liste vide si aucun tournoi n'existe
        """
        try:
            with open(Tournament.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            return list(data.get("_default", {}).values())
        except (FileNotFoundError, json.JSONDecodeError):
            return []
