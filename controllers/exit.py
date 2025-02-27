"""Module de gestion de la sortie du programme."""
import sys


class Exit:
    """Classe gérant la sortie du programme."""

    def __init__(self):
        """Initialise le contrôleur de sortie."""
        from views.menu import MainView
        self.view = MainView()

    def start(self):
        """Termine l'exécution du programme."""
        self.view.show_goodbye()
        sys.exit(0)
