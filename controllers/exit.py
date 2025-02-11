"""Module de gestion de la sortie du programme."""
import sys


class Exit:
    """Classe gérant la sortie du programme."""

    @staticmethod
    def start():
        """Termine l'exécution du programme."""
        print("\n👋 Au revoir !")
        sys.exit(0)
