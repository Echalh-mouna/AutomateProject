class Transition:
    def _init_(self, etat_source, symbole, etat_destination):
        self.etat_source = etat_source
        self.symbole = symbole
        self.etat_destination = etat_destination

    def _repr_(self):
        return f"{self.etat_source} -{self.symbole}-> {self.etat_destination}"