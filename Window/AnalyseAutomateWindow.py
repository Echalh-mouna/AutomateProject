import json
import os
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox,
    QHBoxLayout, QLabel, QFrame, QScrollArea, QDesktopWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont

from model.automate import Automate

class StyleSheet:
    BUTTON_STYLE = """
        QPushButton {
            background-color: #2196F3;
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            min-width: 200px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
    """
    
    TEXT_EDIT_STYLE = """
        QTextEdit {
            background-color: #FFFFFF;
            border: 2px solid #E0E0E0;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Consolas';
            font-size: 12px;
        }
    """

class AnalyseAutomateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyse des Automates")
        self.automate = None
        self.init_ui()
        self.adjust_window_size()

    def adjust_window_size(self):
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        self.resize(width, height)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Analyse des Automates")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet("color: #1565C0; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Create scroll area for buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container widget for scroll area
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Create button groups
        file_group = self.create_button_group("Gestion des fichiers")
        analyse_group = self.create_button_group("Analyse d'automate")
        transform_group = self.create_button_group("Transformations")

        # File operations buttons
        btn_charger = self.create_button("Charger Automate", "📂")
        btn_charger.clicked.connect(self.charger_automate)
        file_group.layout().addWidget(btn_charger)

        # Analysis buttons
        btn_verifier = self.create_button("Vérifier Déterminisme", "🔍")
        btn_verifier.clicked.connect(self.verifier_determinisme)
        analyse_group.layout().addWidget(btn_verifier)

        btn_complet = self.create_button("Vérifier Complétude", "✓")
        btn_complet.clicked.connect(self.verifier_complet)
        analyse_group.layout().addWidget(btn_complet)

        btn_minimal = self.create_button("Vérifier Minimalité", "📊")
        btn_minimal.clicked.connect(self.verifier_minimal)
        analyse_group.layout().addWidget(btn_minimal)

        # Transform buttons
        btn_transformer = self.create_button("Transformer en AFD", "🔄")
        btn_transformer.clicked.connect(self.transformer_en_afd)
        transform_group.layout().addWidget(btn_transformer)

        btn_completer = self.create_button("Compléter automate", "➕")
        btn_completer.clicked.connect(self.completer_automate)
        transform_group.layout().addWidget(btn_completer)

        btn_minimiser = self.create_button("Minimiser automate", "📉")
        btn_minimiser.clicked.connect(self.minimiser_automate)
        transform_group.layout().addWidget(btn_minimiser)

        # Add groups to scroll layout
        scroll_layout.addWidget(file_group)
        scroll_layout.addWidget(analyse_group)
        scroll_layout.addWidget(transform_group)

        # Navigation button at the bottom
        btn_revenir = self.create_button("Retourner à l'accueil", "🏠")
        btn_revenir.clicked.connect(self.revenir_accueil)
        scroll_layout.addWidget(btn_revenir)

        # Add stretch to push everything up
        scroll_layout.addStretch()

        # Set the scroll widget
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Result section
        result_container = QWidget()
        result_layout = QVBoxLayout(result_container)
        result_layout.setContentsMargins(10, 10, 10, 10)
        result_layout.setSpacing(5)
        
        result_label = QLabel("Résultats")
        result_label.setFont(QFont('Arial', 12, QFont.Bold))
        result_label.setStyleSheet("color: #1565C0;")
        result_layout.addWidget(result_label)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas';
                font-size: 12px;
                max-height: 150px;
                min-height: 100px;
            }
        """)
        self.result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        result_layout.addWidget(self.result)

        # Add result container to main layout with reduced size
        main_layout.addWidget(result_container)

        # Set size policies for better resizing behavior
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        result_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Set the main layout stretch factors
        main_layout.setStretchFactor(scroll_area, 4)  # Augmente la proportion de la zone des boutons
        main_layout.setStretchFactor(result_container, 1)  # Réduit la proportion de la zone de résultats

    def create_button_group(self, title):
        group = QFrame()
        group.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)
        layout = QVBoxLayout(group)
        
        label = QLabel(title)
        label.setFont(QFont('Arial', 10, QFont.Bold))
        label.setStyleSheet("color: #1565C0;")
        layout.addWidget(label)
        
        return group

    def create_button(self, text, icon=""):
        btn = QPushButton(f"{icon} {text}")
        btn.setStyleSheet(StyleSheet.BUTTON_STYLE)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return btn

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