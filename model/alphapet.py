class Alphabet:
    def _init_(self, symboles):
        self.symboles = set(symboles)

    def _repr_(self):
        return "{" + ", ".join(self.symboles) + "}"