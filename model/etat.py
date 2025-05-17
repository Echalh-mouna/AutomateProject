#%%
class Etat:
    def __init__(self, nom, est_initial=False, est_final=False):
        self.nom = nom
        self.est_initial = est_initial
        self.est_final = est_final

    def __repr__(self):
        return self.nom