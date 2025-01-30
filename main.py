#!/usr/bin/env python3
"""
Centre d'échecs - Gestionnaire de tournois
Programme de gestion de tournois d'échecs suivant les règles du système suisse.
"""

from views.main_view import MainView
from models.data_manager import DataManager
from controllers.main_controller import MainController

def main():
    """Point d'entrée principal du programme."""
    # Initialisation des composants
    view = MainView()
    data_manager = DataManager()
    controller = MainController(view, data_manager)

    try:
        # Démarrage de l'application
        controller.run()
    except KeyboardInterrupt:
        print("\nFermeture du programme...")
    except Exception as e:
        print(f"\nUne erreur est survenue : {str(e)}")
        raise


class Menu:



class Players:
    def __init__(self, name, surname, birthdate, idchess)


if __name__ == "__main__":
    main()
