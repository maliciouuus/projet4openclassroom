
from controllers.exit import Exit

class MainView():

    def afficher_menu(self):
        print("Centre Échecs")
        print("--------------------")
        print("1. Ajouter un joueur")
        print("2. Afficher la liste des joueurs")
        print("3. Créer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Afficher les rapports")
        print("6. Quitter")
        print("--------------------")
        input_text = "Veuillez saisir le chiffre selon l'option souhaité:"
        number_menu = int(input(f"{input_text}"))
        View(number_menu).checknumber()






class View():
    def __init__(self, number):
        self.number = number

    def checknumber(self):
        if self.number == 6:
            Exit.start()
        if self.number == 2:
            print("voici jouers")
