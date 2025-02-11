"""Module de contrôle des tournois."""
from models.tournament import Tournament
from models.player import Player


class TournamentController:
    """Contrôleur gérant la création et la gestion des tournois."""

    VALID_TIME_CONTROLS = ["Bullet", "Blitz", "Coup rapide"]

    @staticmethod
    def create_tournament():
        """Demande les informations à l'utilisateur et crée un tournoi.

        Returns:
            Tournament: Le tournoi créé
        """
        name = input("Nom du tournoi : ").strip()
        if not name:
            raise ValueError("Le nom du tournoi est obligatoire")

        place = input("Lieu : ").strip()
        if not place:
            raise ValueError("Le lieu du tournoi est obligatoire")

        date = input("Date (JJ-MM-AAAA) : ").strip()

        time_controls = ", ".join(TournamentController.VALID_TIME_CONTROLS)
        while True:
            time_control = input(f"Contrôle du temps ({time_controls}) : ").strip()
            if time_control in TournamentController.VALID_TIME_CONTROLS:
                break
            print("❌ Type de contrôle invalide")

        desc = input("Description du tournoi : ").strip()

        try:
            tournament = Tournament(name, place, date, time_control, desc=desc)
            Tournament.save_tournament(tournament)
            print("✅ Tournoi créé avec succès !")
            return tournament
        except ValueError as e:
            print(f"❌ Erreur : {str(e)}")
            return None

    @staticmethod
    def list_tournaments():
        """Affiche la liste des tournois enregistrés.

        Returns:
            list: Liste des tournois ou None si aucun tournoi n'existe
        """
        tournaments = Tournament.load_tournaments()
        if not tournaments:
            print("❌ Aucun tournoi enregistré.")
            return None

        print("\n📌 Liste des tournois :")
        for idx, tournament in enumerate(tournaments, start=1):
            print(f"{idx}. {tournament['name']} - {tournament['place']} - {tournament['date']}")
            if tournament.get('current_round', 0) > 0:
                print(f"   Round actuel : {tournament['current_round']}/{tournament['nb_rounds']}")
        return tournaments

    @staticmethod
    def manage_tournament(tournament_data):
        """Gère un tournoi en cours.

        Args:
            tournament_data (dict): Données du tournoi
        """
        tournament = Tournament(
            tournament_data["name"],
            tournament_data["place"],
            tournament_data["date"],
            tournament_data["time_control"],
            players=tournament_data.get("players", []),
            nb_rounds=tournament_data.get("nb_rounds", 4),
            rounds=[],  # Les rounds seront recréés
            desc=tournament_data.get("desc", "")
        )
        tournament.current_round = tournament_data.get("current_round", 0)
        tournament.player_scores = tournament_data.get("player_scores", {})

        if not tournament.players:
            print("\n❌ Aucun joueur dans ce tournoi.")
            print("Ajoutez d'abord des joueurs au tournoi.")
            TournamentController.add_players_to_tournament()
            return

        if tournament.current_round >= tournament.nb_rounds:
            print("\n🏆 Ce tournoi est terminé !")
            TournamentController.show_rankings(tournament_data)
            return

        try:
            tournament.start_tournament()
            print(f"\n✅ Round {tournament.current_round} démarré !")

            current_round = tournament.rounds[-1]
            print("\n📌 Matchs du round :")
            for idx, match in enumerate(current_round.matches, start=1):
                print(f"{idx}. {match[0][0]['name']} vs {match[1][0]['name']}")

            results = []
            for idx, match in enumerate(current_round.matches, start=1):
                while True:
                    print(f"\nMatch {idx}: {match[0][0]['name']} vs {match[1][0]['name']}")
                    print("1. Victoire joueur 1")
                    print("2. Victoire joueur 2")
                    print("3. Match nul")
                    try:
                        result = int(input("Résultat : "))
                        if result in [1, 2, 3]:
                            results.append(1 if result == 1 else 2 if result == 2 else 0)
                            break
                        print("❌ Choix invalide")
                    except ValueError:
                        print("❌ Veuillez entrer un chiffre")

            tournament.end_current_round(results)
            print("\n✅ Round terminé !")
            TournamentController.show_rankings(tournament_data)

        except ValueError as e:
            print(f"\n❌ Erreur : {str(e)}")

    @staticmethod
    def show_rankings(tournament_data):
        """Affiche le classement actuel du tournoi.

        Args:
            tournament_data (dict): Données du tournoi
        """
        if not tournament_data.get("players"):
            print("\n❌ Aucun joueur dans ce tournoi.")
            return

        players = tournament_data["players"]
        player_scores = tournament_data.get("player_scores", {})

        sorted_players = sorted(
            players,
            key=lambda x: (player_scores.get(x.get("national_id", ""), 0), x.get("rank", 0)),
            reverse=True
        )

        print("\n🏆 Classement du tournoi :")
        for idx, player in enumerate(sorted_players, start=1):
            score = player_scores.get(player.get("national_id", ""), 0)
            print(f"{idx}. {player.get('name', '')} {player.get('first_name', '')} - "
                  f"Score: {score} - Rang: {player.get('rank', 0)}")

    @staticmethod
    def add_players_to_tournament():
        """Ajoute des joueurs existants à un tournoi.

        Returns:
            bool: True si l'ajout est réussi, False sinon
        """
        tournaments = Tournament.load_tournaments()
        if not tournaments:
            print("❌ Aucun tournoi disponible.")
            return False

        TournamentController.list_tournaments()
        try:
            choice = int(input("Sélectionnez un tournoi (numéro) : ")) - 1
            if choice < 0 or choice >= len(tournaments):
                raise ValueError
        except ValueError:
            print("❌ Sélection invalide.")
            return False

        tournament = tournaments[choice]
        players = Player.load_players()

        if not players:
            print("❌ Aucun joueur disponible.")
            return False

        print("\n📌 Liste des joueurs disponibles :")
        for idx, player in enumerate(players, start=1):
            print(f"{idx}. {player['name']} {player['first_name']} - Rang: {player['rank']}")

        current_players = len(tournament.get("players", []))
        print(f"\nNombre actuel de joueurs : {current_players}")
        print("Note : Le nombre total de joueurs doit être pair pour démarrer le tournoi.")

        selected_players = []
        while True:
            try:
                player_choice = input("Sélectionnez un joueur (numéro) ou 'q' pour arrêter : ").strip()
                if player_choice.lower() == 'q':
                    break
                player_index = int(player_choice) - 1
                if player_index < 0 or player_index >= len(players):
                    raise ValueError

                player = players[player_index]
                existing_players = tournament.get("players", [])
                if any(p["national_id"] == player["national_id"] for p in existing_players):
                    print("❌ Ce joueur est déjà inscrit au tournoi.")
                    continue

                selected_players.append(player)
            except ValueError:
                print("❌ Sélection invalide.")

        if not selected_players:
            print("❌ Aucun joueur sélectionné.")
            return False

        total_players = current_players + len(selected_players)
        if total_players % 2 != 0:
            print("❌ Le nombre total de joueurs doit être pair.")
            print(f"Actuellement : {total_players} joueurs")
            return False

        tournament["players"] = tournament.get("players", []) + selected_players
        Tournament.save_tournament(Tournament(**tournament))
        print("✅ Joueurs ajoutés avec succès !")
        print(f"Nombre total de joueurs : {total_players}")
        return True
