import json
import os

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox
)

from model.automate import Automate


class AnalyseAutomateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyse des Automates")
        self.resize(700, 500)
        self.automate = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        btn_charger = QPushButton("Charger Automate")
        btn_charger.clicked.connect(self.charger_automate)
        layout.addWidget(btn_charger)

        btn_verifier = QPushButton("Vérifier Déterminisme")
        btn_verifier.clicked.connect(self.verifier_determinisme)
        layout.addWidget(btn_verifier)

        btn_transformer = QPushButton("Transformer en AFD")
        btn_transformer.clicked.connect(self.transformer_en_afd)
        layout.addWidget(btn_transformer)

        btn_complet = QPushButton("Vérifier Complétude")
        btn_complet.clicked.connect(self.verifier_complet)
        layout.addWidget(btn_complet)

        btn_completer = QPushButton("Compléter automate")
        btn_completer.clicked.connect(self.completer_automate)
        layout.addWidget(btn_completer)

        btn_minimal = QPushButton("Vérifier Minimalité")
        btn_minimal.clicked.connect(self.verifier_minimal)
        layout.addWidget(btn_minimal)

        btn_minimiser = QPushButton("Minimiser automate")
        btn_minimiser.clicked.connect(self.minimiser_automate)
        layout.addWidget(btn_minimiser)

        btn_revenir = QPushButton("Retourner à l'accueil")
        btn_revenir.clicked.connect(self.revenir_accueil)
        layout.addWidget(btn_revenir)

        self.result = QTextEdit()
        self.result.setReadOnly(True)  # Lecture seule
        layout.addWidget(self.result)

        self.setLayout(layout)

    def verifier_minimal(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate.")
            return
        if not self.automate.est_deterministe():
            QMessageBox.warning(self, "Erreur", "L'automate doit être déterministe pour vérifier la minimalité.")
            return
        if self.automate.est_minimal():
            QMessageBox.information(self, "Minimalité", "✅ L'automate est minimal.")
        else:
            QMessageBox.information(self, "Minimalité", "❌ L'automate n'est PAS minimal.")

    def minimiser_automate(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate.")
            return
        if not self.automate.est_deterministe():
            QMessageBox.warning(self, "Erreur", "L'automate doit être déterministe pour être minimisé.")
            return
        try:
            self.automate = self.automate.minimiser()
            self.result.setText(str(self.automate))
            QMessageBox.information(self, "Succès", "✅ Automate minimisé avec succès.")

            # Demander si l'utilisateur veut sauvegarder l'automate minimisé
            sauvegarder = QMessageBox.question(
                self,
                "Sauvegarde",
                "Voulez-vous sauvegarder l'automate minimisé ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if sauvegarder == QMessageBox.Yes:
                chemin, _ = QFileDialog.getSaveFileName(
                    self,
                    "Sauvegarder l'automate minimisé",
                    "",
                    "Fichiers JSON (*.json);;Tous les fichiers (*)"
                )
                if chemin:
                    with open(chemin, "w", encoding="utf-8") as f:
                        json.dump(self.automate.to_dict(), f, indent=4, ensure_ascii=False)
                    QMessageBox.information(self, "Succès", f"✅ Automate minimisé sauvegardé sous :\n{chemin}")

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la minimisation : {str(e)}")

    def completer_automate(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate d'abord.")
            return

        try:
            self.automate = self.automate.completer()
            self.result.setText(str(self.automate))
            QMessageBox.information(self, "Succès", "✅ L'automate a été complété avec succès.")

            # Demande à l'utilisateur s'il souhaite sauvegarder
            sauvegarder = QMessageBox.question(self, "Sauvegarde", "Voulez-vous sauvegarder l'automate complété ?",
                                               QMessageBox.Yes | QMessageBox.No)
            if sauvegarder == QMessageBox.Yes:
                dossier = QFileDialog.getExistingDirectory(self, "Choisir un dossier de sauvegarde")
                if dossier:
                    chemin = os.path.join(dossier, self.automate.nom + "_complet.json")
                    with open(chemin, "w", encoding="utf-8") as f:
                        json.dump(self.automate.to_dict(), f, indent=4, ensure_ascii=False)
                    QMessageBox.information(self, "Succès", f"✅ Automate complété sauvegardé sous :\n{chemin}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"❌ Erreur lors de la complétion : {str(e)}")

    def charger_automate(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir un automate", "", "Fichiers JSON (*.json)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.automate = Automate.from_dict(json.load(f))
            self.result.setText(str(self.automate))

    def verifier_determinisme(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate d'abord.")
            return
        if self.automate.est_deterministe():
            QMessageBox.information(self, "Déterminisme", "✅ L'automate est déterministe.")
        else:
            QMessageBox.information(self, "Déterminisme", "❌ L'automate N'EST PAS déterministe.")

    def transformer_en_afd(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate d'abord.")
            return

        try:
            afd = self.automate.determiniser()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la déterminisation : {str(e)}")
            return

        # Afficher la représentation de l'AFD (attention à la méthode __str__ de Automate)
        self.result.setText(str(afd))

        # Proposer la sauvegarde de l'AFD
        sauvegarder = QMessageBox.question(
            self,
            "Sauvegarde",
            "Voulez-vous sauvegarder l'AFD ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if sauvegarder == QMessageBox.Yes:
            dossier = QFileDialog.getExistingDirectory(self, "Choisir un dossier de sauvegarde")
        if dossier:
            chemin = os.path.join(dossier, afd.nom + ".json")
            try:
                with open(chemin, "w", encoding="utf-8") as f:
                    json.dump(afd.to_dict(), f, indent=4, ensure_ascii=False)
                QMessageBox.information(self, "Succès", f"AFD sauvegardé sous {chemin}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder le fichier : {str(e)}")

    def verifier_complet(self):
        if not self.automate:
            QMessageBox.warning(self, "Erreur", "Veuillez charger un automate.")
            return
        if self.automate.est_complet():
            QMessageBox.information(self, "Complétude", "✅ L'automate est complet.")
        else:
            QMessageBox.information(self, "Complétude", "❌ L'automate n'est PAS complet.")

    def revenir_accueil(self):
        from interfaceGraphique.AcceuilWindow import AccueilWindow
        self.accueil_window = AccueilWindow()
        self.accueil_window.show()
        self.close()