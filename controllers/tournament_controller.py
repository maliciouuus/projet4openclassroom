"""Module de contrôle des tournois."""
from models.tournament import Tournament
from models.player import Player


class TournamentController:
    """Contrôleur gérant la création et la gestion des tournois."""

    VALID_TIME_CONTROLS = ["Bullet", "Blitz", "Coup rapide"]

    def __init__(self):
        """Initialise le contrôleur des tournois."""
        from views.menu import MainView
        self.view = MainView()

    def create_tournament(self):
        """Demande les informations à l'utilisateur et crée un tournoi.

        Returns:
            Tournament: Le tournoi créé
        """
        try:
            tournament_info = self.view.get_tournament_info(
                self.VALID_TIME_CONTROLS
            )
            tournament = Tournament(**tournament_info)
            Tournament.save_tournament(tournament)
            self.view.show_success_msg()
            return tournament
        except ValueError as e:
            self.view.show_error(str(e))
            return None

    def list_tournaments(self):
        """Affiche la liste des tournois enregistrés.

        Returns:
            list: Liste des tournois ou None si aucun tournoi n'existe
        """
        try:
            tournaments = Tournament.load_tournaments()
            if not tournaments:
                self.view.show_error("Aucun tournoi enregistré.")
                return None

            self.view.display_tournaments_list(tournaments)
            return tournaments
        except ValueError as e:
            self.view.show_error(str(e))
            return None

    def manage_tournament(self, tournament_data):
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
            self.view.show_error("Aucun joueur dans ce tournoi.")
            self.view.show_message("Ajoutez d'abord des joueurs au tournoi.")
            self.add_players_to_tournament()
            return

        if tournament.current_round >= tournament.nb_rounds:
            self.view.show_message("🏆 Ce tournoi est terminé !")
            self.show_rankings(tournament_data)
            return

        try:
            tournament.start_tournament()
            self.view.show_message(
                f"✅ Round {tournament.current_round} démarré !"
            )

            current_round = tournament.rounds[-1]
            self.view.display_round_matches(current_round.matches)

            results = self.view.get_match_results(current_round.matches)
            tournament.end_current_round(results)
            self.view.show_message("✅ Round terminé !")
            self.show_rankings(tournament_data)

        except ValueError as e:
            self.view.show_error(str(e))

    def show_rankings(self, tournament_data):
        """Affiche le classement actuel du tournoi.

        Args:
            tournament_data (dict): Données du tournoi
        """
        if not tournament_data.get("players"):
            self.view.show_error("Aucun joueur dans ce tournoi.")
            return

        players = tournament_data["players"]
        player_scores = tournament_data.get("player_scores", {})

        sorted_players = sorted(
            players,
            key=lambda x: (
                player_scores.get(x.get("national_id", ""), 0),
                x.get("rank", 0)
            ),
            reverse=True
        )

        self.view.display_tournament_rankings(sorted_players, player_scores)

    def add_players_to_tournament(self):
        """Ajoute des joueurs existants à un tournoi.

        Returns:
            bool: True si l'ajout est réussi, False sinon
        """
        tournaments = Tournament.load_tournaments()
        if not tournaments:
            self.view.show_error("Aucun tournoi disponible.")
            return False

        self.list_tournaments()
        try:
            tournoi_index = self.view.get_tournament_choice(len(tournaments))
            if tournoi_index is None:
                return False

            tournament = tournaments[tournoi_index]
            players = Player.load_players()

            if not players:
                self.view.show_error("Aucun joueur disponible.")
                return False

            self.view.display_available_players(players)
            current_players = len(tournament.get("players", []))
            self.view.show_current_players_count(current_players)

            selected_players = self.view.select_players(
                players, tournament.get("players", [])
            )

            if not selected_players:
                self.view.show_error("Aucun joueur sélectionné.")
                return False

            total_players = current_players + len(selected_players)
            if total_players % 2 != 0:
                texte = "Le nombre total de joueurs doit être pair."
                self.view.show_error(texte)
                self.view.show_message(
                    f"Actuellement : {total_players} joueurs"
                )
                return False

            tournament["players"] = (
                tournament.get("players", []) + selected_players
            )
            Tournament.save_tournament(Tournament(**tournament))
            self.view.show_success_msg()
            self.view.show_message(
                f"Nombre total de joueurs : {total_players}"
            )
            return True

        except ValueError as e:
            self.view.show_error(str(e))
            return False
