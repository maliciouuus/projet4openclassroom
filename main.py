#!/usr/bin/env python3
"""
Centre d'échecs - Gestionnaire de tournois
Programme de gestion de tournois d'échecs suivant les règles du système suisse.
"""

from views.menu import MainView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController


def main():
    """Point d'entrée du programme."""
    view = MainView()
    player_controller = PlayerController()
    tournament_controller = TournamentController()
    view.player_controller = player_controller
    view.tournament_controller = tournament_controller
    player_controller.view = view
    tournament_controller.view = view
    view.afficher_menu()


if __name__ == "__main__":
    main()
