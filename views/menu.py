from controllers.exit import Exit
from controllers.player_controller import PlayerController


class MainView:
    """Vue principale affichant le menu et gérant les entrées utilisateur."""

    def afficher_menu(self):
        while True:
            print("\nCentre Échecs")
            print("--------------------")
            print("1. Créer un joueur")
            print("2. Créer un tournoi")
            print("3. Afficher les rapports")
            print("4. Quitter")
            print("--------------------")

            # Demande un choix valide entre 1 et 6
            number_menu = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 6 : ", 1, 6)
            self.check_number(number_menu)

    @staticmethod
    def get_valid_input(prompt, min_val, max_val):
        """Demande une entrée utilisateur et vérifie qu'elle est bien un entier entre min_val et max_val."""
        while True:
            try:
                choice = int(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Erreur : Veuillez entrer un nombre entre {min_val} et {max_val}.")
            except ValueError:
                print("Erreur : Veuillez entrer un chiffre valide.")

    def check_number(self, choice):
        """Exécute l'action correspondant au choix de l'utilisateur."""
        actions = {
            1: PlayerController().add_players,
            2: self.create_tournament,
            3: self.show_rapport,
            6: Exit.start  # Quitte l'application
        }
        actions[choice]()


    def check_number_rapport(self, choice):
        """Exécute l'action correspondant au choix de l'utilisateur."""
        actions = {
            1: PlayerController().add_players,
            2: self.create_tournament,
            3: Exit.start  # coder le retour si possible
        }
        actions[choice]()

    @staticmethod
    def create_player():
        """Demande à l'utilisateur les informations d'un joueur et retourne un dictionnaire."""
        last_name = input("Nom de famille : ").strip()
        first_name = input("Prénom : ").strip()
        national_id = input("Identifiant national d’échecs (ex: AB12345) : ").strip()
        ranking = int(input("Classement initial (facultatif, 0 par défaut) : "))

        return {
            "last_name": last_name,
            "first_name": first_name,
            "national_id": national_id,
            "ranking": ranking
        }

    @staticmethod
    def show_rapport():
        print("--------------------")
        print("1. Joueurs")
        print("2. Tournoi")
        print("3. Retour")
        print("--------------------")
        number_menu = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 3 : ", 1, 3)


 
    def players_menu():

        print("--------------------")
        print("1. Alphabetique")
        print("2. Rang")
        print("3. Retour")
        X = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 3 : ", 1, 3)
        print("cc" if x == 1 else "deux" if x == 2 else "3")

        from models.player import Player
        print(Player.load_players())

    @staticmethod
    def create_tournament():
        """Action pour créer un tournoi."""
        print("Création d'un tournoi...")

    @staticmethod
    def show_tournaments():
        """Action pour afficher la liste des tournois."""
        print("Affichage de la liste des tournois...")

    @staticmethod
    def show_reports():
        """Action pour afficher les rapports."""
        print("Affichage des rapports...")


    @staticmethod
    def show_success_msg():
        """Action pour afficher les rapports."""
        print("Succès")
