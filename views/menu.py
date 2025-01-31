from controllers.exit import Exit
from controllers.player_controller import PlayerController


class MainView:
    """Vue principale affichant le menu et gérant les entrées utilisateur."""

    def afficher_menu(self):
        while True:
            print("\nCentre Échecs")
            print("--------------------")
            print("1. Créer un joueur")
            print("2. Afficher la liste des joueurs")
            print("3. Créer un tournoi")
            print("4. Afficher la liste des tournois")
            print("5. Afficher les rapports")
            print("6. Quitter")
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
            2: self.show_players,
            3: self.create_tournament,
            4: self.show_tournaments,
            5: self.show_reports,
            6: Exit.start  # Quitte l'application
        }
        actions[choice]()

    @staticmethod
    def create_player():
        """Demande à l'utilisateur les informations d'un joueur et retourne un dictionnaire."""
        last_name = input("Nom de famille : ").strip()
        first_name = input("Prénom : ").strip()
        national_id = input("Identifiant national d’échecs (ex: AB12345) : ").strip()
        ranking = int(input("Classement initial (facultatif, 0 par défaut) : ")).strip()

        return {
            "last_name": last_name,
            "first_name": first_name,
            "national_id": national_id,
            "ranking": ranking
        }

    @staticmethod
    def show_players():
        """Action pour afficher la liste des joueurs."""
        print("Affichage de la liste des joueurs...")

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
