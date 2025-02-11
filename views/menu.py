"""Module de gestion du menu principal."""
from controllers.exit import Exit
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player import Player


class MainView:
    """Vue principale affichant le menu et gérant les entrées utilisateur."""

    def __init__(self):
        """Initialise la vue principale."""
        self.player_controller = PlayerController()

    def afficher_menu(self):
        """Affiche le menu principal et gère les interactions utilisateur."""
        while True:
            print("\n🏁 Centre Échecs")
            print("--------------------")
            print("1. 🎭 Créer un joueur")
            print("2. 🏆 Créer un tournoi")
            print("3. 📊 Afficher les rapports")
            print("4. 🎮 Gérer les tournois en cours")
            print("5. ❌ Quitter")
            print("--------------------")

            choix = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 5 : ", 1, 5)
            self.executer_choix_menu(choix)

    @staticmethod
    def get_valid_input(prompt, min_val, max_val):
        """Demande une entrée utilisateur et vérifie qu'elle est valide.

        Args:
            prompt (str): Message à afficher à l'utilisateur
            min_val (int): Valeur minimale acceptée
            max_val (int): Valeur maximale acceptée

        Returns:
            int: Choix valide de l'utilisateur
        """
        while True:
            try:
                choix = int(input(prompt))
                if min_val <= choix <= max_val:
                    return choix
                print(f"Erreur : Veuillez entrer un nombre entre {min_val} et {max_val}.")
            except ValueError:
                print("Erreur : Veuillez entrer un chiffre valide.")

    def executer_choix_menu(self, choix):
        """Exécute l'action correspondant au choix de l'utilisateur.

        Args:
            choix (int): Choix de l'utilisateur
        """
        actions = {
            1: self.creer_joueur,
            2: TournamentController.create_tournament,
            3: self.afficher_rapports,
            4: self.gerer_tournois,
            5: Exit.start
        }
        actions[choix]()

    def creer_joueur(self):
        """Crée un nouveau joueur en demandant les informations à l'utilisateur."""
        player_info = self.create_player()
        self.player_controller.add_players(player_info)

    def afficher_rapports(self):
        """Affiche le menu des rapports et gère les interactions utilisateur."""
        print("--------------------")
        print("1. 👥 Joueurs")
        print("2. 🏆 Tournois")
        print("3. 🔙 Retour")
        print("--------------------")

        choix = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 3 : ", 1, 3)
        self.executer_choix_rapports(choix)

    def executer_choix_rapports(self, choix):
        """Exécute l'action correspondant au choix de l'utilisateur pour les rapports.

        Args:
            choix (int): Choix de l'utilisateur
        """
        actions = {
            1: self.afficher_menu_joueurs,
            2: TournamentController.list_tournaments,
            3: self.afficher_menu
        }
        actions[choix]()

    @staticmethod
    def create_player():
        """Demande à l'utilisateur les informations d'un joueur.

        Returns:
            dict: Dictionnaire contenant les informations du joueur
        """
        last_name = input("Nom de famille : ").strip()
        first_name = input("Prénom : ").strip()
        dob = input("Date de naissance (JJ-MM-AAAA) : ").strip()
        national_id = input("Identifiant national d'échecs (ex: AB12345) : ").strip()
        ranking = input("Classement initial (facultatif, 0 par défaut) : ").strip()

        ranking = int(ranking) if ranking.isdigit() else 0

        return {
            "last_name": last_name,
            "first_name": first_name,
            "dob": dob,
            "national_id": national_id,
            "ranking": ranking
        }

    def afficher_menu_joueurs(self):
        """Affiche le menu de tri des joueurs et gère les interactions utilisateur."""
        print("--------------------")
        print("1. 🔠 Alphabétique")
        print("2. 🔢 Rang")
        print("3. 🔙 Retour")
        choix = self.get_valid_input("Veuillez saisir un chiffre entre 1 et 3 : ", 1, 3)
        self.executer_choix_joueurs(choix)

    def executer_choix_joueurs(self, choix):
        """Affiche les joueurs triés selon l'option choisie.

        Args:
            choix (int): Choix de l'utilisateur
        """
        actions = {
            1: lambda: self.afficher_joueurs_tries(1),
            2: lambda: self.afficher_joueurs_tries(2),
            3: self.afficher_menu
        }
        actions[choix]()

    @staticmethod
    def afficher_joueurs_tries(option):
        """Affiche les joueurs triés par nom ou par rang.

        Args:
            option (int): Option de tri (1: alphabétique, 2: rang)
        """
        players = Player.load_players()
        if not players:
            print("❌ Aucun joueur enregistré.")
            return

        if option == 1:
            sorted_players = sorted(players, key=lambda x: x["name"].lower())
        elif option == 2:
            sorted_players = sorted(players, key=lambda x: x["rank"], reverse=True)
        else:
            print("❌ Option invalide.")
            return

        formatted_players = PlayerController.format_players(sorted_players)
        if formatted_players:
            print("\n📋 Liste des joueurs :")
            print("\n".join(formatted_players))
        else:
            print("❌ Aucun joueur à afficher.")

    def gerer_tournois(self):
        """Affiche le menu de gestion des tournois en cours."""
        tournaments = TournamentController.list_tournaments()
        if not tournaments:
            print("❌ Aucun tournoi disponible.")
            return

        print("\nChoisissez un tournoi à gérer :")
        choix = self.get_valid_input("Numéro du tournoi : ", 1, len(tournaments))
        tournament = tournaments[choix - 1]

        print("\n1. 🎮 Démarrer/Continuer le tournoi")
        print("2. 📊 Voir le classement actuel")
        print("3. 🔙 Retour")

        action = self.get_valid_input("Votre choix : ", 1, 3)
        if action == 1:
            TournamentController.manage_tournament(tournament)
        elif action == 2:
            TournamentController.show_rankings(tournament)
        else:
            self.afficher_menu()

    @staticmethod
    def show_success_msg():
        """Affiche un message de succès."""
        print("✅ Succès !")
