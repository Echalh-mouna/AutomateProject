class Alphabet:
    def __init__(self, symboles):
        self.symboles = set(symboles)

    def __repr__(self):
        return "{" + ", ".join(self.symboles) + "}"