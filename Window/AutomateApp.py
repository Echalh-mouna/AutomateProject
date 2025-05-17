import json
import os
import shutil

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QCheckBox
)

from interfaceGraphique.AcceuilWindow import AccueilWindow
from model.automate import Automate


class AutomateApp(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Gestion Basique des Automates")
        self.resize(1000, 600)
        self.automate = None
        self.base_path = ""
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        form_layout = QVBoxLayout()
        layout.addLayout(form_layout, 1)

        self.nom_automate = QLineEdit()
        form_layout.addWidget(QLabel("Nom de l'automate"))
        form_layout.addWidget(self.nom_automate)
        for text, slot in [
            ("Choisir Dossier", self.choisir_dossier),
            ("Créer Automate", self.creer_automate),
            ("Charger Automate", self.charger_automate)
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            form_layout.addWidget(btn)

        self.etat_name = QLineEdit()
        form_layout.addWidget(QLabel("Nom de l'état"))
        form_layout.addWidget(self.etat_name)
        self.check_initial = QCheckBox("Initial")
        self.check_final = QCheckBox("Final")
        form_layout.addWidget(self.check_initial)
        form_layout.addWidget(self.check_final)
        for text, slot in [
            ("Ajouter État", self.ajouter_etat),
            ("Supprimer État", self.supprimer_etat)
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            form_layout.addWidget(btn)

        self.source = QLineEdit(); self.symbole = QLineEdit(); self.destination = QLineEdit()
        for label, w in [("Source", self.source), ("Symbole", self.symbole), ("Destination", self.destination)]:
            form_layout.addWidget(QLabel(label)); form_layout.addWidget(w)
        for text, slot in [
            ("Ajouter Transition", self.ajouter_transition),
            ("Supprimer Transition", self.supprimer_transition)
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            form_layout.addWidget(btn)

        for text, slot in [
            ("Sauvegarder Automate", self.sauvegarder_automate),
            ("Supprimer Automate", self.supprimer_automate)
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            form_layout.addWidget(btn)

        btn_revenir = QPushButton("Revenir à l'accueil")
        btn_revenir.clicked.connect(self.revenir_accueil)
        form_layout.addWidget(btn_revenir)

        self.result = QTextEdit()
        layout.addWidget(self.result, 2)

    def choisir_dossier(self):
        self.base_path = QFileDialog.getExistingDirectory(self, "Choisir un dossier")

    def creer_automate(self):
        nom = self.nom_automate.text()
        if not nom or not self.base_path:
            QMessageBox.warning(self, "Erreur", "Nom ou dossier manquant.")
            return
        os.makedirs(os.path.join(self.base_path, nom), exist_ok=True)
        self.automate = Automate(nom)
        self.afficher_automate()

    def charger_automate(self):
        chemin = os.path.join(self.base_path, self.nom_automate.text(), f"{self.nom_automate.text()}.json")
        if not os.path.exists(chemin):
            QMessageBox.warning(self, "Erreur", "Fichier introuvable.")
            return
        with open(chemin, "r", encoding="utf-8") as f:
            self.automate = Automate.from_dict(json.load(f))
        self.afficher_automate()

    def ajouter_etat(self):
        if self.automate:
            self.automate.ajouter_etat(self.etat_name.text(), self.check_initial.isChecked(), self.check_final.isChecked())
            self.etat_name.clear()
            self.check_initial.setChecked(False)
            self.check_final.setChecked(False)
            self.afficher_automate()

    def supprimer_etat(self):
        if self.automate:
            self.automate.supprimer_etat(self.etat_name.text())
            self.etat_name.clear()
            self.afficher_automate()

    def ajouter_transition(self):
        if self.automate:
            self.automate.ajouter_transition(self.source.text(), self.symbole.text(), self.destination.text())
            self.source.clear(); self.symbole.clear(); self.destination.clear()
            self.afficher_automate()

    def supprimer_transition(self):
        if self.automate:
            self.automate.supprimer_transition(self.source.text(), self.symbole.text(), self.destination.text())
            self.source.clear(); self.symbole.clear(); self.destination.clear()
            self.afficher_automate()

    def sauvegarder_automate(self):
        if self.automate and self.base_path:
            path = os.path.join(self.base_path, self.automate.nom, f"{self.automate.nom}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.automate.to_dict(), f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Succès", "Automate sauvegardé.")

    def supprimer_automate(self):
        if self.automate and self.base_path:
            path = os.path.join(self.base_path, self.automate.nom)
            if os.path.exists(path):
                shutil.rmtree(path)
                QMessageBox.information(self, "Succès", "Automate supprimé.")
                self.automate = None
                self.resultat.clear()

    def revenir_accueil(self):
        self.accueil_window = AccueilWindow()
        self.accueil_window.show()
        self.close()

    def afficher_automate(self):
        self.result.setText(str(self.automate) if self.automate else "")