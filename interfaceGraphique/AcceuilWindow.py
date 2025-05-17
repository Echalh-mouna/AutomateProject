from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel
)

from Window.AnalyseAutomateWindow import AnalyseAutomateWindow
from Window.MotEtLanguages import MotEtLangages
from model.automate import Automate


class AccueilWindow(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Accueil - Application de Gestion des Automates")
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        titre = QLabel("Bienvenue !")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size:24px;font-weight:bold;margin-bottom:30px;")
        layout.addWidget(titre)

        self.automate_courant = Automate("A1")  # Exemple de création d’un automate par défaut
        self.tous_les_automates = {
            "A1": self.automate_courant,
            # tu peux en ajouter d'autres si besoin
        }

        for text, slot in [
            ("1. Gestion basique des automates", self.ouvrir_gestion_basique),
            ("2. Fonctionnalités d’analyse des automates", self.ouvrir_analyse_automate),
            ("3. Fonctionnalités avancées sur les mots et langages", self.mot_et_langages)
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(
                "QPushButton{background-color:#4CAF50;color:white;font-size:16px;padding:12px;border-radius:8px;} "
                "QPushButton:hover{background-color:#45a049;}"
            )
            btn.clicked.connect(slot)
            layout.addWidget(btn)

    def ouvrir_gestion_basique(self):
        from Window.AutomateApp import AutomateApp
        self.gestion_window = AutomateApp()
        self.gestion_window.show()
        self.close()

    def ouvrir_analyse_automate(self):
        self.analyse_window = AnalyseAutomateWindow()
        self.analyse_window.show()
        self.close()

    def mot_et_langages(self):
        self.mots_langages_window = MotEtLangages(self.automate_courant, self.tous_les_automates)
        self.mots_langages_window.show()
        self.close()
