


class PlayerController:
    """Contrôleur gérant l'ajout des joueurs."""

    def __init__(self):
        #self.players = Player.load_players()  # Charge les joueurs existants
        self.players = None

    def add_players(self):
        """Ajoute de nouveaux joueurs jusqu'à ce que l'utilisateur arrête."""
        from views.menu import MainView
        while True:
            player_info = MainView.create_player()
            import json                
            # Convert Python to JSON  
            json_object = json.dumps(player_info, indent = 4) 
            from models.player import Player
            # Print JSON object
            print(json_object)
            player = Player(player_info)  # Création d'une instance Player

            MainView.show_success_msg()
            break

    def alphabetic_playeurs(self):
        print("cc")


    def rank_playeurs(self):
        print("cc")