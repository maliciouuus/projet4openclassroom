#!/usr/bin/env python3
"""
Centre d'échecs - Gestionnaire de tournois
Programme de gestion de tournois d'échecs suivant les règles du système suisse.
"""

from views.menu import MainView


def main():
    MainView().montrermenu()


if __name__ == "__main__":
    main()
