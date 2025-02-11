"""Module de contrôle des joueurs."""
from models.player import Player


class PlayerController:
    """Contrôleur gérant l'ajout et la gestion des joueurs."""

    def __init__(self):
        """Initialise le contrôleur des joueurs."""
        self.players = []

    def add_players(self, player_info):
        """Ajoute un nouveau joueur à la base de données.

        Args:
            player_info (dict): Informations du joueur à ajouter
        """
        Player.save_player(player_info)

    @staticmethod
    def format_players(players):
        """Formate la liste des joueurs pour l'affichage.

        Args:
            players (list): Liste des joueurs à formater

        Returns:
            list: Liste des joueurs formatée pour l'affichage
        """
        return [
            f"Nom: {player['name']}, "
            f"Prénom: {player['first_name']}, "
            f"Rang: {player['rank']}"
            for player in players
        ]
