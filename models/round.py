"""Module de gestion des tours d'un tournoi."""
from datetime import datetime


class Round:
    """Classe représentant un tour de tournoi."""

    def __init__(self, name, matches=None):
        """Initialise un nouveau tour.

        Args:
            name (str): Nom du tour (ex: "Round 1")
            matches (list, optional): Liste des matchs. Defaults to None.
        """
        self.name = name
        self.matches = matches if matches else []
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None

    def add_match(self, player1, player2):
        """Ajoute un match au tour.

        Args:
            player1 (dict): Premier joueur
            player2 (dict): Deuxième joueur
        """
        match = ([player1, 0], [player2, 0])  # [joueur, score]
        self.matches.append(match)

    def end_round(self):
        """Termine le tour en enregistrant l'heure de fin."""
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_score(self, match_index, winner=None):
        """Met à jour le score d'un match.

        Args:
            match_index (int): Index du match à mettre à jour
            winner (int, optional): 1 pour joueur1, 2 pour joueur2,
                                  None pour match nul
        """
        if 0 <= match_index < len(self.matches):
            if winner == 1:
                self.matches[match_index][0][1] = 1  # Joueur 1 gagne
                self.matches[match_index][1][1] = 0  # Joueur 2 perd
            elif winner == 2:
                self.matches[match_index][0][1] = 0  # Joueur 1 perd
                self.matches[match_index][1][1] = 1  # Joueur 2 gagne
            else:
                self.matches[match_index][0][1] = 0.5  # Match nul
                self.matches[match_index][1][1] = 0.5

    def to_dict(self):
        """Convertit le tour en dictionnaire pour le stockage JSON.

        Returns:
            dict: Dictionnaire représentant le tour
        """
        return {
            "name": self.name,
            "matches": self.matches,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
