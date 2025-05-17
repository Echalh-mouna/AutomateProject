import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QInputDialog
)

from model.automate import Automate


class MotEtLangages(QWidget):
    def _init_(self, automate, autres_automates: dict):
        super()._init_()
        self.automate = automate
        self.autre_automate = None
        self.autres_automates = autres_automates

        self.setWindowTitle("Opérations sur les mots et langages")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # === Affichage de l’image de l’automate ===
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_image)

        # === Boutons de chargement ===
        btn_charger = QPushButton("Charger automate principal")
        btn_charger.clicked.connect(self.charger_automate_principal)
        layout.addWidget(btn_charger)

        btn_charger_autre = QPushButton("Charger un autre automate")
        btn_charger_autre.clicked.connect(self.charger_automate_secondaire)
        layout.addWidget(btn_charger_autre)

        # === Reconnaissance de mot ===
        self.input_mot = QLineEdit()
        self.input_mot.setPlaceholderText("Mot à tester")
        layout.addWidget(self.input_mot)

        bouton_tester = QPushButton("Tester si le mot est reconnu")
        bouton_tester.clicked.connect(self.tester_mot)
        layout.addWidget(bouton_tester)

        # === Longueur maximale ===
        self.input_longueur = QLineEdit()
        self.input_longueur.setPlaceholderText("Longueur maximale")
        layout.addWidget(self.input_longueur)

        bouton_gen = QPushButton("Générer mots acceptés")
        bouton_gen.clicked.connect(self.generer_mots_acceptes)
        layout.addWidget(bouton_gen)

        bouton_rejetes = QPushButton("Afficher mots rejetés")
        bouton_rejetes.clicked.connect(self.mots_rejetes)
        layout.addWidget(bouton_rejetes)

        # === Opérations binaires ===
        bouton_equiv = QPushButton("Tester équivalence")
        bouton_equiv.clicked.connect(self.tester_equivalence)
        layout.addWidget(bouton_equiv)

        bouton_union = QPushButton("Calculer union")
        bouton_union.clicked.connect(self.calculer_union)
        layout.addWidget(bouton_union)

        bouton_intersection = QPushButton("Calculer intersection")
        bouton_intersection.clicked.connect(self.calculer_intersection)
        layout.addWidget(bouton_intersection)

        bouton_complement = QPushButton("Calculer complément")
        bouton_complement.clicked.connect(self.calculer_complement)
        layout.addWidget(bouton_complement)

        # === Retour ===
        btn_revenir = QPushButton("Retourner à l'accueil")
        btn_revenir.clicked.connect(self.revenir_accueil)
        layout.addWidget(btn_revenir)

        # === Zone de résultats ===
        self.resultat = QTextEdit()
        self.resultat.setReadOnly(True)
        layout.addWidget(self.resultat)

        # Initialisation de l'état initial (si automate fourni)
        self.etat_initial = self.get_initial_state(self.automate.to_dict()) if self.automate else None

    def get_initial_state(self, data):
        for etat in data["etats"]:
            if etat.get("est_initial"):
                return etat["nom"]
        return None

    def charger_automate_principal(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un automate principal", "", "Fichiers JSON (*.json)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                jsonData = json.load(f)
                self.etat_initial = self.get_initial_state(jsonData)
                self.automate = Automate.from_dict(jsonData)
            self.resultat.setText(f"✅ Automate principal chargé : {self.automate.nom}")

    def charger_automate_secondaire(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un autre automate", "", "Fichiers JSON (*.json)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                jsonData = json.load(f)
                self.autre_automate = Automate.from_dict(jsonData)
                nom, ok = QInputDialog.getText(self, "Nom de l’automate", "Entrez un nom pour cet automate :")
                if ok and nom:
                    self.autres_automates[nom] = self.autre_automate
                    self.resultat.setText(f"✅ Automate secondaire « {nom} » chargé avec succès.")
                else:
                    self.resultat.setText("❌ Nom invalide. L’automate n’a pas été ajouté.")

    def reconnait(self, mot: str) -> bool:
        etat_courant = self.etat_initial
        for symbole in mot:
            if symbole not in self.automate.alphabet:
                return False
            transition_trouvee = False
            for t in self.automate.transitions:
                if t.source == etat_courant and t.symbole == symbole:
                    etat_courant = t.destination
                    transition_trouvee = True
                    break
            if not transition_trouvee:
                return False
        return etat_courant in [e.nom for e in self.automate.etats.values() if e.est_final]

    def tester_mot(self):
        mot = self.input_mot.text()
        if mot == "":
            self.resultat.setText("❌ Veuillez entrer un mot.")
            return
        reconnu = self.reconnait(mot)
        self.resultat.setText(f"✅ Le mot « {mot} » est reconnu." if reconnu else f"❌ Le mot « {mot} » est rejeté.")

    def generer_mots_acceptes(self):
        try:
            n = int(self.input_longueur.text())
            mots = self.automate.generer_mots_acceptes(n)
            self.resultat.setText("Mots acceptés :\n" + ", ".join(mots))
        except Exception:
            self.resultat.setText("❌ Entrez une longueur maximale valide.")

    def mots_rejetes(self):
        try:
            n = int(self.input_longueur.text())
            mots = self.automate.mots_rejetes(n)
            self.resultat.setText("Mots rejetés :\n" + ", ".join(mots))
        except Exception:
            self.resultat.setText("❌ Entrez une longueur maximale valide.")

    def tester_equivalence(self):
        if not self.autre_automate:
            self.resultat.setText("❌ Aucun automate secondaire chargé.")
            return
        try:
            n = int(self.input_longueur.text())
            equiv = self.automate.est_equivalent(self.autre_automate, n)
            msg = "✅ Les deux automates sont équivalents." if equiv else "❌ Les deux automates ne sont pas équivalents."
            self.resultat.setText(msg)
        except Exception:
            self.resultat.setText("❌ Spécifiez une longueur maximale valide.")

    def calculer_union(self):
        if not self.autre_automate:
            self.resultat.setText("❌ Aucun automate secondaire chargé.")
            return
        try:
            union = self.automate.union(self.autre_automate)
            self.autres_automates[union.nom] = union
            self.resultat.setText(f"✅ Union calculée : {union.nom}")
            self.afficher_automate(union)
        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul de l’union : {str(e)}")

    def calculer_intersection(self):
        if not self.automate or not self.autre_automate:
            self.resultat.setText("❌ Assurez-vous que les deux automates sont chargés.")
            return
        try:
            intersection = self.automate.intersection(self.autre_automate)
            self.autres_automates[intersection.nom] = intersection
            self.resultat.setText(f"✅ Intersection calculée : {intersection.nom}")
            self.afficher_automate(intersection)
        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul de l’intersection : {str(e)}")

    def calculer_complement(self):
        try:
            # Crée un automate complément avec un nom explicite
            complement = self.automate.complement()

            # S'il n'a pas de nom (et ça cause l'erreur), on en donne un ici :
            if not hasattr(complement, 'nom') or not complement.nom:
                complement.nom = f"{self.automate.nom}_complement"

            self.autres_automates[complement.nom] = complement
            self.resultat.setText(f"✅ Complément calculé : {complement.nom}")
            self.afficher_automate(complement)

        except Exception as e:
            self.resultat.setText(f"❌ Erreur lors du calcul du complément : {str(e)}")

    def afficher_automate(self, automate):
        try:
            automate.to_graphviz("temp_automate")
            pixmap = QPixmap("temp_automate.png")
            if not pixmap.isNull():
                self.label_image.setPixmap(pixmap.scaled(500, 300, Qt.KeepAspectRatio))
            else:
                self.resultat.append("❌ Image vide ou non trouvée.")
        except Exception as e:
            self.resultat.append(f"❌ Impossible d'afficher l’automate : {str(e)}")

    def revenir_accueil(self):
        from interfaceGraphique.AcceuilWindow import AccueilWindow
        self.accueil_window = AccueilWindow()
        self.accueil_window.show()
        self.close()