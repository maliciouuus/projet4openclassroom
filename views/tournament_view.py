"""Module de vue des tournois."""
from models.tournament import Tournament


class TournamentView:
    """Classe gérant l'affichage des informations des tournois."""

    @staticmethod
    def create_tournament():
        """Crée un tournoi en demandant les informations à l'utilisateur.

        Returns:
            dict: Dictionnaire contenant les informations du tournoi
        """
        name = input("Nom du tournoi : ").strip()
        place = input("Lieu : ").strip()
        date = input("Date (jj-mm-aaaa) : ").strip()
        time_prompt = "Contrôle du temps (Bullet, Blitz, Rapide) : "
        time_control = input(time_prompt).strip()
        desc = input("Description : ").strip()
        rounds_prompt = "Nombre de rounds (4 par défaut) : "
        nb_rounds = int(input(rounds_prompt) or 4)

        tournament = {
            "name": name,
            "place": place,
            "date": date,
            "time_control": time_control,
            "players": [],
            "nb_rounds": nb_rounds,
            "rounds": [],
            "desc": desc
        }

        return tournament

    @staticmethod
    def display_tournaments():
        """Affiche la liste des tournois enregistrés.

        Returns:
            bool: True si des tournois ont été trouvés, False sinon
        """
        tournaments = Tournament.load_tournaments()
        if not tournaments:
            print("❌ Aucun tournoi trouvé.")
            return False

        for tournament in tournaments:
            print(f"\n🏆 Tournoi : {tournament['name']}")
            print(
                f"📍 Lieu : {tournament['place']} | "
                f"📅 Date : {tournament['date']} | "
                f"⏳ Mode : {tournament['time_control']}"
            )
            print(f"🔢 Nombre de rounds : {tournament['nb_rounds']}")
            print(f"📜 Description : {tournament['desc']}")

        return True
