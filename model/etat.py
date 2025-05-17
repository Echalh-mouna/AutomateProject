class Etat:
    def _init_(self, nom, est_initial=False, est_final=False):
        self.nom = nom
        self.est_initial = est_initial
        self.est_final = est_final

    def _repr_(self):
        return self.nom