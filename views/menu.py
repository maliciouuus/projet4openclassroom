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

            prompt = "Veuillez saisir un chiffre entre 1 et 5 : "
            choix = self.get_valid_input(prompt, 1, 5)
            self.executer_choix_menu(choix)

    def get_valid_input(self, prompt, min_val, max_val):
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
                print(
                    f"Erreur : Veuillez entrer un nombre entre "
                    f"{min_val} et {max_val}."
                )
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
        """Crée un nouveau joueur."""
        player_info = self.create_player()
        self.player_controller.add_players(player_info)

    def afficher_rapports(self):
        """Affiche le menu des rapports."""
        print("--------------------")
        print("1. 👥 Joueurs")
        print("2. 🏆 Tournois")
        print("3. 🔙 Retour")
        print("--------------------")

        prompt = "Veuillez saisir un chiffre entre 1 et 3 : "
        choix = self.get_valid_input(prompt, 1, 3)
        self.executer_choix_rapports(choix)

    def executer_choix_rapports(self, choix):
        """Exécute l'action correspondant au choix des rapports.

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
        id_prompt = "Identifiant national d'échecs (ex: AB12345) : "
        national_id = input(id_prompt).strip()
        rank_prompt = "Classement initial (facultatif, 0 par défaut) : "
        ranking = input(rank_prompt).strip()

        ranking = int(ranking) if ranking.isdigit() else 0

        return {
            "last_name": last_name,
            "first_name": first_name,
            "dob": dob,
            "national_id": national_id,
            "ranking": ranking
        }

    def afficher_menu_joueurs(self):
        """Affiche le menu de tri des joueurs."""
        print("--------------------")
        print("1. 🔠 Alphabétique")
        print("2. 🔢 Rang")
        print("3. 🔙 Retour")
        prompt = "Veuillez saisir un chiffre entre 1 et 3 : "
        choix = self.get_valid_input(prompt, 1, 3)
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
            sorted_players = sorted(
                players,
                key=lambda x: x["rank"],
                reverse=True
            )
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
        prompt = "Numéro du tournoi : "
        choix = self.get_valid_input(prompt, 1, len(tournaments))
        tournament = tournaments[choix - 1]

        print("\n1. 🎮 Démarrer/Continuer le tournoi")
        print("2. 📊 Voir le classement actuel")
        print("3. 🔙 Retour")

        prompt = "Votre choix : "
        action = self.get_valid_input(prompt, 1, 3)
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

    @staticmethod
    def show_error(message):
        """Affiche un message d'erreur.

        Args:
            message (str): Message d'erreur à afficher
        """
        print(f"❌ {message}")

    @staticmethod
    def show_message(message):
        """Affiche un message.

        Args:
            message (str): Message à afficher
        """
        print(message)

    @staticmethod
    def show_goodbye():
        """Affiche le message d'au revoir."""
        print("\n👋 Au revoir !")

    def get_tournament_info(self, valid_time_controls):
        """Demande les informations d'un tournoi à l'utilisateur.

        Args:
            valid_time_controls (list): Liste des contrôles de temps valides

        Returns:
            dict: Informations du tournoi

        Raises:
            ValueError: Si les informations sont invalides
        """
        name = input("Nom du tournoi : ").strip()
        if not name:
            raise ValueError("Le nom du tournoi est obligatoire")

        place = input("Lieu : ").strip()
        if not place:
            raise ValueError("Le lieu du tournoi est obligatoire")

        date = input("Date (JJ-MM-AAAA) : ").strip()

        time_controls = ", ".join(valid_time_controls)
        while True:
            prompt = f"Contrôle du temps ({time_controls}) : "
            time_control = input(prompt).strip()
            if time_control in valid_time_controls:
                break
            self.show_error("Type de contrôle invalide")

        desc = input("Description du tournoi : ").strip()

        return {
            "name": name,
            "place": place,
            "date": date,
            "time_control": time_control,
            "desc": desc
        }

    def display_tournaments_list(self, tournaments):
        """Affiche la liste des tournois.

        Args:
            tournaments (list): Liste des tournois à afficher
        """
        print("\n📌 Liste des tournois :")
        for idx, tournament in enumerate(tournaments, start=1):
            print(
                f"{idx}. {tournament['name']} - "
                f"{tournament['place']} - {tournament['date']}"
            )
            if tournament.get('current_round', 0) > 0:
                current = tournament['current_round']
                total = tournament['nb_rounds']
                print(f"   Round actuel : {current}/{total}")

    def display_round_matches(self, matches):
        """Affiche les matchs d'un round.

        Args:
            matches (list): Liste des matchs à afficher
        """
        print("\n📌 Matchs du round :")
        for idx, match in enumerate(matches, start=1):
            player1 = match[0][0]['name']
            player2 = match[1][0]['name']
            print(f"{idx}. {player1} vs {player2}")

    def get_match_results(self, matches):
        """Demande les résultats des matchs à l'utilisateur.

        Args:
            matches (list): Liste des matchs

        Returns:
            list: Liste des résultats
        """
        results = []
        for idx, match in enumerate(matches, start=1):
            while True:
                player1 = match[0][0]['name']
                player2 = match[1][0]['name']
                print(f"\nMatch {idx}: {player1} vs {player2}")
                print("1. Victoire joueur 1")
                print("2. Victoire joueur 2")
                print("3. Match nul")
                try:
                    result = int(input("Résultat : "))
                    if result in [1, 2, 3]:
                        results.append(
                            1 if result == 1 else 2 if result == 2 else 0
                        )
                        break
                    self.show_error("Choix invalide")
                except ValueError:
                    self.show_error("Veuillez entrer un chiffre")
        return results

    def display_tournament_rankings(self, players, scores):
        """Affiche le classement d'un tournoi.

        Args:
            players (list): Liste des joueurs
            scores (dict): Dictionnaire des scores
        """
        print("\n🏆 Classement du tournoi :")
        for idx, player in enumerate(players, start=1):
            score = scores.get(player.get("national_id", ""), 0)
            name = player.get('name', '')
            first_name = player.get('first_name', '')
            rank = player.get('rank', 0)
            print(
                f"{idx}. {name} {first_name} - "
                f"Score: {score} - Rang: {rank}"
            )

    def get_tournament_choice(self, max_tournaments):
        """Demande à l'utilisateur de choisir un tournoi.

        Args:
            max_tournaments (int): Nombre maximum de tournois

        Returns:
            int: Index du tournoi choisi ou None si invalide
        """
        try:
            choice = int(input("Sélectionnez un tournoi (numéro) : ")) - 1
            if 0 <= choice < max_tournaments:
                return choice
            raise ValueError()
        except ValueError:
            self.show_error("Sélection invalide.")
            return None

    def display_available_players(self, players):
        """Affiche la liste des joueurs disponibles.

        Args:
            players (list): Liste des joueurs
        """
        print("\n📌 Liste des joueurs disponibles :")
        for idx, player in enumerate(players, start=1):
            name = player['name']
            first_name = player['first_name']
            rank = player['rank']
            print(f"{idx}. {name} {first_name} - Rang: {rank}")

    def show_current_players_count(self, count):
        """Affiche le nombre actuel de joueurs.

        Args:
            count (int): Nombre de joueurs
        """
        print(f"\nNombre actuel de joueurs : {count}")
        print("Note : Le nombre total de joueurs doit être pair.")

    def select_players(self, available_players, existing_players):
        """Permet à l'utilisateur de sélectionner des joueurs.

        Args:
            available_players (list): Liste des joueurs disponibles
            existing_players (list): Liste des joueurs déjà dans le tournoi

        Returns:
            list: Liste des joueurs sélectionnés
        """
        selected_players = []
        while True:
            try:
                prompt = (
                    "Sélectionnez un joueur (numéro) "
                    "ou 'q' pour arrêter : "
                )
                player_choice = input(prompt).strip()
                if player_choice.lower() == 'q':
                    break
                player_index = int(player_choice) - 1
                if player_index < 0 or player_index >= len(available_players):
                    raise ValueError

                player = available_players[player_index]
                player_id = player["national_id"]
                if any(
                    p["national_id"] == player_id
                    for p in existing_players
                ):
                    self.show_error("Ce joueur est déjà inscrit au tournoi.")
                    continue

                selected_players.append(player)
            except ValueError:
                self.show_error("Sélection invalide.")

        return selected_players
