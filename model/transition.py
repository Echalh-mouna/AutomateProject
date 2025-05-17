class Transition:
    def __init__(self, source, symbole, destination):
        self.source = source
        self.symbole = symbole
        self.destination = destination

    def __repr__(self):
        return f"{self.source} -{self.symbole}-> {self.destination}"