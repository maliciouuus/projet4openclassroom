from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    """Contrôleur gérant l'ajout des joueurs."""

    def __init__(self):
        self.players = Player.load_players()  # Charge les joueurs existants

    def add_players(self):
        """Ajoute de nouveaux joueurs jusqu'à ce que l'utilisateur arrête."""
        while True:
            player_info = PlayerView.get_player_info()
            player = Player(**player_info)  # Création d'une instance Player
            self.players.append(player.to_dict())  # Ajout sous forme de dict

            Player.save_players(self.players)  # Sauvegarde immédiate dans JSON
            PlayerView.show_success_message()

            if not PlayerView.ask_continue():
                break  # Arrête l'ajout si l'utilisateur ne veut plus continuer
