
import json

class PlayerController:
    """Contrôleur gérant l'ajout des joueurs."""

    def __init__(self):
        #self.players = Player.load_players()  # Charge les joueurs existants
        self.players = None

    def add_players(self):
        """Ajoute de nouveaux joueurs jusqu'à ce que l'utilisateur arrête."""
        from views.menu import MainView
        from models.player import Player

        player_info = MainView.create_player()  # Retourne déjà un dictionnaire
        
        print("Données du joueur avant sauvegarde :", player_info)  # Debug

        player = Player()  # Création d'une instance Player
        player.save_player(player_info)  # Envoie directement le dictionnaire


    @staticmethod
    def format_players(players):
        """Formate la liste des joueurs pour l'affichage."""
        return [f"Nom: {p['name']}, Prénom: {p['first_name']}, Rang: {p['rank']}" for p in players]  #fonction pour view


#en gros il y'a un soucis niveau du type de json entre add users et et save json en gros ça enregistre pas de la bonne façon il faut que tout soit adapté pour ajouter une valeur ç un fichier existrant ou bien créer un fichier similaire si il y'a pas de fichiers et faire en sorte que toutes les fonctions marchent bien entre elles c'est important 
